"""Public listings, anonymous add form, and the admin edit panel."""
from __future__ import annotations

import hmac
import json

from . import channels as channel_rules
from . import config, db, limits, web


def _redirect(location: str, status: int = 303):
    return status, {"Location": location}, b""


def _html(template: str, req: web.Request, status: int = 200, **extra):
    context = {
        "path": req.path,
        "is_admin": req.admin_logged_in(),
        "q": "",
        "active_category": "",
        "active_kind": "",
    }
    context.update(extra)
    return status, "text/html; charset=utf-8", web.render(template, **context)


def _client(req: web.Request) -> str:
    return req.client_ip or "unknown"


def _clean(value: str, limit: int) -> str:
    return (value or "").replace("\x00", "").strip()[:limit]


def _decorate(entry: dict) -> dict:
    entry = dict(entry)
    entry["channels"] = channel_rules.decorate(entry["channels"])
    return entry


def _filters(req: web.Request) -> dict:
    category = req.query.get("category", "")
    kind = req.query.get("kind", "")
    return {
        "q": _clean(req.query.get("q", ""), 100),
        "active_category": category if category in config.CATEGORIES else "",
        "active_kind": kind if kind in config.KINDS else "",
    }


def _parse(form: dict[str, str]) -> tuple[dict, dict, list[dict], list[str], list[dict]]:
    values = {
        "name": _clean(form.get("name", ""), config.MAX_NAME),
        "kind": form.get("kind", "Person"),
        "category": form.get("category", "Community"),
        "description": _clean(form.get("description", ""), config.MAX_DESCRIPTION),
        "location": _clean(form.get("location", ""), config.MAX_LOCATION),
        "submitter_contact": _clean(form.get("submitter_contact", ""), config.MAX_SUBMITTER),
        "admin_note": _clean(form.get("admin_note", ""), config.MAX_ADMIN_NOTE),
        "published": form.get("published") is not None,
    }
    if values["kind"] not in config.KINDS:
        values["kind"] = "Other"
    if values["category"] not in config.CATEGORIES:
        values["category"] = "Other"

    fixed = {
        field: _clean(form.get(field, ""), config.MAX_CHANNEL_VALUE)
        for field in ("phone", "email", "facebook", "instagram", "website", "address")
    }
    custom = []
    for index in range(1, config.MAX_CUSTOM + 1):
        custom.append({
            "label": _clean(form.get(f"custom_label_{index}", ""),
                            config.MAX_CHANNEL_LABEL),
            "value": _clean(form.get(f"custom_value_{index}", ""),
                            config.MAX_CHANNEL_VALUE),
        })

    parsed_channels, errors = channel_rules.parse_channels(form)
    if len(values["name"]) < 2:
        errors.insert(0, "Add a name (at least 2 characters).")
    if not parsed_channels:
        errors.append("Add at least one way to get in touch: phone, email, link, or address.")
    return values, fixed, custom, errors, parsed_channels


def _entry_to_form(entry: dict) -> tuple[dict, dict, list[dict]]:
    split = channel_rules.split_for_edit(entry["channels"])
    values = {
        "name": entry["name"],
        "kind": entry["kind"],
        "category": entry["category"],
        "description": entry["description"],
        "location": entry["location"],
        "submitter_contact": entry["submitter_contact"],
        "admin_note": entry["admin_note"],
        "published": entry["published"],
    }
    return values, split["fixed"], split["custom"]


def home(req: web.Request, **_):
    filters = _filters(req)
    conn = db.connect()
    try:
        db.init_db(conn)
        entries = db.list_entries(
            conn,
            q=filters["q"],
            category=filters["active_category"],
            kind=filters["active_kind"],
            published_only=True,
        )
        stats = db.counts(conn)
    finally:
        conn.close()
    entries = [_decorate(entry) for entry in entries]
    return _html(
        "home.html", req, entries=entries, stats=stats,
        filtered=bool(filters["q"] or filters["active_category"] or filters["active_kind"]),
        **filters,
    )


