"""Checkout: one page, anchored steps, one submit.

Steps live in one form so nothing is lost between pages: packing choices,
fulfillment, the slot, and payment all submit together. Pickup skips the
address entirely. Every surcharge is priced before the customer commits.
"""
from __future__ import annotations

import json
import re

from .. import db, web
from ..services import cart as cart_service
from ..services import customers
from ..services import fulfillment, orders, packing as packing_service
from ..services import payments
from . import cart_count, cart_id, flash, page_context, redirect

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_CARD_RE = re.compile(r"^[\d\s]{12,23}$")


def register(add) -> None:
    add("GET", re.compile(r"^/checkout$"), checkout)
    add("POST", re.compile(r"^/checkout$"), submit)


def _context(conn, req, totals, content, errors=None, values=None):
    cid = cart_id(req)
    customer = customers.current(conn, req)
    if not values and customer is not None:
        saved = customers.address(conn, customer)
        values = {
            "name": customer["name"],
            "email": customer["email"],
            "phone": customer["phone"],
            "fulfillment": customer["fulfillment"],
            "line1": saved["line1"],
            "line2": saved["line2"],
            "city": saved["city"],
            "state": saved["state"],
            "zip": saved["zip"],
            "county": customer["county"],
            "notes": customer["delivery_notes"],
        }
    need = float(totals.get("takehome_lbs") or 0.0) or 1.0
    fulfillment.ensure_slots(conn)
    line_groups: dict[int, dict] = {}
    for line in totals["lines"]:
        if line["item_type"] == "cut":
            groups = packing_service.line_groups_for(conn, line.get("tags"))
            if groups:
                line_groups[line["id"]] = groups
    line_packs = []
    for line in totals["lines"]:
        for group, opts in line_groups.get(line["id"], {}).items():
            line_packs.append({
                "item_id": line["id"],
                "name": line["name"],
                "group_code": group,
                "group_label": opts[0]["group_label"],
                "options": opts,
                "chosen": (line.get("packing") or {}).get(group, ""),
            })
    return page_context(
        conn, req,
        totals=totals, content=content,
        packing_groups=packing_service.options_by_group(conn),
        line_groups=line_groups,
        line_packs=line_packs,
        order_packing=(values or {}).get("_order_packing")
                      or req.session_get("order_packing") or {},
        pickup_slots=fulfillment.upcoming(conn, "pickup", limit=8, need_lbs=need),
        delivery_slots=fulfillment.upcoming(conn, "delivery", limit=8,
                                            need_lbs=need),
        counties=fulfillment.DELIVERY_COUNTIES,
        csrf=req.csrf_token(),
        customer=customer,
        errors=errors or {},
        values=values or {},
        payment_provider=config_name(),
        cart_count=cart_count(conn, req))


def config_name() -> str:
    from .. import config
    return config.PAYMENT_PROVIDER


def checkout(conn: db.sqlite3.Connection, req, **_):
    content = web.shop_content(conn)
    totals = cart_service.totals(conn, cart_id(req),
                                 req.session_get("order_packing"), content)
    if not totals["lines"]:
        flash(req, "Your cart is empty. Add something first.", "warn")
        return redirect("/shop")
    context = _context(conn, req, totals, content)
    return 200, "text/html; charset=utf-8", web.render("checkout.html", **context)


