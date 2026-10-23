"""Whole cow campaigns: one cow, several households, one drop.

A whole cow cannot be sold to one buyer as a single carcass sale, so the
campaign splits it into shares that go to different households. Each
household gets its own order, its own cut sheet, and its own packing
choices, and the cow is butchered once when the campaign fills.

The rules that matter here come from the retail exemption itself: no single
sale may be more than half a carcass, and the bulk of the cow has to go to
households rather than restaurants. The service enforces both so the owner
cannot accidentally build a campaign that breaks them.
"""
from __future__ import annotations

import datetime as _dt
import re
from typing import Any

from .. import db

#: USDA retail exemption: 9 CFR 303.1(d). No single sale may exceed half a
#: carcass, and at least three quarters of the carcass must go to household
#: buyers.
MAX_SHARE_FRACTION = 0.5
MIN_HOUSEHOLD_FRACTION = 0.75


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (text or "").strip().lower()).strip("-")


def campaigns(conn: db.sqlite3.Connection,
              status: str | None = None) -> list[db.sqlite3.Row]:
    sql = "SELECT * FROM share_campaigns"
    params: list[Any] = []
    if status:
        sql += " WHERE status = ?"
        params.append(status)
    sql += " ORDER BY drop_date, id"
    return db.rows(conn, sql, params)


def campaign_by_slug(conn: db.sqlite3.Connection,
                     slug: str) -> db.sqlite3.Row | None:
    return db.one(conn, "SELECT * FROM share_campaigns WHERE slug = ?", (slug,))


def households(conn: db.sqlite3.Connection,
               campaign_id: int) -> list[db.sqlite3.Row]:
    return db.rows(conn, "SELECT * FROM campaign_households "
                         "WHERE campaign_id = ? ORDER BY created_at, id",
                   (campaign_id,))


def household_count(conn: db.sqlite3.Connection, campaign_id: int) -> int:
    return db.scalar(conn, "SELECT COUNT(*) FROM campaign_households "
                           "WHERE campaign_id = ? AND status != 'cancelled'",
                     (campaign_id,)) or 0


def _share_for(conn: db.sqlite3.Connection,
               tier: str) -> db.sqlite3.Row | None:
    """The share tier a campaign hands out, by tier name or slug."""
    tier = (tier or "").strip()
    if not tier:
        return None
    return db.one(conn, "SELECT * FROM shares WHERE tier = ? OR slug = ? "
                        "ORDER BY (tier = ?) DESC LIMIT 1",
                  (tier, f"share-{tier}", tier))


def claimed_lbs(conn: db.sqlite3.Connection, campaign_id: int,
                fallback_lbs: float = 0.0) -> float:
    """Pounds committed to the cow so far."""
    rows = db.rows(conn, "SELECT share_id FROM campaign_households "
                         "WHERE campaign_id = ? AND status != 'cancelled'",
                   (campaign_id,))
    total = 0.0
    for row in rows:
        share = db.one(conn, "SELECT takehome_lbs FROM shares WHERE id = ?",
                       (row["share_id"],))
        total += float(share["takehome_lbs"]) if share else fallback_lbs
    return round(total, 2)


def state(conn: db.sqlite3.Connection,
          campaign: db.sqlite3.Row) -> dict[str, Any]:
    """How full the campaign is, and whether it may still take households."""
    target = max(1, int(campaign["household_target"] or 1))
    joined = household_count(conn, campaign["id"])
    share = _share_for(conn, campaign["share_tier"])
    share_lbs = float(share["takehome_lbs"]) if share else 150.0
    share_price = float(share["price"]) if share else 0.0
    lbs = claimed_lbs(conn, campaign["id"], share_lbs)
    total = float(campaign["total_lbs"] or 0)
    open_now = (campaign["status"] == "open" and joined < target)
    return {
        "target": target,
        "joined": joined,
        "left": max(0, target - joined),
        "claimed_lbs": lbs,
        "total_lbs": total,
        "pct": 0 if total <= 0 else min(100, round(joined / target * 100)),
        "share": share,
        "share_lbs": share_lbs,
        "share_price": share_price,
        "open": open_now,
        "max_share_lbs": round(total * MAX_SHARE_FRACTION, 2),
        "min_household_lbs": round(total * MIN_HOUSEHOLD_FRACTION, 2),
        "drop_date": campaign["drop_date"],
    }


def join(conn: db.sqlite3.Connection, campaign_id: int, name: str,
         email: str, phone: str, note: str = "") -> tuple[bool, str]:
    """Reserve a household's place in a campaign.

    Returns (ok, message). A household can hold one place per campaign, and
    a place must not be larger than half the carcass.
    """
    campaign = db.one(conn, "SELECT * FROM share_campaigns WHERE id = ?",
                      (campaign_id,))
    if campaign is None:
        return False, "That campaign is not open."
    info = state(conn, campaign)
    if not info["open"]:
        return False, "That campaign is full."

    email = (email or "").strip().lower()
    existing = db.one(conn, "SELECT id FROM campaign_households "
                             "WHERE campaign_id = ? AND email = ? "
                             "AND status != 'cancelled'",
                      (campaign_id, email))
    if existing is not None:
        return False, "That email already holds a place in this campaign."

    if info["share_lbs"] > info["max_share_lbs"] + 0.001:
        return False, ("That share is larger than half the carcass, which the "
                       "retail exemption does not allow in one sale.")

    conn.execute(
        "INSERT INTO campaign_households(campaign_id, name, email, phone, "
        "share_id, status, note) VALUES(?, ?, ?, ?, ?, 'reserved', ?)",
        (campaign_id, (name or "").strip(), email, (phone or "").strip(),
         info["share"]["id"] if info["share"] else None, (note or "").strip()))
    conn.commit()

    # The cow is butchered once the campaign is full.
    if household_count(conn, campaign_id) >= info["target"]:
        conn.execute("UPDATE share_campaigns SET status = 'full' WHERE id = ?",
                     (campaign_id,))
        conn.commit()
    return True, "Your place is held. We will email when the cow is cut."


def cancel(conn: db.sqlite3.Connection, household_id: int) -> bool:
    conn.execute("UPDATE campaign_households SET status = 'cancelled' "
                 "WHERE id = ?", (household_id,))
    conn.commit()
    return True


def next_drop_dates(count: int = 6,
                    start: _dt.date | None = None) -> list[str]:
    """The Saturday drop dates the owner can pick for a campaign."""
    start = start or (_dt.date.today() + _dt.timedelta(days=21))
    dates: list[str] = []
    day = start
    while len(dates) < count:
        if day.weekday() == 5:
            dates.append(day.isoformat())
        day += _dt.timedelta(days=1)
    return dates
