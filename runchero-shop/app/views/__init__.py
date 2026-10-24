"""Views: the routes that render pages and handle form posts.

Each submodule exposes ``register(add)`` where ``add`` appends a
``(method, compiled_pattern, handler)`` triple to the route table.
"""
from __future__ import annotations

import json
import re
from typing import Any

from .. import config, db, web
from ..services import customers as customers_service
from ..services import stores as stores_service
from ..web import Request, render


def register(routes) -> None:
    from . import (account, admin, cart, catalog, checkout, events, home, manage,
                   orders, pages, store)

    def add(method, pattern, handler):
        routes.append((method, pattern, handler))

    for module in (home, catalog, cart, checkout, events, orders, account,
                   manage, admin, pages, store):
        module.register(add)


def not_found(conn: db.sqlite3.Connection, req: Request | None = None,
              code: int = 404, message: str = "We could not find that page."):
    context = page_context(conn, req, message=message, code=code)
    body = render("error.html", **context)
    return code, "text/html; charset=utf-8", body


def redirect(location: str, status: int = 303):
    return status, {"Location": location}, ""


def json_response(payload: Any, status: int = 200):
    return status, "application/json; charset=utf-8", json.dumps(payload)


# --------------------------------------------------------------------------
# shared view helpers
# --------------------------------------------------------------------------

def wants_json(req: Request) -> bool:
    return req.wants_json()


def cart_id(req: Request) -> str:
    """A stable anonymous cart id, carried in a signed cookie."""
    cid = req.session_get("cart_id")
    if not cid:
        import secrets
        cid = secrets.token_hex(12)
        req.session_set("cart_id", cid)
    return cid


def cart_count(conn, req: Request | None) -> int:
    """How many items the visitor is carrying, for the nav badge."""
    cid = req.session_get("cart_id") if req else None
    if not cid:
        return 0
    return db.scalar(conn,
                     "SELECT COUNT(*) FROM cart_items WHERE cart_id = ?",
                     (cid,)) or 0


def flash(req: Request, message: str, level: str = "info") -> None:
    """Queue a one-shot message for the next rendered page."""
    messages = req.session_get("flash") or []
    messages.append({"level": level, "message": message})
    req.session_set("flash", messages[-5:])


def take_flashes(req: Request) -> list[dict[str, str]]:
    messages = req.session_get("flash") or []
    if messages:
        req.session_pop("flash")
    return messages


def page_context(conn: db.sqlite3.Connection, req: Request | None = None,
                 force_store: str | None = None,
                 **extra) -> dict[str, Any]:
    path = req.path if req else "/"
    context: dict[str, Any] = {
        "content": web.shop_content(conn),
        "flashes": take_flashes(req) if req else [],
        "path": path,
        "cart_count": cart_count(conn, req),
        "canonical_url": canonical_url(req),
        "og_image": og_image_url(req),
        "customer": customers_service.current(conn, req),
    }
    store_slug = force_store or (
        "fermentation" if path.startswith("/fermentation") else
        "freeze-dried" if path.startswith("/freeze-dried") else "beef")
    context["store_slug"] = store_slug
    context["current_store"] = stores_service.get(conn, store_slug)
    context["all_stores"] = stores_service.all_stores(conn)
    context["social_links"] = db.rows(
        conn, "SELECT * FROM social_links WHERE active = 1 AND store_slug = ? "
        "ORDER BY sort_order", (store_slug,))
    context.update(extra)
    return context


def canonical_url(req: Request | None) -> str:
    """Absolute URL of the current page, for canonical and Open Graph tags."""
    base = config.SITE_URL
    if not base and req is not None:
        host = req.headers.get("Host") or f"{config.DEFAULT_HOST}:{config.DEFAULT_PORT}"
        base = f"http://{host}"
    path = req.path if req else "/"
    if req is not None and req.query:
        path = f"{path}?{req.query}"
    return f"{base}{path}" if base else path


def og_image_url(req: Request | None) -> str:
    """Absolute URL of the social preview image."""
    base = config.SITE_URL
    if not base and req is not None:
        host = req.headers.get("Host") or f"{config.DEFAULT_HOST}:{config.DEFAULT_PORT}"
        base = f"http://{host}"
    request_path = req.path if req else "/"
    path = ("/static/img/og-fermentation.png"
            if request_path.startswith("/fermentation") else
            "/static/img/og-freeze-dried.png"
            if request_path.startswith("/freeze-dried") else
            "/static/img/og-cover.png")
    return f"{base}{path}" if base else path
