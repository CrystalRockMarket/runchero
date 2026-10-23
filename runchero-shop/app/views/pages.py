"""Standalone pages: how it works, market prices, terms, policy, contact."""
from __future__ import annotations

import json
import re

from .. import db, web
from ..services import campaigns as campaigns_service
from ..services import catalog, market, products as products_service
from . import cart_count, canonical_url, page_context, redirect


def register(add) -> None:
    add("GET", re.compile(r"^/how-it-works$"), how_it_works)
    add("GET", re.compile(r"^/market-prices$"), market_prices)
    add("GET", re.compile(r"^/data-sources$"), data_sources)
    add("GET", re.compile(r"^/terms$"), terms)
    add("GET", re.compile(r"^/policy$"), policy)
    add("GET", re.compile(r"^/contact$"), contact)
    add("GET", re.compile(r"^/cow-drops$"), cow_drops)
    add("GET", re.compile(r"^/manifest\.webmanifest$"), manifest)
    add("GET", re.compile(r"^/robots\.txt$"), robots)
    add("GET", re.compile(r"^/sitemap\.xml$"), sitemap)


def how_it_works(conn: db.sqlite3.Connection, req, **_):
    context = page_context(conn, req, cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("how.html", **context)


def market_prices(conn: db.sqlite3.Connection, req, **_):
    cuts = catalog.cuts(conn)
    by_key: dict[str, db.sqlite3.Row] = {}
    for row in cuts:
        key = (row["market_series_key"] or "").strip()
        if key:
            by_key[key] = row
    # The public table is the benchmark behind each cut, so it only carries
    # per-pound series that actually map to something we sell. National
    # averages, spreads, and index series live on the data-sources page.
    table = [row for row in market.market_table(conn)
             if row["unit"] == "lb" and row["series_key"] in by_key]
    context = page_context(
        conn, req, table=table, by_key=by_key,
        stale_days=21, cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("market.html", **context)


def data_sources(conn: db.sqlite3.Connection, req, **_):
    """The receipts behind the receipts: every feed and every rule.

    Linked from the footer only. This is the page a careful buyer (or a
    reporter) opens when they want to know why a number looks the way it
    does.
    """
    feeds = [
        {
            "name": "USDA AMS",
            "title": "Weekly Grocery Store Beef Feature Activity",
            "what": "Advertised per-pound prices at major grocery outlets, "
                    "collected store by store and published weekly as report "
                    "ams_3228.",
            "detail": f"Kentucky is read from the {market.AMS_REGION} region "
                      "block. Only advertised feature prices are used; budget "
                      "&ldquo;value&rdquo; store brands are skipped so the "
                      "comparison stays against USDA Choice product.",
            "cadence": "Weekly",
            "unit": "Per lb, advertised",
            "url": market.AMS_3228_URL,
            "link": "ams_3228.pdf",
            "icon": "truck",
        },
        {
            "name": "USDA ERS",
            "title": "Summary of Retail Prices and Price Spreads",
            "what": "Monthly national retail values for beef, plus the spread "
                    "between what the farmer gets, the wholesaler, and the "
                    "grocery shelf.",
            "detail": "Used for the big-picture series (all-fresh beef, Choice "
                      "beef, ground beef, round roast, sirloin steak) and for "
                      "the price-spread figures cited on the market page.",
            "cadence": "Monthly",
            "unit": "Per lb, national average",
            "url": market.ERS_CSV_URL,
            "link": "Summary of Retail Prices and Price Spreads (CSV)",
            "icon": "notes",
        },
        {
            "name": "BLS",
            "title": "Average Price Data, Ground Beef (CPI)",
            "what": "The Bureau of Labor Statistics' public API, which carries "
                    "the monthly average price shoppers actually pay for "
                    "ground beef.",
            "detail": "Three ground-beef series are tracked: ground chuck, "
                      "ground beef, and lean/extra-lean ground beef. Together "
                      "they anchor the ground-beef cuts in the shop.",
            "cadence": "Monthly",
            "unit": "Per lb, national average",
            "url": market.BLS_API_URL.format(series_id="APU0000703112"),
            "link": "api.bls.gov series APU0000703112",
            "icon": "magnifier",
        },
    ]
    series = [
        {"source": row["source"], "key": row["series_key"],
         "label": row["label"], "region": row["region"]}
        for row in market.market_table(conn)
    ]
    context = page_context(
        conn, req, feeds=feeds, series=series,
        ams_region=market.AMS_REGION,
        stale_days=21, cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("sources.html", **context)


def _md_lite(text: str) -> str:
    """Just enough markdown for the terms: headings, bullets, paragraphs.
    Everything is escaped, so seeded copy can never smuggle markup in."""
    import html as _html
    out: list[str] = []
    in_list = False

    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            close_list()
            continue
        if line.startswith("## "):
            close_list()
            out.append(f'<h2>{_html.escape(line[3:])}</h2>')
        elif line.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{_html.escape(line[2:])}</li>")
        else:
            close_list()
            out.append(f"<p>{_html.escape(line)}</p>")
    close_list()
    return "".join(out)


def terms(conn: db.sqlite3.Connection, req, **_):
    row = db.one(conn, "SELECT * FROM terms_versions ORDER BY id DESC LIMIT 1")
    context = page_context(conn, req, terms=row,
                           terms_html=_md_lite(row["body"]) if row else "",
                           cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("terms.html", **context)


def policy(conn: db.sqlite3.Connection, req, **_):
    context = page_context(conn, req, cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("policy.html", **context)


def contact(conn: db.sqlite3.Connection, req, **_):
    context = page_context(conn, req,
                           social_links=catalog.social_links(conn),
                           cart_count=cart_count(conn, req))
    return 200, "text/html; charset=utf-8", web.render("contact.html", **context)


def cow_drops(conn: db.sqlite3.Connection, req, **_):
    """Legacy explainer URL now lives on the Cow drops page."""
    return redirect("/campaigns", 301)


def manifest(conn: db.sqlite3.Connection, req, **_):
    payload = {
        "name": web.env().globals["site_name"],
        "short_name": web.env().globals["site_short"],
        "description": web.env().globals["site_tagline"],
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "background_color": "#1b1b23",
        "theme_color": "#1b1b23",
        "icons": [
            {"src": "/static/img/icons/favicon-192.png", "sizes": "192x192",
             "type": "image/png"},
            {"src": "/static/img/icons/favicon-512.png", "sizes": "512x512",
             "type": "image/png", "purpose": "any maskable"},
        ],
    }
    return 200, "application/manifest+json", json.dumps(payload)


def robots(conn: db.sqlite3.Connection, req, **_):
    base = canonical_url(req).split("://")[0] + "://" + \
        canonical_url(req).split("://")[1].split("/")[0]
    body = (f"User-agent: *\nAllow: /\nDisallow: /admin\nDisallow: /account\n"
            f"Disallow: /checkout\nDisallow: /order\nDisallow: /manage\n"
            f"Disallow: /cart\nSitemap: {base}/sitemap.xml\n")
    return 200, "text/plain; charset=utf-8", body


def sitemap(conn: db.sqlite3.Connection, req, **_):
    """Every public page, for search engines."""
    base = canonical_url(req).split("://")[0] + "://" + \
        canonical_url(req).split("://")[1].split("/")[0]
    urls: list[tuple[str, str]] = [
        ("/", "1.0"),
        ("/shop", "0.9"),
        ("/packages", "0.8"),
        ("/shares", "0.8"),
        ("/campaigns", "0.8"),
        ("/market-prices", "0.7"),
        ("/data-sources", "0.5"),
        ("/how-it-works", "0.6"),
        ("/terms", "0.4"),
        ("/policy", "0.4"),
        ("/contact", "0.4"),
        ("/fermentation", "0.8"),
        ("/freeze-dried", "0.8"),
    ]
    for primal in catalog.primals(conn):
        urls.append((f"/shop/{primal['slug']}", "0.7"))
    for cut in catalog.cuts(conn):
        urls.append((f"/cut/{cut['slug']}", "0.6"))
    for package in catalog.packages(conn):
        urls.append((f"/package/{package['slug']}", "0.6"))
    for share in catalog.shares(conn):
        urls.append((f"/share/{share['slug']}", "0.6"))
    for campaign in campaigns_service.campaigns(conn):
        urls.append((f"/campaign/{campaign['slug']}", "0.7"))
    for store_slug, prefix in (("fermentation", "fermentation"),
                               ("freeze-dried", "freeze-dried")):
        for product in products_service.list_for(conn, store_slug):
            urls.append((f"/{prefix}/{product['slug']}", "0.6"))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, priority in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{base}{path}</loc>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return 200, "application/xml; charset=utf-8", "\n".join(lines) + "\n"
