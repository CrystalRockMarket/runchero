"""Jinja environment, request object, and shared helpers.

The request object is deliberately tiny: method, path, query, form fields,
cookies, and a signed session cookie. There is no framework here on purpose.
"""
from __future__ import annotations

import base64
import datetime as _dt
import hashlib
import hmac
import json
import os
import re
import secrets
from http.cookies import SimpleCookie
from typing import Any
from urllib.parse import parse_qs

from jinja2 import Environment, FileSystemLoader, select_autoescape

from . import config, db

_env: Environment | None = None

#: Bumped when the default content block changes, so new keys get written.
_CONTENT_VERSION = "2"
_CONTENT_VERSION_KEY = "_content_version"


# --------------------------------------------------------------------------
# secret handling
# --------------------------------------------------------------------------

def secret() -> bytes:
    """A per-process secret. Stable for the life of the process, which is
    enough to sign session cookies; sessions drop on restart, which is fine.
    """
    global _SECRET
    try:
        return _SECRET
    except NameError:
        pass
    if config.SECRET_KEY:
        _SECRET = config.SECRET_KEY.encode("utf-8")
    else:
        _SECRET = secrets.token_bytes(32)
    return _SECRET


_SECRET: bytes = b""


def _sign(payload: bytes) -> str:
    return hmac.new(secret(), payload, hashlib.sha256).hexdigest()[:32]


def sign_value(value: Any) -> str:
    """Encode and sign a JSON-able value for use in a cookie."""
    raw = json.dumps(value, separators=(",", ":")).encode("utf-8")
    blob = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")
    return f"{blob}.{_sign(raw)}"


def unsign_value(token: str) -> Any:
    """Reverse sign_value. Returns None when the signature does not match."""
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
# request
# --------------------------------------------------------------------------

