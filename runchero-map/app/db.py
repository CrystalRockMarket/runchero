"""SQLite storage layer for the Runchero Map.

One file on disk, no server, no daemon: the whole map is a single database
plus a folder of static images. That keeps the backup story trivial and lets
the whole thing live on a stick.

The schema covers the property map: places (buildings/areas/features), their
specs, construction notes, events, maintenance log, photos, records, map
geometry (pixel coordinates), categories, site content, admins, audit log.
"""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable, Iterator

from . import config

SCHEMA_VERSION = 1

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

-- ---------------------------------------------------------------------------
-- place categories (barn, shop, house, storage, field, pond, fence, gate ...)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS categories (
    id         INTEGER PRIMARY KEY,
    slug       TEXT UNIQUE NOT NULL,
    name       TEXT NOT NULL,
    colour     TEXT NOT NULL DEFAULT 'sky',
    icon       TEXT NOT NULL DEFAULT 'box',
    sort_order INTEGER NOT NULL DEFAULT 0
);

-- ---------------------------------------------------------------------------
-- places: buildings, fields, ponds, fences, gates, roads, utilities...
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS places (
    id            INTEGER PRIMARY KEY,
    slug          TEXT UNIQUE NOT NULL,
    name          TEXT NOT NULL,
    category_id   INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    kind          TEXT NOT NULL DEFAULT 'building',
    short_desc    TEXT NOT NULL DEFAULT '',
    year_built    TEXT NOT NULL DEFAULT '',
    construction  TEXT NOT NULL DEFAULT '',
    dimensions    TEXT NOT NULL DEFAULT '',
    area_acres    REAL NOT NULL DEFAULT 0,
    status        TEXT NOT NULL DEFAULT 'active',
    notes         TEXT NOT NULL DEFAULT '',
    sort_order    INTEGER NOT NULL DEFAULT 0,
    hidden        INTEGER NOT NULL DEFAULT 0,
    created_at    TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at    TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_places_category ON places(category_id);
CREATE INDEX IF NOT EXISTS idx_places_kind ON places(kind);

-- pixel geometry on the property map (one or more polygons per place)
CREATE TABLE IF NOT EXISTS place_shapes (
    id        INTEGER PRIMARY KEY,
    place_id  INTEGER NOT NULL REFERENCES places(id) ON DELETE CASCADE,
    shape_type TEXT NOT NULL DEFAULT 'polygon',
    coords    TEXT NOT NULL DEFAULT '[]',
    colour    TEXT NOT NULL DEFAULT '',
    sort_order INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_place_shapes_place ON place_shapes(place_id);

-- specs: free-form key/value facts
CREATE TABLE IF NOT EXISTS place_specs (
    id        INTEGER PRIMARY KEY,
    place_id  INTEGER NOT NULL REFERENCES places(id) ON DELETE CASCADE,
    key       TEXT NOT NULL,
    value     TEXT NOT NULL DEFAULT '',
    sort_order INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_place_specs_place ON place_specs(place_id);

-- photos
CREATE TABLE IF NOT EXISTS place_photos (
    id        INTEGER PRIMARY KEY,
    place_id  INTEGER NOT NULL REFERENCES places(id) ON DELETE CASCADE,
    path      TEXT NOT NULL,
    caption   TEXT NOT NULL DEFAULT '',
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_place_photos_place ON place_photos(place_id);

-- records (events, maintenance, construction notes, inspections, notes)
CREATE TABLE IF NOT EXISTS place_records (
    id         INTEGER PRIMARY KEY,
    place_id   INTEGER NOT NULL REFERENCES places(id) ON DELETE CASCADE,
    kind       TEXT NOT NULL DEFAULT 'note',
    title      TEXT NOT NULL DEFAULT '',
    body       TEXT NOT NULL DEFAULT '',
    occurred_on TEXT NOT NULL DEFAULT '',
    actor      TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_place_records_place ON place_records(place_id);
CREATE INDEX IF NOT EXISTS idx_place_records_kind ON place_records(kind);

-- ---------------------------------------------------------------------------
-- map layers (toggleable: fences, water, power, fields, boundaries)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS map_layers (
    id         INTEGER PRIMARY KEY,
    slug       TEXT UNIQUE NOT NULL,
    name       TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    visible    INTEGER NOT NULL DEFAULT 1,
    sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS layer_features (
    id        INTEGER PRIMARY KEY,
    layer_id  INTEGER NOT NULL REFERENCES map_layers(id) ON DELETE CASCADE,
    name      TEXT NOT NULL DEFAULT '',
    feature_type TEXT NOT NULL DEFAULT 'line',
    coords    TEXT NOT NULL DEFAULT '[]',
    colour    TEXT NOT NULL DEFAULT '',
    note      TEXT NOT NULL DEFAULT '',
    sort_order INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_layer_features_layer ON layer_features(layer_id);

-- ---------------------------------------------------------------------------
-- site content, admins, audit
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS site_content (
    key        TEXT PRIMARY KEY,
    value_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS admins (
    id       INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    passhash TEXT NOT NULL,
    role     TEXT NOT NULL DEFAULT 'owner',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS audit_log (
    id         INTEGER PRIMARY KEY,
    actor      TEXT NOT NULL DEFAULT 'system',
    action     TEXT NOT NULL,
    entity     TEXT NOT NULL DEFAULT '',
    entity_id  TEXT NOT NULL DEFAULT '',
    detail_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_log(created_at);
"""


def connect(path=None):
    db_path = Path(path or config.DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, timeout=15)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA busy_timeout = 10000")
    return conn


def init_db(conn):
    conn.executescript(SCHEMA)
    _migrate(conn)
    conn.execute(
        "INSERT INTO meta(key, value) VALUES('schema_version', ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (str(SCHEMA_VERSION),),
    )
    conn.commit()


_MIGRATIONS = ()

def _migrate(conn):
    for table, column, declaration in _MIGRATIONS:
        try:
            existing = {row["name"] for row in conn.execute(f"PRAGMA table_info({table})")}
        except sqlite3.Error:
            continue
        if existing and column not in existing:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {declaration}")


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
    cur = conn.execute(sql, tuple(params))
    return cur.fetchone()


def scalar(conn, sql, params=()):
    row = one(conn, sql, params)
    return row[0] if row else None


def log_audit(conn, action, entity="", entity_id="", detail="", actor="system"):
    conn.execute(
        "INSERT INTO audit_log(actor, action, entity, entity_id, detail_json) VALUES(?, ?, ?, ?, ?)",
        (actor, action, entity, str(entity_id), detail or "{}"),
    )


def content(conn, key, default=None):
    import json
    row = one(conn, "SELECT value_json FROM site_content WHERE key = ?", (key,))
    if not row:
        return default
    try:
        return json.loads(row["value_json"])
    except (ValueError, TypeError):
        return default


def set_content(conn, key, value):
    import json
    conn.execute(
        "INSERT INTO site_content(key, value_json) VALUES(?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value_json = excluded.value_json, updated_at = datetime('now')",
        (key, json.dumps(value)),
    )
    conn.commit()
