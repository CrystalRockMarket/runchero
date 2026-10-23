"""Admin: login, the pricing console, market observations, orders, audits."""
from __future__ import annotations

import json
import re
import time
from urllib.parse import urlsplit

from .. import db, web
from ..services import (auth, market, pricing,
                        stores as stores_service,
                        products as products_service, uploads)
from . import cart_count, flash, page_context, redirect


# --------------------------------------------------------------------------
# auth helpers
# --------------------------------------------------------------------------

def is_admin(req) -> bool:
    return bool(req and req.session_get("admin_id"))


def require_admin(conn, req, store_slug: str | None = None):
    if not is_admin(req):
        return redirect("/admin/login")
    if store_slug and not stores_service.has_access(
            conn, _admin_id(conn, req), store_slug):
        return redirect("/admin")
    return None


# --------------------------------------------------------------------------
# routes
# --------------------------------------------------------------------------

def register(add) -> None:
    add("GET", re.compile(r"^/admin$"), index)
    add("GET", re.compile(r"^/admin/login$"), login_form)
    add("POST", re.compile(r"^/admin/login$"), login_submit)
    add("POST", re.compile(r"^/admin/logout$"), logout)
    add("GET", re.compile(r"^/admin/pricing$"), pricing_console)
    add("POST", re.compile(r"^/admin/pricing/preview$"), pricing_preview)
    add("POST", re.compile(r"^/admin/pricing/apply$"), pricing_apply)
    add("POST", re.compile(r"^/admin/pricing/revert$"), pricing_revert)
    add("GET", re.compile(r"^/admin/integrity$"), integrity)
    add("GET", re.compile(r"^/admin/market$"), market_admin)
    add("POST", re.compile(r"^/admin/market$"), market_admin_post)
    add("POST", re.compile(r"^/admin/market/refresh$"), market_refresh)
    add("GET", re.compile(r"^/admin/orders$"), orders_admin)
    add("GET", re.compile(r"^/admin/access$"), access_admin)
    add("POST", re.compile(r"^/admin/access$"), access_admin_post)
    add("POST", re.compile(r"^/admin/access/new$"), access_admin_create)
    add("POST", re.compile(r"^/admin/access/delete$"), access_admin_delete)
    add("GET", re.compile(r"^/admin/social$"), social_admin)
    add("POST", re.compile(r"^/admin/social$"), social_admin_post)
    add("GET", re.compile(r"^/admin/products$"), products_admin)
    add("GET", re.compile(r"^/admin/products/new$"), product_new)
    add("POST", re.compile(r"^/admin/products/new$"), product_create)
    add("GET", re.compile(r"^/admin/products/(?P<pid>\d+)/edit$"), product_edit)
    add("POST", re.compile(r"^/admin/products/(?P<pid>\d+)/edit$"), product_update)
    add("POST", re.compile(r"^/admin/products/(?P<pid>\d+)/delete$"), product_delete)


