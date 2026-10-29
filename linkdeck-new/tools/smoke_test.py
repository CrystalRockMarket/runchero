#!/usr/bin/env python3
"""End-to-end smoke test for LinkDeck.

Runs against an isolated temporary SQLite database and never touches the
production DB. Usage:

    source venv/bin/activate
    python tools/smoke_test.py

Exits non-zero on the first failed assertion.
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

_tmp = tempfile.NamedTemporaryFile(prefix="linkdeck_smoke_", suffix=".db", delete=False)
os.environ["LD_DB_PATH"] = _tmp.name
os.environ["LD_ADMIN_PASSWORD"] = "smoke-admin-pass"
os.environ["LD_SECRET_KEY"] = "smoke-secret-key"
os.environ.setdefault("LD_FRONTEND_BASE_URL", "http://testserver")

from fastapi.testclient import TestClient  # noqa: E402

from app.httpd import app  # noqa: E402

FAILS = 0


def check(label: str, condition: bool, detail: str = "") -> None:
    global FAILS
    if condition:
        print(f"  PASS  {label}")
    else:
        FAILS += 1
        print(f"  FAIL  {label} {detail}")


def main() -> int:
    with TestClient(app) as c:
        print("Health & pages")
        check("health", c.get("/health").json().get("ok") is True)
        for path in ("/", "/submit", "/plans", "/login", "/admin"):
            check(f"GET {path}", c.get(path).status_code == 200)
        check("dashboard redirects anon", c.get("/dashboard", follow_redirects=False).status_code == 302)

        print("Deck & submission")
        check("seeded deck", len(c.get("/api/offers").json()) > 0)
        r = c.post(
            "/api/offers",
            json={"brand": "Smoke", "link": "https://example.com/x", "headline": "Test", "category": "Food", "plan": "free"},
        )
        check("anon submit 201", r.status_code == 201, r.text)
        oid = r.json()["id"]
        bad = c.post(
            "/api/offers",
            json={"brand": "X", "link": "not-a-url", "headline": "y", "category": "Food", "plan": "free"},
        )
        check("rejects bad url", bad.status_code == 400)

        print("Tracking & voting")
        check("click", c.post(f"/api/click/{oid}").status_code == 200)
        v = c.post(f"/api/vote/{oid}?is_up=true&voter_key=smoke").json()
        check("vote counts", v.get("upvotes") == 1)
        v2 = c.post(f"/api/vote/{oid}?is_up=true&voter_key=smoke").json()
        check("vote dedup", v2.get("already") is True)
        stats = c.get(f"/api/stats/offer/{oid}").json()
        check("stats clicks", stats.get("clicks") == 1)

        print("Magic link login")
        r = c.post("/auth/magic/send", data={"email": "smoke@example.com"})
        data = r.json()
        check("magic dev link", bool(data.get("dev_link")))
        path = "/" + data["dev_link"].split("//", 1)[1].split("/", 1)[1]
        r = c.get(path, follow_redirects=False)
        check("magic verify redirects", r.status_code == 302)
        check("session cookie set", bool(r.cookies.get("ld_session")))
        check("dashboard authed", c.get("/dashboard", follow_redirects=False).status_code == 200)

        print("Admin")
        r = c.post("/auth/admin/login", data={"password": "smoke-admin-pass"}, follow_redirects=False)
        check("admin login redirect", r.status_code == 302)
        check("admin panel", c.get("/admin/panel", follow_redirects=False).status_code == 200)
        r = c.post(f"/api/admin/offers/{oid}/status", json={"status": "active"})
        check("approve offer", r.status_code == 200 and r.json().get("status") == "active")
        check("admin stats", c.get("/api/admin/stats").status_code == 200)

        print("Security headers")
        headers = c.get("/").headers
        check("CSP", "content-security-policy" in {k.lower() for k in headers})
        check("frame deny", headers.get("x-frame-options") == "DENY")

    try:
        os.unlink(_tmp.name)
    except OSError:
        pass

    print()
    if FAILS:
        print(f"{FAILS} check(s) failed")
        return 1
    print("All checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())