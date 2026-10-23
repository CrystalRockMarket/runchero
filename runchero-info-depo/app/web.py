"""Jinja environment and shared template helpers."""
from __future__ import annotations

import datetime as _dt
import re
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from . import config, db, md

_env: Environment | None = None


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
        _env.filters["prettydate"] = pretty_date
        _env.filters["wikilink"] = wikilink
        _env.filters["monthname"] = month_name
        _env.filters["slugify"] = slugify
        _env.globals.update(
            site_name=config.SITE_NAME,
            site_short=config.SITE_SHORT,
            site_tagline=config.SITE_TAGLINE,
            site_badge=config.SITE_BADGE,
            site_version=config.SITE_VERSION,
            read_only=config.READ_ONLY,
            static_url=static_url,
        )
    return _env


def render(template: str, **context: Any) -> str:
    return env().get_template(template).render(**context)


def static_url(path: str) -> str:
    return f"/static/{path.lstrip('/')}"


def filesize(num: int | None) -> str:
    if not num:
        return "-"
    step = 1024.0
    for unit in ("B", "KB", "MB", "GB"):
        if num < step:
            return f"{num:.0f} {unit}" if unit == "B" else f"{num:.1f} {unit}"
        num /= step
    return f"{num:.1f} TB"


def pretty_date(value: str | None) -> str:
    if not value:
        return ""
    try:
        stamp = _dt.datetime.fromisoformat(value.replace("Z", ""))
    except ValueError:
        return value
    return stamp.strftime("%d %b %Y")


_MONTHS = ["January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December"]


def month_name(value: int | str | None) -> str:
    try:
        index = int(value) - 1
    except (TypeError, ValueError):
        return ""
    if 0 <= index < 12:
        return _MONTHS[index]
    return ""


_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def slugify(text: str) -> str:
    """Turn a heading or glossary term into a URL-friendly anchor."""
    return re.sub(r"[^a-z0-9]+", "-", (text or "").strip().lower()).strip("-")


def _slugify_term(term: str) -> str:
    """Glossary terms are stored with capitals and spaces; links are slugs."""
    return slugify(term)


def wikilink(conn: db.sqlite3.Connection, slug: str) -> tuple[str, str] | None:
    """Resolve a wiki slug to (url, title) for the markdown renderer."""
    if not _SLUG_RE.match(slug):
        return None
    row = db.one(conn, "SELECT name, kind FROM collections WHERE slug = ?", (slug,))
    if row:
        prefix = {"crop": "/grow", "animal": "/animals", "topic": "/topic"}[row["kind"]]
        return f"{prefix}/{slug}", row["name"]
    row = db.one(conn, "SELECT title FROM books WHERE slug = ?", (slug,))
    if row:
        return f"/library/archive/{slug}", row["title"]
    row = db.one(conn, "SELECT model FROM vehicles WHERE slug = ?", (slug,))
    if row:
        return f"/vehicles/{slug}", row["model"]
    row = db.one(conn, "SELECT name FROM formulas WHERE slug = ?", (slug,))
    if row:
        return f"/formulas?q={slug}#formula-{slug}", row["name"]
    row = db.one(conn, "SELECT term FROM glossary "
                        "WHERE REPLACE(LOWER(term), ' ', '-') = ?", (slug,))
    if row:
        return f"/search?q={row['term']}", row["term"]
    words = slug.replace("-", " ")
    return f"/search?q={words}", words.title()


def make_resolver(conn: db.sqlite3.Connection) -> md.Resolver:
    def resolve(slug: str) -> tuple[str, str] | None:
        return wikilink(conn, slug)
    return resolve
