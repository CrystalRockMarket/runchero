"""Order assembly: totals, market snapshot, order codes, receipts, ICS."""
from __future__ import annotations

import datetime as _dt
import json
import secrets
from typing import Any

from .. import db
from . import cart as cart_service
from . import fulfillment as fulfillment_service
from . import market, packing


def new_code() -> str:
    return f"RB-{secrets.token_hex(4).upper()}"


def place(conn: db.sqlite3.Connection, *, cart_id: str, email: str,
          phone: str, name: str, fulfillment: str, county: str,
          address: dict[str, Any], slot_id: int, order_packing: dict[str, str],
          totals: dict[str, Any], notes: str, terms_version: str,
          subscribe: str = "", referral_code: str = "",
          customer_id: int | None = None
          ) -> tuple[int, str] | None:
    """Turn a cart into an order. Reserves slot pounds before charging."""
    lines = totals["lines"]
    if not lines:
        return None
    has_beef = any(line["item_type"] != "product" for line in lines)
    for line in lines:
        if line["item_type"] == "product":
            if line.get("variant_id"):
                stock = db.one(conn,
                               "SELECT active, stock FROM product_variants "
                               "WHERE id = ?", (line["variant_id"],))
                stock_lbs = float(stock["stock"]) if stock else 0.0
                active = bool(stock["active"]) if stock else False
            else:
                stock = db.one(conn,
                               "SELECT active, stock FROM products WHERE id = ?",
                               (line["ref_id"],))
                stock_lbs = float(stock["stock"]) if stock else 0.0
                active = bool(stock["active"]) if stock else False
            if (stock is None or not active
                    or stock_lbs < float(line["qty"])):
                return None
    takehome = float(totals.get("takehome_lbs") or 0.0) or 1.0

    slot = db.one(conn, "SELECT * FROM slots WHERE id = ?", (slot_id,))
    if slot is None or not fulfillment_service.reserve(conn, slot_id, takehome):
        return None

    series_keys = []
    for line in lines:
        if line["item_type"] == "cut":
            row = db.one(conn, "SELECT market_series_key FROM cuts WHERE id = ?",
                         (line["ref_id"],))
            if row and row["market_series_key"]:
                series_keys.append(row["market_series_key"])
    snapshot = market.snapshot_for(conn, series_keys)

    code = new_code()
    tax_total = 0.0
    discount_total = 0.0
    cursor = conn.execute(
        "INSERT INTO orders(code, email, phone, customer_name, fulfillment, "
        "address_json, county, slot_id, subtotal, packing_total, "
        "delivery_fee, discount_total, tax_total, total, savings_total, "
        "market_snapshot_json, packing_json, terms_version, notes, status, "
        "referral_code, customer_id) "
        "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
        "'placed', ?, ?)",
        (code, email, phone, name, fulfillment,
         json.dumps(address), county, slot_id,
         totals["subtotal"], totals["packing_total"], totals["delivery_fee"],
         discount_total, tax_total, totals["total"], totals["savings"],
         json.dumps(snapshot),
         json.dumps(packing.describe(conn, order_packing) if has_beef else []),
         terms_version, notes, referral_code, customer_id))
    order_id = cursor.lastrowid

    for line in lines:
        conn.execute(
            "INSERT INTO order_items(order_id, item_type, ref_id, variant_id, "
            "store_slug, name, qty, unit, unit_price, line_total, "
            "packing_total, market_price, savings, packing_json, note) "
            "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (order_id, line["item_type"], line["ref_id"],
             line.get("variant_id"),
             line.get("store_slug", "beef"), line["name"],
             line["qty"], line["unit"], line["price_per_lb"],
             line["base_total"], line["packing_total"], line["market_price"],
             line["savings"], json.dumps(line["packing"]), line["note"]))
        if line["item_type"] == "cut":
            conn.execute("UPDATE cuts SET stock_lbs = MAX(0, stock_lbs - ?) "
                         "WHERE id = ?",
                         (line["takehome_lbs"], line["ref_id"]))
        elif line["item_type"] == "product":
            if line.get("variant_id"):
                conn.execute("UPDATE product_variants SET stock = stock - ? "
                             "WHERE id = ? AND stock >= ? AND active = 1",
                             (line["qty"], line["variant_id"], line["qty"]))
            else:
                conn.execute("UPDATE products SET stock = stock - ? "
                             "WHERE id = ? AND stock >= ? AND active = 1",
                             (line["qty"], line["ref_id"], line["qty"]))

    if subscribe:
        _create_subscription(conn, email, subscribe, order_id, totals)

    conn.execute("DELETE FROM cart_items WHERE cart_id = ?", (cart_id,))
    db.log_audit(conn, "order.placed", "order", order_id,
                 json.dumps({"code": code, "total": totals["total"],
                             "fulfillment": fulfillment}), actor="shop")
    conn.commit()
    return order_id, code


