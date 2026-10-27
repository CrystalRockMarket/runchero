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
    }
    context.update(extra)
    return status, "text/html; charset=utf-8", web.render(template, **context)



def _group_by_letter(entries: list[dict]) -> list[tuple[str, list[dict]]]:
    """Group entries by uppercase first letter of name; non-letters under '#'."""
    groups: dict[str, list[dict]] = {}
    order: list[str] = []
    for entry in entries:
        name = (entry.get("name") or "").strip()
        letter = name[0].upper() if name and name[0].isalpha() else (name[0].upper() if name else "#")
        if letter not in groups:
            groups[letter] = []
            order.append(letter)
        groups[letter].append(entry)
    return [(letter, groups[letter]) for letter in order]


def _directory_stats(conn) -> dict:
    return {
        "people": db.counts(conn, "person")["published"],
        "places": db.counts(conn, "place")["published"],
        "total": db.counts(conn)["published"],
        "signatures": db.guestbook_count(conn),
    }


def _directory_meta(kind: str) -> dict:
    if kind == "place":
        return {
            "kind": kind,
            "page_title": "Places directory",
            "page_description": (
                "Businesses, farms, homes, and shared spaces in the Runchero "
                "community. Browse locations or add one to the directory."
            ),
            "hero_eyebrow": "Businesses, farms, homes, and shared spaces",
            "hero_heading": "Find places to shop, visit, stay, or gather.",
            "hero_lede": (
                "A directory of the places that make Runchero work: shops, "
                "farms, workshops, venues, homes, and community spaces. Add a "
                "place in a minute. No account needed."
            ),
            "card_icon": "home.png",
            "view_label": "View place",
            "empty_title_filtered": "No places match that search",
            "empty_hint_filtered": "Try a different word, or clear the filters to see every place.",
            "empty_title_empty": "No places listed yet",
            "empty_hint_empty": "Know a business, farm, home, or shared space? Add the first place.",
            "cta_title": "Know a place that should be listed?",
            "cta_text": (
                "Add a business, farm, home, or community space so neighbours "
                "can find it. It appears right away; only an admin can edit it."
            ),
        }
    return {
        "kind": "person",
        "page_title": "Community directory",
        "page_description": (
            "Meet the people of the Runchero community. Browse neighbours and "
            "add yourself to the local directory."
        ),
        "hero_eyebrow": "The people of Runchero, on the local network",
        "hero_heading": "Find your neighbours. Share what you can offer.",
        "hero_lede": (
            "A directory of people in the Runchero community. Browse freely, "
            "or add yourself in a minute. No account needed."
        ),
        "card_icon": "person.png",
        "view_label": "View profile",
        "empty_title_filtered": "No neighbours match that search",
        "empty_hint_filtered": "Try a different word, or clear the filters to see everyone.",
        "empty_title_empty": "No people here yet",
        "empty_hint_empty": "The directory is empty. Be the first neighbour to add yourself.",
        "cta_title": "Not listed yet?",
        "cta_text": (
            "Add yourself to the neighbourhood directory. It appears right "
            "away, and only an admin can edit or remove it afterwards."
        ),
    }


def _directory_page(req: web.Request, kind: str):
    kind = _kind(kind)
    meta = _directory_meta(kind)
    categories = config.KINDS[kind]["categories"]
    filters = _filters(req, categories)
    conn = db.connect()
    try:
        db.init_db(conn)
        entries = db.list_entries(
            conn,
            q=filters["q"],
            category=filters["active_category"],
            kind=kind,
            published_only=True,
        )
        stats = _directory_stats(conn)
        letter_groups = _group_by_letter(entries)
    finally:
        conn.close()
    entries = [_decorate(entry) for entry in entries]
    return _html(
        "directory.html", req, entries=entries, stats=stats, categories=categories,
        letter_groups=letter_groups, filtered=bool(filters["q"] or filters["active_category"]),
        **meta, **filters,
    )


def places(req: web.Request, **_):
    return _directory_page(req, "place")


def _kind(kind: str) -> str:
    return kind if kind in config.KINDS else "person"

def _client(req: web.Request) -> str:
    return req.client_ip or "unknown"


def _clean(value: str, limit: int) -> str:
    return (value or "").replace("\x00", "").strip()[:limit]


def _decorate(entry: dict) -> dict:
    entry = dict(entry)
    entry["channels"] = channel_rules.decorate(entry["channels"])
    return entry


def _filters(req: web.Request, categories: list[str] | None = None) -> dict:
    if categories is None:
        categories = config.CATEGORIES
    category = req.query.get("category", "")
    return {
        "q": _clean(req.query.get("q", ""), 100),
        "active_category": category if category in categories else "",
    }


def _parse(form: dict[str, str], kind: str = "person") -> tuple[dict, dict, list[dict], list[str], list[dict]]:
    kind = _kind(kind)
    categories = config.KINDS[kind]["categories"]
    values = {
        "name": _clean(form.get("name", ""), config.MAX_NAME),
        "kind": kind,
        "category": form.get("category", categories[0]),
        "description": _clean(form.get("description", ""), config.MAX_DESCRIPTION),
        "location": _clean(form.get("location", ""), config.MAX_LOCATION),
        "submitter_contact": _clean(form.get("submitter_contact", ""), config.MAX_SUBMITTER),
        "admin_note": _clean(form.get("admin_note", ""), config.MAX_ADMIN_NOTE),
        "published": form.get("published") is not None,
    }
    if values["category"] not in categories:
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
        "category": entry["category"],
        "description": entry["description"],
        "location": entry["location"],
        "submitter_contact": entry["submitter_contact"],
        "admin_note": entry["admin_note"],
        "published": entry["published"],
    }
    return values, split["fixed"], split["custom"]


