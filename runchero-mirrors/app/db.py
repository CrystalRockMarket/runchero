"""SQLite storage for Runchero Mirrors."""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path

from . import config

SCHEMA_VERSION = 3

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS mirrors (
    id               INTEGER PRIMARY KEY,
    slug             TEXT UNIQUE NOT NULL,
    name             TEXT NOT NULL,
    url              TEXT NOT NULL,
    description      TEXT NOT NULL DEFAULT '',
    submitter_name   TEXT NOT NULL DEFAULT '',
    notes            TEXT NOT NULL DEFAULT '',
    status           TEXT NOT NULL DEFAULT 'queued',
    dir_name         TEXT NOT NULL,
    output_dir       TEXT NOT NULL,
    speed            TEXT NOT NULL DEFAULT 'very-slow',
    pid              INTEGER,
    cancel_requested INTEGER NOT NULL DEFAULT 0,
    entry_path       TEXT NOT NULL DEFAULT '',
    serve_root       TEXT NOT NULL DEFAULT '',
    started_at       TEXT,
    finished_at      TEXT,
    last_activity    TEXT,
    created_at       TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at       TEXT NOT NULL DEFAULT (datetime('now')),
    error_log        TEXT NOT NULL DEFAULT '',
    options_json     TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS mirror_stats (
    id              INTEGER PRIMARY KEY,
    mirror_id       INTEGER NOT NULL REFERENCES mirrors(id) ON DELETE CASCADE,
    pages_saved     INTEGER NOT NULL DEFAULT 0,
    files_saved     INTEGER NOT NULL DEFAULT 0,
    bytes_saved     INTEGER NOT NULL DEFAULT 0,
    links_processed INTEGER NOT NULL DEFAULT 0,
    errors_count    INTEGER NOT NULL DEFAULT 0,
    rate_bps        INTEGER NOT NULL DEFAULT 0,
    updated_at      TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(mirror_id)
);

CREATE TABLE IF NOT EXISTS mirror_logs (
    id         INTEGER PRIMARY KEY,
    mirror_id  INTEGER NOT NULL REFERENCES mirrors(id) ON DELETE CASCADE,
    line       TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_mirrors_status ON mirrors(status);
CREATE INDEX IF NOT EXISTS idx_mirrors_created ON mirrors(created_at);
CREATE INDEX IF NOT EXISTS idx_mirror_logs_mirror ON mirror_logs(mirror_id, id);
"""

_MIGRATIONS = (
    ("mirrors", "speed", "TEXT NOT NULL DEFAULT 'very-slow'"),
    ("mirrors", "cancel_requested", "INTEGER NOT NULL DEFAULT 0"),
    ("mirrors", "entry_path", "TEXT NOT NULL DEFAULT ''"),
    ("mirrors", "serve_root", "TEXT NOT NULL DEFAULT ''"),
    ("mirrors", "last_activity", "TEXT"),
    ("mirrors", "options_json", "TEXT NOT NULL DEFAULT '{}'"),
    ("mirror_stats", "rate_bps", "INTEGER NOT NULL DEFAULT 0"),
)


def connect(path=None):
    db_path = Path(path or config.DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, timeout=15)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA busy_timeout = 10000")
    return conn


def _migrate(conn) -> None:
    for table, column, declaration in _MIGRATIONS:
        try:
            existing = {row["name"] for row in conn.execute(f"PRAGMA table_info({table})")}
        except sqlite3.Error:
            continue
        if existing and column not in existing:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {declaration}")


def init_db(conn) -> None:
    conn.executescript(SCHEMA)
    _migrate(conn)
    conn.execute(
        "INSERT INTO meta(key, value) VALUES('schema_version', ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (str(SCHEMA_VERSION),),
    )
    conn.commit()


@contextmanager
def session(path=None):
    conn = connect(path)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def rows(conn, sql, params=()):
    return list(conn.execute(sql, tuple(params)))


def one(conn, sql, params=()):
    return conn.execute(sql, tuple(params)).fetchone()


def scalar(conn, sql, params=()):
    row = one(conn, sql, params)
    return row[0] if row else None


def log_line(conn, mirror_id: int, line: str) -> None:
    conn.execute(
        "INSERT INTO mirror_logs(mirror_id, line) VALUES(?, ?)",
        (mirror_id, line[:2000]),
    )
