"""SQLite storage layer.

One file on disk, no server, no daemon: the whole depot is a single database
plus a folder of ebooks. That keeps the backup story trivial (copy two paths)
and lets the whole thing live on a stick.
"""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable, Iterator

from . import config

SCHEMA_VERSION = 4

SCHEMA = """
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS categories (
    id         INTEGER PRIMARY KEY,
    slug       TEXT UNIQUE NOT NULL,
    name       TEXT NOT NULL,
    icon       TEXT NOT NULL DEFAULT 'list',
    accent     TEXT NOT NULL DEFAULT 'grass',
    blurb      TEXT NOT NULL DEFAULT '',
    parent_id  INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    kind       TEXT NOT NULL DEFAULT 'article'
);

CREATE TABLE IF NOT EXISTS vehicles (
    id          INTEGER PRIMARY KEY,
    slug        TEXT UNIQUE NOT NULL,
    kind        TEXT NOT NULL,
    make        TEXT NOT NULL DEFAULT '',
    model       TEXT NOT NULL DEFAULT '',
    year_from   INTEGER,
    year_to     INTEGER,
    engine      TEXT NOT NULL DEFAULT '',
    drive       TEXT NOT NULL DEFAULT '',
    power       TEXT NOT NULL DEFAULT '',
    notes       TEXT NOT NULL DEFAULT '',
    origin      TEXT NOT NULL DEFAULT 'ai-organized',
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS articles (
    id           INTEGER PRIMARY KEY,
    slug         TEXT UNIQUE NOT NULL,
    title        TEXT NOT NULL,
    category_id  INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    summary      TEXT NOT NULL DEFAULT '',
    body         TEXT NOT NULL DEFAULT '',
    author       TEXT NOT NULL DEFAULT '',
    source       TEXT NOT NULL DEFAULT 'community',
    origin       TEXT NOT NULL DEFAULT 'ai-generated',
    difficulty   TEXT NOT NULL DEFAULT 'easy',
    vehicle_id   INTEGER REFERENCES vehicles(id) ON DELETE SET NULL,
    tags         TEXT NOT NULL DEFAULT '',
    read_minutes INTEGER NOT NULL DEFAULT 3,
    status       TEXT NOT NULL DEFAULT 'published',
    featured     INTEGER NOT NULL DEFAULT 0,
    views        INTEGER NOT NULL DEFAULT 0,
    created_at   TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at   TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_articles_category ON articles(category_id);
CREATE INDEX IF NOT EXISTS idx_articles_vehicle ON articles(vehicle_id);

CREATE TABLE IF NOT EXISTS article_vehicles (
    article_id INTEGER NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    vehicle_id INTEGER NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
    PRIMARY KEY (article_id, vehicle_id)
);

CREATE TABLE IF NOT EXISTS books (
    id          INTEGER PRIMARY KEY,
    slug        TEXT UNIQUE NOT NULL,
    title       TEXT NOT NULL,
    author      TEXT NOT NULL DEFAULT '',
    publisher   TEXT NOT NULL DEFAULT '',
    year        INTEGER,
    language    TEXT NOT NULL DEFAULT 'en',
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    format      TEXT NOT NULL DEFAULT 'TEXT',
    pages       INTEGER,
    bytes       INTEGER NOT NULL DEFAULT 0,
    sha256      TEXT NOT NULL DEFAULT '',
    rel_path    TEXT NOT NULL DEFAULT '',
    summary     TEXT NOT NULL DEFAULT '',
    source      TEXT NOT NULL DEFAULT 'gutenberg',
    source_url  TEXT NOT NULL DEFAULT '',
    license     TEXT NOT NULL DEFAULT '',
    motif       TEXT NOT NULL DEFAULT 'book',
    base        TEXT NOT NULL DEFAULT 'sky',
    accent      TEXT NOT NULL DEFAULT 'sun',
    added_at    TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_books_category ON books(category_id);

CREATE TABLE IF NOT EXISTS book_vehicles (
    book_id    INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    vehicle_id INTEGER NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, vehicle_id)
);
CREATE INDEX IF NOT EXISTS idx_book_vehicles_vehicle ON book_vehicles(vehicle_id);

CREATE TABLE IF NOT EXISTS sources (
    id         INTEGER PRIMARY KEY,
    slug       TEXT UNIQUE NOT NULL,
    title      TEXT NOT NULL,
    author     TEXT NOT NULL DEFAULT '',
    kind       TEXT NOT NULL DEFAULT 'other',
    url        TEXT NOT NULL DEFAULT '',
    license    TEXT NOT NULL DEFAULT '',
    book_slug  TEXT NOT NULL DEFAULT '',
    note       TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_sources_kind ON sources(kind);

CREATE TABLE IF NOT EXISTS citations (
    id         INTEGER PRIMARY KEY,
    page_kind  TEXT NOT NULL,
    page_slug  TEXT NOT NULL,
    source_id  INTEGER NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    role       TEXT NOT NULL DEFAULT 'background',
    locator    TEXT NOT NULL DEFAULT '',
    note       TEXT NOT NULL DEFAULT '',
    UNIQUE(page_kind, page_slug, source_id, role, locator)
);
CREATE INDEX IF NOT EXISTS idx_citations_page ON citations(page_kind, page_slug);

CREATE TABLE IF NOT EXISTS formula_topics (
    id         INTEGER PRIMARY KEY,
    slug       TEXT UNIQUE NOT NULL,
    name       TEXT NOT NULL,
    blurb      TEXT NOT NULL DEFAULT '',
    sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS formulas (
    id         INTEGER PRIMARY KEY,
    slug       TEXT UNIQUE NOT NULL,
    name       TEXT NOT NULL,
    topic      TEXT NOT NULL DEFAULT 'general',
    expression TEXT NOT NULL DEFAULT '',
    symbols    TEXT NOT NULL DEFAULT '',
    units      TEXT NOT NULL DEFAULT '',
    how        TEXT NOT NULL DEFAULT '',
    example    TEXT NOT NULL DEFAULT '',
    tags       TEXT NOT NULL DEFAULT '',
    origin     TEXT NOT NULL DEFAULT 'ai-organized'
);
CREATE INDEX IF NOT EXISTS idx_formulas_topic ON formulas(topic);

CREATE TABLE IF NOT EXISTS submissions (
    id           INTEGER PRIMARY KEY,
    kind         TEXT NOT NULL DEFAULT 'ebook',
    title        TEXT NOT NULL DEFAULT '',
    author       TEXT NOT NULL DEFAULT '',
    source_url   TEXT NOT NULL DEFAULT '',
    notes        TEXT NOT NULL DEFAULT '',
    file_name    TEXT NOT NULL DEFAULT '',
    bytes        INTEGER NOT NULL DEFAULT 0,
    sha256       TEXT NOT NULL DEFAULT '',
    status       TEXT NOT NULL DEFAULT 'pending',
    submitted_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS glossary (
    id         INTEGER PRIMARY KEY,
    term       TEXT UNIQUE NOT NULL,
    definition TEXT NOT NULL,
    category   TEXT NOT NULL DEFAULT 'general',
    icon       TEXT NOT NULL DEFAULT 'notes'
);

CREATE TABLE IF NOT EXISTS calendar (
    id     INTEGER PRIMARY KEY,
    month  INTEGER NOT NULL,
    region TEXT NOT NULL DEFAULT 'temperate',
    crop   TEXT NOT NULL DEFAULT '',
    task   TEXT NOT NULL,
    icon   TEXT NOT NULL DEFAULT 'seedling'
);
CREATE INDEX IF NOT EXISTS idx_calendar_month ON calendar(month);

CREATE TABLE IF NOT EXISTS collections (
    id            INTEGER PRIMARY KEY,
    slug          TEXT UNIQUE NOT NULL,
    name          TEXT NOT NULL,
    kind          TEXT NOT NULL DEFAULT 'crop',
    group_slug    TEXT NOT NULL DEFAULT '',
    group_name    TEXT NOT NULL DEFAULT '',
    subgroup_slug TEXT NOT NULL DEFAULT '',
    subgroup_name TEXT NOT NULL DEFAULT '',
    icon          TEXT NOT NULL DEFAULT 'seedling',
    accent        TEXT NOT NULL DEFAULT 'grass',
    summary       TEXT NOT NULL DEFAULT '',
    aliases       TEXT NOT NULL DEFAULT '',
    scientific    TEXT NOT NULL DEFAULT '',
    featured      INTEGER NOT NULL DEFAULT 0,
    sort_order    INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_collections_kind ON collections(kind, group_slug, subgroup_slug, sort_order);

CREATE TABLE IF NOT EXISTS collection_books (
    collection_id INTEGER NOT NULL REFERENCES collections(id) ON DELETE CASCADE,
    book_id       INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    role          TEXT NOT NULL DEFAULT 'book',
    note          TEXT NOT NULL DEFAULT '',
    rank          INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (collection_id, book_id)
);
CREATE INDEX IF NOT EXISTS idx_collection_books_book ON collection_books(book_id);

CREATE VIRTUAL TABLE IF NOT EXISTS search_fts USING fts5(
    kind UNINDEXED,
    kind_id UNINDEXED,
    title,
    body,
    tags,
    tokenize = 'porter unicode61'
);

CREATE TABLE IF NOT EXISTS book_sections (
    id         INTEGER PRIMARY KEY,
    book_id    INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    book_slug  TEXT NOT NULL,
    ordinal    INTEGER NOT NULL,
    heading    TEXT NOT NULL DEFAULT '',
    body       TEXT NOT NULL,
    char_count INTEGER NOT NULL DEFAULT 0,
    UNIQUE(book_id, ordinal)
);
CREATE INDEX IF NOT EXISTS idx_book_sections_book ON book_sections(book_id);
CREATE INDEX IF NOT EXISTS idx_book_sections_slug ON book_sections(book_slug);

CREATE VIRTUAL TABLE IF NOT EXISTS section_fts USING fts5(
    book_slug UNINDEXED,
    heading,
    body,
    content = 'book_sections',
    content_rowid = 'id',
    tokenize = 'porter unicode61'
);
"""


