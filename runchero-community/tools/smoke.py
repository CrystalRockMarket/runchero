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
PORT = 8094
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
            return (response.status, response.geturl(), dict(response.headers),
                    response.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as exc:
        return (exc.code, exc.geturl(), dict(exc.headers),
                exc.read().decode("utf-8", "replace"))


def csrf_from(html: str) -> str:
    match = re.search(r'name="_csrf" value="([^"]+)"', html)
    return match.group(1) if match else ""


def listing_form(token: str, **overrides) -> dict:
    data = {
        "_csrf": token,
        "name": "Smoke Test Neighbour",
        "category": "Skills & Help",
        "description": "A test neighbour created by the smoke test and deleted afterwards.",
        "location": "South Runchero",
        "submitter_contact": "private@example.com",
        "phone": "555 0199",
        "email": "smoke@example.com",
        "facebook": "@smoke.apiary",
        "instagram": "",
        "website": "smoke.example.com",
        "address": "",
        "custom_label_1": "Signal",
        "custom_value_1": "555 0188",
        "custom_label_2": "",
        "custom_value_2": "",
        "custom_label_3": "",
        "custom_value_3": "",
        "company": "",
    }
    data.update(overrides)
    return data


def main() -> int:
    failures = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        print(("ok   " if condition else "FAIL ") + name
              + ((" — " + detail) if detail and not condition else ""))
        if not condition:
            failures.append(name)

    tmp = tempfile.mkdtemp(prefix="community-smoke-")
    env = dict(os.environ)
    env.update({
        "RDIR_HOST": HOST,
        "RDIR_PORT": str(PORT),
        "RDIR_DB_PATH": str(Path(tmp) / "community.db"),
        "RDIR_DATA_DIR": tmp,
        "RDIR_PID_PATH": str(Path(tmp) / "smoke.pid"),
        "RDIR_LOG_PATH": str(Path(tmp) / "smoke.log"),
        "RDIR_ADMIN_PASSWORD": PASSWORD,
        "RDIR_SUBMISSIONS_PER_HOUR": "100",
    })
    server = subprocess.Popen(
        [sys.executable, "run.py", "--host", HOST, "--port", str(PORT)],
        cwd=str(ROOT), env=env, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True,
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
            print(server.stdout.read() if server.stdout else "")
            print("server failed to start")
            return 1

        status, _, headers, body = fetch(opener, "/")
        check("home responds 200", status == 200, str(status))
        check("home has directory heading", "Neighbours" in body)
        check("empty directory message", "The directory is empty" in body)
        check("excluded earth.love absent", "earth.love" not in body.lower())
        check("excluded games-earth absent", "games-earth" not in body.lower())
        check("CSP header present", "Content-Security-Policy" in headers)
        check("nosniff header", headers.get("X-Content-Type-Options") == "nosniff")

        status, _, headers, _ = fetch(opener, "/static/img/icons/chat.png")
        check("icon served", status == 200 and headers.get("Content-Type") == "image/png",
              str(status))
        status, _, headers, _ = fetch(opener, "/static/css/community.css")
        check("styles served", status == 200 and "text/css" in headers.get("Content-Type", ""),
              str(status))

        status, _, _, form = fetch(opener, "/add")
        check("add form responds 200", status == 200, str(status))
        check("add form explains lock", "locked" in form.lower())
        token = csrf_from(form)
        check("add form has csrf", bool(token))

        status, _, _, body = fetch(opener, "/add", listing_form(
            token, phone="", email="", facebook="", website="",
            custom_value_1="",
        ))
        check("listing without contact rejected",
              status == 400 and "Please fix this" in body, str(status))

        status, _, _, body = fetch(opener, "/add", listing_form(token, _csrf="bad"))
        check("bad csrf rejected", status == 400, str(status))

        status, final, _, body = fetch(opener, "/add", listing_form(token))
        match = re.search(r"/added/(\d+)", final)
        check("valid listing accepted", status == 200 and bool(match), final)
        check("confirmation says locked", "locked" in body.lower())
        entry_id = match.group(1) if match else "0"

        status, _, _, body = fetch(opener, f"/entry/{entry_id}")
        check("public detail responds 200", status == 200, str(status))
        check("detail shows name", "Smoke Test Neighbour" in body)
        check("detail shows phone", "555 0199" in body)
        check("detail has mailto link", "mailto:smoke@example.com" in body)
        check("detail has facebook link", "facebook.com/smoke.apiary" in body)
        check("private contact hidden publicly", "private@example.com" not in body)

        status, _, _, body = fetch(opener, "/?q=Smoke+Test")
        check("search finds listing", "Smoke Test Neighbour" in body)
        status, _, _, body = fetch(opener, "/?category=Skills+%26+Help")
        check("filters find listing", "Smoke Test Neighbour" in body)
        status, _, _, _ = fetch(opener, "/entry/99999")
        check("missing listing is 404", status == 404, str(status))

        status, _, _, body = fetch(opener, "/add", listing_form(
            token, name="Bot Listing", company="spam"))
        status2, _, _, _ = fetch(opener, "/?q=Bot+Listing")
        check("honeypot submission ignored", "Bot Listing" not in body, str(status))

        status, final, _, body = fetch(opener, "/admin")
        check("admin requires login", status == 200 and "/admin/login" in final
              and "Admin sign in" in body, final)
        status, _, _, body = fetch(opener, "/admin/login")
        login_token = csrf_from(body)
        status, _, _, body = fetch(opener, "/admin/login", {
            "_csrf": login_token, "user": "runchero", "password": "wrong"})
        check("bad password rejected", status == 401 and "did not match" in body,
              str(status))

        status, final, _, body = fetch(opener, "/admin/login", {
            "_csrf": login_token, "user": "runchero", "password": PASSWORD})
        check("admin login works", status == 200 and "/admin" in final
              and "People in the directory" in body, final)
        check("admin sees submitter contact", "private@example.com" in body)
        admin_token = csrf_from(body)

        status, final, _, body = fetch(
            opener, f"/admin/entries/{entry_id}/publish", {"_csrf": admin_token})
        check("hide listing works", status == 200 and "Hidden" in body
              and "Visibility changed" in body, final)

        anon = build_opener()
        status, _, _, body = fetch(anon, "/?q=Smoke+Test")
        check("hidden listing absent from public", "Smoke Test Neighbour" not in body)
        status, _, _, _ = fetch(anon, f"/entry/{entry_id}")
        check("hidden listing public detail 404", status == 404, str(status))

        status, _, _, form = fetch(opener, f"/admin/entries/{entry_id}/edit")
        check("edit form responds 200", status == 200, str(status))
        edit_token = csrf_from(form)

        status, final, _, body = fetch(
            opener, f"/admin/entries/{entry_id}",
            listing_form(edit_token, name="Smoke Test Neighbour Updated",
                         admin_note="Smoke checked", published="1"),
        )
        check("edit saves changes", status == 200 and "Listing updated" in body
              and "Smoke Test Neighbour Updated" in body, final)

        status, _, _, body = fetch(opener, f"/entry/{entry_id}")
        check("edited listing is public", status == 200
              and "Smoke Test Neighbour Updated" in body, str(status))

        status, final, _, body = fetch(
            opener, f"/admin/entries/{entry_id}/delete", {"_csrf": admin_token})
        check("delete works", status == 200 and "Listing deleted" in body
              and "Smoke Test Neighbour Updated" not in body, final)

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
