"""Jinja environment, signed sessions, and small request/response helpers."""
from __future__ import annotations

import base64
import datetime as _dt
import hashlib
import hmac
import json
import os
import secrets
from dataclasses import dataclass, field
from http.cookies import SimpleCookie
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs

from jinja2 import Environment, FileSystemLoader, select_autoescape

from . import config

_env: Environment | None = None


# --------------------------------------------------------------------------
# secret handling
# --------------------------------------------------------------------------

def secret() -> bytes:
    """A secret that survives restarts, so open forms keep working."""
    global _SECRET
    try:
        return _SECRET
    except NameError:
        pass
    if config.SECRET_KEY:
        _SECRET = config.SECRET_KEY.encode("utf-8")
        return _SECRET
    path = config.DATA_DIR / ".mirrors-session-secret"
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            raw = path.read_text(encoding="ascii").strip()
            if len(raw) >= 32:
                _SECRET = raw.encode("ascii")
                return _SECRET
        raw = secrets.token_hex(32)
        path.write_text(raw, encoding="ascii")
        try:
            path.chmod(0o600)
        except OSError:
            pass
        _SECRET = raw.encode("ascii")
    except OSError:
        _SECRET = secrets.token_bytes(32)
    return _SECRET


_SECRET: bytes = b""


def _sign(payload: bytes) -> str:
    return hmac.new(secret(), payload, hashlib.sha256).hexdigest()[:32]


def sign_value(value: Any) -> str:
    raw = json.dumps(value, separators=(",", ":")).encode("utf-8")
    blob = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")
    return f"{blob}.{_sign(raw)}"


def unsign_value(token: str) -> Any:
    if not token or "." not in token:
        return None
    blob, _, signature = token.rpartition(".")
    padding = "=" * (-len(blob) % 4)
    try:
        raw = base64.urlsafe_b64decode(blob + padding)
    except (ValueError, TypeError):
        return None
    if not hmac.compare_digest(_sign(raw), signature):
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return None


# --------------------------------------------------------------------------
# response helpers
# --------------------------------------------------------------------------

@dataclass
class FilePayload:
    """A file streamed by the server instead of being read into memory."""
    path: Path
    content_type: str
    extra: dict[str, str] = field(default_factory=dict)


# --------------------------------------------------------------------------
# request
# --------------------------------------------------------------------------

