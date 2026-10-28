"""Security: password hashing, sessions, CSRF, rate limiting."""
from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SESSION_SECRET = settings.SECRET_KEY
SESSION_ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def new_token() -> str:
    return secrets.token_urlsafe(32)


def create_access_token(subject: str | int, expires_delta: timedelta) -> str:
    now = datetime.now(timezone.utc)
    expire = now + expires_delta
    to_encode = {
        "sub": str(subject),
        "iat": now,
        "exp": expire,
        "type": "access",
    }
    return jwt.encode(to_encode, SESSION_SECRET, algorithm=SESSION_ALGORITHM)


def create_refresh_token(subject: str | int) -> str:
    return create_access_token(subject, timedelta(days=30))


def decode_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SESSION_SECRET, algorithms=[SESSION_ALGORITHM])
        return payload
    except JWTError:
        return None


def create_csrf_token() -> str:
    return secrets.token_urlsafe(32)


def get_current_user_id(request: Request) -> int:
    """Extract current user ID from session cookie. Returns 0 if not logged in."""
    try:
        token = request.cookies.get("ld_session")
        if not token:
            return 0
        payload = decode_token(token)
        if not payload:
            return 0
        return int(payload.get("sub", 0))
    except Exception:
        return 0


# SlowAPI rate limiter (configured in httpd; imported lazily where needed)
from slowapi import Limiter
from slowapi.util import get_remote_address


def get_identifier(request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return get_remote_address(request)


limiter = Limiter(key_func=get_identifier)