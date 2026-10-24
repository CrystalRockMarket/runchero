#!/usr/bin/env python3
"""Smoke test the running shop: every public page, the cart flow, the full
checkout, the packing options, subscriptions, and the admin console.

    python3 tools/smoke.py [base_url]

Defaults to http://127.0.0.1:8081. Exits non-zero on the first failure, and
prints one line per check.
"""
from __future__ import annotations

import http.cookiejar
import base64
import io
import json
import os
import re
import sys
import time
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request
from PIL import Image

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8081"
STAMP = str(int(time.time()))
ORDER_EMAIL = f"smoke+{STAMP}@example.com"
ACCOUNT_EMAIL = f"account+{STAMP}@example.com"
# Admin credentials for the console checks. Set RBS_ADMIN_PASSWORD to run
# them; without it the admin section is skipped.
ADMIN_USER = os.environ.get("RBS_ADMIN_USER", "runchero")
ADMIN_PASSWORD = os.environ.get("RBS_ADMIN_PASSWORD", "")

class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Stop urllib from following redirects, so a flash stays on the page."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(jar))
plain_opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(jar), NoRedirect)
PASS = 0
FAIL = 0


def get(path: str) -> tuple[int, str]:
    try:
        with opener.open(BASE + path, timeout=20) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")


def post(path: str, fields: dict, follow: bool = True) -> tuple[int, str]:
    data = urllib.parse.urlencode(fields).encode("utf-8")
    client = opener if follow else plain_opener
    try:
        with client.open(BASE + path, data=data, timeout=20) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")


