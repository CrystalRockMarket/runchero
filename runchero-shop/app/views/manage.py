"""Subscription management: token link, skip, pause, resume, cancel."""
from __future__ import annotations

import re

from .. import db, web
from . import cart_count, flash, page_context, redirect


def register(add) -> None:
    add("GET", re.compile(r"^/manage$"), entry)
    add("POST", re.compile(r"^/manage$"), entry_post)
    add("GET", re.compile(r"^/manage/(?P<token>[A-Za-z0-9_-]+)$"), manage)
    add("POST", re.compile(r"^/manage/(?P<token>[A-Za-z0-9_-]+)$"), manage_post)


def entry(conn: db.sqlite3.Connection, req, **_):
    context = page_context(conn, req, csrf=req.csrf_token(),
                           cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("manage_entry.html",
                                                       **context)


def entry_post(conn: db.sqlite3.Connection, req, **_):
    if not req.csrf_ok():
        return redirect("/manage")
    email = (req.form.get("email") or "").strip().lower()
    row = db.one(conn, "SELECT * FROM subscribers WHERE email = ?", (email,))
    if row is None:
        flash(req, "No subscription found for that email.", "warn")
        return redirect("/manage")
    return redirect(f"/manage/{row['token']}")


def _load(conn, token: str):
    return db.one(conn, "SELECT * FROM subscribers WHERE token = ?", (token,))


def _subscriptions(conn, subscriber_id: int):
    return db.rows(conn, "SELECT * FROM subscriptions WHERE subscriber_id = ? "
                         "ORDER BY id DESC", (subscriber_id,))


def manage(conn: db.sqlite3.Connection, req, token: str, **_):
    subscriber = _load(conn, token)
    if subscriber is None:
        from . import not_found
        return not_found(conn, req, message="That manage link is not valid.")
    subs = _subscriptions(conn, subscriber["id"])
    import json
    items = []
    for sub in subs:
        try:
            items.append(json.loads(sub["items_json"] or "[]"))
        except (ValueError, TypeError):
            items.append([])
    context = page_context(
        conn, req, subscriber=subscriber,
        pairs=list(zip(subs, items)),
        csrf=req.csrf_token(),
        cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("manage.html", **context)


def manage_post(conn: db.sqlite3.Connection, req, token: str, **_):
    subscriber = _load(conn, token)
    if subscriber is None:
        from . import not_found
        return not_found(conn, req, message="That manage link is not valid.")
    if not req.csrf_ok():
        return redirect(f"/manage/{token}")
    action = req.form.get("action", "")
    sub_id = 0
    try:
        sub_id = int(req.form.get("sub", "0") or 0)
    except ValueError:
        sub_id = 0
    sub = db.one(conn,
                 "SELECT * FROM subscriptions WHERE id = ? AND subscriber_id = ?",
                 (sub_id, subscriber["id"])) if sub_id else None

    if action == "skip" and sub is not None:
        conn.execute("UPDATE subscriptions SET skips = skips + 1 WHERE id = ?",
                     (sub_id,))
        _note(conn, sub_id, "A delivery was skipped.")
        flash(req, "Next delivery skipped.", "ok")
    elif action == "pause" and sub is not None:
        conn.execute("UPDATE subscriptions SET status = 'paused' WHERE id = ?",
                     (sub_id,))
        _note(conn, sub_id, "Paused at customer request.")
        flash(req, "Subscription paused.", "ok")
    elif action == "resume" and sub is not None:
        conn.execute("UPDATE subscriptions SET status = 'active' WHERE id = ?",
                     (sub_id,))
        _note(conn, sub_id, "Resumed at customer request.")
        flash(req, "Subscription resumed.", "ok")
    elif action == "cancel" and sub is not None:
        conn.execute("UPDATE subscriptions SET status = 'cancelled' WHERE id = ?",
                     (sub_id,))
        _note(conn, sub_id, "Cancelled at customer request. No phone call "
                           "required.")
        flash(req, "Subscription cancelled. You will not be billed again.", "ok")
    elif action == "cadence" and sub is not None:
        cadence = req.form.get("cadence", "")
        if cadence in ("weekly", "biweekly", "monthly", "quarterly"):
            conn.execute("UPDATE subscriptions SET cadence = ? WHERE id = ?",
                         (cadence, sub_id))
            _note(conn, sub_id, f"Cadence changed to {cadence}.")
            flash(req, f"Cadence changed to {cadence}.", "ok")
    elif action == "cancel_all":
        conn.execute("UPDATE subscriptions SET status = 'cancelled' "
                     "WHERE subscriber_id = ?", (subscriber["id"],))
        conn.execute("UPDATE subscribers SET status = 'cancelled' WHERE id = ?",
                     (subscriber["id"],))
        flash(req, "All subscriptions cancelled.", "ok")
    conn.commit()
    return redirect(f"/manage/{token}")


def _note(conn, sub_id: int, text: str) -> None:
    conn.execute("INSERT INTO subscription_events(subscription_id, event, "
                 "detail) VALUES(?, 'change', ?)", (sub_id, text))