def entry_detail(req: web.Request, entry_id: str = "", **_):
    try:
        rid = int(entry_id)
    except (TypeError, ValueError):
        return _html("error.html", req, status=404, code=404,
                     message="That listing does not exist.")
    conn = db.connect()
    try:
        db.init_db(conn)
        entry = db.get_entry(conn, rid, published_only=not req.admin_logged_in())
    finally:
        conn.close()
    if entry is None:
        return _html("error.html", req, status=404, code=404,
                     message="That listing does not exist or has been hidden.")
    return _html("entry.html", req, entry=_decorate(entry))


def add_form(req: web.Request, **_):
    values = {"name": "", "kind": "Person", "category": "Community",
              "description": "", "location": "", "submitter_contact": "",
              "admin_note": "", "published": True}
    fixed = {field: "" for field in
             ("phone", "email", "facebook", "instagram", "website", "address")}
    custom = [{"label": "", "value": ""} for _ in range(config.MAX_CUSTOM)]
    return _html(
        "add.html", req, csrf=req.csrf_token(), values=values, fixed=fixed,
        custom=custom, errors=[],
    )


def add_submit(req: web.Request, **_):
    if not req.csrf_ok():
        values = {"name": "", "kind": "Person", "category": "Community",
                  "description": "", "location": "", "submitter_contact": "",
                  "admin_note": "", "published": True}
        fixed = {field: "" for field in
                 ("phone", "email", "facebook", "instagram", "website", "address")}
        custom = [{"label": "", "value": ""} for _ in range(config.MAX_CUSTOM)]
        return _html(
            "add.html", req, status=400, csrf=req.csrf_token(), values=values,
            fixed=fixed, custom=custom,
            errors=["Your form session expired. Reload the page and try again."],
        )

    if req.form.get("company"):
        return _redirect("/")

    values, fixed, custom, errors, parsed_channels = _parse(req.form)
    values["published"] = True
    values["admin_note"] = ""
    too_many = False
    if not errors and not limits.allow(
        f"add:{_client(req)}", config.SUBMISSIONS_PER_HOUR, 3600
    ):
        errors.append("Too many listings from this device. Please wait an hour and try again.")
        too_many = True

    if errors:
        return _html(
            "add.html", req, status=429 if too_many else 400,
            csrf=req.csrf_token(), values=values, fixed=fixed, custom=custom,
            errors=errors,
        )

    conn = db.connect()
    try:
        db.init_db(conn)
        entry_id = db.create_entry(conn, values, parsed_channels)
    finally:
        conn.close()
    return _redirect(f"/added/{entry_id}")


def added(req: web.Request, entry_id: str = "", **_):
    try:
        rid = int(entry_id)
    except (TypeError, ValueError):
        return _redirect("/")
    conn = db.connect()
    try:
        db.init_db(conn)
        entry = db.get_entry(conn, rid, published_only=True)
    finally:
        conn.close()
    if entry is None:
        return _redirect("/")
    return _html("added.html", req, entry=_decorate(entry))


def admin_login(req: web.Request, **_):
    if req.admin_logged_in():
        return _redirect("/admin")
    return _html("admin_login.html", req, csrf=req.csrf_token(), error="")


def admin_login_submit(req: web.Request, **_):
    if not req.csrf_ok():
        return _html("admin_login.html", req, status=400,
                     csrf=req.csrf_token(),
                     error="Your form session expired. Reload and try again.")
    if not limits.allow(f"login:{_client(req)}", config.LOGIN_ATTEMPTS_PER_15_MIN, 900):
        return _html("admin_login.html", req, status=429,
                     csrf=req.csrf_token(),
                     error="Too many attempts. Wait 15 minutes and try again.")
    user = req.form.get("user", "")
    password = req.form.get("password", "")
    user_ok = hmac.compare_digest(user, config.ADMIN_USER)
    password_ok = hmac.compare_digest(password, config.ADMIN_PASSWORD)
    if not (user_ok and password_ok):
        return _html("admin_login.html", req, status=401,
                     csrf=req.csrf_token(),
                     error="That username or password did not match.")
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
    filters = _filters(req)
    status = req.query.get("status", "all")
    if status not in ("all", "published", "hidden"):
        status = "all"
    conn = db.connect()
    try:
        db.init_db(conn)
        entries = db.list_entries(
            conn,
            q=filters["q"],
            category=filters["active_category"],
            kind=filters["active_kind"],
            published_only=False,
            order="created",
        )
        stats = db.counts(conn)
    finally:
        conn.close()
    if status == "published":
        entries = [entry for entry in entries if entry["published"]]
    elif status == "hidden":
        entries = [entry for entry in entries if not entry["published"]]
    entries = [_decorate(entry) for entry in entries]
    message = ""
    if req.query.get("updated"):
        message = "Listing updated."
    elif req.query.get("deleted"):
        message = "Listing deleted."
    elif req.query.get("toggled"):
        message = "Visibility changed."
    return _html(
        "admin.html", req, csrf=req.csrf_token(), entries=entries,
        stats=stats, active_status=status, message=message, **filters,
    )


