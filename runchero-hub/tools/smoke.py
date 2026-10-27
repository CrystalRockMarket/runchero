#!/usr/bin/env python3
"""End-to-end checks using a throwaway database and port."""
from __future__ import annotations

import http.cookiejar
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOST = "127.0.0.1"
PORT = 8095
BASE = f"http://{HOST}:{PORT}"
PASSWORD = "smoke-pass"


def build_opener() -> urllib.request.OpenerDirector:
    jar = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))


def fetch(opener, path: str, data: dict | None = None):
    body = None
    headers = {}
    if data is not None:
        body = urllib.parse.urlencode(data).encode()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    request = urllib.request.Request(BASE + path, data=body, headers=headers)
    try:
        with opener.open(request, timeout=10) as response:
            return response.status, response.geturl(), dict(response.headers), response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.geturl(), dict(exc.headers), exc.read().decode("utf-8", "replace")


def csrf_from(html: str) -> str:
    match = re.search(r'name="_csrf" value="([^"]+)"', html)
    return match.group(1) if match else ""


def main() -> int:
    failures = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        print(("ok   " if condition else "FAIL ") + name + ((" — " + detail) if detail and not condition else ""))
        if not condition:
            failures.append(name)

    tmp = tempfile.mkdtemp(prefix="hub-smoke-")
    env = dict(os.environ)
    env.update({
        "RHUB_HOST": HOST,
        "RHUB_PORT": str(PORT),
        "RHUB_DB_PATH": str(Path(tmp) / "hub.db"),
        "RHUB_DATA_DIR": tmp,
        "RHUB_ADMIN_PASSWORD": PASSWORD,
        "RHUB_SUBMISSIONS_PER_HOUR": "100",
    })
    server = subprocess.Popen(
        [sys.executable, "run.py", "--host", HOST, "--port", str(PORT)],
        cwd=str(ROOT),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    opener = build_opener()
    try:
        for _ in range(80):
            if server.poll() is not None:
                break
            try:
                status, _, _, _ = fetch(opener, "/healthz")
                if status == 200:
                    break
            except Exception:
                pass
            time.sleep(0.2)
        if server.poll() is not None:
            output = server.stdout.read() if server.stdout else ""
            print(output)
            print("server failed to start")
            return 1

        status, _, headers, body = fetch(opener, "/")
        check("home responds 200", status == 200, str(status))
        check("home lists info depo", "Runchero Information Depo" in body)
        check("home lists shop", "Runchero Beef" in body)
        check("home lists hub links tool", "Runchero Links" in body)
        check("home shows request CTA", "Request a new app" in body)
        check("excluded earth.love absent", "earth.love" not in body.lower())
        check("excluded games-earth absent", "games-earth" not in body.lower())
        check("CSP header present", "Content-Security-Policy" in headers)
        check("nosniff header", headers.get("X-Content-Type-Options") == "nosniff")

        status, _, headers, _ = fetch(opener, "/static/img/shots/info-depo.png")
        check("screenshot served", status == 200 and headers.get("Content-Type") == "image/png", str(status))

        status, _, _, form = fetch(opener, "/request")
        check("request form responds 200", status == 200, str(status))
        token = csrf_from(form)
        check("request form has csrf", bool(token))

        status, final, _, body = fetch(opener, "/request", {
            "_csrf": token,
            "name": "Smoke Tester",
            "contact": "smoke@example.com",
            "title": "Smoke test idea",
            "category": "Community",
            "description": "A test idea created by the smoke test and deleted afterwards.",
            "website": "",
        })
        check("valid request accepted", status == 200 and "Thanks" in body, str(status))

        status, _, _, body = fetch(opener, "/request", {
            "_csrf": token,
            "name": "",
            "contact": "",
            "title": "x",
            "category": "Community",
            "description": "short",
            "website": "",
        })
        check("invalid request rejected", status == 400 and "Please fix this" in body, str(status))

        status, _, _, login = fetch(opener, "/admin/login")
        login_token = csrf_from(login)
        status, final, _, body = fetch(opener, "/admin/login", {
            "_csrf": login_token,
            "user": "runchero",
            "password": PASSWORD,
        })
        check("admin login works", status == 200 and "/admin" in final and "Community app requests" in body, final)
        check("submitted request visible", "Smoke test idea" in body)

        match = re.search(r'id="request-(\d+)"', body)
        check("request id found", bool(match))
        request_id = match.group(1) if match else "0"
        admin_token = csrf_from(body)

        status, final, _, body = fetch(opener, f"/admin/requests/{request_id}/status", {
            "_csrf": admin_token,
            "status": "planned",
            "admin_note": "Smoke checked",
        })
        check("status update works", status == 200 and "Request updated" in body and "Planned" in body, final)

        status, final, _, body = fetch(opener, f"/admin/requests/{request_id}/delete", {
            "_csrf": admin_token,
        })
        check("delete works", status == 200 and "Request deleted" in body and "Smoke test idea" not in body, final)

        status, _, _, body = fetch(opener, "/healthz")
        check("health still ok", status == 200 and '"ok": true' in body, body[:80])

        status, _, _, _ = fetch(opener, "/no-such-page")
        check("404 for missing page", status == 404, str(status))
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()

    print()
    if failures:
        print(f"{len(failures)} check(s) failed")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
