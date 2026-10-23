"""Catalog pages: the shop grid, cut pages, packages, and shares."""
from __future__ import annotations

import re

from .. import db, web
from ..services import campaigns as campaigns_service
from ..services import catalog, market, packing
from . import cart_count, flash, not_found, page_context, redirect

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def register(add) -> None:
    add("GET", re.compile(r"^/shop$"), shop)
    add("GET", re.compile(r"^/shop/(?P<primal>[a-z0-9-]+)$"), shop)
    add("GET", re.compile(r"^/cut/(?P<slug>[a-z0-9-]+)$"), cut)
    add("GET", re.compile(r"^/packages$"), packages)
    add("GET", re.compile(r"^/package/(?P<slug>[a-z0-9-]+)$"), package)
    add("GET", re.compile(r"^/shares$"), shares)
    add("GET", re.compile(r"^/share/(?P<slug>[a-z0-9-]+)$"), share)
    add("GET", re.compile(r"^/campaigns$"), campaigns)
    add("GET", re.compile(r"^/campaign/(?P<slug>[a-z0-9-]+)$"), campaign)
    add("POST", re.compile(r"^/campaign/(?P<slug>[a-z0-9-]+)/join$"), campaign_join)


SORTS = [
    ("featured", "Featured"),
    ("price-asc", "Price: low to high"),
    ("price-desc", "Price: high to low"),
    ("deal", "Biggest savings"),
    ("name", "Name: A to Z"),
]


def _sort_cuts(cuts, comparisons, sort):
    """Order the shop without losing the filter the customer arrived with."""
    if sort == "price-asc":
        cuts.sort(key=lambda c: (c["price_per_lb"] or c["runchero_price"],
                                 c["name"]))
    elif sort == "price-desc":
        cuts.sort(key=lambda c: (c["price_per_lb"] or c["runchero_price"],
                                 c["name"]), reverse=True)
    elif sort == "name":
        cuts.sort(key=lambda c: c["name"].lower())
    elif sort == "deal":
        def key(c):
            cmp = comparisons.get(c["slug"]) or {}
            ranked = bool(cmp.get("available") and cmp.get("under")
                          and not cmp.get("stale"))
            return (ranked, cmp.get("pct", 0.0))
        cuts.sort(key=key, reverse=True)
    return cuts


def shop(conn: db.sqlite3.Connection, req, primal: str | None = None, **_):
    primal_slug = primal
    tag = req.query.get("tag") or None
    search = req.query.get("q") or None
    sort = req.query.get("sort") or "featured"
    if sort not in {key for key, _ in SORTS}:
        sort = "featured"
    primals = catalog.primals(conn)
    current = None
    for row in primals:
        if row["slug"] == primal_slug:
            current = row
            break
    if primal_slug and current is None:
        return not_found(conn, req,
                         message="We do not have a cut group by that name.")
    cuts = catalog.cuts(conn, primal_slug=primal_slug, tag=tag, search=search)
    comparisons = {c["slug"]: market.compare(conn, c) for c in cuts}
    cuts = _sort_cuts(cuts, comparisons, sort)

    context = page_context(
        conn, req,
        primals=primals, current=current, cuts=cuts,
        comparisons=comparisons, tag=tag, search=search, sort=sort,
        sorts=SORTS,
        tags=catalog.tag_list(conn), csrf=req.csrf_token(),
        cart_count=cart_count(conn, req),
    )
    return 200, "text/html; charset=utf-8", web.render("shop.html", **context)


def cut(conn: db.sqlite3.Connection, req, slug: str, **_):
    row = catalog.cut_by_slug(conn, slug)
    if row is None:
        return not_found(conn, req, message="We do not carry that cut.")
    comparison = market.compare(conn, row)
    related = catalog.cuts(conn, primal_slug=row["primal_slug"], limit=4)
    related = [r for r in related if r["slug"] != slug][:4]
    line_groups = packing.line_groups_for(conn, row["tags"])
    context = page_context(
        conn, req,
        cut=row, comparison=comparison, related=related,
        line_groups=line_groups,
        primals=catalog.primals(conn), csrf=req.csrf_token(),
        cart_count=cart_count(conn, req),
    )
    return 200, "text/html; charset=utf-8", web.render("cut.html", **context)


def packages(conn: db.sqlite3.Connection, req, **_):
    rows = catalog.packages(conn)
    context = page_context(
        conn, req, packages=rows, csrf=req.csrf_token(),
        cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("packages.html", **context)


def package(conn: db.sqlite3.Connection, req, slug: str, **_):
    row = catalog.package_by_slug(conn, slug)
    if row is None:
        return not_found(conn, req, message="That package is not available.")
    items = catalog.package_items(conn, row["id"])
    context = page_context(
        conn, req, package=row, items=items, csrf=req.csrf_token(),
        cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("package.html", **context)


def shares(conn: db.sqlite3.Connection, req, **_):
    rows = catalog.shares(conn)
    choice = market.latest(conn, "ers:choice_beef_retail")
    context = page_context(
        conn, req, shares=rows, choice=choice, csrf=req.csrf_token(),
        cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("shares.html", **context)


def share(conn: db.sqlite3.Connection, req, slug: str, **_):
    row = catalog.share_by_slug(conn, slug)
    if row is None:
        return not_found(conn, req, message="That share is not available.")
    contents = catalog.share_contents(conn, row["takehome_lbs"],
                                      row["price_per_lb"])
    choice = market.latest(conn, "ers:choice_beef_retail")
    context = page_context(
        conn, req, share=row, contents=contents, choice=choice,
        all_shares=catalog.shares(conn), csrf=req.csrf_token(),
        cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("share.html", **context)


def campaigns(conn: db.sqlite3.Connection, req, **_):
    rows = campaigns_service.campaigns(conn)
    states = {row["id"]: campaigns_service.state(conn, row) for row in rows}
    context = page_context(conn, req, campaigns=rows, states=states,
                           csrf=req.csrf_token(),
                           cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("campaigns.html",
                                                        **context)


def campaign(conn: db.sqlite3.Connection, req, slug: str, **_):
    row = campaigns_service.campaign_by_slug(conn, slug)
    if row is None:
        return not_found(conn, req, message="That campaign is not open.")
    info = campaigns_service.state(conn, row)
    context = page_context(conn, req, campaign=row, info=info,
                           csrf=req.csrf_token(),
                           cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("campaign.html",
                                                        **context)


def campaign_join(conn: db.sqlite3.Connection, req, slug: str, **_):
    if not req.csrf_ok():
        flash(req, "Your session expired. Please try again.", "error")
        return redirect(f"/campaign/{slug}")
    row = campaigns_service.campaign_by_slug(conn, slug)
    if row is None:
        return not_found(conn, req, message="That campaign is not open.")
    name = (req.form.get("name") or "").strip()
    email = (req.form.get("email") or "").strip()
    phone = (req.form.get("phone") or "").strip()
    note = (req.form.get("note") or "").strip()
    if len(name) < 2:
        flash(req, "Tell us the household name.", "error")
        return redirect(f"/campaign/{slug}")
    if not _EMAIL_RE.match(email):
        flash(req, "We need a working email to hold your place.", "error")
        return redirect(f"/campaign/{slug}")
    ok, message = campaigns_service.join(conn, row["id"], name, email, phone,
                                         note)
    flash(req, message, "ok" if ok else "error")
    return redirect(f"/campaign/{slug}")
