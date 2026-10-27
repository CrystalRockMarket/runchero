"""Public directory, anonymous idea requests, and the admin review panel."""
from __future__ import annotations

import hmac
from dataclasses import asdict

from . import config, db, limits, projects, web


def _redirect(location: str, status: int = 303):
    return status, {"Location": location}, b""


def _html(template: str, req: web.Request, status: int = 200, **extra):
    context = {
        "path": req.path,
        "is_admin": req.admin_logged_in(),
        "projects": _cards(req),
        "project_count": len(projects.visible_projects()),
    }
    context.update(extra)
    return status, "text/html; charset=utf-8", web.render(template, **context)


def _cards(req: web.Request) -> list[dict]:
    host = req.headers.get("Host") or "127.0.0.1"
    cards = []
    for project in projects.visible_projects():
        card = asdict(project)
        card["tags"] = list(project.tags)
        card["url"] = projects.project_url(project, host)
        cards.append(card)
    return cards


def _client(req: web.Request) -> str:
    return req.client_ip or "unknown"


def _clean(value: str, limit: int) -> str:
    text = (value or "").replace("\x00", "").strip()
    return text[:limit]


def home(req: web.Request, **_):
    return _html("home.html", req)


def request_form(req: web.Request, **_):
    return _html(
        "request.html",
        req,
        csrf=req.csrf_token(),
        values={"name": "", "contact": "", "title": "", "description": "", "category": "Other"},
        errors=[],
    )


def request_submit(req: web.Request, **_):
    if not req.csrf_ok():
        return _html(
            "request.html",
            req,
            status=400,
            csrf=req.csrf_token(),
            values={},
            errors=["Your form session expired. Please reload the page and try again."],
        )

    if req.form.get("website"):
        return _redirect("/thanks")

    values = {
        "name": _clean(req.form.get("name", ""), config.MAX_NAME),
        "contact": _clean(req.form.get("contact", ""), config.MAX_CONTACT),
        "title": _clean(req.form.get("title", ""), config.MAX_TITLE),
        "description": _clean(req.form.get("description", ""), config.MAX_DESCRIPTION),
        "category": _clean(req.form.get("category", ""), config.MAX_CATEGORY),
    }
    if values["category"] not in config.CATEGORIES:
        values["category"] = "Other"

    errors = []
    if len(values["title"]) < 3:
        errors.append("Give the idea a short name (at least 3 characters).")
    if len(values["description"]) < 10:
        errors.append("Describe the idea in a sentence or two (at least 10 characters).")

    if not errors and not limits.allow(
        f"submit:{_client(req)}", config.SUBMISSIONS_PER_HOUR, 3600
    ):
        return _html(
            "request.html",
            req,
            status=429,
            csrf=req.csrf_token(),
            values=values,
            errors=["Too many ideas from this device. Please wait an hour and try again."],
        )

    if errors:
        return _html(
            "request.html",
            req,
            status=400,
            csrf=req.csrf_token(),
            values=values,
            errors=errors,
        )

    conn = db.connect()
    try:
        db.init_db(conn)
        db.create_request(
            conn,
            name=values["name"],
            contact=values["contact"],
            title=values["title"],
            description=values["description"],
            category=values["category"],
        )
    finally:
        conn.close()
    return _redirect("/thanks")


def thanks(req: web.Request, **_):
    return _html("thanks.html", req)


def admin_login(req: web.Request, **_):
    if req.admin_logged_in():
        return _redirect("/admin")
    return _html("admin_login.html", req, csrf=req.csrf_token(), error="")


def admin_login_submit(req: web.Request, **_):
    if not req.csrf_ok():
        return _html(
            "admin_login.html",
            req,
            status=400,
            csrf=req.csrf_token(),
            error="Your form session expired. Reload and try again.",
        )
    if not limits.allow(f"login:{_client(req)}", config.LOGIN_ATTEMPTS_PER_15_MIN, 900):
        return _html(
            "admin_login.html",
            req,
            status=429,
            csrf=req.csrf_token(),
            error="Too many attempts. Wait 15 minutes and try again.",
        )
    user = req.form.get("user", "")
    password = req.form.get("password", "")
    user_ok = hmac.compare_digest(user, config.ADMIN_USER)
    password_ok = hmac.compare_digest(password, config.ADMIN_PASSWORD)
    if not (user_ok and password_ok):
        return _html(
            "admin_login.html",
            req,
            status=401,
            csrf=req.csrf_token(),
            error="That username or password did not match.",
        )
    req.login_admin()
    return _redirect("/admin")


def admin_logout(req: web.Request, **_):
    if not req.admin_logged_in():
        return _redirect("/admin/login")
    if not req.csrf_ok():
        return _html("error.html", req, status=400, code=400,
                     message="Your form session expired. Please try again.")
    req.logout_admin()
    return _redirect("/")


def admin_home(req: web.Request, **_):
    if not req.admin_logged_in():
        return _redirect("/admin/login")
    status = req.query.get("status", "")
    if status not in config.STATUSES:
        status = ""
    query = _clean(req.query.get("q", ""), 100)
    conn = db.connect()
    try:
        db.init_db(conn)
        rows = db.list_requests(conn, status=status or None, query=query)
        stats = db.counts(conn)
    finally:
        conn.close()
    message = ""
    if req.query.get("updated"):
        message = "Request updated."
    elif req.query.get("deleted"):
        message = "Request deleted."
    return _html(
        "admin.html",
        req,
        csrf=req.csrf_token(),
        requests=rows,
        stats=stats,
        active_status=status,
        query=query,
        message=message,
    )


def admin_update(req: web.Request, request_id: str = "", action: str = "", **_):
    if not req.admin_logged_in():
        return _redirect("/admin/login")
    if not req.csrf_ok():
        return _html("error.html", req, status=400, code=400,
                     message="Your form session expired. Please try again.")
    try:
        rid = int(request_id)
    except (TypeError, ValueError):
        return _html("error.html", req, status=400, code=400,
                     message="That request number is not valid.")
    conn = db.connect()
    try:
        db.init_db(conn)
        existing = db.get_request(conn, rid)
        if existing is None:
            return _html("error.html", req, status=404, code=404,
                         message="That request no longer exists.")
        if action == "delete":
            db.delete_request(conn, rid)
            return _redirect("/admin?deleted=1")
        if action == "status":
            status = req.form.get("status", "")
            if status not in config.STATUSES:
                status = "new"
            note = _clean(req.form.get("admin_note", ""), config.MAX_ADMIN_NOTE)
            db.update_request(conn, rid, status=status, note=note)
            return _redirect("/admin?updated=1")
    finally:
        conn.close()
    return _redirect("/admin")


def health(req: web.Request, **_):
    import json

    conn = db.connect()
    try:
        db.init_db(conn)
        stats = db.counts(conn)
    finally:
        conn.close()
    payload = {
        "ok": True,
        "service": config.SITE_NAME,
        "version": config.SITE_VERSION,
        "projects": len(projects.visible_projects()),
        "requests": stats["total"],
    }
    return 200, "application/json; charset=utf-8", json.dumps(payload, indent=2)


def not_found(req: web.Request, **_):
    return _html("error.html", req, status=404, code=404,
                 message="That page does not exist.")


def server_error(req: web.Request, **_):
    return _html("error.html", req, status=500, code=500,
                 message="Something went wrong on our side. Try again.")
