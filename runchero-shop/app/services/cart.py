"""Cart reads and writes, plus the totals math the checkout depends on.

A cart is an anonymous row keyed by a signed cookie, so a shopper never needs
an account and never loses their basket when they come back.
"""
from __future__ import annotations

import json
import time
from typing import Any

from .. import db
from . import market, packing


def ensure(conn: db.sqlite3.Connection, cart_id: str) -> None:
    conn.execute(
        "INSERT OR IGNORE INTO carts(id) VALUES(?)", (cart_id,))
    conn.commit()


def _resolve(conn: db.sqlite3.Connection, item: db.sqlite3.Row) -> dict[str, Any] | None:
    """Turn a cart row into a priced line, or drop it if the item vanished."""
    kind = item["item_type"]
    ref = item["ref_id"]
    if kind == "cut":
        row = db.one(conn, "SELECT * FROM cuts WHERE id = ? AND active = 1", (ref,))
        if row is None:
            return None
        unit_lbs = float(row["unit_lbs"]) or 1.0
        price_per_lb = float(row["runchero_price"])
        line_total = round(price_per_lb * unit_lbs * float(item["qty"]), 2)
        market_row = market.latest(conn, (row["market_series_key"] or "").strip())
        market_price = float(market_row["value"]) if market_row else 0.0
        savings = round(max(0.0, market_price - price_per_lb) * unit_lbs
                        * float(item["qty"]), 2) if market_price else 0.0
        try:
            packing_choice = json.loads(item["packing_json"] or "{}")
        except (ValueError, TypeError):
            packing_choice = {}
        surcharge = packing.line_surcharge(
            conn,
            {"item_type": "cut", "ref_id": ref, "tags": row["tags"] or ""},
            float(item["qty"]), unit_lbs * float(item["qty"]), line_total,
            packing_choice)
        return {
            "id": item["id"],
            "item_type": kind,
            "ref_id": ref,
            "slug": row["slug"],
            "name": row["name"],
            "icon": row["icon"],
            "tags": row["tags"] or "",
            "qty": float(item["qty"]),
            "unit": row["unit"],
            "unit_lbs": unit_lbs,
            "price_per_lb": price_per_lb,
            "line_total": round(line_total + surcharge, 2),
            "base_total": line_total,
            "packing_total": surcharge,
            "packing": packing_choice,
            "note": item["note"] or "",
            "market_price": market_price,
            "savings": savings,
            "takehome_lbs": unit_lbs * float(item["qty"]),
            "stock_lbs": float(row["stock_lbs"]),
        }
    if kind == "package":
        row = db.one(conn, "SELECT * FROM packages WHERE id = ? AND active = 1",
                     (ref,))
        if row is None:
            return None
        qty = float(item["qty"])
        price = float(row["price"])
        line_total = round(price * qty, 2)
        compare = float(row["compare_at"]) or price
        savings = round(max(0.0, compare - price) * qty, 2)
        return {
            "id": item["id"],
            "item_type": kind,
            "ref_id": ref,
            "slug": row["slug"],
            "name": row["name"],
            "icon": row["icon"],
            "qty": qty,
            "unit": "package",
            "unit_lbs": float(row["total_lbs"]) or 0.0,
            "price_per_lb": price,
            "line_total": line_total,
            "base_total": line_total,
            "packing_total": 0.0,
            "packing": {},
            "note": item["note"] or "",
            "market_price": compare,
            "savings": savings,
            "takehome_lbs": float(row["total_lbs"]) * qty,
            "stock_lbs": 0.0,
        }
    if kind == "share":
        row = db.one(conn, "SELECT * FROM shares WHERE id = ? AND active = 1",
                     (ref,))
        if row is None:
            return None
        qty = float(item["qty"])
        price = float(row["price"])
        line_total = round(price * qty, 2)
        choice = db.one(conn, "SELECT value FROM market_prices "
                              "WHERE series_key = 'ers:choice_beef_retail' "
                              "ORDER BY observed_at DESC LIMIT 1")
        market_lb = float(choice["value"]) if choice else 9.94
        savings = round(max(0.0, market_lb * float(row["takehome_lbs"]) - price)
                        * qty, 2)
        return {
            "id": item["id"],
            "item_type": kind,
            "ref_id": ref,
            "slug": row["slug"],
            "name": row["name"],
            "icon": row["icon"],
            "qty": qty,
            "unit": "share",
            "unit_lbs": float(row["takehome_lbs"]),
            "price_per_lb": float(row["price_per_lb"]),
            "line_total": line_total,
            "base_total": line_total,
            "packing_total": 0.0,
            "packing": {},
            "note": item["note"] or "",
            "market_price": market_lb * float(row["takehome_lbs"]),
            "savings": savings,
            "takehome_lbs": float(row["takehome_lbs"]) * qty,
            "stock_lbs": 0.0,
        }
    if kind == "product":
        variant_id = item["variant_id"]
        variant = None
        if variant_id:
            variant = db.one(
                conn,
                "SELECT * FROM product_variants WHERE id = ? AND active = 1",
                (variant_id,),
            )
        if variant is None:
            variant = db.one(
                conn,
                "SELECT * FROM product_variants WHERE product_id = ? "
                "AND active = 1 ORDER BY sort_order, id LIMIT 1",
                (ref,),
            )
        row = db.one(
            conn,
            "SELECT * FROM products WHERE id = ? AND active = 1",
            (variant["product_id"] if variant else ref,),
        )
        if row is None:
            return None
        if variant:
            ref = variant["product_id"]
            price = float(variant["price"])
            unit = variant["unit"]
            unit_lbs = float(variant["unit_lbs"]) or 0.0
            stock = float(variant["stock"])
            compare_at = float(variant["compare_at"])
            name = f"{row['name']} · {variant['size_label']}"
            icon = row["icon"] or "box"
        else:
            qty = float(item["qty"])
            price = float(row["price"])
            unit = row["unit"]
            unit_lbs = float(row["unit_lbs"]) or 0.0
            stock = float(row["stock"])
            compare_at = float(row["compare_at"])
            name = row["name"]
            icon = row["icon"] or "box"
        qty = float(item["qty"])
        line_total = round(price * qty, 2)
        # Other-brand comparisons are displayed with their source on the
        # product page, never added to the beef-only grocery-savings claim.
        savings = 0.0
        return {
            "id": item["id"],
            "item_type": kind,
            "ref_id": ref,
            "variant_id": variant["id"] if variant else None,
            "slug": row["slug"],
            "name": name,
            "icon": icon,
            "store_slug": row["store_slug"],
            "qty": qty,
            "unit": unit,
            "unit_lbs": unit_lbs,
            "price_per_lb": price,
            "line_total": line_total,
            "base_total": line_total,
            "packing_total": 0.0,
            "packing": {},
            "note": item["note"] or "",
            "market_price": compare_at or price,
            "savings": savings,
            "takehome_lbs": unit_lbs * qty,
            "stock_lbs": stock,
        }
    return None


