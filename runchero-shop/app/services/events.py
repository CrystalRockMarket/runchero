"""Community events: canning / fermenting workshops and other co-op
gatherings, editable from the admin console."""
from __future__ import annotations

from datetime import date, datetime
from typing import Any

from .. import db


def list_events(
    conn: db.sqlite3.Connection,
    active_only: bool = True,
    upcoming_only: bool = False,
) -> list[db.sqlite3.Row]:
    sql = "SELECT * FROM events"
    params: list[Any] = []
    conditions: list[str] = []
    if active_only:
        conditions.append("active = 1")
    if upcoming_only:
        conditions.append("event_date >= date('now')")
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    sql += " ORDER BY event_date, start_time, id"
    return db.rows(conn, sql, params)


def get(conn: db.sqlite3.Connection, event_id: int) -> db.sqlite3.Row | None:
    return db.one(conn, "SELECT * FROM events WHERE id = ?", (event_id,))


def create(conn: db.sqlite3.Connection, **fields: Any) -> int:
    cur = conn.execute(
        "INSERT INTO events(title, description, event_date, start_time, "
        "end_time, location, capacity, active, sort_order) "
        "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            fields.get("title", ""),
            fields.get("description", ""),
            fields.get("event_date", ""),
            fields.get("start_time", ""),
            fields.get("end_time", ""),
            fields.get("location", ""),
            int(fields.get("capacity", 0) or 0),
            1 if fields.get("active", True) else 0,
            int(fields.get("sort_order", 0) or 0),
        ),
    )
    conn.commit()
    return int(cur.lastrowid)


def update(conn: db.sqlite3.Connection, event_id: int, **fields: Any) -> None:
    row = get(conn, event_id)
    if row is None:
        return
    conn.execute(
        "UPDATE events SET title=?, description=?, event_date=?, start_time=?, "
        "end_time=?, location=?, capacity=?, active=?, sort_order=? WHERE id=?",
        (
            fields.get("title", row["title"]),
            fields.get("description", row["description"]),
            fields.get("event_date", row["event_date"]),
            fields.get("start_time", row["start_time"]),
            fields.get("end_time", row["end_time"]),
            fields.get("location", row["location"]),
            int(fields.get("capacity", row["capacity"]) or 0),
            1 if fields.get("active", bool(row["active"])) else 0,
            int(fields.get("sort_order", row["sort_order"]) or 0),
            event_id,
        ),
    )
    conn.commit()


def delete(conn: db.sqlite3.Connection, event_id: int) -> None:
    conn.execute("UPDATE events SET active = 0 WHERE id = ?", (event_id,))
    conn.commit()


def is_upcoming(row: db.sqlite3.Row) -> bool:
    try:
        day = datetime.strptime(row["event_date"], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return False
    return day >= date.today()
