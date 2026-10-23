"""Generic products sold by the co-op stores (non-beef)."""
from __future__ import annotations

from typing import Any

from .. import db


def list_for(conn: db.sqlite3.Connection, store_slug: str,
             active_only: bool = True) -> list[db.sqlite3.Row]:
    sql = ("SELECT * FROM products WHERE store_slug = ?")
    params: list[Any] = [store_slug]
    if active_only:
        sql += " AND active = 1"
    sql += " ORDER BY sort_order, id"
    return db.rows(conn, sql, params)


def get(conn: db.sqlite3.Connection, store_slug: str, slug: str) -> db.sqlite3.Row | None:
    return db.one(conn,
                  "SELECT * FROM products WHERE store_slug = ? AND slug = ?",
                  (store_slug, slug))


def get_by_id(conn: db.sqlite3.Connection, pid: int) -> db.sqlite3.Row | None:
    return db.one(conn, "SELECT * FROM products WHERE id = ?", (pid,))


def create(conn: db.sqlite3.Connection, **fields: Any) -> int:
    cur = conn.execute(
        "INSERT INTO products(store_slug, slug, name, kind, unit, unit_lbs, "
        "price, compare_at, compare_brand, compare_size, compare_url, "
        "compare_observed_at, image, icon, blurb, serving, stock, tags, "
        "featured, active, sort_order) "
        "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(store_slug, slug) DO NOTHING",
        (fields["store_slug"], fields["slug"], fields["name"],
         fields.get("kind", "item"), fields.get("unit", "each"),
         float(fields.get("unit_lbs", 0) or 0),
         float(fields.get("price", 0) or 0),
         float(fields.get("compare_at", 0) or 0),
         fields.get("compare_brand", ""), fields.get("compare_size", ""),
         fields.get("compare_url", ""), fields.get("compare_observed_at", ""),
         fields.get("image", ""),
         fields.get("icon", "box"),
         fields.get("blurb", ""), fields.get("serving", ""),
         float(fields.get("stock", 0) or 0), fields.get("tags", ""),
         1 if fields.get("featured") else 0,
         1 if fields.get("active", True) else 0,
         int(fields.get("sort_order", 0) or 0)))
    conn.commit()
    row = conn.execute(
        "SELECT id FROM products WHERE store_slug = ? AND slug = ?",
        (fields["store_slug"], fields["slug"])).fetchone()
    return int(row["id"])


def update(conn: db.sqlite3.Connection, pid: int, **fields: Any) -> None:
    row = get_by_id(conn, pid)
    if row is None:
        return
    conn.execute(
        "UPDATE products SET store_slug=?, slug=?, name=?, kind=?, unit=?, "
        "unit_lbs=?, price=?, compare_at=?, compare_brand=?, compare_size=?, "
        "compare_url=?, compare_observed_at=?, image=?, icon=?, blurb=?, serving=?, "
        "stock=?, tags=?, featured=?, active=?, sort_order=? WHERE id=?",
        (fields.get("store_slug", row["store_slug"]),
         fields.get("slug", row["slug"]),
         fields.get("name", row["name"]),
         fields.get("kind", row["kind"]),
         fields.get("unit", row["unit"]),
         float(fields.get("unit_lbs", row["unit_lbs"]) or 0),
         float(fields.get("price", row["price"]) or 0),
         float(fields.get("compare_at", row["compare_at"]) or 0),
         fields.get("compare_brand", row["compare_brand"]),
         fields.get("compare_size", row["compare_size"]),
         fields.get("compare_url", row["compare_url"]),
         fields.get("compare_observed_at", row["compare_observed_at"]),
         fields.get("image", row["image"]),
         fields.get("icon", row["icon"]),
         fields.get("blurb", row["blurb"]),
         fields.get("serving", row["serving"]),
         float(fields.get("stock", row["stock"]) or 0),
         fields.get("tags", row["tags"]),
         1 if fields.get("featured", bool(row["featured"])) else 0,
         1 if fields.get("active", bool(row["active"])) else 0,
         int(fields.get("sort_order", row["sort_order"]) or 0),
         pid))
    conn.commit()


def delete(conn: db.sqlite3.Connection, pid: int) -> None:
    conn.execute("UPDATE products SET active = 0 WHERE id = ?", (pid,))
    conn.commit()


def decrement_stock(conn: db.sqlite3.Connection, pid: int, amount: float) -> None:
    conn.execute("UPDATE products SET stock = MAX(0, stock - ?) WHERE id = ?",
                 (amount, pid))
