"""Customer accounts: sign up, sign in, profile, preferences, order history.

Passwords use the same PBKDF2 helper as the admin console. Email verification
is modelled in the schema and the sign-up flow, but the demo verifies
immediately instead of sending mail; swapping in a real mailer later only
means setting ``verify=False`` and sending the token.
"""
from __future__ import annotations

import datetime as _dt
import json
import re
from typing import Any

from .. import db
from . import auth

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MIN_PASSWORD = 8

CONTACT_METHODS = ("email", "phone", "text")
FULFILLMENT_KINDS = ("pickup", "delivery")


def normalise_email(email: str) -> str:
    return (email or "").strip().lower()


def email_ok(email: str) -> bool:
    return bool(EMAIL_RE.match(normalise_email(email)))


def by_id(conn: db.sqlite3.Connection, customer_id: int) -> db.sqlite3.Row | None:
    return db.one(conn, "SELECT * FROM customers WHERE id = ?", (customer_id,))


def by_email(conn: db.sqlite3.Connection,
             email: str) -> db.sqlite3.Row | None:
    return db.one(conn, "SELECT * FROM customers WHERE email = ?",
                  (normalise_email(email),))


def current(conn: db.sqlite3.Connection, req) -> db.sqlite3.Row | None:
    """The signed-in customer for this request, if any."""
    if req is None:
        return None
    customer_id = req.session_get("customer_id")
    if not customer_id:
        return None
    row = by_id(conn, customer_id)
    if row is None:
        req.session_pop("customer_id")
    return row


def create(conn: db.sqlite3.Connection, *, email: str, password: str,
           name: str, phone: str = "", verify: bool = True) -> db.sqlite3.Row:
    email = normalise_email(email)
    now = _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        "INSERT INTO customers(email, passhash, name, phone, email_verified, "
        "verified_at) VALUES(?, ?, ?, ?, ?, ?)",
        (email, auth.hash_password(password), name.strip(), phone.strip(),
         1 if verify else 0, now if verify else ""))
    conn.commit()
    row = by_email(conn, email)
    assert row is not None
    return row


def authenticate(conn: db.sqlite3.Connection, email: str,
                 password: str) -> db.sqlite3.Row | None:
    row = by_email(conn, email)
    if row is None or not auth.check_password(password, row["passhash"]):
        return None
    conn.execute("UPDATE customers SET last_login = datetime('now') "
                 "WHERE id = ?", (row["id"],))
    conn.commit()
    return by_id(conn, row["id"])


def update_profile(conn: db.sqlite3.Connection, customer_id: int, *,
                   name: str, phone: str) -> None:
    conn.execute("UPDATE customers SET name = ?, phone = ? WHERE id = ?",
                 (name.strip(), phone.strip(), customer_id))
    conn.commit()


def update_email(conn: db.sqlite3.Connection, customer_id: int, email: str,
                 verify: bool = True) -> None:
    now = _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = db.one(conn, "SELECT email FROM customers WHERE id = ?",
                 (customer_id,))
    old = row["email"] if row else ""
    new = normalise_email(email)
    conn.execute(
        "UPDATE customers SET email = ?, email_verified = ?, verified_at = ? "
        "WHERE id = ?",
        (new, 1 if verify else 0, now if verify else "", customer_id))
    # Standing orders follow the household, unless the new address already
    # belongs to another subscriber (the column is UNIQUE).
    if old and old != new:
        conn.execute(
            "UPDATE subscribers SET email = ? WHERE email = ? "
            "AND NOT EXISTS (SELECT 1 FROM subscribers WHERE email = ?)",
            (new, old, new))
    conn.commit()


def change_password(conn: db.sqlite3.Connection, customer_id: int,
                    password: str) -> None:
    conn.execute("UPDATE customers SET passhash = ? WHERE id = ?",
                 (auth.hash_password(password), customer_id))
    conn.commit()


def address(conn: db.sqlite3.Connection,
            customer: db.sqlite3.Row) -> dict[str, str]:
    try:
        data = json.loads(customer["address_json"] or "{}")
    except (ValueError, TypeError):
        data = {}
    if not isinstance(data, dict):
        data = {}
    return {
        "line1": str(data.get("line1") or ""),
        "line2": str(data.get("line2") or ""),
        "city": str(data.get("city") or ""),
        "state": str(data.get("state") or "KY"),
        "zip": str(data.get("zip") or ""),
    }


def save_preferences(conn: db.sqlite3.Connection, customer_id: int, *,
                     fulfillment: str, address: dict[str, str], county: str,
                     delivery_notes: str, recurring_day: int,
                     contact_method: str, market_updates: bool) -> None:
    conn.execute(
        "UPDATE customers SET fulfillment = ?, address_json = ?, county = ?, "
        "delivery_notes = ?, recurring_day = ?, contact_method = ?, "
        "market_updates = ? WHERE id = ?",
        (fulfillment, json.dumps(address), county,
         delivery_notes.strip(), recurring_day, contact_method,
         1 if market_updates else 0, customer_id))
    conn.commit()


def orders_for(conn: db.sqlite3.Connection, customer: db.sqlite3.Row,
               limit: int | None = None) -> list[db.sqlite3.Row]:
    sql = ("SELECT * FROM orders "
           "WHERE customer_id = ? "
           "   OR (customer_id IS NULL AND lower(email) = lower(?)) "
           "ORDER BY created_at DESC, id DESC")
    params: list[Any] = [customer["id"], customer["email"]]
    if limit:
        sql += " LIMIT ?"
        params.append(limit)
    return db.rows(conn, sql, params)


def order_stats(conn: db.sqlite3.Connection,
                customer: db.sqlite3.Row) -> dict[str, Any]:
    orders = orders_for(conn, customer)
    spend = sum(float(row["total"] or 0) for row in orders
                if row["payment_status"] in ("paid", "pending"))
    return {
        "count": len(orders),
        "spend": spend,
        "last": orders[0] if orders else None,
    }


def subscriber_for(conn: db.sqlite3.Connection,
                   customer: db.sqlite3.Row) -> db.sqlite3.Row | None:
    """The standing-order record that shares this customer's email."""
    return db.one(conn, "SELECT * FROM subscribers WHERE email = ?",
                  (customer["email"],))