def admin_edit_form(req: web.Request, entry_id: str = "", **_):
    if not req.admin_logged_in():
        return _redirect("/admin/login")
    try:
        rid = int(entry_id)
    except (TypeError, ValueError):
        return _html("error.html", req, status=404, code=404,
                     message="That listing does not exist.")
    conn = db.connect()
    try:
        db.init_db(conn)
        entry = db.get_entry(conn, rid)
    finally:
        conn.close()
    if entry is None:
        return _html("error.html", req, status=404, code=404,
                     message="That listing no longer exists.")
    values, fixed, custom = _entry_to_form(entry)
    return _html(
        "admin_edit.html", req, csrf=req.csrf_token(), entry=entry,
        values=values, fixed=fixed, custom=custom, errors=[],
    )


def admin_edit_submit(req: web.Request, entry_id: str = "", **_):
    if not req.admin_logged_in():
        return _redirect("/admin/login")
    if not req.csrf_ok():
        return _html("error.html", req, status=400, code=400,
                     message="Your form session expired. Please try again.")
    try:
        rid = int(entry_id)
    except (TypeError, ValueError):
        return _html("error.html", req, status=404, code=404,
                     message="That listing does not exist.")
    conn = db.connect()
    try:
        db.init_db(conn)
        entry = db.get_entry(conn, rid)
        if entry is None:
            return _html("error.html", req, status=404, code=404,
                         message="That listing no longer exists.")
        values, fixed, custom, errors, parsed_channels = _parse(req.form)
        if errors:
            return _html(
                "admin_edit.html", req, status=400, csrf=req.csrf_token(),
                entry=entry, values=values, fixed=fixed, custom=custom,
                errors=errors,
            )
        db.update_entry(conn, rid, values, parsed_channels)
    finally:
        conn.close()
    return _redirect("/admin?updated=1")


def admin_delete(req: web.Request, entry_id: str = "", **_):
    if not req.admin_logged_in():
        return _redirect("/admin/login")
    if not req.csrf_ok():
        return _html("error.html", req, status=400, code=400,
                     message="Your form session expired. Please try again.")
    try:
        rid = int(entry_id)
    except (TypeError, ValueError):
        return _redirect("/admin")
    conn = db.connect()
    try:
        db.init_db(conn)
        db.delete_entry(conn, rid)
    finally:
        conn.close()
    return _redirect("/admin?deleted=1")


def admin_toggle(req: web.Request, entry_id: str = "", **_):
    if not req.admin_logged_in():
        return _redirect("/admin/login")
    if not req.csrf_ok():
        return _html("error.html", req, status=400, code=400,
                     message="Your form session expired. Please try again.")
    try:
        rid = int(entry_id)
    except (TypeError, ValueError):
        return _redirect("/admin")
    conn = db.connect()
    try:
        db.init_db(conn)
        entry = db.get_entry(conn, rid)
        if entry is not None:
            db.set_published(conn, rid, not entry["published"])
    finally:
        conn.close()
    return _redirect("/admin?toggled=1")


def health(req: web.Request, **_):
    conn = db.connect()
    try:
        db.init_db(conn)
        stats = db.counts(conn)
    finally:
        conn.close()
    payload = {"ok": True, "service": config.SITE_NAME,
               "version": config.SITE_VERSION, "listings": stats}
    return 200, "application/json; charset=utf-8", json.dumps(payload, indent=2)


def not_found(req: web.Request, **_):
    return _html("error.html", req, status=404, code=404,
                 message="That page does not exist.")


def server_error(req: web.Request, **_):
    return _html("error.html", req, status=500, code=500,
                 message="Something went wrong on our side. Try again.")
