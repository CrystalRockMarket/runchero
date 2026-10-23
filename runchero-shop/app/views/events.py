"""Community events: public calendar and admin CRUD."""
from __future__ import annotations

import re

from .. import db, web
from ..services import events as events_service
from . import cart_count, page_context, not_found, redirect, flash


def register(add) -> None:
    add("GET", re.compile(r"^/events$"), events_list)
    add("GET", re.compile(r"^/admin/events$"), admin_events)
    add("POST", re.compile(r"^/admin/events$"), admin_events_create)
    add("GET", re.compile(r"^/admin/events/(?P<eid>\d+)/edit$"), admin_events_edit)
    add("POST", re.compile(r"^/admin/events/(?P<eid>\d+)/edit$"), admin_events_update)
    add("POST", re.compile(r"^/admin/events/(?P<eid>\d+)/delete$"), admin_events_delete)


def events_list(conn: db.sqlite3.Connection, req, **_):
    events = events_service.list_events(conn, active_only=True, upcoming_only=True)
    context = page_context(
        conn, req, events=events, cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("events.html", **context)


def admin_events(conn: db.sqlite3.Connection, req, **_):
    if not req.session_get("admin_id"):
        return redirect("/admin/login")
    events = events_service.list_events(conn, active_only=False)
    context = page_context(
        conn, req, events=events,
        cart_count=cart_count(conn, req),
        csrf=req.csrf_token(),
        admin_name=req.session_get("admin_name"))
    context["block_robots"] = True
    return 200, "text/html; charset=utf-8", web.render("admin/events.html", **context)


def admin_events_create(conn: db.sqlite3.Connection, req, **_):
    if not req.session_get("admin_id"):
        return redirect("/admin/login")
    if not req.csrf_ok():
        return redirect("/admin/events")
    events_service.create(
        conn, title=(req.form.get("title") or "").strip(),
        description=(req.form.get("description") or "").strip(),
        event_date=(req.form.get("event_date") or "").strip(),
        start_time=(req.form.get("start_time") or "").strip(),
        end_time=(req.form.get("end_time") or "").strip(),
        location=(req.form.get("location") or "").strip(),
        capacity=req.form.get("capacity") or 0,
        active=req.form.get("active") == "on",
        sort_order=req.form.get("sort_order") or 0)
    flash(req, "Event created.", "ok")
    return redirect("/admin/events")


def admin_events_edit(conn: db.sqlite3.Connection, req, eid, **_):
    if not req.session_get("admin_id"):
        return redirect("/admin/login")
    event = events_service.get(conn, int(eid))
    if event is None:
        return redirect("/admin/events")
    context = page_context(
        conn, req, event=event,
        cart_count=cart_count(conn, req),
        csrf=req.csrf_token(),
        admin_name=req.session_get("admin_name"))
    context["block_robots"] = True
    return 200, "text/html; charset=utf-8", web.render("admin/events_edit.html", **context)


def admin_events_update(conn: db.sqlite3.Connection, req, eid, **_):
    if not req.session_get("admin_id"):
        return redirect("/admin/login")
    if not req.csrf_ok():
        return redirect("/admin/events")
    events_service.update(
        conn, int(eid),
        title=(req.form.get("title") or "").strip(),
        description=(req.form.get("description") or "").strip(),
        event_date=(req.form.get("event_date") or "").strip(),
        start_time=(req.form.get("start_time") or "").strip(),
        end_time=(req.form.get("end_time") or "").strip(),
        location=(req.form.get("location") or "").strip(),
        capacity=req.form.get("capacity") or 0,
        active=req.form.get("active") == "on",
        sort_order=req.form.get("sort_order") or 0)
    flash(req, "Event updated.", "ok")
    return redirect("/admin/events")


def admin_events_delete(conn: db.sqlite3.Connection, req, eid, **_):
    if not req.session_get("admin_id"):
        return redirect("/admin/login")
    if not req.csrf_ok():
        return redirect("/admin/events")
    events_service.delete(conn, int(eid))
    flash(req, "Event removed.", "ok")
    return redirect("/admin/events")
