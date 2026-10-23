"""Fulfillment: delivery zones, pickup slots, cutoffs, pound capacity.

Capacity is counted in pounds, not order count. A 79 lb eighth share and a
1 lb ground beef pack are not the same thing to haul, so a slot sells out by
weight. The county dropdown is authoritative; ZIP codes only prefill the
county and warn when they straddle a line.
"""
from __future__ import annotations

import datetime as _dt
from typing import Any

from .. import db

#: The counties we deliver to, and the ZIP prefixes that usually sit inside
#: them. The dropdown decides; the ZIP only advises.
DELIVERY_COUNTIES = ("Shelby", "Henry", "Spencer", "Nelson", "Jefferson")

ZIP_COUNTY: dict[str, str] = {
    "40065": "Shelby", "40022": "Shelby", "40067": "Simpsonville-Shelby",
    "40006": "Shelby", "40050": "Henry", "40004": "Nelson",
    "40055": "Spencer", "40051": "Henry", "40052": " Spencer",
    "40245": "Jefferson", "40241": "Jefferson", "40223": "Jefferson",
    "40228": "Jefferson", "40272": "Jefferson", "40059": "Jefferson",
}

#: ZIPs that straddle county lines. A customer in one of these is told to
#: trust the county dropdown rather than the auto-fill.
STRADDLE_ZIPS = {"40019", "40023", "40057", "40068", "40071", "40076",
                 "40245", "40059"}

#: Delivery runs twice a week. Wednesday orders close Tuesday 11:59pm,
#: Saturday orders close Friday 11:59pm.
DELIVERY_DAYS = {2: "Wednesday", 5: "Saturday"}  # weekday number -> name
CUTOFF_LEAD_DAYS = 1
CUTOFF_HOUR = 23
CUTOFF_MINUTE = 59

#: Pickup windows at The Crea, per the locked decision.
PICKUP_WINDOWS = ("Wednesday 16:00-19:00", "Saturday 10:00-14:00")
DELIVERY_WINDOWS = ("Wednesday 17:00-20:00", "Saturday 10:00-14:00")

#: Rough pound capacity per run. Pickup fits more than a delivery route.
PICKUP_CAPACITY_LBS = 1500.0
DELIVERY_CAPACITY_LBS = 600.0

#: How far ahead slots are kept open.
SLOT_HORIZON_DAYS = 28


def _parse_window(window: str) -> tuple[_dt.time, _dt.time]:
    day, hours = window.split(" ", 1)
    start_text, end_text = hours.split("-")
    start = _dt.datetime.strptime(start_text.strip(), "%H:%M").time()
    end = _dt.datetime.strptime(end_text.strip(), "%H:%M").time()
    return start, end


def _window_parts(window: str) -> tuple[int, _dt.time, _dt.time]:
    day_name, hours = window.split(" ", 1)
    weekdays = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
                "Friday": 4, "Saturday": 5, "Sunday": 6}
    start, end = _parse_window(window)
    return weekdays[day_name], start, end


def cutoff_for(service_date: str) -> str:
    """When ordering closes for a given delivery or pickup date."""
    try:
        day = _dt.date.fromisoformat(service_date)
    except ValueError:
        return ""
    cutoff = day - _dt.timedelta(days=CUTOFF_LEAD_DAYS)
    return f"{cutoff.isoformat()}T{CUTOFF_HOUR:02d}:{CUTOFF_MINUTE:02d}:00"


def slot_label(row: db.sqlite3.Row) -> str:
    try:
        day = _dt.date.fromisoformat(row["service_date"])
    except (ValueError, TypeError):
        return row["service_date"]
    return day.strftime("%a %b %d")


def window_label(row: db.sqlite3.Row) -> str:
    return f"{row['window_start']}-{row['window_end']}"


