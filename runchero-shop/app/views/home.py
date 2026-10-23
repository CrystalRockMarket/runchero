"""Home page: a funnel, not a wall of cuts.

The featured move is filling the freezer (shares and boxes). Under that come
the week's best shelf comparisons and the cuts the neighborhood keeps buying.
"""
from __future__ import annotations

import re

from .. import db, web
from ..services import catalog, market
from . import cart_count, page_context


def register(add) -> None:
    add("GET", re.compile(r"^/$"), home)


#: The six ways people actually think about buying beef, kept low on the page.
ENTRIES = [
    ("shop?tag=steak", "Steak Night", "Ribeyes, strips, filets", "cow"),
    ("shop?primal=ground", "Ground Beef", "Burgers, tacos, chili", "cow"),
    ("shop?tag=roast", "Slow Cooker", "Roasts for the family", "calendar"),
    ("shop?tag=smoker", "Smoker Cuts", "Brisket, ribs, tri-tip", "cow"),
    ("shares", "Fill the Freezer", "Bulk packs and cow shares", "download"),
    ("packages", "Packages", "Curated bundles and deals", "box"),
]


def _best_deals(conn, cuts, comparisons, limit=6):
    """The cuts that beat their published benchmark by the widest margin."""
    ranked = []
    for cut in cuts:
        cmp = comparisons.get(cut["slug"]) or {}
        if not cmp.get("available") or not cmp.get("under") or cmp.get("stale"):
            continue
        ranked.append((cmp["pct"], cut))
    ranked.sort(key=lambda pair: pair[0], reverse=True)
    return [cut for _, cut in ranked[:limit]]


def home(conn: db.sqlite3.Connection, req, **_):
    shares = sorted(catalog.shares(conn), key=lambda r: r["sort_order"],
                    reverse=True)
    boxes = catalog.packages(conn, limit=4)
    all_cuts = catalog.cuts(conn)
    comparisons = {c["slug"]: market.compare(conn, c) for c in all_cuts}
    deals = _best_deals(conn, all_cuts, comparisons)
    deal_slugs = {c["slug"] for c in deals}
    favorites = [c for c in all_cuts
                 if c["featured"] and c["slug"] not in deal_slugs][:6]
    if len(favorites) < 6:
        for cut in all_cuts:
            if cut["slug"] not in deal_slugs and cut not in favorites:
                favorites.append(cut)
            if len(favorites) >= 6:
                break
    links = catalog.social_links(conn)

    context = page_context(
        conn, req,
        entries=ENTRIES,
        boxes=boxes,
        shares=shares,
        deals=deals,
        comparisons=comparisons,
        favorites=favorites,
        ground_cut=catalog.cut_by_slug(conn, "ground-beef-80-20"),
        social_links=links,
        ground=market.latest(conn, "ers:ground_beef"),
        choice=market.latest(conn, "ers:choice_beef_retail"),
        stale_days=21,
        cart_count=cart_count(conn, req),
    )
    return 200, "text/html; charset=utf-8", web.render("home.html", **context)
