"""Co-op stores: the businesses sharing this site."""
from __future__ import annotations

from typing import Any

from .. import db


def all_stores(conn: db.sqlite3.Connection, active_only: bool = True) -> list[db.sqlite3.Row]:
    sql = "SELECT * FROM stores"
    if active_only:
        sql += " WHERE active = 1"
    sql += " ORDER BY sort_order, slug"
    return db.rows(conn, sql)


def get(conn: db.sqlite3.Connection, slug: str) -> db.sqlite3.Row | None:
    return db.one(conn, "SELECT * FROM stores WHERE slug = ?", (slug,))


def has_access(conn: db.sqlite3.Connection, admin_id: int | None,
               store_slug: str) -> bool:
    """Check the explicit full-access flag or a store grant."""
    if admin_id is None:
        return False
    admin = db.one(conn, "SELECT full_access FROM admins WHERE id = ?",
                   (admin_id,))
    if admin is None:
        return False
    if admin["full_access"]:
        return True
    rows = db.rows(conn,
                   "SELECT store_slug FROM admin_store_access WHERE admin_id = ?",
                   (admin_id,))
    return any(r["store_slug"] == store_slug for r in rows)


def accessible_stores(conn: db.sqlite3.Connection,
                      admin_id: int | None) -> list[db.sqlite3.Row]:
    stores = all_stores(conn, active_only=False)
    if admin_id is None:
        return []
    admin = db.one(conn, "SELECT full_access FROM admins WHERE id = ?",
                   (admin_id,))
    if admin is None:
        return []
    if admin["full_access"]:
        return stores
    rows = db.rows(conn,
                   "SELECT store_slug FROM admin_store_access WHERE admin_id = ?",
                   (admin_id,))
    allowed = {r["store_slug"] for r in rows}
    return [s for s in stores if s["slug"] in allowed]


def set_access(conn: db.sqlite3.Connection, admin_id: int,
               store_slugs: list[str], full_access: bool = False) -> None:
    conn.execute("DELETE FROM admin_store_access WHERE admin_id = ?", (admin_id,))
    conn.execute("UPDATE admins SET full_access = ? WHERE id = ?",
                 (1 if full_access else 0, admin_id))
    if not full_access:
        for slug in store_slugs:
            conn.execute(
                "INSERT OR IGNORE INTO admin_store_access(admin_id, store_slug) "
                "VALUES(?, ?)", (admin_id, slug))
    conn.commit()


def is_full_admin(conn: db.sqlite3.Connection, admin_id: int | None) -> bool:
    if admin_id is None:
        return False
    return bool(db.scalar(conn, "SELECT full_access FROM admins WHERE id = ?",
                          (admin_id,)))
