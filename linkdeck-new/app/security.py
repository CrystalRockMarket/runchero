"""Security: password hashing, sessions, CSRF, rate limiting."""
from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from app.config import settings

SESSION_SECRET = settings.SECRET_KEY
SESSION_ALGORITHM = "HS256"
SESSION_COOKIE = settings.SESSION_COOKIE_NAME
CSRF_COOKIE = settings.CSRF_COOKIE_NAME


def _pw_bytes(password: str) -> bytes:
    # bcrypt only uses the first 72 bytes; truncate explicitly (bcrypt>=4 raises otherwise).
    return password.encode("utf-8")[:72]


def hash_password(password: str) -> str:
    return bcrypt.hashpw(_pw_bytes(password), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(_pw_bytes(password), hashed.encode("utf-8"))
    except Exception:
        return False


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def new_token() -> str:
    return secrets.token_urlsafe(32)


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SESSION_SECRET, algorithms=[SESSION_ALGORITHM])
    except JWTError:
        return None


def create_csrf_token() -> str:
    return secrets.token_urlsafe(32)


def client_ip(request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return (request.client.host if request.client else "") or ""


# SlowAPI rate limiter (configured in httpd; imported lazily where needed)
from slowapi import Limiter
from slowapi.util import get_remote_address


def get_identifier(request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return get_remote_address(request)


limiter = Limiter(key_func=get_identifier)