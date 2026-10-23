"""Views registration."""
from __future__ import annotations

from .. import config, web
from ..web import Request, render


def register(routes) -> None:
    from . import home, add, dashboard, browse, api

    def add_route(method, pattern, handler):
        routes.append((method, pattern, handler))

    for module in (home, add, dashboard, browse, api):
        module.register(add_route)


def not_found(conn, req=None, code=404, message="Page not found."):
    ctx = page_context(conn, req, message=message, code=code)
    body = render("error.html", **ctx)
    return code, "text/html; charset=utf-8", body


def server_error(conn, req=None):
    ctx = page_context(conn, req, message="Something went wrong while saving this site.", code=500)
    body = render("error.html", **ctx)
    return 500, "text/html; charset=utf-8", body


def redirect(location, status=303):
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


def flash(req: Request, message: str, level: str = "info"):
    messages = req.session.get("flash") or []
    messages.append({"level": level, "message": message})
    req.session["flash"] = messages[-5:]
    # persist
    if not req.session:
        req.clear_cookie("rmm_session")
    else:
        req.set_cookie("rmm_session", web.sign_value(req.session))


def take_flashes(req: Request | None):
    if not req:
        return []
    messages = req.session.get("flash") or []
    if messages:
        req.session.pop("flash", None)
        if not req.session:
            req.clear_cookie("rmm_session")
        else:
            req.set_cookie("rmm_session", web.sign_value(req.session))
    return messages
