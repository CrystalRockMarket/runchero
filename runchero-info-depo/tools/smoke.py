#!/usr/bin/env python3
"""Smoke test the running depot.

Start the server first, then:

    python3 tools/smoke.py                # default http://127.0.0.1:8080
    python3 tools/smoke.py --base http://127.0.0.1:9000
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request

RAW_LINK = re.compile(r"\[\[[^\]]+\]\]")
BROKEN_LINK = re.compile(r'<span class="wikilink missing">')

CHECKS: list[tuple[str, str, int]] = [
    ("/", "home", 200),
    ("/grow", "grow depots", 200),
    ("/grow/tomato", "tomato depot", 200),
    ("/grow/potato", "potato depot", 200),
    ("/animals", "animal depots", 200),
    ("/animals/cattle", "cattle depot", 200),
    ("/animals/honey-bee", "honey bee depot", 200),
    ("/farm", "farm shelves", 200),
    ("/farm?q=soil", "farm filter", 200),
    ("/workshop", "workshop shelves", 200),
    ("/workshop?sort=name", "workshop sort", 200),
    ("/survival", "survival shelves", 200),
    ("/home", "home shelves", 200),
    ("/kitchen", "kitchen shelves", 200),
    ("/collections", "topic depots", 200),
    ("/topic/kitchen", "kitchen depot", 200),
    ("/topic/farm", "farm depot", 200),
    ("/topic/workshop", "workshop depot", 200),
    ("/vehicles", "machine index", 200),
    ("/repair", "repair library", 200),
    ("/vehicles?type=tractor", "tractor brands", 200),
    ("/vehicles?type=tractor&make=Ford", "Ford models", 200),
    ("/repair?type=chainsaw", "chainsaw brands", 200),
    ("/repair?type=chainsaw&make=STIHL", "STIHL placeholder", 200),
    ("/repair?type=hand-tools&make=Stanley", "tool brand placeholder", 200),
    ("/repair?type=combine", "combine brands", 200),
    ("/vehicles/ford-3000", "machine", 200),
    ("/library", "library", 200),
    ("/library/archive", "archive", 200),
    ("/library/archive?cat=lib-manuals", "manual shelf", 200),
    ("/library/archive/ford-manual-ford-2000-4000-shop-manual-supp-1963", "manual book", 200),
    ("/read/ford-manual-ford-2000-4000-shop-manual-supp-1963", "manual reader", 200),
    ("/sources", "sources", 200),
    ("/sources?kind=manual", "manual sources", 200),
    ("/sources?kind=book", "book sources", 200),
    ("/sources?kind=ai-organized", "index sources", 200),
    ("/sources?q=ford&kind=manual", "manual search", 200),
    ("/sources?q=engines", "source search", 200),
    ("/vehicles/ford-2000", "Ford vehicle", 200),
    ("/search?q=ford&source=manual", "source search", 200),
    ("/library/archive/farm-mechanics", "book", 200),
    ("/library/community", "old community redirect", 200),
    ("/library/submit", "old submit redirect", 200),
    ("/section/growing", "old shelf redirect", 200),
    ("/formulas", "formulas", 200),
    ("/conversions", "conversions", 200),
    ("/hub/wheat", "wheat hub redirect", 200),
    ("/hub/cattle", "cattle hub redirect", 200),
    ("/hub/ford-tractors", "Ford tractor topic", 200),
    ("/topic/electrical", "electrical depot", 200),
    ("/formulas?topic=kitchen", "formulas by topic", 200),
    ("/formulas?topic=advanced-maths", "advanced maths", 200),
    ("/formulas?q=torque", "formulas search", 200),
    ("/search?q=soil", "search", 200),
    ("/search?q=stock&kind=formula", "formula search", 200),
    ("/read/farm-mechanics", "reader", 200),
    ("/download/farm-mechanics", "download", 200),
    ("/api/search?q=soil", "api search", 200),
    ("/api/stats", "api stats", 200),
    ("/robots.txt", "robots", 200),
    ("/manifest.webmanifest", "manifest", 200),
    ("/sw.js", "service worker", 200),
    ("/static/css/pixel.css", "stylesheet", 200),
    ("/static/js/app.js", "script", 200),
    ("/static/img/logo.png", "logo", 200),
    ("/static/img/icons/cow.png", "icon", 200),
    ("/static/img/covers/farm-mechanics.png", "cover", 200),
    ("/grow/does-not-exist", "missing depot", 404),
    ("/library/archive/does-not-exist", "missing book", 404),
]

# Pages whose wiki links are checked for dead ends, not just for a status code.
LINK_PAGES = [
    "/grow/tomato",
    "/animals/cattle",
    "/topic/kitchen",
    "/topic/farm",
    "/library",
    "/formulas",
    "/formulas?q=torque",
    "/formulas?topic=workshop",
    "/formulas?topic=advanced-maths",
    "/conversions",
    "/hub/wheat",
    "/hub/ford-tractors",
    "/search?q=stock&kind=formula",
]


def get(base: str, path: str, method: str = "GET"):
    request = urllib.request.Request(base + path, method=method)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as error:
        return error.code, error.read()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Smoke test the depot")
    parser.add_argument("--base", default="http://127.0.0.1:8080")
    args = parser.parse_args(argv)
    base = args.base.rstrip("/")

    failures = 0
    for path, label, expected in CHECKS:
        status, body = get(base, path)
        mark = "ok " if status == expected else "FAIL"
        if status != expected:
            failures += 1
        print(f"  {mark} {status:>3}  {label:<18} {path}")

    status, body = get(base, "/api/stats")
    stats = json.loads(body)
    print(f"  stats: {stats}")
    if not stats.get("collections") or not stats.get("books"):
        print("  FAIL  the depot is empty")
        failures += 1

    status, body = get(base, "/library/submit", method="POST")
    print(f"  {'ok ' if status == 405 else 'FAIL'} {status:>3}  post is refused")
    if status != 405:
        failures += 1

    for path in LINK_PAGES:
        status, body = get(base, path)
        page = body.decode("utf-8", "replace")
        raw = RAW_LINK.findall(page)
        broken = BROKEN_LINK.findall(page)
        ok = status == 200 and not raw and not broken
        if not ok:
            failures += 1
        detail = ""
        if raw:
            detail = f" {len(raw)} unrendered"
        if broken:
            detail += f" {len(broken)} dead"
        print(f"  {'ok ' if ok else 'FAIL'} {status:>3}  links{'':<11} {path}{detail}")

    print(f"\n{'all good' if not failures else f'{failures} failure(s)'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