def _create_subscription(conn: db.sqlite3.Connection, email: str,
                          cadence: str, order_id: int,
                          totals: dict[str, Any]) -> None:
    from .. import web
    content = web.shop_content(conn)
    discount = float(content.get("share_discount", 5.0))
    if cadence == "quarterly":
        discount = float(content.get("share_discount_quarterly", 8.0))
    subscriber = db.one(conn, "SELECT * FROM subscribers WHERE email = ?",
                        (email,))
    if subscriber is None:
        token = secrets.token_urlsafe(16)
        conn.execute(
            "INSERT INTO subscribers(email, cadence, discount_pct, token, "
            "status) VALUES(?, ?, ?, ?, 'active')",
            (email, cadence, discount, token))
        subscriber = db.one(conn, "SELECT * FROM subscribers WHERE email = ?",
                            (email,))
    cadence_days = {"weekly": 7, "biweekly": 14, "monthly": 30,
                    "quarterly": 91}
    next_date = (_dt.date.today()
                 + _dt.timedelta(days=cadence_days.get(cadence, 30))).isoformat()
    conn.execute(
        "INSERT INTO subscriptions(subscriber_id, order_id, items_json, "
        "status, cadence, next_date) VALUES(?, ?, ?, 'active', ?, ?)",
        (subscriber["id"], order_id,
         json.dumps([{k: v for k, v in line.items()
                      if k in ("item_type", "ref_id", "name", "qty",
                               "packing")} for line in totals["lines"]]),
         cadence, next_date))
    conn.execute("UPDATE subscribers SET cadence = ?, next_date = ? "
                 "WHERE id = ?",
                 (cadence, next_date, subscriber["id"]))


def by_code(conn: db.sqlite3.Connection, code: str) -> db.sqlite3.Row | None:
    return db.one(conn, "SELECT * FROM orders WHERE code = ?", (code,))


def order_items(conn: db.sqlite3.Connection, order_id: int) -> list[db.sqlite3.Row]:
    return db.rows(conn, "SELECT * FROM order_items WHERE order_id = ? "
                         "ORDER BY id", (order_id,))


def slot_for(conn: db.sqlite3.Connection, order: db.sqlite3.Row) -> db.sqlite3.Row | None:
    if order["slot_id"] is None:
        return None
    return db.one(conn, "SELECT * FROM slots WHERE id = ?",
                  (order["slot_id"],))


def ics_for(conn: db.sqlite3.Connection, order: db.sqlite3.Row) -> str | None:
    slot = slot_for(conn, order)
    if slot is None:
        return None
    try:
        day = _dt.date.fromisoformat(slot["service_date"])
        start = _dt.datetime.combine(
            day, _dt.datetime.strptime(slot["window_start"], "%H:%M").time())
        end = _dt.datetime.combine(
            day, _dt.datetime.strptime(slot["window_end"], "%H:%M").time())
    except (ValueError, TypeError):
        return None
    stamp = "YYYYMMDDTHHMMSS"
    summary = (f"Runchero pickup {order['code']}" if order["fulfillment"] == "pickup"
               else f"Runchero delivery {order['code']}")
    lines = [
        "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Runchero Beef//EN",
        "BEGIN:VEVENT",
        f"UID:{order['code']}@runchero",
        f"DTSTAMP:{_dt.datetime.now().strftime(stamp)}",
        f"DTSTART:{start.strftime(stamp)}",
        f"DTEND:{end.strftime(stamp)}",
        f"SUMMARY:{summary}",
        "END:VEVENT", "END:VCALENDAR",
    ]
    return "\r\n".join(lines) + "\r\n"