def connect(path: Path | None = None) -> sqlite3.Connection:
    db_path = Path(path or config.DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, timeout=15)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    # WAL lets the server keep reading while the seeder writes.
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA busy_timeout = 10000")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    for statement in (
        "ALTER TABLE books ADD COLUMN theme TEXT",
        "ALTER TABLE articles ADD COLUMN origin TEXT NOT NULL DEFAULT 'ai-generated'",
        "ALTER TABLE vehicles ADD COLUMN origin TEXT NOT NULL DEFAULT 'ai-organized'",
        "ALTER TABLE formulas ADD COLUMN origin TEXT NOT NULL DEFAULT 'ai-organized'",
    ):
        try:
            conn.execute(statement)
        except sqlite3.OperationalError:
            pass
    conn.execute(
        "INSERT INTO meta(key, value) VALUES('schema_version', ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (str(SCHEMA_VERSION),),
    )
    conn.commit()


@contextmanager
def session(path: Path | None = None) -> Iterator[sqlite3.Connection]:
    conn = connect(path)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


# --------------------------------------------------------------------------
# query helpers
# --------------------------------------------------------------------------
def rows(conn: sqlite3.Connection, sql: str,
         params: Iterable[Any] = ()) -> list[sqlite3.Row]:
    return list(conn.execute(sql, tuple(params)))


