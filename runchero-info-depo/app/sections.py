"""Split archived books into searchable chapters and passages.

The catalogue index only knows titles and blurbs. This module reads the local
text files and builds a second FTS index of the actual pages, so a search can
land inside a cookbook chapter instead of stopping at the cover.
"""
from __future__ import annotations

import html
import re
import sqlite3
from pathlib import Path

from . import config, db

SECTION_CHARS = 2400
MIN_SECTION_CHARS = 80
SUPPORTED_FORMATS = ("TEXT", "HTML", "MANUAL")

_HEADING_WORDS = re.compile(
    r"^(chapter|book|part|section|lesson|lecture|article|recipe|receipt|"
    r"preserv|canning|pickl|ferment|dairy|cheese|bread|pastry|cake|candy|"
    r"soup|sauce|fish|meat|poultry|game|vegetable|salad|coffee|tea|wine|beer|"
    r"cider|vinegar|nutrition|diet|food|household|kitchen|miscellaneous)\b",
    re.IGNORECASE,
)


def clean_text(raw: str, fmt: str = "TEXT") -> str:
    """Strip markup and Gutenberg boilerplate from a local book file."""
    text = raw
    if fmt == "HTML":
        text = re.sub(r"(?is)<(script|style).*?</\1>", " ", text)
        text = re.sub(r"(?s)<[^>]+>", " ", text)
        text = html.unescape(text)
    start = text.find("*** START OF")
    if start != -1:
        newline = text.find("\n", start)
        if newline != -1:
            text = text[newline + 1:]
    end = text.find("*** END OF")
    if end != -1:
        text = text[:end]
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\x0c", "\n\n")
    return text.strip()


def _clean_line(line: str) -> str:
    line = " ".join(line.replace("\t", " ").split())
    return line.strip(" *_=~-")


def _is_heading(line: str) -> bool:
    if not (3 <= len(line) <= 92):
        return False
    letters = [ch for ch in line if ch.isalpha()]
    if len(letters) < 3:
        return False
    if line.endswith((".", ",", ";", ":", "?", "!")) and not _HEADING_WORDS.match(line):
        return False
    if re.search(r"(\.\s*){4,}", line) or line.count("  ") > 2:
        return False
    upper = sum(1 for ch in letters if ch.isupper()) / len(letters)
    title = sum(1 for word in line.split() if word[:1].isupper()) / max(1, len(line.split()))
    if upper >= 0.72:
        return True
    if title >= 0.78 and len(line.split()) <= 9 and not re.search(r"\d{3,}", line):
        return _HEADING_WORDS.match(line) is not None
    return False


def _split_long(paragraph: str, size: int) -> list[str]:
    if len(paragraph) <= size:
        return [paragraph]
    parts: list[str] = []
    rest = paragraph
    while len(rest) > size:
        cut = rest.rfind(". ", size // 2, size)
        if cut == -1:
            cut = rest.rfind(" ", size // 2, size)
        if cut == -1:
            cut = size
        parts.append(rest[:cut + 1].strip())
        rest = rest[cut + 1:].strip()
    if rest:
        parts.append(rest)
    return parts


def split_sections(text: str) -> list[tuple[str, str]]:
    """Return a list of (heading, body) passages, preserving chapter titles."""
    paragraphs = re.split(r"\n\s*\n", text)
    sections: list[tuple[str, str]] = []
    heading = ""
    buf: list[str] = []
    buf_len = 0

    def flush() -> None:
        nonlocal buf, buf_len
        body = "\n\n".join(part for part in buf if part).strip()
        if body and len(body) >= MIN_SECTION_CHARS:
            sections.append((heading, body))
        buf = []
        buf_len = 0

    for raw_para in paragraphs:
        lines = [_clean_line(line) for line in raw_para.splitlines()]
        lines = [line for line in lines if line]
        if not lines:
            continue
        first = lines[0]
        if len(lines) <= 3 and _is_heading(first):
            flush()
            heading = first[:160]
            rest = " ".join(lines[1:]).strip()
            if rest:
                buf.append(rest)
                buf_len += len(rest)
            continue
        para = " ".join(lines)
        for piece in _split_long(para, SECTION_CHARS):
            if buf_len and buf_len + len(piece) + 2 > SECTION_CHARS:
                flush()
            buf.append(piece)
            buf_len += len(piece) + 2
    flush()
    return sections


def _book_path(book: sqlite3.Row) -> Path:
    return config.ARCHIVE_DIR / book["rel_path"]


def index_book(conn: sqlite3.Connection, book: sqlite3.Row) -> int:
    path = _book_path(book)
    if not path.exists() or not path.is_file():
        return 0
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0
    text = clean_text(raw, book["format"])
    sections = split_sections(text)
    if not sections:
        return 0
    conn.execute("DELETE FROM book_sections WHERE book_id = ?", (book["id"],))
    conn.executemany(
        "INSERT INTO book_sections(book_id, book_slug, ordinal, heading, body, "
        "char_count) VALUES(?,?,?,?,?,?)",
        [(book["id"], book["slug"], i, heading, body, len(body))
         for i, (heading, body) in enumerate(sections, start=1)],
    )
    return len(sections)


def index_all(conn: sqlite3.Connection, force: bool = False,
              progress=None) -> tuple[int, int]:
    """Index books that have no sections yet. Returns (books, sections)."""
    if force:
        conn.execute("DELETE FROM book_sections")
    conn.execute(
        "DELETE FROM book_sections WHERE book_id NOT IN (SELECT id FROM books)")
    books = db.rows(
        conn,
        "SELECT b.* FROM books b WHERE b.format IN (?,?,?) "
        "AND NOT EXISTS (SELECT 1 FROM book_sections s WHERE s.book_id = b.id) "
        "ORDER BY b.title",
        SUPPORTED_FORMATS,
    )
    total_sections = 0
    indexed = 0
    for book in books:
        count = index_book(conn, book)
        if count:
            indexed += 1
            total_sections += count
        if progress:
            progress(book, count)
    if books:
        conn.execute("INSERT INTO section_fts(section_fts) VALUES('rebuild')")
        conn.execute(
            "INSERT INTO meta(key, value) VALUES('sections_version', '1') "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value")
    conn.commit()
    return indexed, total_sections