def items(conn: db.sqlite3.Connection, cart_id: str) -> list[dict[str, Any]]:
    ensure(conn, cart_id)
    rows = db.rows(conn,
                   "SELECT * FROM cart_items WHERE cart_id = ? "
                   "ORDER BY sort_order, id", (cart_id,))
    out: list[dict[str, Any]] = []
    for row in rows:
        line = _resolve(conn, row)
        if line is not None:
            out.append(line)
    return out


def add(conn: db.sqlite3.Connection, cart_id: str, item_type: str,
        ref_id: int, qty: float = 1.0, packing: dict | None = None,
        note: str = "", variant_id: int | None = None) -> None:
    ensure(conn, cart_id)
    existing = db.one(conn,
                      "SELECT id, qty FROM cart_items WHERE cart_id = ? "
                      "AND item_type = ? AND ref_id = ? "
                      "AND (variant_id IS ? OR variant_id = ?)",
                      (cart_id, item_type, ref_id, variant_id, variant_id))
    if existing:
        conn.execute("UPDATE cart_items SET qty = qty + ? WHERE id = ?",
                     (qty, existing["id"]))
    else:
        order = db.scalar(conn,
                          "SELECT COALESCE(MAX(sort_order), 0) + 1 "
                          "FROM cart_items WHERE cart_id = ?", (cart_id,))
        conn.execute(
            "INSERT INTO cart_items(cart_id, item_type, ref_id, qty, "
            "variant_id, packing_json, note, sort_order) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
            (cart_id, item_type, ref_id, qty,
             variant_id,
             json.dumps(packing or {}), note, order))
    conn.execute("UPDATE carts SET updated_at = datetime('now') WHERE id = ?",
                 (cart_id,))
    conn.commit()