def index(conn: db.sqlite3.Connection, req, **_):
    guard = require_admin(conn, req)
    if guard:
        return guard
    if not _is_full_admin(conn, req):
        return redirect("/admin/products")
    stats = {
        "cuts": db.scalar(conn, "SELECT COUNT(*) FROM cuts WHERE active = 1"),
        "orders": db.scalar(conn, "SELECT COUNT(*) FROM orders"),
        "revenue": db.scalar(conn, "SELECT COALESCE(SUM(total), 0) FROM orders "
                                   "WHERE payment_status = 'paid'"),
        "subscribers": db.scalar(conn, "SELECT COUNT(*) FROM subscribers "
                                       "WHERE status = 'active'"),
        "audits": db.scalar(conn, "SELECT COUNT(*) FROM price_audits"),
    }
    context = page_context(conn, req, stats=stats,
                           integrity=pricing.claim_integrity(conn),
                           csrf=req.csrf_token(),
                           cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("admin/index.html",
                                                       **context)


def login_form(conn: db.sqlite3.Connection, req, **_):
    if is_admin(req):
        return redirect("/admin")
    context = page_context(conn, req, csrf=req.csrf_token(),
                           error=req.session_pop("login_error"),
                           cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("admin/login.html",
                                                      **context)


def login_submit(conn: db.sqlite3.Connection, req, **_):
    if not req.csrf_ok():
        return redirect("/admin/login")
    username = (req.form.get("username") or "").strip()
    password = req.form.get("password") or ""
    row = db.one(conn, "SELECT * FROM admins WHERE username = ?", (username,))
    if row is None or not auth.check_password(password, row["passhash"]):
        time.sleep(0.3)
        req.session_set("login_error", "That username and password do not match.")
        return redirect("/admin/login")
    req.session_set("admin_id", row["id"])
    req.session_set("admin_name", row["username"])
    db.log_audit(conn, "admin.login", "admin", row["id"], "",
                 actor=row["username"])
    conn.commit()
    return redirect("/admin")


def logout(conn: db.sqlite3.Connection, req, **_):
    if req.csrf_ok():
        req.session_pop("admin_id")
        req.session_pop("admin_name")
    return redirect("/admin/login")


# -- pricing console ------------------------------------------------------

def _grid(conn, scope: str = "all", value: str = "", search: str | None = None):
    return pricing.scope_cuts(conn, scope, value, search)


def pricing_console(conn: db.sqlite3.Connection, req, **_):
    guard = require_admin(conn, req, "beef")
    if guard:
        return guard
    scope = req.query.get("scope", "all") or "all"
    value = req.query.get("value", "") or ""
    search = req.query.get("q", "") or None
    cuts = _grid(conn, scope, value, search)
    comparisons = {}
    from ..services import market as market_service
    for cut in cuts:
        comparisons[cut["id"]] = market_service.compare(conn, cut)
    rules = db.rows(conn, "SELECT * FROM price_rules ORDER BY priority DESC, id")
    context = page_context(
        conn, req, cuts=cuts, comparisons=comparisons, rules=rules,
        scope=scope, value=value, search=search or "",
        primals=db.rows(conn, "SELECT * FROM primals ORDER BY sort_order"),
        sections=db.rows(conn, "SELECT * FROM sections ORDER BY sort_order"),
        audits=pricing.audit_log(conn, limit=12),
        preview=req.session_pop("pricing_preview") or None,
        csrf=req.csrf_token(), admin_name=req.session_get("admin_name"),
        cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("admin/pricing.html",
                                                       **context)


def _action_from_form(form) -> dict:
    return {
        "scope": form.get("scope", "all") or "all",
        "value": (form.get("value", "") or "").strip(),
        "kind": form.get("kind", "rake") or "rake",
        "discount": float(form.get("discount", "20") or 20),
        "percent": float(form.get("percent", "0") or 0),
        "price": float(form.get("price", "0") or 0),
        "amount": float(form.get("amount", "0") or 0),
        "search": (form.get("q", "") or "").strip() or None,
    }


def pricing_preview(conn: db.sqlite3.Connection, req, **_):
    guard = require_admin(conn, req, "beef")
    if guard:
        return guard
    if not req.csrf_ok():
        return redirect("/admin/pricing")
    action = _action_from_form(req.form)
    rows = pricing.preview(conn, action)
    changed = [row for row in rows if abs(row["delta"]) >= 0.005]
    summary = {
        "action": action,
        "rows": rows[:400],
        "changed": len(changed),
        "total": len(rows),
        "revenue_delta": round(sum(row["delta"] for row in changed), 2),
    }
    req.session_set("pricing_preview", summary)
    return redirect(f"/admin/pricing?scope={action['scope']}&value="
                    f"{action['value']}&q={action['search'] or ''}")


def pricing_apply(conn: db.sqlite3.Connection, req, **_):
    guard = require_admin(conn, req, "beef")
    if guard:
        return guard
    if not req.csrf_ok():
        return redirect("/admin/pricing")
    action = _action_from_form(req.form)
    if req.form.get("confirm") != "yes":
        req.session_set("pricing_preview", {
            "action": action, "rows": [], "changed": 0, "total": 0,
            "error": "Tick the confirm box before applying.",
        })
        return redirect("/admin/pricing")
    actor = req.session_get("admin_name") or "admin"
    summary = pricing.apply(conn, action, actor)
    db.log_audit(conn, f"pricing.{action['kind']}", "cuts", "",
                 json.dumps({"changed": summary["changed"]}), actor=actor)
    conn.commit()
    flash(req, f"Repriced {summary['changed']} cuts.", "ok")
    return redirect("/admin/pricing")


def pricing_revert(conn: db.sqlite3.Connection, req, **_):
    guard = require_admin(conn, req, "beef")
    if guard:
        return guard
    if not req.csrf_ok():
        return redirect("/admin/pricing")
    try:
        audit_id = int(req.form.get("audit", "0") or 0)
    except ValueError:
        audit_id = 0
    actor = req.session_get("admin_name") or "admin"
    if audit_id and pricing.revert(conn, audit_id, actor):
        flash(req, "Prices reverted to where they were before that change.", "ok")
    else:
        flash(req, "That change could not be reverted.", "error")
    return redirect("/admin/pricing")


def integrity(conn: db.sqlite3.Connection, req, **_):
    guard = require_admin(conn, req, "beef")
    if guard:
        return guard
    flagged = pricing.claim_integrity(conn)
    from ..services import market as market_service
    comparisons = {cut["id"]: market_service.compare(conn, cut)
                   for cut in flagged}
    context = page_context(conn, req, flagged=flagged, comparisons=comparisons,
                           csrf=req.csrf_token(),
                           admin_name=req.session_get("admin_name"),
                           cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("admin/integrity.html",
                                                       **context)


# -- market observations --------------------------------------------------

def market_admin(conn: db.sqlite3.Connection, req, **_):
    guard = require_admin(conn, req, "beef")
    if guard:
        return guard
    observations = db.rows(conn, "SELECT * FROM local_observations "
                                 "ORDER BY observed_at DESC, id DESC LIMIT 50")
    cuts = db.rows(conn, "SELECT id, name, market_series_key FROM cuts "
                         "WHERE active = 1 ORDER BY name")
    context = page_context(conn, req, observations=observations, cuts=cuts,
                           csrf=req.csrf_token(),
                           admin_name=req.session_get("admin_name"),
                           cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("admin/market.html",
                                                      **context)


def market_admin_post(conn: db.sqlite3.Connection, req, **_):
    guard = require_admin(conn, req, "beef")
    if guard:
        return guard
    if not req.csrf_ok():
        return redirect("/admin/market")
    form = req.form
    series_key = (form.get("series_key") or "").strip()
    store = (form.get("store") or "").strip()
    observed = (form.get("observed_at") or "").strip()
    try:
        value = float(form.get("value", "0") or 0)
    except ValueError:
        value = 0.0
    if series_key and store and value > 0 and observed:
        actor = req.session_get("admin_name") or "admin"
        conn.execute(
            "INSERT INTO local_observations(series_key, store, value, "
            "observed_at, note, actor) VALUES(?, ?, ?, ?, ?, ?)",
            (series_key, store, value, observed,
             (form.get("note") or "").strip(), actor))
        db.log_audit(conn, "market.observation", "series", series_key,
                     json.dumps({"store": store, "value": value}), actor=actor)
        conn.commit()
        flash(req, "Observation saved.", "ok")
    else:
        flash(req, "Series, store, price, and date are all required.", "error")
    return redirect("/admin/market")


def market_refresh(conn: db.sqlite3.Connection, req, **_):
    guard = require_admin(conn, req, "beef")
    if guard:
        return guard
    if not req.csrf_ok():
        return redirect("/admin/market")
    results = market.refresh(conn)
    summary = []
    for result in results:
        if result.ok:
            summary.append(f"{result.provider}: {len(result.observations)} series")
        else:
            summary.append(f"{result.provider}: unavailable ({result.error[:60]})")
    flash(req, " | ".join(summary), "ok" if any(r.ok for r in results) else "warn")
    return redirect("/admin/market")


def orders_admin(conn: db.sqlite3.Connection, req, **_):
    guard = require_admin(conn, req)
    if guard:
        return guard
    accessible = stores_service.accessible_stores(conn, _admin_id(conn, req))
    slugs = [row["slug"] for row in accessible]
    if slugs:
        marks = ",".join("?" for _ in slugs)
        rows = db.rows(
            conn, "SELECT DISTINCT o.* FROM orders o JOIN order_items oi "
            "ON oi.order_id = o.id WHERE oi.store_slug IN (" + marks + ") "
            "ORDER BY o.id DESC LIMIT 100", slugs)
    else:
        rows = []
    context = page_context(conn, req, orders=rows,
                           stores=accessible,
                           admin_name=req.session_get("admin_name"),
                           csrf=req.csrf_token(),
                           cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("admin/orders.html",
                                                       **context)


# -- per-store admin access ----------------------------------------------

def access_admin(conn, req, **_):
    guard = require_admin(conn, req)
    if guard:
        return guard
    if not _is_full_admin(conn, req):
        return redirect("/admin")
    admins = db.rows(conn, "SELECT * FROM admins ORDER BY username")
    stores = stores_service.all_stores(conn, active_only=False)
    access = {}
    for a in admins:
        access[a["id"]] = {r["store_slug"] for r in db.rows(
            conn, "SELECT store_slug FROM admin_store_access WHERE admin_id = ?",
            (a["id"],))}
    context = page_context(conn, req, admins=admins, stores=stores, access=access,
                           current_admin_id=_admin_id(conn, req),
                           csrf=req.csrf_token(),
                           admin_name=req.session_get("admin_name"),
                           cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("admin/access.html", **context)


def access_admin_post(conn, req, **_):
    guard = require_admin(conn, req)
    if guard:
        return guard
    if not _is_full_admin(conn, req):
        return redirect("/admin")
    if not req.csrf_ok():
        return redirect("/admin/access")
    try:
        admin_id = int(req.form.get("admin_id") or 0)
    except ValueError:
        return redirect("/admin/access")
    slugs = req.getlist("store_slug") if hasattr(req, "getlist") else []
    # form may submit repeated; fallback to single
    if not slugs:
        v = req.form.get("store_slug")
        slugs = [v] if v else []
    full_access = req.form.get("full_access") == "on"
    valid = {row["slug"] for row in stores_service.all_stores(conn, active_only=False)}
    slugs = [slug for slug in slugs if slug in valid]
    if not full_access and not slugs:
        flash(req, "Select at least one store, or grant full access.", "error")
        return redirect("/admin/access")
    target = db.one(conn, "SELECT full_access FROM admins WHERE id = ?",
                    (admin_id,))
    if target is None:
        flash(req, "That admin account no longer exists.", "error")
        return redirect("/admin/access")
    full_admins = int(db.scalar(conn,
                               "SELECT COUNT(*) FROM admins WHERE full_access = 1") or 0)
    if target and target["full_access"] and not full_access and full_admins <= 1:
        flash(req, "Keep at least one full-access admin account.", "error")
        return redirect("/admin/access")
    db.log_audit(conn, "admin.access.update", "admin", admin_id,
                 json.dumps({"full_access": full_access, "stores": slugs}),
                 actor=req.session_get("admin_name") or "admin")
    stores_service.set_access(conn, admin_id, slugs, full_access=full_access)
    flash(req, "Access updated.", "ok")
    return redirect("/admin/access")


def access_admin_create(conn, req, **_):
    guard = require_admin(conn, req)
    if guard:
        return guard
    if not _is_full_admin(conn, req):
        return redirect("/admin")
    if not req.csrf_ok():
        return redirect("/admin/access")
    username = (req.form.get("username") or "").strip()
    password = req.form.get("password") or ""
    full_access = req.form.get("full_access") == "on"
    slugs = req.getlist("store_slug")
    if not re.fullmatch(r"[A-Za-z0-9_.-]{3,40}", username):
        flash(req, "Username must be 3–40 letters, numbers, dots, dashes, or underscores.", "error")
        return redirect("/admin/access")
    if len(password) < 12:
        flash(req, "Use a password with at least 12 characters.", "error")
        return redirect("/admin/access")
    valid = {row["slug"] for row in stores_service.all_stores(conn, active_only=False)}
    slugs = [slug for slug in slugs if slug in valid]
    if not full_access and not slugs:
        flash(req, "Select at least one store, or grant full access.", "error")
        return redirect("/admin/access")
    try:
        cur = conn.execute(
            "INSERT INTO admins(username, passhash, role, full_access) "
            "VALUES(?, ?, 'store_admin', ?)",
            (username, auth.hash_password(password), 1 if full_access else 0))
    except db.sqlite3.IntegrityError:
        flash(req, "That username is already in use.", "error")
        return redirect("/admin/access")
    admin_id = int(cur.lastrowid)
    db.log_audit(conn, "admin.create", "admin", admin_id,
                 json.dumps({"username": username, "full_access": full_access,
                             "stores": slugs}),
                 actor=req.session_get("admin_name") or "admin")
    stores_service.set_access(conn, admin_id, slugs, full_access=full_access)
    flash(req, "Admin account created.", "ok")
    return redirect("/admin/access")


def access_admin_delete(conn, req, **_):
    guard = require_admin(conn, req)
    if guard:
        return guard
    if not _is_full_admin(conn, req):
        return redirect("/admin")
    if not req.csrf_ok():
        return redirect("/admin/access")
    try:
        target_id = int(req.form.get("admin_id") or 0)
    except ValueError:
        target_id = 0
    if target_id <= 0 or target_id == _admin_id(conn, req):
        flash(req, "You cannot delete the active admin account.", "error")
        return redirect("/admin/access")
    target = db.one(conn, "SELECT username, full_access FROM admins WHERE id = ?",
                    (target_id,))
    if target is None:
        return redirect("/admin/access")
    if target["full_access"] and int(db.scalar(
            conn, "SELECT COUNT(*) FROM admins WHERE full_access = 1") or 0) <= 1:
        flash(req, "Keep at least one full-access admin account.", "error")
        return redirect("/admin/access")
    db.log_audit(conn, "admin.delete", "admin", target_id,
                 json.dumps({"username": target["username"]}),
                 actor=req.session_get("admin_name") or "admin")
    conn.execute("DELETE FROM admins WHERE id = ?", (target_id,))
    conn.commit()
    flash(req, "Admin account removed.", "ok")
    return redirect("/admin/access")


# -- product CRUD --------------------------------------------------------

def _admin_store_slug(req) -> str:
    return (req.query.get("store") or req.form.get("store_slug") or "").strip()


def products_admin(conn, req, **_):
    guard = require_admin(conn, req)
    if guard:
        return guard
    store_slug = _admin_store_slug(req)
    stores = stores_service.accessible_stores(conn, _admin_id(conn, req))
    if not stores:
        return redirect("/admin")
    if not store_slug and stores:
        store_slug = stores[0]["slug"]
    if not any(s["slug"] == store_slug for s in stores):
        return redirect("/admin/products?store=" + stores[0]["slug"])
    store = stores_service.get(conn, store_slug) if store_slug else None
    products = products_service.list_for(conn, store_slug, active_only=False) if store_slug else []
    context = page_context(conn, req, stores=stores, store=store,
                           products=products, store_slug=store_slug,
                           csrf=req.csrf_token(),
                           admin_name=req.session_get("admin_name"),
                           cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("admin/products.html", **context)


def social_admin(conn, req, **_):
    guard = require_admin(conn, req)
    if guard:
        return guard
    stores = stores_service.accessible_stores(conn, _admin_id(conn, req))
    if not stores:
        return redirect("/admin")
    store_slug = _admin_store_slug(req) or stores[0]["slug"]
    if not any(s["slug"] == store_slug for s in stores):
        return redirect("/admin/social?store=" + stores[0]["slug"])
    links = db.rows(conn,
                    "SELECT * FROM social_links WHERE store_slug = ? "
                    "ORDER BY sort_order, id", (store_slug,))
    context = page_context(conn, req, stores=stores, store=stores_service.get(conn, store_slug),
                           store_slug=store_slug,
                           links=links, csrf=req.csrf_token(),
                           admin_name=req.session_get("admin_name"),
                           cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("admin/social.html", **context)


def social_admin_post(conn, req, **_):
    guard = require_admin(conn, req)
    if guard:
        return guard
    if not req.csrf_ok():
        return redirect("/admin/social")
    store_slug = (req.form.get("store_slug") or "").strip()
    if (stores_service.get(conn, store_slug) is None
            or not stores_service.has_access(conn, _admin_id(conn, req), store_slug)):
        return redirect("/admin")
    action = req.form.get("action") or "add"
    if action == "delete":
        try:
            link_id = int(req.form.get("link_id") or 0)
        except ValueError:
            link_id = 0
        conn.execute("UPDATE social_links SET active = 0 "
                     "WHERE id = ? AND store_slug = ?", (link_id, store_slug))
        db.log_audit(conn, "store.social.deactivate", "social_link", link_id,
                     json.dumps({"store": store_slug}),
                     actor=req.session_get("admin_name") or "admin")
        conn.commit()
        flash(req, "Social link deactivated.", "ok")
    else:
        label = (req.form.get("label") or "").strip()
        url = (req.form.get("url") or "").strip()
        blurb = (req.form.get("blurb") or "").strip()
        parsed_url = urlsplit(url)
        if len(label) < 2 or parsed_url.scheme not in ("https", "http") or not parsed_url.netloc:
            flash(req, "Enter a label and a full http(s) URL.", "error")
            return redirect(f"/admin/social?store={store_slug}")
        if action == "update":
            try:
                link_id = int(req.form.get("link_id") or 0)
            except ValueError:
                link_id = 0
            conn.execute(
                "UPDATE social_links SET label = ?, url = ?, blurb = ?, "
                "active = ? WHERE id = ? AND store_slug = ?",
                (label, url, blurb, 1 if req.form.get("active") == "on" else 0,
                 link_id, store_slug))
            db.log_audit(conn, "store.social.update", "social_link", link_id,
                         json.dumps({"store": store_slug, "url": url}),
                         actor=req.session_get("admin_name") or "admin")
        else:
            cur = conn.execute(
                "INSERT INTO social_links(store_slug, label, url, kind, blurb, "
                "icon, sort_order, active) VALUES(?, ?, ?, 'social', ?, 'link', "
                "COALESCE((SELECT MAX(sort_order) + 1 FROM social_links "
                "WHERE store_slug = ?), 1), 1)",
                (store_slug, label, url, blurb, store_slug))
            db.log_audit(conn, "store.social.create", "social_link", cur.lastrowid,
                         json.dumps({"store": store_slug, "url": url}),
                         actor=req.session_get("admin_name") or "admin")
        conn.commit()
        flash(req, "Social link saved.", "ok")
    return redirect(f"/admin/social?store={store_slug}")


def product_new(conn, req, **_):
    guard = require_admin(conn, req)
    if guard:
        return guard
    store_slug = _admin_store_slug(req)
    stores = stores_service.accessible_stores(conn, _admin_id(conn, req))
    if not stores:
        return redirect("/admin")
    if not store_slug and stores:
        store_slug = stores[0]["slug"]
    if not any(s["slug"] == store_slug for s in stores):
        return redirect("/admin/products?store=" + stores[0]["slug"])
    context = page_context(conn, req, stores=stores, store_slug=store_slug,
                           product=None, csrf=req.csrf_token(),
                           admin_name=req.session_get("admin_name"),
                           cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("admin/product_form.html", **context)


def product_create(conn, req, **_):
    guard = require_admin(conn, req)
    if guard:
        return guard
    if not req.csrf_ok():
        return redirect("/admin/products")
    store_slug = _admin_store_slug(req)
    if (stores_service.get(conn, store_slug) is None
            or not stores_service.has_access(conn, _admin_id(conn, req), store_slug)):
        return redirect("/admin/products")
    slug = (req.form.get("slug") or "").strip().lower()
    name = (req.form.get("name") or "").strip()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or not name:
        flash(req, "Use a lowercase hyphenated slug and enter a product name.", "error")
        return redirect(f"/admin/products/new?store={store_slug}")
    image_url = ""
    f = req.files.get("image")
    if f:
        image_url = uploads.save_upload(store_slug, f, slug or "img")
        if not image_url:
            flash(req, "Image upload failed. Use a valid image under 2 MB.", "error")
            return redirect(f"/admin/products/new?store={store_slug}")
    try:
        product_id = products_service.create(conn, store_slug=store_slug,
                           slug=slug,
                           name=name,
                           kind=(req.form.get("kind") or "item").strip(),
                           unit=(req.form.get("unit") or "each").strip(),
                           unit_lbs=req.form.get("unit_lbs") or 0,
                           price=req.form.get("price") or 0,
                           compare_at=req.form.get("compare_at") or 0,
                           compare_brand=(req.form.get("compare_brand") or "").strip(),
                           compare_size=(req.form.get("compare_size") or "").strip(),
                           compare_url=_http_url(req.form.get("compare_url") or ""),
                           compare_observed_at=(req.form.get("compare_observed_at") or "").strip(),
                           image=image_url,
                           icon=(req.form.get("icon") or "box").strip(),
                           blurb=(req.form.get("blurb") or "").strip(),
                           serving=(req.form.get("serving") or "").strip(),
                           stock=req.form.get("stock") or 0,
                           tags=(req.form.get("tags") or "").strip(),
                           featured=req.form.get("featured") == "on",
                           active=True,
                           sort_order=req.form.get("sort_order") or 0)
    except (ValueError, db.sqlite3.IntegrityError):
        flash(req, "Product could not be saved. Check its price and unique slug.", "error")
        return redirect(f"/admin/products/new?store={store_slug}")
    db.log_audit(conn, "store.product.create", "product", product_id,
                 json.dumps({"store": store_slug, "slug": slug, "name": name}),
                 actor=req.session_get("admin_name") or "admin")
    conn.commit()
    flash(req, "Product created.", "ok")
    return redirect(f"/admin/products?store={store_slug}")


def product_edit(conn, req, pid, **_):
    guard = require_admin(conn, req)
    if guard:
        return guard
    product = products_service.get_by_id(conn, int(pid))
    if product is None:
        return redirect("/admin/products")
    if not stores_service.has_access(conn, _admin_id(conn, req), product["store_slug"]):
        return redirect("/admin/products")
    stores = stores_service.accessible_stores(conn, _admin_id(conn, req)) or stores_service.all_stores(conn)
    context = page_context(conn, req, stores=stores,
                           store=stores_service.get(conn, product["store_slug"]),
                           store_slug=product["store_slug"],
                           product=product, csrf=req.csrf_token(),
                           admin_name=req.session_get("admin_name"),
                           cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("admin/product_form.html", **context)


def product_update(conn, req, pid, **_):
    guard = require_admin(conn, req)
    if guard:
        return guard
    if not req.csrf_ok():
        return redirect("/admin/products")
    product = products_service.get_by_id(conn, int(pid))
    if product is None:
        return redirect("/admin/products")
    store_slug = product["store_slug"]
    if not stores_service.has_access(conn, _admin_id(conn, req), store_slug):
        return redirect("/admin/products")
    image_url = product["image"]
    slug = (req.form.get("slug") or "").strip().lower()
    name = (req.form.get("name") or "").strip()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or not name:
        flash(req, "Use a lowercase hyphenated slug and enter a product name.", "error")
        return redirect(f"/admin/products/{pid}/edit")
    f = req.files.get("image")
    if f and f.get("data"):
        new_url = uploads.save_upload(store_slug, f, slug or "img")
        if new_url:
            image_url = new_url
        else:
            flash(req, "Image upload failed. Use a valid image under 2 MB.", "error")
            return redirect(f"/admin/products/{pid}/edit")
    try:
        products_service.update(conn, int(pid),
                           store_slug=(req.form.get("store_slug") or store_slug).strip(),
                           slug=slug,
                           name=name,
                           kind=(req.form.get("kind") or "item").strip(),
                           unit=(req.form.get("unit") or "each").strip(),
                           unit_lbs=req.form.get("unit_lbs") or product["unit_lbs"],
                           price=req.form.get("price") or product["price"],
                           compare_at=req.form.get("compare_at") or product["compare_at"],
                           compare_brand=(req.form.get("compare_brand") or "").strip(),
                           compare_size=(req.form.get("compare_size") or "").strip(),
                           compare_url=_http_url(req.form.get("compare_url") or ""),
                           compare_observed_at=(req.form.get("compare_observed_at") or "").strip(),
                           image=image_url,
                           icon=(req.form.get("icon") or product["icon"]).strip(),
                           blurb=(req.form.get("blurb") or "").strip(),
                           serving=(req.form.get("serving") or "").strip(),
                           stock=req.form.get("stock") or product["stock"],
                           tags=(req.form.get("tags") or "").strip(),
                           featured=req.form.get("featured") == "on",
                           active=req.form.get("active") == "on",
                           sort_order=req.form.get("sort_order") or product["sort_order"])
    except (ValueError, db.sqlite3.IntegrityError):
        flash(req, "Product could not be saved. Check its price and unique slug.", "error")
        return redirect(f"/admin/products/{pid}/edit")
    db.log_audit(conn, "store.product.update", "product", pid,
                 json.dumps({"store": store_slug, "slug": slug, "name": name}),
                 actor=req.session_get("admin_name") or "admin")
    conn.commit()
    flash(req, "Product updated.", "ok")
    return redirect(f"/admin/products?store={store_slug}")


def product_delete(conn, req, pid, **_):
    guard = require_admin(conn, req)
    if guard:
        return guard
    if not req.csrf_ok():
        return redirect("/admin/products")
    product = products_service.get_by_id(conn, int(pid))
    if product is None:
        return redirect("/admin/products")
    if not stores_service.has_access(conn, _admin_id(conn, req), product["store_slug"]):
        return redirect("/admin/products")
    products_service.delete(conn, int(pid))
    db.log_audit(conn, "store.product.deactivate", "product", pid,
                 json.dumps({"store": product["store_slug"],
                             "slug": product["slug"]}),
                 actor=req.session_get("admin_name") or "admin")
    conn.commit()
    flash(req, "Product deactivated.", "ok")
    return redirect(f"/admin/products?store={product['store_slug']}")


def _admin_id(conn, req):
    try:
        value = req.session_get("admin_id")
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _is_full_admin(conn, req) -> bool:
    return stores_service.is_full_admin(conn, _admin_id(conn, req))


def _http_url(value: str) -> str:
    value = (value or "").strip()
    parsed = urlsplit(value)
    return value if parsed.scheme in ("http", "https") and parsed.netloc else ""