def home(req: web.Request, **_):
    return _directory_page(req, "person")


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
    values = {"name": "", "category": "Neighbours",
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
        values = {"name": "", "category": "Neighbours",
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


def place_add_form(req: web.Request, **_):
    values = {"name": "", "category": "Community Space",
              "description": "", "location": "", "submitter_contact": "",
              "admin_note": "", "published": True}
    fixed = {field: "" for field in
             ("phone", "email", "facebook", "instagram", "website", "address")}
    custom = [{"label": "", "value": ""} for _ in range(config.MAX_CUSTOM)]
    return _html(
        "add_place.html", req, csrf=req.csrf_token(), values=values, fixed=fixed,
        custom=custom, errors=[],
    )


def place_add_submit(req: web.Request, **_):
    if not req.csrf_ok():
        values = {"name": "", "category": "Community Space",
                  "description": "", "location": "", "submitter_contact": "",
                  "admin_note": "", "published": True}
        fixed = {field: "" for field in
                 ("phone", "email", "facebook", "instagram", "website", "address")}
        custom = [{"label": "", "value": ""} for _ in range(config.MAX_CUSTOM)]
        return _html(
            "add_place.html", req, status=400, csrf=req.csrf_token(), values=values,
            fixed=fixed, custom=custom,
            errors=["Your form session expired. Reload the page and try again."],
        )

    if req.form.get("company"):
        return _redirect("/places")

    values, fixed, custom, errors, parsed_channels = _parse(req.form, "place")
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
            "add_place.html", req, status=429 if too_many else 400,
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



def _guestbook_parse(form: dict[str, str]) -> tuple[str, str, list[str]]:
    name = _clean(form.get("name", ""), config.MAX_NAME)
    note = _clean(form.get("note", ""), config.MAX_DESCRIPTION)
    errors = []
    if len(name) < 2:
        errors.append("Add your name (at least 2 characters).")
    if len(note) < 2:
        errors.append("Add a short note about your time here (at least 2 characters).")
    return name, note, errors


def guestbook(req: web.Request, **_):
    conn = db.connect()
    try:
        db.init_db(conn)
        entries = db.guestbook_entries(conn)
        count = db.guestbook_count(conn)
    finally:
        conn.close()
    return _html("guestbook.html", req, csrf=req.csrf_token(), entries=entries,
                 count=count, values={"name": "", "note": ""}, errors=[])


def guestbook_sign(req: web.Request, **_):
    if not req.csrf_ok():
        values = {"name": "", "note": ""}
        conn = db.connect()
        try:
            db.init_db(conn)
            entries = db.guestbook_entries(conn)
            count = db.guestbook_count(conn)
        finally:
            conn.close()
        return _html("guestbook.html", req, status=400, csrf=req.csrf_token(),
                     entries=entries, count=count, values=values,
                     errors=["Your form session expired. Reload the page and try again."])

    if req.form.get("company"):
        return _redirect("/guestbook")

    name, note, errors = _guestbook_parse(req.form)
    if not errors and not limits.allow(f"guestbook:{_client(req)}", 5, 3600):
        errors.append("Too many signatures from this device. Please wait an hour and try again.")

    if errors:
        conn = db.connect()
        try:
            db.init_db(conn)
            entries = db.guestbook_entries(conn)
            count = db.guestbook_count(conn)
        finally:
            conn.close()
        return _html("guestbook.html", req, status=400, csrf=req.csrf_token(),
                     entries=entries, count=count,
                     values={"name": name, "note": note}, errors=errors)

    conn = db.connect()
    try:
        db.init_db(conn)
        db.guestbook_sign(conn, name, note)
    finally:
        conn.close()
    return _redirect("/guestbook")


def guestbook_admin_delete(req: web.Request, entry_id: str = "", **_):
    if not req.admin_logged_in():
        return _redirect("/admin/login")
    if not req.csrf_ok():
        return _html("error.html", req, status=400, code=400,
                     message="Your form session expired. Please try again.")
    try:
        rid = int(entry_id)
    except (TypeError, ValueError):
        return _redirect("/guestbook")
    conn = db.connect()
    try:
        db.init_db(conn)
        db.guestbook_delete(conn, rid)
    finally:
        conn.close()
    return _redirect("/guestbook?deleted=1")


def guestbook_admin_toggle(req: web.Request, entry_id: str = "", **_):
    if not req.admin_logged_in():
        return _redirect("/admin/login")
    if not req.csrf_ok():
        return _html("error.html", req, status=400, code=400,
                     message="Your form session expired. Please try again.")
    try:
        rid = int(entry_id)
    except (TypeError, ValueError):
        return _redirect("/guestbook")
    conn = db.connect()
    try:
        db.init_db(conn)
        db.guestbook_toggle(conn, rid)
    finally:
        conn.close()
    return _redirect("/guestbook?toggled=1")


def not_found(req: web.Request, **_):
    return _html("error.html", req, status=404, code=404,
                 message="That page does not exist.")


def server_error(req: web.Request, **_):
    return _html("error.html", req, status=500, code=500,
                 message="Something went wrong on our side. Try again.")
