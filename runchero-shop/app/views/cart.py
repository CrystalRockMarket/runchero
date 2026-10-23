"""Cart page and the cart form actions."""
from __future__ import annotations

import json
import re

from .. import db, web
from ..services import cart as cart_service
from ..services import packing as packing_service
from . import cart_count, cart_id, flash, page_context, redirect


def register(add) -> None:
    add("GET", re.compile(r"^/cart$"), view)
    add("POST", re.compile(r"^/cart/add$"), add_item)
    add("POST", re.compile(r"^/cart/qty$"), set_qty)
    add("POST", re.compile(r"^/cart/remove$"), remove_item)
    add("POST", re.compile(r"^/cart/packing$"), set_packing)
    add("POST", re.compile(r"^/cart/clear$"), clear)


def _totals(conn, req, order_packing=None):
    content = web.shop_content(conn)
    cid = cart_id(req)
    return cart_service.totals(conn, cid, order_packing, content), content, cid


def view(conn: db.sqlite3.Connection, req, **_):
    totals, content, cid = _totals(conn, req, req.session_get("order_packing"))
    line_groups: dict[int, dict] = {}
    for line in totals["lines"]:
        if line["item_type"] == "cut":
            groups = packing_service.line_groups_for(conn, line.get("tags"))
            if groups:
                line_groups[line["id"]] = groups
    context = page_context(
        conn, req,
        totals=totals, content=content,
        packing_groups=packing_service.options_by_group(conn),
        line_groups=line_groups,
        order_packing=req.session_get("order_packing") or {},
        csrf=req.csrf_token(),
        cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("cart.html", **context)


def add_item(conn: db.sqlite3.Connection, req, **_):
    if not req.csrf_ok():
        flash(req, "Your session expired. Please try again.", "error")
        return redirect("/cart")
    form = req.form
    item_type = form.get("type", "cut")
    try:
        ref_id = int(form.get("ref", "0"))
        qty = max(0.25, float(form.get("qty", "1") or 1))
    except ValueError:
        flash(req, "That quantity does not look right.", "error")
        return redirect("/cart")
    if item_type not in ("cut", "package", "share", "product") or ref_id <= 0:
        flash(req, "We could not add that item.", "error")
        return redirect("/cart")
    variant_id = None
    if item_type == "product":
        try:
            variant_id = int(form.get("variant_id") or 0) or None
        except ValueError:
            variant_id = None
        line = _product_line(conn, ref_id, variant_id, qty)
        if line is None:
            flash(req, "That product is currently out of stock.", "error")
            return redirect("/cart")
        store_slug = line["store_slug"]
        slug = line["slug"]
        if line["unit"] != "lb" and not qty.is_integer():
            flash(req, "Choose a whole number of packages.", "error")
            return redirect(f"/{store_slug}/{slug}")
        current_qty = float(db.scalar(
            conn, "SELECT COALESCE(SUM(qty), 0) FROM cart_items "
            "WHERE cart_id = ? AND item_type = 'product' AND ref_id = ? "
            "AND (variant_id IS ? OR variant_id = ?)",
            (cart_id(req), ref_id, variant_id, variant_id)) or 0)
        if current_qty + qty > float(line["stock_lbs"]):
            flash(req, f"Only {line['stock_lbs']:g} are available.", "error")
            return redirect(f"/{store_slug}/{slug}")
    try:
        choice = json.loads(form.get("packing", "{}") or "{}")
        if not isinstance(choice, dict):
            choice = {}
    except (ValueError, TypeError):
        choice = {}
    # Line level choices arrive as plain fields named after their group.
    allowed = packing_service.group_codes(conn)
    for group in allowed:
        value = form.get(group)
        if value:
            choice[group] = value
    cart_service.add(conn, cart_id(req), item_type, ref_id, qty,
                     choice, form.get("note", ""), variant_id)
    name = form.get("name", "Item")
    flash(req, f"Added {name} to your cart.", "ok")
    return redirect(form.get("next") or "/cart")


def _product_line(conn: db.sqlite3.Connection, product_id: int,
                  variant_id: int | None, qty: float) -> dict | None:
    """Resolve a product (with optional variant) into a cart line dict,
    or None if it cannot be stocked."""
    variant = None
    if variant_id:
        variant = db.one(conn,
                         "SELECT * FROM product_variants WHERE id = ? "
                         "AND active = 1", (variant_id,))
    if variant is None:
        variant = db.one(conn,
                         "SELECT * FROM product_variants WHERE product_id = ? "
                         "AND active = 1 ORDER BY sort_order, id LIMIT 1",
                         (product_id,))
    row = db.one(conn,
                 "SELECT * FROM products WHERE id = ? AND active = 1",
                 (variant["product_id"] if variant else product_id,))
    if row is None:
        return None
    if variant:
        price = float(variant["price"])
        unit = variant["unit"]
        unit_lbs = float(variant["unit_lbs"]) or 0.0
        stock = float(variant["stock"])
        name = f"{row['name']} · {variant['size_label']}"
    else:
        price = float(row["price"])
        unit = row["unit"]
        unit_lbs = float(row["unit_lbs"]) or 0.0
        stock = float(row["stock"])
        name = row["name"]
    if stock <= 0:
        return None
    return {
        "store_slug": row["store_slug"],
        "slug": row["slug"],
        "name": name,
        "unit": unit,
        "unit_lbs": unit_lbs,
        "stock_lbs": stock,
    }


def set_qty(conn: db.sqlite3.Connection, req, **_):
    if not req.csrf_ok():
        return redirect("/cart")
    try:
        item_id = int(req.form.get("id", "0"))
        qty = float(req.form.get("qty", "1"))
    except ValueError:
        return redirect("/cart")
    if item_id > 0:
        row = db.one(conn,
                     "SELECT item_type, ref_id, variant_id FROM cart_items "
                     "WHERE id = ? AND cart_id = ?", (item_id, cart_id(req)))
        if row and row["item_type"] == "product":
            line = _product_line(conn, row["ref_id"], row["variant_id"], qty)
            if line is None:
                product = db.one(conn,
                                 "SELECT slug, store_slug FROM products "
                                 "WHERE id = ?", (row["ref_id"],))
                flash(req, "That quantity is not available.", "error")
                return redirect(f"/{product['store_slug']}/{product['slug']}"
                                if product else "/cart")
        cart_service.set_qty(conn, cart_id(req), item_id, qty)
    return redirect("/cart")


def remove_item(conn: db.sqlite3.Connection, req, **_):
    if not req.csrf_ok():
        return redirect("/cart")
    try:
        item_id = int(req.form.get("id", "0"))
    except ValueError:
        return redirect("/cart")
    if item_id > 0:
        cart_service.remove(conn, cart_id(req), item_id)
        flash(req, "Removed from your cart.", "ok")
    return redirect("/cart")


def set_packing(conn: db.sqlite3.Connection, req, **_):
    if not req.csrf_ok():
        return redirect("/cart")
    form = req.form
    if form.get("scope") == "order":
        allowed = {row["group_code"] for row in packing_service.options(conn)}
        choice = {key: value for key, value in form.items()
                  if key in allowed and value}
        req.session_set("order_packing", choice)
        flash(req, "Packing preferences saved.", "ok")
        return redirect("/cart")
    try:
        item_id = int(form.get("id", "0"))
    except ValueError:
        return redirect("/cart")
    if item_id <= 0:
        return redirect("/cart")
    allowed = {row["group_code"] for row in packing_service.options(conn)}
    choice = {key: value for key, value in form.items()
              if key in allowed and value}
    cart_service.set_line_packing(conn, cart_id(req), item_id, choice)
    flash(req, "Packing choice saved for that line.", "ok")
    return redirect("/cart")


def clear(conn: db.sqlite3.Connection, req, **_):
    if not req.csrf_ok():
        return redirect("/cart")
    cart_service.clear(conn, cart_id(req))
    flash(req, "Your cart is empty.", "ok")
    return redirect("/cart")