def one(conn: sqlite3.Connection, sql: str,
        params: Iterable[Any] = ()) -> sqlite3.Row | None:
    cur = conn.execute(sql, tuple(params))
    return cur.fetchone()


def scalar(conn: sqlite3.Connection, sql: str,
           params: Iterable[Any] = ()) -> Any:
    row = one(conn, sql, params)
    return row[0] if row else None


def category_map(conn: sqlite3.Connection) -> dict[int, sqlite3.Row]:
    return {r["id"]: r for r in rows(conn, "SELECT * FROM categories")}


def categories(conn: sqlite3.Connection, kind: str | None = None) -> list[sqlite3.Row]:
    if kind:
        return rows(conn,
                    "SELECT * FROM categories WHERE kind = ? ORDER BY sort_order, name",
                    (kind,))
    return rows(conn, "SELECT * FROM categories ORDER BY sort_order, name")


def articles(conn: sqlite3.Connection, category_slug: str | None = None,
             limit: int | None = None, offset: int = 0) -> list[sqlite3.Row]:
    sql = (
        "SELECT a.*, c.name AS category_name, c.slug AS category_slug, "
        "       c.icon AS category_icon, c.accent AS category_accent "
        "FROM articles a LEFT JOIN categories c ON c.id = a.category_id "
        "WHERE a.status = 'published'"
    )
    params: list[Any] = []
    if category_slug:
        sql += " AND (c.slug = ? OR c.parent_id = (SELECT id FROM categories WHERE slug = ?))"
        params += [category_slug, category_slug]
    sql += " ORDER BY a.updated_at DESC, a.title"
    if limit is not None:
        sql += " LIMIT ? OFFSET ?"
        params += [limit, offset]
    return rows(conn, sql, params)


