"""Views: routes that render pages and handle form posts."""
from __future__ import annotations

import json
import re
from typing import Any

from .. import config, db, web
from ..web import Request, render


def register(routes) -> None:
    from . import admin, mapview, places

    def add(method, pattern, handler):
        routes.append((method, pattern, handler))

    for module in (mapview, places, admin):
        module.register(add)


def not_found(conn, req=None, code=404, message="We could not find that page."):
    context = page_context(conn, req, message=message, code=code)
    body = render("error.html", **context)
    return code, "text/html; charset=utf-8", body


def redirect(location, status=303):
    return status, {"Location": location}, ""


def json_response(payload, status=200):
    return status, "application/json; charset=utf-8", json.dumps(payload)


def flash(req, message, level="info"):
    messages = req.session_get("flash") or []
    messages.append({"level": level, "message": message})
    req.session_set("flash", messages[-5:])


def take_flashes(req):
    messages = req.session_get("flash") or []
    if messages:
        req.session_pop("flash")
    return messages


def page_context(conn, req=None, **extra):
    path = req.path if req else "/"
    context = {
        "content": web.map_content(conn),
        "flashes": take_flashes(req) if req else [],
        "path": path,
        "canonical_url": (req.path if req else "/"),
        "csrf": (req.csrf_token() if req else ""),
        "admin_name": (req.session_get("admin_name") if req else None),
    }
    context.update(extra)
    return context


def is_admin(req):
    return bool(req and req.session_get("admin_id"))
