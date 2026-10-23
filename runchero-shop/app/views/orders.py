"""Order pages: the receipt, the pickup instructions, the calendar file."""
from __future__ import annotations

import re

from .. import db, web
from ..services import fulfillment, orders
from . import cart_count, flash, page_context, redirect


def register(add) -> None:
    add("GET", re.compile(r"^/orders$"), lookup)
    add("GET", re.compile(r"^/order/(?P<code>[A-Za-z0-9-]+)$"), show)
    add("GET", re.compile(r"^/order/(?P<code>[A-Za-z0-9-]+)\.ics$"), ics)


def lookup(conn: db.sqlite3.Connection, req, **_):
    code = (req.query.get("code") or "").strip()
    if code:
        order = orders.by_code(conn, code.upper())
        if order is not None:
            return redirect(f"/order/{order['code']}")
        flash(req, "No order matched that code.", "warn")
    context = page_context(conn, req, cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("orders.html", **context)


def show(conn: db.sqlite3.Connection, req, code: str, **_):
    order = orders.by_code(conn, code.upper())
    if order is None:
        from . import not_found
        return not_found(conn, req, message="We could not find that order.")
    items = orders.order_items(conn, order["id"])
    slot = orders.slot_for(conn, order)
    import json
    try:
        address = json.loads(order["address_json"] or "{}")
    except (ValueError, TypeError):
        address = {}
    try:
        packing_note = json.loads(order["packing_json"] or "[]")
    except (ValueError, TypeError):
        packing_note = []
    context = page_context(
        conn, req, order=order, items=items, slot=slot, address=address,
        has_beef=any(item["store_slug"] == "beef" for item in items),
        packing_note=packing_note,
        fulfillment=fulfillment,
        cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("order.html", **context)


def ics(conn: db.sqlite3.Connection, req, code: str, **_):
    order = orders.by_code(conn, code.upper())
    if order is None:
        return 404, "text/plain; charset=utf-8", "not found"
    body = orders.ics_for(conn, order)
    if body is None:
        return 404, "text/plain; charset=utf-8", "not found"
    return 200, "text/calendar; charset=utf-8", body
