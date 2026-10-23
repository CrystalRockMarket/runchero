"""Admin: login, dashboard, categories, layers, settings, audit."""
from __future__ import annotations

import json
import re

from .. import db, web
from . import page_context, redirect, flash


def register(add):
    add("GET", re.compile(r"^/admin$"), index)
    add("GET", re.compile(r"^/admin/login$"), login_form)
    add("POST", re.compile(r"^/admin/login$"), login_submit)
    add("POST", re.compile(r"^/admin/logout$"), logout)
    add("GET", re.compile(r"^/admin/categories$"), categories)
    add("POST", re.compile(r"^/admin/categories$"), categories_post)
    add("GET", re.compile(r"^/admin/layers$"), layers)
    add("POST", re.compile(r"^/admin/layers$"), layers_post)
    add("GET", re.compile(r"^/admin/settings$"), settings_form)
    add("POST", re.compile(r"^/admin/settings$"), settings_post)
    add("GET", re.compile(r"^/admin/audit$"), audit)


def _guard(conn, req):
    if not req.session_get("admin_id"):
        return redirect("/admin/login")
    return None


def index(conn, req, **_):
    g = _guard(conn, req)
    if g: return g
    stats = {
        "places": db.scalar(conn, "SELECT COUNT(*) FROM places"),
        "visible": db.scalar(conn, "SELECT COUNT(*) FROM places WHERE hidden=0"),
        "records": db.scalar(conn, "SELECT COUNT(*) FROM place_records"),
        "photos": db.scalar(conn, "SELECT COUNT(*) FROM place_photos"),
        "layers": db.scalar(conn, "SELECT COUNT(*) FROM map_layers"),
    }
    recent = db.rows(conn, "SELECT * FROM audit_log ORDER BY id DESC LIMIT 15")
    ctx = page_context(conn, req, stats=stats, recent=[dict(r) for r in recent], title="Admin")
    return 200, "text/html; charset=utf-8", web.render("admin/index.html", **ctx)


def login_form(conn, req, **_):
    if req.session_get("admin_id"):
        return redirect("/admin")
    ctx = page_context(conn, req, error=req.session_pop("login_error"), title="Login")
    return 200, "text/html; charset=utf-8", web.render("admin/login.html", **ctx)


def login_submit(conn, req, **_):
    if not req.csrf_ok():
        return redirect("/admin/login")
    from ..services import auth
    username = (req.form.get("username") or "").strip()
    password = req.form.get("password") or ""
    row = db.one(conn, "SELECT * FROM admins WHERE username = ?", (username,))
    if row is None or not auth.check_password(password, row["passhash"]):
        import time; time.sleep(0.3)
        req.session_set("login_error", "That username and password do not match.")
        return redirect("/admin/login")
    req.session_set("admin_id", row["id"])
    req.session_set("admin_name", row["username"])
    db.log_audit(conn, "admin.login", "admin", row["id"], "", actor=row["username"])
    conn.commit()
    return redirect("/admin")


def logout(conn, req, **_):
    if req.csrf_ok():
        req.session_pop("admin_id")
        req.session_pop("admin_name")
    return redirect("/admin/login")


def categories(conn, req, **_):
    g = _guard(conn, req)
    if g: return g
    cats = db.rows(conn, "SELECT * FROM categories ORDER BY sort_order,name")
    ctx = page_context(conn, req, categories=[dict(c) for c in cats], title="Categories")
    return 200, "text/html; charset=utf-8", web.render("admin/categories.html", **ctx)


def categories_post(conn, req, **_):
    g = _guard(conn, req)
    if g: return g
    if not req.csrf_ok():
        return redirect("/admin/categories")
    # upsert by slug
    slug = (req.form.get("slug") or "").strip().lower().replace(" ", "-")
    name = (req.form.get("name") or "").strip()
    if slug and name:
        conn.execute("""INSERT INTO categories(slug,name,colour,icon,sort_order) VALUES(?,?,?,?,?)
                        ON CONFLICT(slug) DO UPDATE SET name=excluded.name, colour=excluded.colour, icon=excluded.icon, sort_order=excluded.sort_order""",
                    (slug, name, req.form.get("colour","sky"), req.form.get("icon","box"), int(req.form.get("sort_order") or 0)))
        conn.commit()
        flash(req, f"Saved category {name}.", "ok")
    # delete
    delslug = req.form.get("delete_slug")
    if delslug:
        conn.execute("DELETE FROM categories WHERE slug=?", (delslug,))
        conn.commit()
        flash(req, "Deleted category.", "ok")
    return redirect("/admin/categories")


def layers(conn, req, **_):
    g = _guard(conn, req)
    if g: return g
    layers = db.rows(conn, "SELECT * FROM map_layers ORDER BY sort_order,name")
    ctx = page_context(conn, req, layers=[dict(l) for l in layers], title="Layers")
    return 200, "text/html; charset=utf-8", web.render("admin/layers.html", **ctx)


def layers_post(conn, req, **_):
    g = _guard(conn, req)
    if g: return g
    if not req.csrf_ok():
        return redirect("/admin/layers")
    slug = (req.form.get("slug") or "").strip().lower().replace(" ", "-")
    name = (req.form.get("name") or "").strip()
    if slug and name:
        conn.execute("""INSERT INTO map_layers(slug,name,description,visible,sort_order) VALUES(?,?,?,?,?)
                        ON CONFLICT(slug) DO UPDATE SET name=excluded.name, description=excluded.description, visible=excluded.visible, sort_order=excluded.sort_order""",
                    (slug, name, req.form.get("description",""), 1 if req.form.get("visible")=="1" else 0, int(req.form.get("sort_order") or 0)))
        conn.commit()
        flash(req, f"Saved layer {name}.", "ok")
    delslug = req.form.get("delete_slug")
    if delslug:
        conn.execute("DELETE FROM map_layers WHERE slug=?", (delslug,))
        conn.commit()
        flash(req, "Deleted layer.", "ok")
    return redirect("/admin/layers")


def settings_form(conn, req, **_):
    g = _guard(conn, req)
    if g: return g
    content = web.map_content(conn)
    ctx = page_context(conn, req, content=content, title="Settings")
    return 200, "text/html; charset=utf-8", web.render("admin/settings.html", **ctx)


def settings_post(conn, req, **_):
    g = _guard(conn, req)
    if g: return g
    if not req.csrf_ok():
        return redirect("/admin/settings")
    for key in ("site_title","site_subtitle","banner","contact_email","map_width","map_height","theme"):
        val = req.form.get(key)
        if val is None:
            continue
        if key in ("map_width","map_height"):
            try: val = int(val)
            except ValueError: continue
        db.set_content(conn, key, val)
    flash(req, "Settings saved.", "ok")
    return redirect("/admin/settings")


def audit(conn, req, **_):
    g = _guard(conn, req)
    if g: return g
    rows = db.rows(conn, "SELECT * FROM audit_log ORDER BY id DESC LIMIT 100")
    ctx = page_context(conn, req, rows=[dict(r) for r in rows], title="Audit Log")
    return 200, "text/html; charset=utf-8", web.render("admin/audit.html", **ctx)