class Request:
    """Everything a view might need about the incoming call."""

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

    # -- form ------------------------------------------------------------
    @property
    def form(self) -> dict[str, str]:
        if self._form is None:
            self._form = {}
            if self.body:
                ctype = (self.headers.get("Content-Type") or "").lower()
                if "application/json" in ctype:
                    return self._form
                if ctype.startswith("multipart/form-data"):
                    import email
                    from email import policy

                    message = email.message_from_bytes(
                        b"Content-Type: "
                        + (self.headers.get("Content-Type") or "").encode(
                            "ascii", "replace")
                        + b"\r\nMIME-Version: 1.0\r\n\r\n" + self.body,
                        policy=policy.default)
                    if message.is_multipart():
                        for part in message.iter_parts():
                            name = part.get_param(
                                "name", header="content-disposition")
                            if name and not part.get_filename():
                                payload = part.get_payload(decode=True) or b""
                                self._form[name] = payload.decode(
                                    part.get_content_charset() or "utf-8",
                                    "replace")
                    return self._form
                try:
                    text = self.body.decode("utf-8", "replace")
                except Exception:  # pragma: no cover - defensive
                    return self._form
                for key, values in parse_qs(text, keep_blank_values=True).items():
                    self._form[key] = values[-1]
            return self._form
        return self._form

    @property
    def files(self) -> dict[str, dict[str, Any]]:
        """Multipart file uploads, keyed by field name. Empty if not multipart."""
        if not hasattr(self, "_files"):
            self._files = {}
            if self.body:
                import email
                from email import policy

                ctype = self.headers.get("Content-Type") or ""
                if ctype.lower().startswith("multipart/form-data"):
                    message = email.message_from_bytes(
                        b"Content-Type: " + ctype.encode("ascii", "replace")
                        + b"\r\nMIME-Version: 1.0\r\n\r\n" + self.body,
                        policy=policy.default)
                    if message.is_multipart():
                        for part in message.iter_parts():
                            name = part.get_param("name", header="content-disposition")
                            filename = part.get_filename()
                            if not name or not filename:
                                continue
                            self._files[name] = {
                                "filename": filename,
                                "content_type": part.get_content_type(),
                                "data": part.get_payload(decode=True) or b"",
                            }
        return self._files

    def getlist(self, key: str) -> list[str]:
        """Every value submitted for a repeated field name."""
        if not self.body:
            return []
        try:
            text = self.body.decode("utf-8", "replace")
        except Exception:  # pragma: no cover - defensive
            return []
        return parse_qs(text, keep_blank_values=True).get(key, [])

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

    # -- cookies ---------------------------------------------------------
    @property
    def cookies(self) -> dict[str, str]:
        jar = SimpleCookie()
        try:
            jar.load(self.headers.get("Cookie") or "")
        except Exception:  # pragma: no cover - defensive
            return {}
        return {key: morsel.value for key, morsel in jar.items()}

    def get_cookie(self, name: str) -> str | None:
        return self.cookies.get(name)

    def set_cookie(self, name: str, value: str, max_age: int = 60 * 60 * 24 * 30,
                   http_only: bool = True) -> None:
        parts = [f"{name}={value}", f"Path=/", f"Max-Age={max_age}", "SameSite=Lax"]
        if http_only:
            parts.append("HttpOnly")
        if os.environ.get("RBS_SECURE_COOKIES", "0") in ("1", "true", "yes"):
            parts.append("Secure")
        cookie = "; ".join(parts)
        # One cookie per name: a later write replaces the earlier one so the
        # browser never keeps a stale session.
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

    # -- session ---------------------------------------------------------
    def session_get(self, key: str, default: Any = None) -> Any:
        return self.session.get(key, default)

    def session_set(self, key: str, value: Any) -> None:
        self.session[key] = value
        self._flush_session()

    def session_pop(self, key: str, default: Any = None) -> Any:
        value = self.session.pop(key, default)
        self._flush_session()
        return value

    def _flush_session(self) -> None:
        if not self.session:
            self.clear_cookie("rbs_session")
            return
        self.set_cookie("rbs_session", sign_value(self.session))

    def load_session(self) -> None:
        raw = self.get_cookie("rbs_session")
        if raw:
            data = unsign_value(raw)
            if isinstance(data, dict):
                self.session = data

    # -- helpers ---------------------------------------------------------
    def wants_json(self) -> bool:
        accept = (self.headers.get("Accept") or "").lower()
        return "application/json" in accept and "text/html" not in accept

    def csrf_token(self) -> str:
        token = self.session.get("_csrf")
        if not token:
            token = secrets.token_urlsafe(24)
            self.session_set("_csrf", token)
        return token

    def csrf_ok(self) -> bool:
        sent = self.form.get("_csrf") or self.headers.get("X-CSRF-Token") or ""
        expected = self.session.get("_csrf") or ""
        return bool(expected) and hmac.compare_digest(expected, sent)


# --------------------------------------------------------------------------
# jinja
# --------------------------------------------------------------------------

