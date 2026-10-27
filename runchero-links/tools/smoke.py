#!/usr/bin/env python3
"""End-to-end checks against a running Runchero Links server."""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request


def fetch(base: str, path: str, data: dict | None = None):
    body = None
    headers = {"Accept": "text/html"}
    if data is not None:
        body = urllib.parse.urlencode(data).encode()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    request = urllib.request.Request(base + path, data=body, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status, dict(response.headers), response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers), exc.read().decode("utf-8", "replace")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="http://127.0.0.1:8091")
    args = parser.parse_args()
    base = args.base.rstrip("/")
    failures = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        print(("ok   " if condition else "FAIL ") + name + ((" — " + detail) if detail and not condition else ""))
        if not condition:
            failures.append(name)

    status, headers, body = fetch(base, "/")
    check("home responds 200", status == 200, str(status))
    check("home shows converter", "Convert a link" in body)
    check("home shows search", "Search Amazon" in body)
    check("home shows estimator", "What could this earn?" in body)
    check("CSP header present", "Content-Security-Policy" in headers)
    check("nosniff header", headers.get("X-Content-Type-Options") == "nosniff")
    check("no-referrer header", headers.get("Referrer-Policy") == "no-referrer")

    status, _, body = fetch(base, "/how")
    check("how responds 200", status == 200, str(status))
    check("how explains tagging", "Add the tag" in body)

    status, headers, body = fetch(base, "/healthz")
    check("health responds 200", status == 200, str(status))
    try:
        check("health is json ok", json.loads(body).get("ok") is True)
    except ValueError:
        check("health is json ok", False, body[:80])

    sample = "https://www.amazon.com/Some-Name/dp/B08N5WRWNW/ref=abc?th=1"
    status, _, body = fetch(base, "/convert", {"urls": sample})
    check("convert responds 200", status == 200, str(status))
    match = re.search(r'class="result-url"[^>]*value="([^"]+)"', body)
    affiliate = match.group(1) if match else ""
    check("converted product link", affiliate == "https://www.amazon.com/dp/B08N5WRWNW?tag=runchero-20", affiliate)
    check("tracking removed", "ref=abc" not in affiliate, affiliate)

    status, _, body = fetch(base, "/convert", {"urls": "https://example.com/dp/B08N5WRWNW"})
    check("rejects non-amazon", status == 200 and "Only Amazon links" in body)

    status, _, body = fetch(base, "/api/convert", {"urls": sample})
    try:
        payload = json.loads(body)
        check("api convert ok", status == 200 and payload["converted"] == 1, body[:120])
    except (ValueError, KeyError):
        check("api convert ok", False, body[:120])

    status, _, body = fetch(base, "/api/search?" + urllib.parse.urlencode({"q": "canning jars"}))
    try:
        payload = json.loads(body)
        check("api search ok", status == 200 and "canning%20jars" in payload["affiliate_url"], body[:120])
    except (ValueError, KeyError):
        check("api search ok", False, body[:120])

    status, _, _ = fetch(base, "/no-such-page")
    check("404 for missing page", status == 404, str(status))

    status, headers, _ = fetch(base, "/static/css/links.css")
    check("stylesheet served", status == 200 and "text/css" in headers.get("Content-Type", ""))

    print()
    if failures:
        print(f"{len(failures)} check(s) failed")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