def article_by_slug(conn: sqlite3.Connection, slug: str) -> sqlite3.Row | None:
    return one(conn,
               "SELECT a.*, c.name AS category_name, c.slug AS category_slug, "
               "       c.icon AS category_icon, c.accent AS category_accent "
               "FROM articles a LEFT JOIN categories c ON c.id = a.category_id "
               "WHERE a.slug = ?",
               (slug,))


def books(conn: sqlite3.Connection, category_slug: str | None = None,
          limit: int | None = None) -> list[sqlite3.Row]:
    sql = (
        "SELECT b.*, c.name AS category_name, c.slug AS category_slug, "
        "       c.icon AS category_icon, c.accent AS category_accent "
        "FROM books b LEFT JOIN categories c ON c.id = b.category_id "
    )
    params: list[Any] = []
    if category_slug:
        sql += " WHERE c.slug = ?"
        params.append(category_slug)
    sql += " ORDER BY b.title"
    if limit is not None:
        sql += " LIMIT ?"
        params.append(limit)
    return rows(conn, sql, params)


def book_by_slug(conn: sqlite3.Connection, slug: str) -> sqlite3.Row | None:
    return one(conn,
               "SELECT b.*, c.name AS category_name, c.slug AS category_slug, "
               "       c.icon AS category_icon, c.accent AS category_accent "
               "FROM books b LEFT JOIN categories c ON c.id = b.category_id "
               "WHERE b.slug = ?",
               (slug,))


