"""Storefront pages for the co-op businesses (non-beef)."""
from __future__ import annotations

import re

from .. import db, web
from ..services import products as products_service
from ..services import stores as stores_service
from ..services import variants as variants_service
from . import cart_count, page_context, not_found


def register(add) -> None:
    add("GET", re.compile(r"^/fermentation$"), lambda c, r, **k: store_list(c, r, "fermentation", **k))
    add("GET", re.compile(r"^/fermentation/(?P<slug>[a-z0-9-]+)$"),
        lambda c, r, slug, **k: store_detail(c, r, "fermentation", slug, **k))
    add("GET", re.compile(r"^/freeze-dried$"), lambda c, r, **k: store_list(c, r, "freeze-dried", **k))
    add("GET", re.compile(r"^/freeze-dried/(?P<slug>[a-z0-9-]+)$"),
        lambda c, r, slug, **k: store_detail(c, r, "freeze-dried", slug, **k))


def _guard_store(conn, slug):
    store = stores_service.get(conn, slug)
    if store is None or not store["active"]:
        return None
    return store


def store_list(conn, req, store_slug, **_):
    store = _guard_store(conn, store_slug)
    if store is None:
        return not_found(conn, req, message="That store is not open.")
    products = products_service.list_for(conn, store_slug)
    rows = []
    for p in products:
        variants = variants_service.list_for_product(
            conn, p["id"], active_only=True)
        default = variants[0] if variants else None
        rows.append({"product": p, "variants": variants, "default": default})
    context = page_context(
        conn, req, store=store, rows=rows, url_prefix=store_slug,
        cart_count=cart_count(conn, req), csrf=req.csrf_token())
    return 200, "text/html; charset=utf-8", web.render("store_list.html", **context)


def store_detail(conn, req, store_slug, slug, **_):
    store = _guard_store(conn, store_slug)
    if store is None:
        return not_found(conn, req, message="That store is not open.")
    product = products_service.get(conn, store_slug, slug)
    if product is None or not product["active"]:
        return not_found(conn, req, message="We do not carry that item.")
    variants = variants_service.list_for_product(
        conn, product["id"], active_only=True)
    default = variants[0] if variants else None
    others = [p for p in products_service.list_for(conn, store_slug)
              if p["id"] != product["id"]][:4]
    context = page_context(
        conn, req, store=store, product=product, variants=variants,
        default=default, others=others, url_prefix=store_slug,
        cart_count=cart_count(conn, req), csrf=req.csrf_token())
    return 200, "text/html; charset=utf-8", web.render("store_detail.html", **context)
