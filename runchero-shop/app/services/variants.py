"""Product variants: packaged sizes for the same item (pint, quart, half
gallon, 5 gallon, 10 gallon). Each variant carries its own price, stock
and optional benchmark comparison so the co-op can discount bulk sizes."""
from __future__ import annotations

from typing import Any

from .. import db


#: Standard sizes the co-op stores stock, smallest to largest.
STANDARD_SIZES: list[tuple[str, str, float, int]] = [
    ("pint", "Pint (16 oz)", 1.04, 1),
    ("quart", "Quart (32 oz)", 2.08, 2),
    ("half-gallon", "Half gallon (64 oz)", 4.16, 3),
    ("gallon", "Gallon (128 oz)", 8.32, 4),
    ("5-gallon", "5 gallon pail", 41.6, 5),
    ("10-gallon", "10 gallon pail", 83.2, 6),
]


def list_for_product(
    conn: db.sqlite3.Connection, product_id: int, active_only: bool = True
) -> list[db.sqlite3.Row]:
    sql = "SELECT * FROM product_variants WHERE product_id = ?"
    params: list[Any] = [product_id]
    if active_only:
        sql += " AND active = 1"
    sql += " ORDER BY sort_order, id"
    return db.rows(conn, sql, params)


def get(conn: db.sqlite3.Connection, variant_id: int) -> db.sqlite3.Row | None:
    return db.one(
        conn, "SELECT * FROM product_variants WHERE id = ?", (variant_id,)
    )


def create(conn: db.sqlite3.Connection, product_id: int, **fields: Any) -> int:
    cur = conn.execute(
        "INSERT INTO product_variants(product_id, size_label, unit, unit_lbs, "
        "price, compare_at, stock, sort_order, active) "
        "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(product_id, size_label) DO UPDATE SET "
        "unit = excluded.unit, unit_lbs = excluded.unit_lbs, "
        "price = excluded.price, compare_at = excluded.compare_at, "
        "stock = excluded.stock, sort_order = excluded.sort_order, "
        "active = excluded.active",
        (
            product_id,
            fields.get("size_label", "Each"),
            fields.get("unit", "each"),
            float(fields.get("unit_lbs", 0) or 0),
            float(fields.get("price", 0) or 0),
            float(fields.get("compare_at", 0) or 0),
            float(fields.get("stock", 0) or 0),
            int(fields.get("sort_order", 0) or 0),
            1 if fields.get("active", True) else 0,
        ),
    )
    conn.commit()
    row = conn.execute(
        "SELECT id FROM product_variants WHERE product_id = ? AND size_label = ?",
        (product_id, fields.get("size_label", "Each"))).fetchone()
    return int(row["id"])


def update(conn: db.sqlite3.Connection, variant_id: int, **fields: Any) -> None:
    row = get(conn, variant_id)
    if row is None:
        return
    conn.execute(
        "UPDATE product_variants SET product_id=?, size_label=?, unit=?, "
        "unit_lbs=?, price=?, compare_at=?, stock=?, sort_order=?, active=? "
        "WHERE id=?",
        (
            fields.get("product_id", row["product_id"]),
            fields.get("size_label", row["size_label"]),
            fields.get("unit", row["unit"]),
            float(fields.get("unit_lbs", row["unit_lbs"]) or 0),
            float(fields.get("price", row["price"]) or 0),
            float(fields.get("compare_at", row["compare_at"]) or 0),
            float(fields.get("stock", row["stock"]) or 0),
            int(fields.get("sort_order", row["sort_order"]) or 0),
            1 if fields.get("active", bool(row["active"])) else 0,
            variant_id,
        ),
    )
    conn.commit()


def delete(conn: db.sqlite3.Connection, variant_id: int) -> None:
    conn.execute(
        "UPDATE product_variants SET active = 0 WHERE id = ?", (variant_id,)
    )
    conn.commit()


def decrement_stock(
    conn: db.sqlite3.Connection, variant_id: int, amount: float
) -> None:
    conn.execute(
        "UPDATE product_variants SET stock = MAX(0, stock - ?) WHERE id = ?",
        (amount, variant_id),
    )


def seed_standard_variants(
    conn: db.sqlite3.Connection, product_id: int
) -> None:
    """Give a jar-style product the standard size ladder with bulk discounts.

    Each larger size costs a little less per unit than the one below it.
    """
    base = db.one(conn, "SELECT price FROM products WHERE id = ?", (product_id,))
    base_price = float(base["price"]) if base else 0.0
    per_unit = base_price / 1.04  # price per pint-equivalent from base pint
    size_index = 0
    for key, label, lbs, _order in STANDARD_SIZES:
        size_index += 1
        # Bulk discount: larger pails cost less per unit.
        discount = 0.0 if key == "pint" else min(0.25, (size_index - 1) * 0.05)
        price = round(per_unit * lbs * (1.0 - discount), 2)
        stock = 24 if key in ("pint", "quart") else 6
        conn.execute(
            "INSERT INTO product_variants(product_id, size_label, unit, unit_lbs, "
            "price, stock, sort_order, active) VALUES(?, ?, ?, ?, ?, ?, ?, 1) "
            "ON CONFLICT(product_id, size_label) DO NOTHING",
            (product_id, label, "each", lbs, price, stock, size_index),
        )
        conn.execute(
            "UPDATE product_variants SET unit = 'each', unit_lbs = ?, "
            "sort_order = ?, active = 1 "
            "WHERE product_id = ? AND size_label = ?",
            (lbs, size_index, product_id, label),
        )