def vehicles(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return rows(conn, "SELECT * FROM vehicles ORDER BY kind, make, model")


def formula_topics(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return rows(conn, "SELECT * FROM formula_topics ORDER BY sort_order, name")


def formulas(conn: sqlite3.Connection, topic: str | None = None,
             query: str | None = None) -> list[sqlite3.Row]:
    sql = "SELECT * FROM formulas WHERE 1=1"
    params: list[Any] = []
    if topic:
        sql += " AND topic = ?"
        params.append(topic)
    if query:
        like = f"%{query}%"
        sql += (" AND (name LIKE ? OR expression LIKE ? OR symbols LIKE ? "
                "OR how LIKE ? OR example LIKE ? OR units LIKE ? OR tags LIKE ?")
        params.extend([like] * 7)
        # A wiki link points at the slug, and a slug is dashed, so look for the
        # dashed form of the typed word as well.
        dashed = query.strip().lower().replace(" ", "-")
        if dashed:
            sql += " OR slug LIKE ?"
            params.append(f"%{dashed}%")
        sql += ")"
    sql += " ORDER BY topic, name"
    return rows(conn, sql, params)


def formula_by_slug(conn: sqlite3.Connection, slug: str) -> sqlite3.Row | None:
    return one(conn, "SELECT * FROM formulas WHERE slug = ?", (slug,))


def vehicle_by_slug(conn: sqlite3.Connection, slug: str) -> sqlite3.Row | None:
    return one(conn, "SELECT * FROM vehicles WHERE slug = ?", (slug,))


def stats(conn: sqlite3.Connection) -> dict[str, int]:
    return {
        "collections": scalar(conn, "SELECT COUNT(*) FROM collections"),
        "crops": scalar(conn, "SELECT COUNT(*) FROM collections WHERE kind='crop'"),
        "animals": scalar(conn, "SELECT COUNT(*) FROM collections WHERE kind='animal'"),
        "topics": scalar(conn, "SELECT COUNT(*) FROM collections WHERE kind='topic'"),
        "books": scalar(conn, "SELECT COUNT(*) FROM books"),
        "manuals": scalar(conn, "SELECT COUNT(*) FROM books WHERE format='MANUAL'"),
        "vehicles": scalar(conn, "SELECT COUNT(*) FROM vehicles"),
        "categories": scalar(conn, "SELECT COUNT(*) FROM categories"),
        "pages": scalar(conn, "SELECT COALESCE(SUM(pages),0) FROM books"),
        "bytes": scalar(conn, "SELECT COALESCE(SUM(bytes),0) FROM books"),
        "pending": scalar(conn, "SELECT COUNT(*) FROM submissions WHERE status='pending'"),
        "formulas": scalar(conn, "SELECT COUNT(*) FROM formulas"),
    }


# --------------------------------------------------------------------------
# collections (crops, animals, topics)
# --------------------------------------------------------------------------
def collections(conn: sqlite3.Connection, kind: str | None = None,
                group: str | None = None,
                query: str | None = None) -> list[sqlite3.Row]:
    sql = ("SELECT c.*, (SELECT COUNT(*) FROM collection_books cb "
           "WHERE cb.collection_id = c.id) AS source_count "
           "FROM collections c WHERE 1=1")
    params: list[Any] = []
    if kind:
        sql += " AND c.kind = ?"
        params.append(kind)
    if group:
        sql += " AND c.group_slug = ?"
        params.append(group)
    if query:
        like = f"%{query}%"
        sql += (" AND (c.name LIKE ? OR c.summary LIKE ? OR c.aliases LIKE ? "
                "OR c.scientific LIKE ? OR c.group_name LIKE ? "
                "OR c.subgroup_name LIKE ?)")
        params.extend([like] * 6)
    sql += " ORDER BY c.group_slug, c.sort_order, c.name"
    return rows(conn, sql, params)


def collection_by_slug(conn: sqlite3.Connection,
                       slug: str) -> sqlite3.Row | None:
    return one(conn,
               "SELECT c.*, (SELECT COUNT(*) FROM collection_books cb "
               "WHERE cb.collection_id = c.id) AS source_count "
               "FROM collections c WHERE c.slug = ?", (slug,))


def collection_books(conn: sqlite3.Connection,
                     collection_id: int) -> list[sqlite3.Row]:
    return rows(conn,
                "SELECT b.*, c.name AS category_name, cb.role, cb.note AS shelf_note, "
                "       cb.rank "
                "FROM collection_books cb JOIN books b ON b.id = cb.book_id "
                "LEFT JOIN categories c ON c.id = b.category_id "
                "WHERE cb.collection_id = ? "
                "ORDER BY cb.rank, cb.role, b.title", (collection_id,))


def collection_related(conn: sqlite3.Connection,
                       collection: sqlite3.Row, limit: int = 8) -> list[sqlite3.Row]:
    return rows(conn,
                "SELECT c.*, (SELECT COUNT(*) FROM collection_books cb "
                "WHERE cb.collection_id = c.id) AS source_count "
                "FROM collections c WHERE c.kind = ? AND c.id != ? "
                "AND (c.group_slug = ? OR c.subgroup_slug = ?) "
                "ORDER BY CASE WHEN c.subgroup_slug = ? THEN 0 ELSE 1 END, "
                "c.sort_order, c.name LIMIT ?",
                (collection["kind"], collection["id"], collection["group_slug"],
                 collection["subgroup_slug"], collection["subgroup_slug"], limit))


def collection_children(conn: sqlite3.Connection,
                        collection: sqlite3.Row) -> list[sqlite3.Row]:
    return rows(conn,
                "SELECT c.*, (SELECT COUNT(*) FROM collection_books cb "
                "WHERE cb.collection_id = c.id) AS source_count "
                "FROM collections c WHERE c.kind = ? AND c.group_slug = ? "
                "AND c.id != ? ORDER BY c.sort_order, c.name",
                (collection["kind"], collection["group_slug"], collection["id"]))


def collection_book_ids(conn: sqlite3.Connection,
                        kind: str) -> list[int]:
    return [r["book_id"] for r in conn.execute(
        "SELECT DISTINCT cb.book_id FROM collection_books cb "
        "JOIN collections c ON c.id = cb.collection_id WHERE c.kind = ?",
        (kind,))]


def recent_collection_books(conn: sqlite3.Connection, kind: str,
                            limit: int = 8) -> list[sqlite3.Row]:
    return rows(conn,
                "SELECT DISTINCT b.* FROM books b "
                "JOIN collection_books cb ON cb.book_id = b.id "
                "JOIN collections c ON c.id = cb.collection_id "
                "WHERE c.kind = ? ORDER BY b.added_at DESC, b.title LIMIT ?",
                (kind, limit))


# --------------------------------------------------------------------------
# full text search
# --------------------------------------------------------------------------
def reindex(conn: sqlite3.Connection) -> None:
    """Rebuild the FTS index from books, formulas and collection indexes."""
    conn.execute("DELETE FROM search_fts")
    for row in conn.execute(
        "SELECT id, title, summary, author, publisher FROM books"
    ):
        conn.execute(
            "INSERT INTO search_fts(kind, kind_id, title, body, tags) "
            "VALUES('book', ?, ?, ?, ?)",
            (row["id"], row["title"], row["summary"], f"{row['author']} {row['publisher']}"),
        )
    for row in conn.execute(
        "SELECT id, name, expression, symbols, units, how, example, tags FROM formulas"
    ):
        conn.execute(
            "INSERT INTO search_fts(kind, kind_id, title, body, tags) "
            "VALUES('formula', ?, ?, ?, ?)",
            (row["id"], row["name"],
             f"{row['expression']} {row['symbols']} {row['how']} {row['example']}",
             row["tags"]),
        )
    for row in conn.execute(
        "SELECT id, name, summary, aliases, scientific, group_name, subgroup_name "
        "FROM collections"
    ):
        conn.execute(
            "INSERT INTO search_fts(kind, kind_id, title, body, tags) "
            "VALUES('collection', ?, ?, ?, ?)",
            (row["id"], row["name"],
             f"{row['summary']} {row['aliases']} {row['scientific']} "
             f"{row['group_name']} {row['subgroup_name']}",
             f"{row['group_name']} {row['subgroup_name']}"),
        )


def search(conn: sqlite3.Connection, query: str, kind: str | None = None,
           limit: int = 40) -> list[sqlite3.Row]:
    """FTS5 search over books, formulas and collection indexes."""
    terms = [t for t in query.replace('"', " ").split() if t]
    if not terms:
        return []
    match = " ".join(f'"{t}"*' for t in terms)
    sql = (
        "SELECT kind, kind_id, title, "
        "       snippet(search_fts, 3, char(1), char(2), ' ... ', 24) AS snip, "
        "       bm25(search_fts) AS score "
        "FROM search_fts WHERE search_fts MATCH ?"
    )
    params: list[Any] = [match]
    kinds = [k.strip() for k in (kind or "").split(",") if k.strip()]
    if kinds:
        sql += " AND kind IN (%s)" % ",".join("?" * len(kinds))
        params.extend(kinds)
    sql += " ORDER BY score LIMIT ?"
    params.append(limit)
    return rows(conn, sql, params)


def search_sections(conn: sqlite3.Connection, query: str, kind: str | None = None,
                    limit: int = 24) -> list[sqlite3.Row]:
    """Search chapter text and return book metadata plus a snippet."""
    terms = [t for t in query.replace('"', " ").split() if t]
    if not terms:
        return []
    match = " ".join(f'"{t}"*' for t in terms)
    sql = (
        "SELECT b.slug, b.title, b.author, b.year, b.format, b.category_id, "
        "       s.heading, s.ordinal, "
        "       snippet(section_fts, 2, char(1), char(2), ' ... ', 34) AS snip, "
        "       bm25(section_fts) AS score "
        "FROM section_fts "
        "JOIN book_sections s ON s.id = section_fts.rowid "
        "JOIN books b ON b.id = s.book_id "
        "WHERE section_fts MATCH ?"
    )
    params: list[Any] = [match]
    if kind == "manual":
        sql += " AND b.format = 'MANUAL'"
    elif kind == "book":
        sql += " AND b.format != 'MANUAL'"
    sql += " ORDER BY score LIMIT ?"
    params.append(limit)
    return rows(conn, sql, params)


def sources_for(conn: sqlite3.Connection, page_kind: str,
                page_slug: str) -> list[sqlite3.Row]:
    """Sources cited by one page, depot, book, manual or formula."""
    return rows(conn,
        "SELECT s.slug, s.title, s.author, s.kind, s.url, s.license, "
        "       s.book_slug, s.note, c.role, c.locator, c.note AS citation_note "
        "FROM citations c JOIN sources s ON s.id = c.source_id "
        "WHERE c.page_kind = ? AND c.page_slug = ? "
        "ORDER BY CASE c.role WHEN 'primary' THEN 0 WHEN 'index' THEN 1 "
        "         WHEN 'manual' THEN 2 ELSE 3 END, s.title",
        (page_kind, page_slug))


def source_kind_counts(conn: sqlite3.Connection) -> dict[str, int]:
    result: dict[str, int] = {}
    for row in conn.execute(
        "SELECT kind, COUNT(*) n FROM sources GROUP BY kind ORDER BY kind"
    ):
        result[row["kind"]] = row["n"]
    return result


def counts_by_category(conn: sqlite3.Connection) -> dict[str, int]:
    result: dict[str, int] = {}
    for row in conn.execute(
        "SELECT c.slug, COUNT(b.id) AS n FROM categories c "
        "LEFT JOIN books b ON b.category_id = c.id "
        "GROUP BY c.slug"
    ):
        result[row["slug"]] = row["n"]
    return result