def submit(conn: db.sqlite3.Connection, req, **_):
    content = web.shop_content(conn)
    cid = cart_id(req)
    customer = customers.current(conn, req)
    form = req.form
    errors: dict[str, str] = {}

    if not req.csrf_ok():
        flash(req, "Your session expired. Please try again.", "error")
        return redirect("/checkout")

    order_packing = _collect_order_packing(conn, form)
    req.session_set("order_packing", order_packing)
    _apply_line_packing(conn, cid, form)
    totals = cart_service.totals(conn, cid, order_packing, content)
    if not totals["lines"]:
        flash(req, "Your cart is empty.", "warn")
        return redirect("/shop")
    if not totals["meets_min"]:
        errors["cart"] = (f"Orders start at ${content['min_order']:.0f}. "
                          f"Add ${totals['to_min_order']:.2f} more to check out.")

    fulfillment_kind = form.get("fulfillment", "")
    if fulfillment_kind not in ("pickup", "delivery"):
        errors["fulfillment"] = "Choose pickup or delivery."

    name = (form.get("name") or "").strip()
    email = (form.get("email") or "").strip().lower()
    phone = (form.get("phone") or "").strip()
    if len(name) < 2:
        errors["name"] = "Tell us who to expect."
    if not _EMAIL_RE.match(email):
        errors["email"] = "We need a working email for your receipt."
    if len(phone) < 7:
        errors["phone"] = "A phone number helps the driver find you."

    address: dict = {}
    county = ""
    if fulfillment_kind == "delivery":
        address = {
            "line1": (form.get("line1") or "").strip(),
            "line2": (form.get("line2") or "").strip(),
            "city": (form.get("city") or "").strip(),
            "state": (form.get("state") or "KY").strip().upper(),
            "zip": (form.get("zip") or "").strip(),
        }
        county = (form.get("county") or "").strip().title()
        if len(address["line1"]) < 4:
            errors["line1"] = "We need a street address to deliver."
        if len(address["city"]) < 2:
            errors["city"] = "Which town?"
        if not re.match(r"^\d{5}$", address["zip"] or ""):
            errors["zip"] = "A five digit ZIP, please."
        if not fulfillment.county_allowed(county):
            errors["county"] = ("We deliver to " +
                                ", ".join(fulfillment.DELIVERY_COUNTIES) +
                                " counties.")

    slot_id = 0
    try:
        slot_id = int(form.get("slot", "0") or 0)
    except ValueError:
        slot_id = 0
    slot = db.one(conn, "SELECT * FROM slots WHERE id = ?", (slot_id,)) \
        if slot_id else None
    if slot is None:
        errors["slot"] = "Pick a pickup time or delivery window."
    elif slot["kind"] != fulfillment_kind:
        errors["slot"] = ("That time is for " +
                          ("pickup" if slot["kind"] == "pickup" else "delivery") +
                          ". Choose one that matches your choice above.")
    elif not fulfillment.order_open(slot):
        errors["slot"] = "That window has closed. Please pick another."

    takehome = float(totals.get("takehome_lbs") or 0.0) or 1.0
    if slot is not None and fulfillment.remaining_lbs(slot) + 0.001 < takehome:
        errors["slot"] = "That window is full for an order this size."

    terms_ok = form.get("terms") == "on"
    if not terms_ok:
        errors["terms"] = "Please accept the terms to place the order."

    card = (form.get("card") or "").strip()
    exp = (form.get("exp") or "").strip()
    cvc = (form.get("cvc") or "").strip()
    if not _CARD_RE.match(card):
        errors["card"] = "Enter the card number as it reads on the card."
    if not re.match(r"^\d{2}\s*/\s*\d{2,4}$", exp):
        errors["exp"] = "Expiry as MM/YY."
    if not re.match(r"^\d{3,4}$", cvc):
        errors["cvc"] = "The three digits on the back."

    if errors:
        context = _context(conn, req, totals, content, errors=errors,
                           values={**form, "_order_packing": order_packing})
        return 200, "text/html; charset=utf-8", web.render("checkout.html", **context)

    subscribe = form.get("subscribe") or ""
    if subscribe and subscribe not in ("weekly", "biweekly", "monthly",
                                       "quarterly"):
        subscribe = ""

    placed = orders.place(
        conn, cart_id=cid, email=email, phone=phone, name=name,
        fulfillment=fulfillment_kind, county=county, address=address,
        slot_id=slot_id, order_packing=order_packing, totals=totals,
        notes=(form.get("notes") or "").strip(),
        terms_version=str(content.get("terms_version", "1.0")),
        subscribe=subscribe,
        referral_code=(form.get("referral") or "").strip(),
        customer_id=customer["id"] if customer is not None else None)
    if placed is None:
        errors["slot"] = "That window just filled up. Please pick another."
        context = _context(conn, req, totals, content, errors=errors,
                           values={**form, "_order_packing": order_packing})
        return 200, "text/html; charset=utf-8", web.render("checkout.html", **context)

    order_id, code = placed
    charge = payments.provider().charge(
        totals["total"], f"Runchero Beef order {code}",
        {"card": card, "email": email, "name": name})
    if charge.ok:
        conn.execute("UPDATE orders SET payment_status = 'paid', "
                     "payment_ref = ? WHERE id = ?",
                     (charge.reference, order_id))
        conn.commit()
        flash(req, f"Order {code} placed. See you at the pickup!", "ok")
        return redirect(f"/order/{code}")
    conn.execute("UPDATE orders SET payment_status = 'failed' WHERE id = ?",
                 (order_id,))
    conn.commit()
    errors["card"] = (charge.error or
                      "The payment did not go through. Try another card.")
    context = _context(conn, req, totals, content, errors=errors,
                       values={**form, "_order_packing": order_packing})
    return 200, "text/html; charset=utf-8", web.render("checkout.html", **context)


def _collect_order_packing(conn, form) -> dict[str, str]:
    allowed = {row["group_code"] for row in packing_service.options(conn)}
    choice = {key: value for key, value in form.items()
              if key in allowed and value and value != "standard"}
    return choice


def _apply_line_packing(conn, cid: str, form) -> None:
    """Save the pack size the customer picked for a specific cart line.

    Line choices come in as ``line_<cart item id>_<group>`` fields so one
    radio group per line can live in the same form as everything else.
    """
    allowed = packing_service.group_codes(conn)
    for key, value in form.items():
        if not key.startswith("line_") or not value:
            continue
        parts = key.split("_")
        if len(parts) != 3:
            continue
        try:
            item_id = int(parts[1])
        except ValueError:
            continue
        group = parts[2]
        if group not in allowed:
            continue
        current = cart_service.line_packing(conn, cid, item_id)
        current[group] = value
        cart_service.set_line_packing(conn, cid, item_id, current)