def ensure_slots(conn: db.sqlite3.Connection, horizon: int = SLOT_HORIZON_DAYS,
                 today: _dt.date | None = None) -> int:
    """Top up the slot calendar out to the horizon. Idempotent.

    Called by the daily job and opportunistically before the checkout page
    renders, so a quiet shop still shows live dates.
    """
    today = today or _dt.date.today()
    created = 0
    for offset in range(horizon + 1):
        day = today + _dt.timedelta(days=offset)
        for window in PICKUP_WINDOWS:
            created += _ensure_one(conn, "pickup", day, window,
                                   PICKUP_CAPACITY_LBS)
        for window in DELIVERY_WINDOWS:
            created += _ensure_one(conn, "delivery", day, window,
                                   DELIVERY_CAPACITY_LBS)
    conn.commit()
    return created


def _ensure_one(conn: db.sqlite3.Connection, kind: str, day: _dt.date,
                window: str, capacity: float) -> int:
    weekday, start, end = _window_parts(window)
    if day.weekday() != weekday:
        return 0
    start_text = start.strftime("%H:%M")
    end_text = end.strftime("%H:%M")
    existing = db.one(conn,
                      "SELECT id FROM slots WHERE kind = ? AND service_date = ? "
                      "AND window_start = ?", (kind, day.isoformat(), start_text))
    if existing:
        return 0
    conn.execute(
        "INSERT INTO slots(kind, service_date, window_start, window_end, "
        "capacity_lbs, reserved_lbs, cutoff_at, label) "
        "VALUES(?, ?, ?, ?, ?, 0, ?, ?)",
        (kind, day.isoformat(), start_text, end_text, capacity,
         cutoff_for(day.isoformat()),
         f"{day.strftime('%A')} {start_text}-{end_text}"))
    return 1


def upcoming(conn: db.sqlite3.Connection, kind: str, limit: int = 12,
             need_lbs: float = 0.0) -> list[db.sqlite3.Row]:
    """Open slots of one kind, soonest first, that can still take an order."""
    rows = db.rows(conn,
                   "SELECT * FROM slots WHERE kind = ? AND active = 1 "
                   "AND service_date >= date('now') "
                   "ORDER BY service_date, window_start LIMIT 40", (kind,))
    out = []
    for row in rows:
        remaining = float(row["capacity_lbs"]) - float(row["reserved_lbs"])
        if remaining + 0.001 < need_lbs:
            continue
        if not order_open(row):
            continue
        out.append(row)
        if len(out) >= limit:
            break
    return out


def order_open(row: db.sqlite3.Row) -> bool:
    """Is this slot still taking orders?"""
    try:
        cutoff = _dt.datetime.fromisoformat(row["cutoff_at"])
    except (ValueError, TypeError):
        return True
    return _dt.datetime.now() <= cutoff


def remaining_lbs(row: db.sqlite3.Row) -> float:
    return max(0.0, float(row["capacity_lbs"]) - float(row["reserved_lbs"]))


def reserve(conn: db.sqlite3.Connection, slot_id: int, lbs: float) -> bool:
    """Take pounds out of a slot. Fails if the slot cannot cover them."""
    row = db.one(conn, "SELECT * FROM slots WHERE id = ?", (slot_id,))
    if row is None or not order_open(row):
        return False
    if remaining_lbs(row) + 0.001 < lbs:
        return False
    conn.execute("UPDATE slots SET reserved_lbs = reserved_lbs + ? "
                 "WHERE id = ?", (lbs, slot_id))
    return True


def release(conn: db.sqlite3.Connection, slot_id: int, lbs: float) -> None:
    conn.execute("UPDATE slots SET reserved_lbs = MAX(0, reserved_lbs - ?) "
                 "WHERE id = ?", (lbs, slot_id))


def county_for_zip(zip_code: str) -> str | None:
    cleaned = "".join(ch for ch in (zip_code or "") if ch.isdigit())[:5]
    return ZIP_COUNTY.get(cleaned)


def zip_note(zip_code: str) -> str | None:
    cleaned = "".join(ch for ch in (zip_code or "") if ch.isdigit())[:5]
    if cleaned in STRADDLE_ZIPS:
        return (f"ZIP {cleaned} straddles county lines. Pick the county your "
                "address sits in.")
    return None


def county_allowed(county: str) -> bool:
    return (county or "").strip().title() in DELIVERY_COUNTIES


def zones() -> list[dict[str, Any]]:
    return [{"name": name, "slug": name.lower()} for name in DELIVERY_COUNTIES]
