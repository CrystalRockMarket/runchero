"""Administrator authentication for the submission review panel.

Passwords are stored as a PBKDF2 hash in the database. Session cookies are signed
with a local secret and carry an expiry. No third-party auth service is needed.
"""
from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import json
import os
import secrets
import sqlite3
import time
from pathlib import Path

from . import config

COOKIE = "rid_admin"
PBKDF2_ITERATIONS = 260_000


def _meta_get(conn: sqlite3.Connection, key: str) -> str:
    row = conn.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
    return row[0] if row else ""


def hash_password(password: str, salt: bytes | None = None,
                  iterations: int = PBKDF2_ITERATIONS) -> str:
    salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt,
                                 iterations)
    return (f"pbkdf2_sha256${iterations}$"
            f"{base64.urlsafe_b64encode(salt).decode()}$"
            f"{base64.urlsafe_b64encode(digest).decode()}")


def set_password(conn: sqlite3.Connection, password: str) -> None:
    if len(password) < 8:
        raise ValueError("Use at least 8 characters.")
    conn.execute(
        "INSERT INTO meta(key, value) VALUES('admin_password_hash', ?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (hash_password(password),),
    )
    conn.commit()


def configured(conn: sqlite3.Connection) -> bool:
    return bool(config.ADMIN_PASSWORD or _meta_get(conn, "admin_password_hash"))


def verify_password(conn: sqlite3.Connection, password: str) -> bool:
    if config.ADMIN_PASSWORD:
        return hmac.compare_digest(password, config.ADMIN_PASSWORD)
    stored = _meta_get(conn, "admin_password_hash")
    if not stored:
        return False
    try:
        _scheme, iterations, salt_b64, digest_b64 = stored.split("$", 3)
        candidate = hash_password(password,
                                  base64.urlsafe_b64decode(salt_b64.encode()),
                                  int(iterations))
    except (ValueError, TypeError, UnicodeDecodeError, binascii.Error):
        return False
    return hmac.compare_digest(candidate, stored)


def _secret() -> bytes:
    if config.ADMIN_SECRET:
        return config.ADMIN_SECRET.encode("utf-8")
    path = Path(config.DATA_DIR) / "admin.secret"
    if path.exists():
        return path.read_bytes().strip()
    path.parent.mkdir(parents=True, exist_ok=True)
    value = secrets.token_hex(32).encode("ascii")
    path.write_bytes(value)
    try:
        path.chmod(0o600)
    except OSError:
        pass
    return value


def make_session() -> str:
    payload = base64.urlsafe_b64encode(json.dumps({
        "exp": int(time.time()) + config.ADMIN_SESSION_SECONDS,
        "nonce": secrets.token_hex(8),
    }, separators=(",", ":")).encode()).decode().rstrip("=")
    sig = hmac.new(_secret(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}.{sig}"


def verify_session(token: str | None) -> str | None:
    if not token or "." not in token:
        return None
    payload, signature = token.rsplit(".", 1)
    expected = hmac.new(_secret(), payload.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        return None
    try:
        padded = payload + "=" * (-len(payload) % 4)
        data = json.loads(base64.urlsafe_b64decode(padded.encode()))
        if int(data.get("exp", 0)) < int(time.time()):
            return None
    except (ValueError, TypeError, UnicodeDecodeError, json.JSONDecodeError,
            binascii.Error):
        return None
    return token


def csrf_token(session_token: str) -> str:
    return hmac.new(_secret(), b"csrf:" + session_token.encode(),
                    hashlib.sha256).hexdigest()


def check_csrf(session_token: str | None, supplied: str | None) -> bool:
    if not session_token or not supplied:
        return False
    return hmac.compare_digest(csrf_token(session_token), supplied)


def parse_cookies(header: str | None) -> dict[str, str]:
    if not header:
        return {}
    result = {}
    for part in header.split(";"):
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        result[key.strip()] = value.strip()
    return result


def session_from_cookies(cookies: dict[str, str]) -> str | None:
    return verify_session(cookies.get(COOKIE))


def cookie_header(token: str) -> str:
    return (f"{COOKIE}={token}; Path=/; HttpOnly; SameSite=Strict; "
            f"Max-Age={config.ADMIN_SESSION_SECONDS}")


def clear_cookie_header() -> str:
    return f"{COOKIE}=; Path=/; HttpOnly; SameSite=Strict; Max-Age=0"