def post_multipart(path: str, fields: dict[str, str],
                   files: dict[str, tuple[str, str, bytes]] | None = None,
                   follow: bool = True) -> tuple[int, str]:
    boundary = "----RuncheroSmokeBoundary"
    chunks: list[bytes] = []
    for name, value in fields.items():
        chunks.extend([
            f"--{boundary}\r\n".encode(),
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(),
            str(value).encode("utf-8"), b"\r\n",
        ])
    for name, (filename, content_type, data) in (files or {}).items():
        chunks.extend([
            f"--{boundary}\r\n".encode(),
            (f'Content-Disposition: form-data; name="{name}"; '
             f'filename="{filename}"\r\n').encode(),
            f"Content-Type: {content_type}\r\n\r\n".encode(),
            data, b"\r\n",
        ])
    chunks.append(f"--{boundary}--\r\n".encode())
    request = urllib.request.Request(
        BASE + path, data=b"".join(chunks),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST")
    client = opener if follow else plain_opener
    try:
        with client.open(request, timeout=20) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")


def csrf_from(html: str) -> str:
    match = re.search(r'name="_csrf" value="([^"]+)"', html)
    return match.group(1) if match else ""


def check(label: str, condition: bool, detail: str = "") -> None:
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  ok    {label}")
    else:
        FAIL += 1
        print(f"  FAIL  {label} {detail}")


def expect_page(path: str, needle: str, label: str | None = None) -> None:
    status, body = get(path)
    check(label or path, status == 200 and needle in body,
          f"(status {status})")


def main() -> int:
    global jar, opener, plain_opener
    print(f"smoke testing {BASE}")

    # -- public pages -----------------------------------------------------
    expect_page("/", "Runchero", "home")
    expect_page("/shop", "cuts", "shop")
    status, body = get("/shop")
    slug = ""
    match = re.search(r'href="/cut/([a-z0-9-]+)"', body)
    if match:
        slug = match.group(1)
    check("shop lists cuts", bool(slug))
    if slug:
        expect_page(f"/cut/{slug}", "Add to cart", f"cut page {slug}")
    expect_page("/packages", "Package", "packages")
    status, body = get("/packages")
    match = re.search(r'href="/package/([a-z0-9-]+)"', body)
    if match:
        expect_page(f"/package/{match.group(1)}", "inside", "package page")
    expect_page("/shares", "share", "shares")
    status, body = get("/shares")
    match = re.search(r'href="/share/([a-z0-9-]+)"', body)
    if match:
        expect_page(f"/share/{match.group(1)}", "Reserve", "share page")

    # -- accessibility and seo ---------------------------------------------
    for path in ("/", "/shop", "/packages", "/shares", "/campaigns",
                 "/market-prices", "/data-sources", "/how-it-works", "/terms",
                 "/contact"):
        status, body = get(path)
        ok = status == 200
        check(f"{path} has one h1", body.count("<h1") == 1)
        check(f"{path} has a title", "<title>" in body and "</title>" in body)
        check(f"{path} has a meta description",
              'name="description"' in body)
        check(f"{path} has a canonical link", 'rel="canonical"' in body)
        check(f"{path} has open graph tags",
              'property="og:title"' in body and 'property="og:description"' in body)
        check(f"{path} has a skip link", 'class="skip-link"' in body)
        check(f"{path} labels the nav", 'aria-label="Main"' in body)

    status, home_page = get("/")
    match = re.search(r'property="og:image" content="([^"]+)"', home_page)
    check("home advertises a real social card",
          bool(match) and match.group(1).endswith("/static/img/og-cover.png"))
    status, body = get("/shop")
    home_desc = re.search(r'name="description" content="([^"]*)"', home_page)
    shop_desc = re.search(r'name="description" content="([^"]*)"', body)
    check("pages carry their own meta description",
          bool(home_desc and shop_desc)
          and home_desc.group(1) != shop_desc.group(1))
    for asset in ("/static/img/og-cover.png",
                  "/static/img/og-fermentation.png",
                  "/static/img/og-freeze-dried.png",
                  "/static/img/icons/favicon-180.png",
                  "/static/img/icons/favicon-192.png",
                  "/static/img/icons/favicon-512.png"):
        status, _ = get(asset)
        check(f"{asset} serves", status == 200, f"(status {status})")
    status, body = get("/manifest.webmanifest")
    check("manifest offers install icons",
          status == 200 and "favicon-192.png" in body
          and "512x512" in body and "#1b1b23" in body)
    status, body = get("/robots.txt")
    check("robots.txt points at the sitemap", "Sitemap:" in body)
    check("robots.txt closes private areas",
          all(f"Disallow: {path}" in body for path in
              ("/account", "/checkout", "/order", "/manage", "/cart")))
    status, body = get("/sitemap.xml")
    check("sitemap is xml", status == 200 and "<urlset" in body
          and "<loc>" in body)
    check("sitemap lists the shop", "/shop" in body and "/campaigns" in body)
    check("sitemap lists cut groups", "/shop/chuck" in body)
    check("sitemap lists the data sources", "/data-sources" in body)
    check("sitemap lists co-op stores",
          "/fermentation" in body and "/freeze-dried" in body)
    check("sitemap lists co-op bulk and how-it-works",
          "/fermentation/bulk" in body
          and "/fermentation/how-it-works" in body
          and "/freeze-dried/how-it-works" in body)
    status, _ = get("/shop/not-a-cut-group")
    check("unknown cut group is a 404", status == 404, f"(status {status})")
    status, body = get("/market-prices")
    check("market table only carries mapped per-pound rows",
          "not mapped" not in body and "Benchmark / lb" in body)
    status, body = get("/fermentation")
    check("Fermentation Station storefront", status == 200
          and "Fermentation Station" in body and "Kombucha" in body)
    check("fermentation storefront has ten seeded products",
          body.count('<article class="card">') == 10)
    check("fermentation uses its own brand in the document title",
          "Fermentation Station | Runchero Beef</title>" in body
          and "/static/img/og-fermentation.png" in body)
    check("fermentation does not inherit beef social links",
          "facebook.com/runchero" not in body)
    status, body = get("/fermentation/kombucha-classic")
    check("kombucha item page", status == 200 and "16 oz bottle" in body)
    status, body = get("/fermentation")
    nav = re.search(r'<nav class="mainnav".*?</nav>', body, re.S)
    mainnav = nav.group(0) if nav else ""
    check("fermentation nav drops the beef-only links",
          'href="/fermentation/bulk"' in mainnav
          and 'href="/shares"' not in mainnav
          and 'href="/packages"' not in mainnav
          and 'href="/campaigns"' not in mainnav
          and 'href="/market-prices"' not in mainnav)
    check("top menu carries sign in and cart inline",
          "Sign in" in mainnav and "Cart" in mainnav
          and "My Order" not in body and 'class="top-actions"' not in body)
    nav = re.search(r'<nav class="mainnav".*?</nav>', home_page, re.S)
    beefnav = nav.group(0) if nav else ""
    check("beef nav keeps its own links",
          all(f'href="{path}"' in beefnav for path in
              ("/packages", "/shares", "/campaigns", "/market-prices")))
    status, bulk = get("/fermentation/bulk")
    check("fermentation bulk page prices 25/50/100 lb lots",
          status == 200 and "25 lb" in bulk and "50 lb" in bulk
          and "100 lb" in bulk and "made to order" in bulk.lower()
          and "The Crea" in bulk and "Refrigerated" in bulk)
    status, how = get("/fermentation/how-it-works")
    check("fermentation how-it-works tells the local farm story",
          status == 200 and "How Fermentation Station works" in how
          and "community farm" in how and "downtown" in how
          and "The Crea" in how)
    status, body = get("/freeze-dried")
    check("Runchero Freeze-Dried storefront", status == 200
          and "Runchero Freeze-Dried" in body
          and "/static/img/og-freeze-dried.png" in body
          and "produce by the pound" in body.lower()
          and "Ready meals &amp; bulk lots" in body)
    check("freeze-dried storefront has meals and 100-pouch lots",
          "Homemade Curry Meal" in body and "100 pouches" in body)
    nav = re.search(r'<nav class="mainnav".*?</nav>', body, re.S)
    mainnav = nav.group(0) if nav else ""
    check("freeze-dried nav drops the beef-only links",
          'href="/shares"' not in mainnav
          and 'href="/packages"' not in mainnav
          and 'href="/campaigns"' not in mainnav
          and 'href="/market-prices"' not in mainnav)
    status, body = get("/freeze-dried/fd-corn")
    check("freeze-dried comparison cites its package and source",
          status == 200 and "North Bay Trading" in body
          and "$25.69/lb equivalent" in body and "View source" in body)

    # -- data sources explainer -------------------------------------------
    status, body = get("/data-sources")
    check("sources names the AMS report",
          "ams_3228" in body or "Feature Activity" in body)
    check("sources names the ERS report",
          "Retail Prices and Price Spreads" in body)
    check("sources names the BLS series", "BLS" in body and "APU0000703112" in body)
    check("sources links the public reports",
          "ams.usda.gov" in body and "ers.usda.gov" in body
          and "bls.gov" in body)
    check("sources explains the margin", "margin" in body.lower())
    status, home_body = get("/")
    check("footer links the sources page", 'href="/data-sources"' in home_body)
    check("footer has an admin login button",
          'class="btn small ghost" href="/admin/login"' in home_body)
    check("sources page is footer-only", home_body.count('href="/data-sources"') == 1)

    # -- landing funnel order ---------------------------------------------
    orders = []
    for marker in ('id="freezer-h"', 'id="deals-h"', 'id="favorites-h"'):
        orders.append(home_body.find(marker))
    check("home leads with fill-the-freezer",
          0 <= orders[0] < orders[1] < orders[2])
    check("home shows freezer boxes", "Freezer box" in home_body)
    check("home shows market band", "market-band" in home_body)
    check("home deals show a percent under shelf", "deal-pct" in home_body)

    # -- every cut has its own artwork ------------------------------------
    status, shop_body = get("/shop")
    thumb_icons = re.findall(
        r'<div class="thumb">\s*<img src="/static/img/icons/([a-z_0-9]+)@4x\.png"',
        shop_body)
    check("cut cards have real cut artwork",
          len(thumb_icons) >= 70 and "cow" not in thumb_icons,
          f"({len(thumb_icons)} cards, {len(set(thumb_icons))} sprites)")

    # -- shop sorting -----------------------------------------------------
    status, asc = get("/shop?sort=price-asc")
    status2, desc = get("/shop?sort=price-desc")
    def first_price(markup):
        m = re.search(r'<span class="price">\$([\d.]+)', markup)
        return float(m.group(1)) if m else -1.0
    check("price sort ascending", 0 < first_price(asc) <= first_price(desc))
    check("sort control keeps the choice",
          'value="price-asc" selected' in asc)
    status, deals = get("/shop?sort=deal")
    check("deal sort renders", status == 200 and "Biggest savings" in deals)
    status, bad = get("/shop?sort=bogus")
    check("unknown sort falls back to featured",
          status == 200 and 'value="featured" selected' in bad)

    # -- whole cow campaigns -----------------------------------------------
    expect_page("/campaigns", "cow", "campaigns")
    status, body = get("/campaigns")
    match = re.search(r'href="/campaign/([a-z0-9-]+)"', body)
    if match:
        slug = match.group(1)
        status, body = get(f"/campaign/{slug}")
        check("campaign page renders", status == 200 and "Households" in body)
        token = csrf_from(body)
        if token:
            email = "campaign-smoke@example.com"
            status, body = post(f"/campaign/{slug}/join", {
                "_csrf": token, "name": "Smoke household",
                "email": email, "phone": "5025550000", "note": ""},
                follow=False)
            status, body = get(f"/campaign/{slug}")
            check("campaign join accepted", "place is held" in body.lower()
                  or "already holds" in body.lower())
            token = csrf_from(body)
            status, body = post(f"/campaign/{slug}/join", {
                "_csrf": token, "name": "Smoke household again",
                "email": email, "phone": "5025550000"}, follow=False)
            status, body = get(f"/campaign/{slug}")
            check("one place per household", "already holds" in body.lower())
    expect_page("/how-it-works", "How buying", "how it works")
    expect_page("/market-prices", "grocery", "market prices")
    status, body = get("/campaigns")
    check("cow drops are named consistently", "<h1>Cow drops</h1>" in body)
    status, body = get("/shop?q=jerky")
    check("per-each cut cards price each", "each</small>" in body)
    status, body = get("/cut/beef-jerky")
    check("per-each cut page says each",
          "Priced each." in body and "lb per each" not in body)
    expect_page("/terms", "Terms", "terms")
    expect_page("/policy", "Shop policy", "policy")
    expect_page("/contact", "Contact", "contact")
    expect_page("/orders", "Find your order", "order lookup")
    status, _ = get("/definitely-not-a-page")
    check("404 renders", status == 404, f"(status {status})")

    # -- isolation: the depot must not move ------------------------------
    status, body = get("/")
    check("no depot leak", "Information Depo" not in body)

    # -- product-only cart: no beef minimum, packing, or grocery-savings claim --
    status, body = get("/fermentation/kombucha-classic")
    token = csrf_from(body)
    ref_match = re.search(r'name="ref" value="(\d+)"', body)
    product_ref = ref_match.group(1) if ref_match else ""
    if token and product_ref:
        status, body = post("/cart/add", {
            "_csrf": token, "type": "product", "ref": product_ref,
            "qty": "1", "name": "Kombucha, Classic",
            "next": "/cart"})
        status, body = get("/cart")
        check("single fermented product can reach checkout",
              "Kombucha, Classic" in body and "Continue to checkout" in body
              and "order minimum" not in body.lower())
        check("product-only cart hides beef packing and savings",
              "Under the grocery shelf" not in body
              and "Customize packing for the whole order" not in body)
        token = csrf_from(body)
        post("/cart/clear", {"_csrf": token})

    # -- cart flow ---------------------------------------------------------
    status, body = get("/shop")
    token = csrf_from(body)
    check("csrf token on shop", bool(token))
    match = re.search(
        r'name="type" value="cut">\s*<input type="hidden" name="ref" '
        r'value="(\d+)"', body)
    if not match:
        matches = re.findall(r'name="ref" value="(\d+)"', body)
        ref = matches[0] if matches else ""
    else:
        ref = match.group(1)
    check("a cut id found for cart test", bool(ref))
    if ref and token:
        # Enough pounds to clear the $99 minimum order, so the checkout is
        # actually reachable.
        status, body = post("/cart/add", {
            "_csrf": token, "type": "cut", "ref": ref, "qty": "8",
            "name": "Smoke test cut", "next": "/cart"})
        check("add to cart", 'class="count"' in body or "cart" in body.lower())
        status, body = get("/cart")
        check("cart page shows a line", "Your cart" in body
              and "cart-line" in body, "(item missing)")
        check("cart shows savings", "saves" in body or "Under the grocery shelf"
              in body or "under the shelf price" in body)
        check("cart counts lines, not pounds", "1 item &middot;" in body)
        check("cart is noindex",
              'name="robots" content="noindex"' in body)
        status, body = get("/shop")
        match = re.search(r'id="cart-count">(\d+)<', body)
        check("cart badge counts lines", bool(match) and match.group(1) == "1",
              f"(badge {match.group(1) if match else 'missing'})")
        status, body = get("/fermentation/kombucha-classic")
        token = csrf_from(body)
        product_match = re.search(r'name="ref" value="(\d+)"', body)
        product_ref = product_match.group(1) if product_match else ""
        if token and product_ref:
            post("/cart/add", {"_csrf": token, "type": "product",
                                "ref": product_ref, "qty": "1",
                                "name": "Kombucha, Classic", "next": "/cart"})
            status, body = get("/cart")
            check("mixed beef and fermentation cart", "Kombucha, Classic" in body
                  and "2 items" in body)

    # -- create the account before checkout, so the order links to it ------
    status, body = get("/account/signup")
    signup_token = csrf_from(body)
    check("signup form renders",
          status == 200 and "Create your account" in body)
    if signup_token:
        status, body = post("/account/signup", {
            "_csrf": signup_token, "name": "Account Smoke",
            "email": ORDER_EMAIL, "phone": "5025550177",
            "password": "smoke-pass-123", "password2": "different-pass"})
        check("signup rejects mismatched passwords",
              status == 200 and "do not match" in body)
        status, body = post("/account/signup", {
            "_csrf": signup_token, "name": "Account Smoke",
            "email": ORDER_EMAIL, "phone": "5025550177",
            "password": "smoke-pass-123", "password2": "smoke-pass-123"})
        check("signup creates and signs in",
              status == 200 and "Hi, Account" in body
              and "Email verified" in body, f"(status {status})")
        check("demo verification is disclosed", "Demo mode" in body)
        check("account pages are noindex",
              'name="robots" content="noindex"' in body)
        # Signing in rotates the CSRF token; refresh before the cart POSTs.
        status, body = get("/shop")
        token = csrf_from(body)

    # -- line level packing: ground beef comes in packs ---------------------
    status, body = get("/shop?q=ground")
    ground_ref = ""
    matches = re.findall(r'name="ref" value="(\d+)"', body)
    if matches:
        ground_ref = matches[0]
    check("a ground cut found", bool(ground_ref))
    if ground_ref and token:
        status, body = post("/cart/add", {
            "_csrf": token, "type": "cut", "ref": ground_ref, "qty": "2",
            "ground_pack": "lb1", "next": "/cart"})
        status, body = get("/cart")
        check("ground pack size stored on the line", "1 lb packs" in body,
              "(line packing missing)")

    # -- checkout: packing options present ---------------------------------
    status, body = get("/checkout")
    check("checkout renders", status == 200 and "How should it be packed" in body,
          f"(status {status})")
    check("paper wrap offered", "Butcher paper" in body)
    check("vacuum default offered", "Vacuum sealed" in body)
    check("portioning offered", "Portioned 10 oz steaks" in body)
    check("gift wrap offered", "handwritten card" in body)
    check("ground pack sizes offered", "5 lb packs" in body
          or "1 lb packs" in body or "Ground Beef Pack Size" in body)
    check("slot list rendered", "Pickup times" in body and "Delivery windows" in body)
    check("terms checkbox", "terms of service" in body)
    check("demo badge on mock payments", "no card is charged" in body)

    # -- checkout validation: empty submit fails politely ------------------
    token = csrf_from(body) or token
    if token:
        status, body = post("/checkout", {"_csrf": token})
        check("checkout rejects empty submit",
              "Tell us who to expect" in body or "Choose pickup" in body)

    # -- full happy-path order ---------------------------------------------
    code = ""
    status, body = get("/checkout")
    token = csrf_from(body)
    slot = ""
    match = re.search(r'name="slot" value="(\d+)"', body)
    if match:
        slot = match.group(1)
    if token and ref and slot:
        fields = {
            "_csrf": token, "wrap": "paper", "portioning": "steak_10",
            "bagging": "bulk", "gift": "no", "labeling": "standard",
            "fulfillment": "pickup", "slot": slot,
            "name": "Smoke Tester", "email": ORDER_EMAIL,
            "phone": "5025551234", "card": "4242 4242 4242 4242",
            "exp": "12/29", "cvc": "123", "terms": "on",
            "notes": "smoke order", "subscribe": "monthly",
        }
        status, body = post("/checkout", fields)
        match = re.search(r"/order/(RB-[A-Z0-9]+)", body)
        code = match.group(1) if match else ""
        check("order placed and receipt shown", bool(code), "(no order code)")
        if code:
            status, body = get(f"/order/{code}")
            check("receipt renders", status == 200 and code in body)
            check("receipt shows packing choices", "Packing" in body)
            check("receipt shows savings", "Under the grocery shelf" in body)
            check("receipt is honest about demo payment",
                  "No payment was charged" in body and "Keep this page" in body)
            check("receipt drops false email promises",
                  "confirmation at" not in body)
            check("receipt is noindex",
                  'name="robots" content="noindex"' in body)
            status, body = get(f"/order/{code}.ics")
            check("ics calendar file", status == 200
                  and body.startswith("BEGIN:VCALENDAR"))

    # -- subscription management -------------------------------------------
    status, body = get("/manage")
    token = csrf_from(body)
    if token:
        status, body = post("/manage", {"_csrf": token,
                                        "email": ORDER_EMAIL})
        match = re.search(r"/manage/([A-Za-z0-9_-]{8,})", body)
        if match:
            manage_token = match.group(1)
            status, body = get(f"/manage/{manage_token}")
            check("manage page renders", status == 200
                  and "Your subscription" in body)
            token2 = csrf_from(body)
            status, body = post(f"/manage/{manage_token}",
                                {"_csrf": token2, "action": "skip", "sub": "1"})
            check("skip works", status in (200, 303))
        else:
            # redirect happened; follow manually
            check("manage email lookup responded", status in (200, 303))

    # -- admin console ------------------------------------------------------
    status, body = get("/admin/login")
    check("admin login page", status == 200 and "Owner login" in body)
    status, body = get("/admin/pricing")
    check("admin requires login", "Owner login" in body or status == 303)

    if ADMIN_PASSWORD:
        status, body = get("/admin/login")
        token = csrf_from(body)
        status, body = post("/admin/login", {
            "_csrf": token, "username": ADMIN_USER,
            "password": ADMIN_PASSWORD})
        status, body = get("/admin")
        check("admin dashboard", status == 200 and "Pricing" in body
              and "<h1>" in body and
              'name="robots" content="noindex"' in body,
              f"(status {status})")
        for path, needle in (("/admin/pricing", "Pricing console"),
                             ("/admin/integrity", "Integrity"),
                             ("/admin/market", "Market"),
                             ("/admin/orders", "Orders")):
            status, body = get(path)
            check(f"admin {path}", status == 200 and needle.lower() in
                  body.lower(), f"(status {status})")

        status, body = get("/admin/products?store=fermentation")
        check("admin product console lists Fermentation Station",
              status == 200 and "Kombucha, Classic" in body
              and 'name="robots" content="noindex"' in body)
        status, body = get("/admin/access")
        check("full admin can manage store access",
              status == 200 and "Add an admin" in body)

        # Exercise a store-scoped admin separately so the owner session stays
        # available for the remaining console checks.
        token = csrf_from(body)
        scoped_user = f"ferm-smoke-{STAMP}"
        status, body = post("/admin/access/new", {
            "_csrf": token, "username": scoped_user,
            "password": "smoke-access-password-123",
            "store_slug": "fermentation"})
        check("create a store-scoped admin", status == 200
              and scoped_user in body)
        owner_jar, owner_opener, owner_plain = jar, opener, plain_opener
        jar = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
        plain_opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(jar), NoRedirect)
        status, body = get("/admin/login")
        token = csrf_from(body)
        status, body = post("/admin/login", {
            "_csrf": token, "username": scoped_user,
            "password": "smoke-access-password-123"})
        check("scoped admin signs in", status == 200
              and "Fermentation Station" in body)
        status, body = get("/admin/products?store=freeze-dried")
        check("scoped admin is limited to assigned store",
              status == 200 and "Kombucha, Classic" in body
              and "Freeze-Dried Sweet Corn" not in body)
        status, body = get("/admin/access")
        check("scoped admin cannot edit access grants",
              status == 200 and "Add an admin" not in body)
        try:
            plain_opener.open(BASE + "/admin/pricing", timeout=20)
            pricing_status = 200
        except urllib.error.HTTPError as exc:
            pricing_status = exc.code
        check("scoped admin cannot edit beef pricing", pricing_status == 303)
        jar, opener, plain_opener = owner_jar, owner_opener, owner_plain
        status, body = get("/admin/access")
        scoped_match = re.search(
            rf'<h2[^>]*>{re.escape(scoped_user)}</h2>.*?name="admin_id" value="(\d+)"',
            body, re.S)
        if scoped_match:
            token = csrf_from(body)
            status, body = post("/admin/access/delete", {
                "_csrf": token, "admin_id": scoped_match.group(1)})
            check("remove temporary scoped admin", status == 200
                  and scoped_user not in body)
        else:
            check("remove temporary scoped admin", False)

        # Multipart image upload, price edit, and soft delete from the GUI.
        status, body = get("/admin/products/new?store=fermentation")
        token = csrf_from(body)
        image_buffer = io.BytesIO()
        Image.new("RGB", (3, 2), (30, 140, 90)).save(image_buffer, format="PNG")
        test_slug = f"smoke-upload-{STAMP}"
        test_name = f"Smoke Upload Item {STAMP}"
        status, body = post_multipart("/admin/products/new", {
            "_csrf": token, "store_slug": "fermentation", "slug": test_slug,
            "name": test_name, "kind": "item", "unit": "jar",
            "price": "3.25", "compare_at": "0", "compare_brand": "",
            "compare_size": "", "compare_url": "", "compare_observed_at": "",
            "unit_lbs": "0", "stock": "5", "blurb": "Upload test item",
            "serving": "One jar", "tags": "smoke", "sort_order": "999",
        }, {"image": ("smoke.png", "image/png", image_buffer.getvalue())})
        check("admin product image upload creates item",
              status == 200 and test_name in body)
        status, product_page = get(f"/fermentation/{test_slug}")
        image_match = re.search(r'src="(/static/img/uploads/[^\"]+)"', product_page)
        uploaded_url = image_match.group(1) if image_match else ""
        asset_status, _ = get(uploaded_url) if uploaded_url else (404, "")
        check("uploaded product image is served",
              status == 200 and asset_status == 200)
        product_id_match = re.search(
            rf'<tr>\s*<td>{re.escape(test_name)}.*?href="/admin/products/(\d+)/edit"',
            body, re.S)
        product_id = product_id_match.group(1) if product_id_match else ""
        if product_id:
            status, edit_body = get(f"/admin/products/{product_id}/edit")
            token = csrf_from(edit_body)
            status, body = post_multipart(f"/admin/products/{product_id}/edit", {
                "_csrf": token, "store_slug": "fermentation", "slug": test_slug,
                "name": test_name, "kind": "item", "unit": "jar",
                "price": "4.75", "compare_at": "0", "compare_brand": "",
                "compare_size": "", "compare_url": "", "compare_observed_at": "",
                "unit_lbs": "0", "stock": "5", "blurb": "Upload test item",
                "serving": "One jar", "tags": "smoke", "sort_order": "999",
                "active": "on",
            })
            check("admin changes product price", status == 200 and "$4.75" in body)
            token = csrf_from(body)
            post(f"/admin/products/{product_id}/delete", {"_csrf": token})
            status, _ = get(f"/fermentation/{test_slug}")
            check("admin deactivates product", status == 404)
        else:
            check("uploaded item appears in admin product list", False)

        # Preview a repricing, then apply it, then revert it.
        status, body = get("/admin/pricing?scope=tag&value=ground")
        token = csrf_from(body)
        fields = {"_csrf": token, "scope": "tag", "value": "ground",
                  "kind": "rake", "discount": "25", "confirm": "yes"}
        status, body = post("/admin/pricing/preview", fields)
        status, body = get("/admin/pricing?scope=tag&value=ground")
        check("pricing preview shows rows", "Preview" in body
              and "Ground" in body, "(preview missing)")
        status, body = post("/admin/pricing/apply", fields)
        status, body = get("/admin/pricing")
        check("pricing apply recorded", "Repriced" in body
              or "audit" in body.lower())
        audit = ""
        match = re.search(r'name="audit" value="(\d+)"', body)
        if match:
            audit = match.group(1)
        check("audit id offered for revert", bool(audit))
        if audit:
            token = csrf_from(body)
            status, body = post("/admin/pricing/revert",
                                {"_csrf": token, "audit": audit})
            status, body = get("/admin/pricing")
            check("pricing revert works", "reverted" in body.lower()
                  or "Reverted" in body)

    # -- customer accounts -------------------------------------------------
    status, body = get("/account/logout")
    check("logout is POST only", status == 404)
    status, body = get("/account")
    check("account dashboard renders for the signed-in customer",
          status == 200 and "Hi, Account" in body
          and "Email verified" in body, f"(status {status})")
    if code:
        check("the order is linked to the account", code in body,
              "(order missing from dashboard)")
    status, body = get("/account/preferences")
    check("preferences form renders",
          status == 200 and "Preferred day of the month" in body)
    token = csrf_from(body)
    if token:
        status, body = post("/account/preferences", {
            "_csrf": token, "fulfillment": "delivery",
            "line1": "123 Barn Rd", "line2": "",
            "city": "Shelbyville", "state": "KY", "zip": "40065",
            "county": "Shelby",
            "delivery_notes": "Blue cooler by the door",
            "recurring_day": "12", "contact_method": "text"})
        check("preferences save", "Preferences saved" in body)
        status, body = get("/account/preferences")
        check("preferences persist",
              'value="123 Barn Rd"' in body and "Blue cooler" in body
              and 'value="12" selected' in body)

    status, body = get("/shop")
    token = csrf_from(body)
    if token and ref:
        post("/cart/add", {"_csrf": token, "type": "cut", "ref": ref,
                           "qty": "8", "next": "/cart"})
    status, body = get("/checkout")
    check("checkout prefills the saved address",
          status == 200 and 'value="123 Barn Rd"' in body,
          f"(status {status})")

    status, body = get("/account/profile")
    token = csrf_from(body)
    if token:
        status, body = post("/account/profile", {
            "_csrf": token, "name": "Account Smoke",
            "email": ACCOUNT_EMAIL, "phone": "5025550177",
            "current_password": "smoke-pass-123"})
        check("email change works",
              status == 200 and ACCOUNT_EMAIL in body)
        status, body = get("/account")
        check("standing order follows the email change",
              "Standing order" in body and ACCOUNT_EMAIL in body)

    status, body = get("/account/password")
    token = csrf_from(body)
    if token:
        status, body = post("/account/password", {
            "_csrf": token, "current_password": "smoke-pass-123",
            "password": "smoke-pass-456",
            "password2": "smoke-pass-456"})
        check("password change works", "Password changed" in body)

    status, body = get("/account/orders")
    check("order history renders",
          status == 200 and (code in body if code else True),
          "(order missing from history)")

    status, body = get("/account")
    token = csrf_from(body)
    if token:
        status, body = post("/account/logout", {"_csrf": token})
        check("logout returns to the store",
              status == 200 and 'href="/account/login"' in body)
    status, body = get("/account")
    check("signed-out account redirects to login",
          status == 200 and 'action="/account/login"' in body)
    status, body = get("/account/signup")
    check("signup is still offered to guests",
          status == 200 and "Create your account" in body)

    status, body = get("/account/login")
    token = csrf_from(body)
    if token:
        status, body = post("/account/login", {
            "_csrf": token, "email": ACCOUNT_EMAIL,
            "password": "not-the-password"})
        check("wrong password is rejected",
              status == 200 and "do not match" in body)
        status, body = post("/account/login", {
            "_csrf": token, "email": ACCOUNT_EMAIL,
            "password": "smoke-pass-456"})
        check("login with the new password works",
              status == 200 and "Hi, Account" in body)
    status, body = get("/account/orders")
    check("order history survives the email change",
          status == 200 and (code in body if code else True),
          "(order missing after email change)")

    print(f"\n{PASS} passed, {FAIL} failed")
    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