def set_qty(conn: db.sqlite3.Connection, cart_id: str, item_id: int,
            qty: float) -> None:
    if qty <= 0:
        remove(conn, cart_id, item_id)
        return
    conn.execute("UPDATE cart_items SET qty = ? WHERE id = ? AND cart_id = ?",
                 (qty, item_id, cart_id))
    conn.execute("UPDATE carts SET updated_at = datetime('now') WHERE id = ?",
                 (cart_id,))
    conn.commit()


def remove(conn: db.sqlite3.Connection, cart_id: str, item_id: int) -> None:
    conn.execute("DELETE FROM cart_items WHERE id = ? AND cart_id = ?",
                 (item_id, cart_id))
    conn.execute("UPDATE carts SET updated_at = datetime('now') WHERE id = ?",
                 (cart_id,))
    conn.commit()


def set_line_packing(conn: db.sqlite3.Connection, cart_id: str, item_id: int,
                     packing: dict) -> None:
    conn.execute("UPDATE cart_items SET packing_json = ? WHERE id = ? "
                 "AND cart_id = ?",
                 (json.dumps(packing), item_id, cart_id))
    conn.commit()


def line_packing(conn: db.sqlite3.Connection, cart_id: str,
                 item_id: int) -> dict[str, str]:
    """The packing choices already saved on one cart line."""
    row = db.one(conn, "SELECT packing_json FROM cart_items WHERE id = ? "
                       "AND cart_id = ?", (item_id, cart_id))
    if row is None:
        return {}
    try:
        data = json.loads(row["packing_json"] or "{}")
    except (ValueError, TypeError):
        return {}
    return data if isinstance(data, dict) else {}


def clear(conn: db.sqlite3.Connection, cart_id: str) -> None:
    conn.execute("DELETE FROM cart_items WHERE cart_id = ?", (cart_id,))
    conn.commit()


def totals(conn: db.sqlite3.Connection, cart_id: str,
           order_packing: dict[str, str] | None = None,
           content: dict[str, Any] | None = None) -> dict[str, Any]:
    """Subtotal, packing charges, savings, and the delivery fee math.

    The minimum order and free delivery thresholds come from site content so
    the owner can tune them without a code change.
    """
    lines = items(conn, cart_id)
    content = content or {}
    # The beef minimum belongs to the beef business. Other co-op stores can
    # sell a small jar or pouch on its own; mixed carts retain the beef rule.
    has_beef = any(line["item_type"] != "product" for line in lines)
    min_order = float(content.get("min_order", 99.0)) if has_beef else 0.0
    free_over = float(content.get("free_delivery_over", 159.0))
    fee = float(content.get("delivery_fee", 15.0))

    subtotal = round(sum(line["base_total"] for line in lines), 2)
    packing_lines = round(sum(line["packing_total"] for line in lines), 2)
    beef_lines = [line for line in lines if line["item_type"] != "product"]
    packing_order = packing.order_surcharge(
        conn, order_packing or {}, beef_lines) if order_packing and beef_lines else 0.0
    savings = round(sum(line["savings"] for line in lines), 2)
    lbs = round(sum(line["takehome_lbs"] for line in lines), 2)
    count = len(lines)

    fee_due = fee if (subtotal and subtotal < free_over) else 0.0
    to_free = round(max(0.0, free_over - subtotal), 2)
    to_min = round(max(0.0, min_order - subtotal), 2)

    return {
        "lines": lines,
        "has_beef": has_beef,
        "count": count,
        "subtotal": subtotal,
        "packing_lines": packing_lines,
        "packing_order": packing_order,
        "packing_total": round(packing_lines + packing_order, 2),
        "savings": savings,
        "takehome_lbs": lbs,
        "delivery_fee": fee_due,
        "free_delivery_over": free_over,
        "to_free_delivery": to_free,
        "min_order": min_order,
        "to_min_order": to_min,
        "meets_min": subtotal >= min_order if min_order else True,
        "prepaid_total": round(subtotal + packing_lines + packing_order, 2),
        "total": round(subtotal + packing_lines + packing_order + fee_due, 2),
    }
