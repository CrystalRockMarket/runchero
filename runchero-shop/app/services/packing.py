"""Packing options: wrap style, portioning, bagging, gift wrap, extras.

Everything here is priced per pound unless it is explicitly a per-cut or
per-order charge, so the surcharge scales honestly with a 3 lb steak versus
a 79 lb share. The savings badge always refers to the base cut price, before
any packing choice, and the product page says so.
"""
from __future__ import annotations

import json
from typing import Any

from .. import db


def groups(conn: db.sqlite3.Connection) -> list[db.sqlite3.Row]:
    return db.rows(conn, "SELECT * FROM packing_groups ORDER BY sort_order")


def options(conn: db.sqlite3.Connection,
            group_code: str | None = None) -> list[db.sqlite3.Row]:
    sql = ("SELECT po.*, pg.label AS group_label, pg.scope AS group_scope "
           "FROM packing_options po "
           "JOIN packing_groups pg ON pg.code = po.group_code")
    params: list[Any] = []
    if group_code:
        sql += " WHERE po.group_code = ?"
        params.append(group_code)
    sql += " ORDER BY po.group_code, po.sort_order, po.id"
    return db.rows(conn, sql, params)


def options_by_group(conn: db.sqlite3.Connection) -> dict[str, list[db.sqlite3.Row]]:
    out: dict[str, list[db.sqlite3.Row]] = {}
    for row in options(conn):
        out.setdefault(row["group_code"], []).append(row)
    return out


def group_codes(conn: db.sqlite3.Connection) -> set[str]:
    return {row["group_code"] for row in options(conn)}


def line_groups_for(conn: db.sqlite3.Connection,
                    tags: str | None) -> dict[str, list[db.sqlite3.Row]]:
    """Line level packing groups that apply to a cut with these tags.

    Ground beef, for example, is sold in 1, 2, 5, or 10 lb packs, and that
    choice belongs to the line rather than to the whole order.
    """
    item = {"item_type": "cut", "tags": tags or ""}
    out: dict[str, list[db.sqlite3.Row]] = {}
    for group in groups(conn):
        if (group["scope"] or "line").strip() != "line":
            continue
        applicable = [row for row in options(conn, group["code"])
                      if _applies(row, item)]
        if applicable:
            out[group["code"]] = applicable
    return out


def default_for(conn: db.sqlite3.Connection, group_code: str) -> db.sqlite3.Row | None:
    return db.one(conn,
                  "SELECT * FROM packing_options WHERE group_code = ? "
                  "AND is_default = 1 LIMIT 1", (group_code,))


def option_by_code(conn: db.sqlite3.Connection, group_code: str,
                   code: str) -> db.sqlite3.Row | None:
    return db.one(conn,
                  "SELECT po.*, pg.label AS group_label, pg.scope AS group_scope "
                  "FROM packing_options po "
                  "JOIN packing_groups pg ON pg.code = po.group_code "
                  "WHERE po.group_code = ? AND po.code = ?", (group_code, code))


def _applies(row: db.sqlite3.Row, item: dict[str, Any]) -> bool:
    target = (row["applies_to"] or "all").strip()
    if not target or target == "all":
        return True
    try:
        tags = json.loads(target)
    except (ValueError, TypeError):
        tags = [t.strip() for t in target.split(",") if t.strip()]
    if not tags:
        return True
    item_tags = set((item.get("tags") or "").split(","))
    item_type = item.get("item_type") or ""
    ref = str(item.get("ref_id") or "")
    for tag in tags:
        if tag in item_tags or tag == item_type or tag == ref:
            return True
    return False


def line_surcharge(conn: db.sqlite3.Connection, item: dict[str, Any],
                   qty: float, lbs: float, base_price: float,
                   packing: dict[str, str] | None) -> float:
    """The packing surcharge for one cart line under one set of choices."""
    if not packing:
        return 0.0
    total = 0.0
    for group_code, code in packing.items():
        if code in ("", None, "standard"):
            continue
        row = option_by_code(conn, group_code, code)
        if row is None or not _applies(row, item):
            continue
        mode = row["price_mode"]
        amount = float(row["amount"])
        if mode == "per_lb":
            total += amount * lbs
        elif mode == "per_unit":
            total += amount * max(1.0, qty)
        elif mode == "percent":
            total += base_price * amount / 100.0
        elif mode == "flat":
            total += amount
    return round(total, 2)


def order_surcharge(conn: db.sqlite3.Connection, packing: dict[str, str],
                    lines: list[dict[str, Any]]) -> float:
    """Flat, order-wide charges such as a gift box, charged once."""
    if not packing:
        return 0.0
    total = 0.0
    for group_code, code in packing.items():
        if code in ("", None, "standard"):
            continue
        row = option_by_code(conn, group_code, code)
        if row is None or row["price_mode"] != "flat":
            continue
        applies = False
        for item in lines:
            if _applies(row, item):
                applies = True
                break
        if applies:
            total += float(row["amount"])
    return round(total, 2)


def describe(conn: db.sqlite3.Connection,
             packing: dict[str, str]) -> list[dict[str, Any]]:
    """Human readable packing summary for a receipt or a pick sheet."""
    out: list[dict[str, Any]] = []
    if not packing:
        return out
    for group_code, code in packing.items():
        if code in ("", None, "standard"):
            continue
        row = option_by_code(conn, group_code, code)
        if row is None:
            continue
        out.append({
            "group": group_code,
            "group_label": row["group_label"],
            "code": code,
            "label": row["label"],
            "price_mode": row["price_mode"],
            "amount": float(row["amount"]),
        })
    return out
