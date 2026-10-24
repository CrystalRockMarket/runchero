"""View registry and shared response helpers."""
from __future__ import annotations

from ..web import Request, render


def register(routes) -> None:
    from . import add, api, browse, home

    def add_route(method, pattern, handler):
        routes.append((method, pattern, handler))

    for module in (home, add, browse, api):
        module.register(add_route)


def not_found(conn, req=None, code=404, message="We could not find that page."):
    ctx = page_context(conn, req, message=message, code=code)
    body = render("error.html", **ctx)
    return code, "text/html; charset=utf-8", body


def server_error(conn, req=None):
    ctx = page_context(
        conn, req,
        message="The depot hit a snag. Please try again.",
        code=500,
    )
    body = render("error.html", **ctx)
    return 500, "text/html; charset=utf-8", body


def redirect(location: str, status: int = 303):
    return status, {"Location": location}, ""


def page_context(conn, req: Request | None = None, **extra):
    path = req.path if req else "/"
    ctx = {
        "path": path,
        "flashes": take_flashes(req) if req else [],
        "csrf": req.csrf_token() if req else "",
    }
    ctx.update(extra)
    return ctx


def flash(req: Request, message: str, level: str = "info") -> None:
    messages = req.session.get("flash") or []
    messages.append({"level": level, "message": message})
    req.session_set("flash", messages[-5:])


def take_flashes(req: Request | None) -> list[dict]:
    if not req:
        return []
    messages = req.session.get("flash") or []
    if messages:
        req.session_pop("flash")
    return messages