class Request:
    """Everything a page needs to know about the incoming call."""

    def __init__(self, method: str, path: str, query: dict[str, str],
                 headers, body: bytes, params: dict[str, str] | None = None):
        self.method = method
        self.path = path
        self.query = query
        self.headers = headers
        self.body = body
        self.params = params or {}
        self._form: dict[str, str] | None = None
        self._json: Any = None
        self._json_parsed = False
        self.session: dict[str, Any] = {}
        self.set_cookies: list[str] = []

    @property
    def form(self) -> dict[str, str]:
        if self._form is None:
            self._form = {}
            if self.body:
                ctype = (self.headers.get("Content-Type") or "").lower()
                if "application/json" in ctype:
                    return self._form
                try:
                    text = self.body.decode("utf-8", "replace")
                except Exception:
                    return self._form
                for key, values in parse_qs(text, keep_blank_values=True).items():
                    self._form[key] = values[-1]
        return self._form

    @property
    def json_body(self) -> Any:
        if not self._json_parsed:
            self._json_parsed = True
            self._json = None
            if self.body:
                try:
                    self._json = json.loads(self.body.decode("utf-8"))
                except (ValueError, UnicodeDecodeError):
                    self._json = None
        return self._json

    @property
    def cookies(self) -> dict[str, str]:
        jar = SimpleCookie()
        try:
            jar.load(self.headers.get("Cookie") or "")
        except Exception:
            return {}
        return {key: morsel.value for key, morsel in jar.items()}

    def get_cookie(self, name: str) -> str | None:
        return self.cookies.get(name)

    def set_cookie(self, name: str, value: str, max_age: int = 60 * 60 * 24 * 14,
                   http_only: bool = True) -> None:
        parts = [f"{name}={value}", "Path=/", f"Max-Age={max_age}", "SameSite=Lax"]
        if http_only:
            parts.append("HttpOnly")
        if os.environ.get("RMM_SECURE_COOKIES", "0") in ("1", "true", "yes"):
            parts.append("Secure")
        cookie = "; ".join(parts)
        for index, existing in enumerate(self.set_cookies):
            if existing.startswith(f"{name}="):
                self.set_cookies[index] = cookie
                return
        self.set_cookies.append(cookie)

    def clear_cookie(self, name: str) -> None:
        blank = f"{name}=; Path=/; Max-Age=0; SameSite=Lax; HttpOnly"
        for index, existing in enumerate(self.set_cookies):
            if existing.startswith(f"{name}="):
                self.set_cookies[index] = blank
                return
        self.set_cookies.append(blank)

    def load_session(self) -> None:
        raw = self.get_cookie("rmm_session")
        if raw:
            data = unsign_value(raw)
            if isinstance(data, dict):
                self.session = data

    def _flush_session(self) -> None:
        if not self.session:
            self.clear_cookie("rmm_session")
        else:
            self.set_cookie("rmm_session", sign_value(self.session))

    def session_get(self, key: str, default: Any = None) -> Any:
        return self.session.get(key, default)

    def session_set(self, key: str, value: Any) -> None:
        self.session[key] = value
        self._flush_session()

    def session_pop(self, key: str, default: Any = None) -> Any:
        value = self.session.pop(key, default)
        self._flush_session()
        return value

    def csrf_token(self) -> str:
        token = self.session.get("_csrf")
        if not token:
            token = secrets.token_urlsafe(24)
            self.session["_csrf"] = token
            self._flush_session()
        return token

    def csrf_ok(self) -> bool:
        sent = self.form.get("_csrf") or self.headers.get("X-CSRF-Token") or ""
        expected = self.session.get("_csrf") or ""
        return bool(expected) and hmac.compare_digest(expected, sent)

    def host(self) -> str:
        return (self.headers.get("Host") or "localhost").split(":")[0]


# --------------------------------------------------------------------------
# jinja
# --------------------------------------------------------------------------

def _parse_ts(value: str | None) -> _dt.datetime | None:
    if not value:
        return None
    try:
        return _dt.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except (TypeError, ValueError):
        return None


def filesize(value: int | float | None) -> str:
    try:
        value = float(value or 0)
    except (TypeError, ValueError):
        return "0 B"
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{value:.1f} TB"


def prettydatetime(value: str | None) -> str:
    parsed = _parse_ts(value)
    if not parsed:
        return "—"
    return parsed.strftime("%b %-d, %Y · %-I:%M %p")


def prettydate(value: str | None) -> str:
    parsed = _parse_ts(value)
    if not parsed:
        return "—"
    return parsed.strftime("%b %-d, %Y")


def duration_between(started_at: str | None, finished_at: str | None = None) -> str:
    start = _parse_ts(started_at)
    if not start:
        return "—"
    end = _parse_ts(finished_at) or _dt.datetime.utcnow()
    seconds = max(0, int((end - start).total_seconds()))
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}h {minutes}m"
    if minutes:
        return f"{minutes}m {secs}s"
    return f"{secs}s"


def env() -> Environment:
    global _env
    if _env is None:
        _env = Environment(
            loader=FileSystemLoader(str(config.TEMPLATES_DIR)),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        _env.filters["filesize"] = filesize
        _env.filters["prettydatetime"] = prettydatetime
        _env.filters["prettydate"] = prettydate
        _env.filters["duration"] = duration_between
        _env.globals.update(
            site_name=config.SITE_NAME,
            site_short=config.SITE_SHORT,
            site_tagline=config.SITE_TAGLINE,
            site_badge=config.SITE_BADGE,
            site_version=config.SITE_VERSION,
            default_speed=config.DEFAULT_SPEED,
            speed_profiles=config.CRAWL_PROFILES,
            static_url=lambda p: f"/static/{p.lstrip('/')}",
        )
    return _env


def render(template: str, **context: Any) -> str:
    return env().get_template(template).render(**context)