def env() -> Environment:
    global _env
    if _env is None:
        _env = Environment(
            loader=FileSystemLoader(str(config.TEMPLATES_DIR)),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        _env.filters["money"] = money
        _env.filters["pct"] = pct
        _env.filters["prettydate"] = pretty_date
        _env.filters["prettydatetime"] = pretty_datetime
        _env.filters["slugify"] = slugify
        _env.filters["shortdate"] = short_date
        _env.globals.update(
            site_name=config.SITE_NAME,
            site_short=config.SITE_SHORT,
            site_tagline=config.SITE_TAGLINE,
            site_badge=config.SITE_BADGE,
            site_version=config.SITE_VERSION,
            site_locale=config.LOCALE,
            static_url=static_url,
        )
    return _env


def render(template: str, **context: Any) -> str:
    return env().get_template(template).render(**context)


def static_url(path: str) -> str:
    return f"/static/{path.lstrip('/')}"


def money(amount: float | int | None) -> str:
    """Format a dollar amount the way a price tag should read."""
    if amount is None:
        amount = 0
    amount = float(amount)
    if abs(amount - round(amount)) < 0.005:
        return f"${amount:,.0f}"
    return f"${amount:,.2f}"


def pct(value: float | int | None, total: float | int | None) -> int:
    """A clamped 0-100 percentage, for progress bars."""
    try:
        value = float(value or 0)
        total = float(total or 0)
    except (TypeError, ValueError):
        return 0
    if total <= 0:
        return 0
    return max(0, min(100, round(value / total * 100)))


def pretty_date(value: str | None) -> str:
    if not value:
        return ""
    try:
        stamp = _dt.datetime.fromisoformat(value.replace("Z", ""))
    except ValueError:
        return value
    return stamp.strftime("%d %b %Y")


def pretty_datetime(value: str | None) -> str:
    if not value:
        return ""
    try:
        stamp = _dt.datetime.fromisoformat(value.replace("Z", ""))
    except ValueError:
        return value
    return stamp.strftime("%a %d %b %Y, %-I:%M %p").replace("  ", " ")


def short_date(value: str | None) -> str:
    if not value:
        return ""
    try:
        stamp = _dt.datetime.fromisoformat(value.replace("Z", ""))
    except ValueError:
        return value
    return stamp.strftime("%a %d %b")


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (text or "").strip().lower()).strip("-")


# --------------------------------------------------------------------------
# content lookup used by nearly every template
# --------------------------------------------------------------------------

def shop_content(conn: db.sqlite3.Connection) -> dict[str, Any]:
    """The editable shop settings, read once per request.

    Defaults are written once, in a single transaction, and then read back in
    one query. Writing on every request would hold the write lock against the
    other threads for no reason.
    """
    defaults: dict[str, Any] = {
        "pickup_name": "The Crea",
        "pickup_address": "601 Main St, Shelbyville, KY 40065",
        "pickup_hours": "Wed 4:00pm - 7:00pm, Sat 10:00am - 2:00pm",
        "pickup_instructions": "Park out front and text your order code.",
        "delivery_fee": 15.0,
        "free_delivery_over": 159.0,
        "min_order": 99.0,
        "default_discount_pct": 20.0,
        "tax_rate": 0.0,
        "tax_note": "No sales tax on beef for home use in Kentucky.",
        "delivery_days": ["Wednesday", "Saturday"],
        "delivery_counties": ["Shelby", "Henry", "Spencer", "Nelson", "Jefferson"],
        "cutoff_hour": 23,
        "cutoff_minute": 59,
        "cutoff_lead_days": 1,
        "share_discount": 5.0,
        "share_discount_quarterly": 8.0,
        "subscriber_free_delivery": True,
        "facebook_url": config.FACEBOOK_URL,
        "contact_email": config.CONTACT_EMAIL,
        "wrap_paper_fee": 0.75,
        "wrap_both_fee": 1.25,
        "gift_wrap_fee": 6.0,
        "terms_version": "1.0",
        "banner": "Demo shop. No card is charged and no beef is shipped.",
    }
    if db.content(conn, _CONTENT_VERSION_KEY) != _CONTENT_VERSION:
        for key, value in defaults.items():
            conn.execute(
                "INSERT INTO site_content(key, value_json) VALUES(?, ?) "
                "ON CONFLICT(key) DO NOTHING",
                (key, json.dumps(value)))
        conn.execute(
            "INSERT INTO site_content(key, value_json) VALUES(?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value_json = excluded.value_json",
            (_CONTENT_VERSION_KEY, json.dumps(_CONTENT_VERSION)))
        conn.commit()

    merged = dict(defaults)
    for row in db.rows(conn, "SELECT key, value_json FROM site_content"):
        if row["key"] not in defaults:
            continue
        try:
            merged[row["key"]] = json.loads(row["value_json"])
        except (ValueError, TypeError):
            continue
    return merged
