"""SQLite storage for community directory listings."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from . import config


def connect(path: Path | str | None = None) -> sqlite3.Connection:
    target = Path(path or config.DB_PATH)
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(target, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            name TEXT NOT NULL,
            kind TEXT NOT NULL DEFAULT 'person',
            category TEXT NOT NULL DEFAULT 'Neighbours',
            description TEXT NOT NULL DEFAULT '',
            location TEXT NOT NULL DEFAULT '',
            published INTEGER NOT NULL DEFAULT 1,
            submitter_contact TEXT NOT NULL DEFAULT '',
            admin_note TEXT NOT NULL DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_id INTEGER NOT NULL REFERENCES entries(id) ON DELETE CASCADE,
            kind TEXT NOT NULL DEFAULT 'contact',
            label TEXT NOT NULL,
            value TEXT NOT NULL,
            sort_order INTEGER NOT NULL DEFAULT 0
        );
        CREATE INDEX IF NOT EXISTS idx_entries_published ON entries(published);
        CREATE INDEX IF NOT EXISTS idx_entries_name ON entries(name);
        CREATE INDEX IF NOT EXISTS idx_channels_entry ON channels(entry_id);
        CREATE TABLE IF NOT EXISTS guestbook (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            name TEXT NOT NULL,
            note TEXT NOT NULL DEFAULT '',
            published INTEGER NOT NULL DEFAULT 1
        );
        CREATE INDEX IF NOT EXISTS idx_guestbook_created ON guestbook(created_at DESC);
        CREATE INDEX IF NOT EXISTS idx_guestbook_published ON guestbook(published);
        """
    )
    columns = {row["name"] for row in conn.execute("PRAGMA table_info(entries)")}
    if "kind" not in columns:
        conn.execute("ALTER TABLE entries ADD COLUMN kind TEXT NOT NULL DEFAULT 'person'")
    conn.execute("UPDATE entries SET kind = 'person' WHERE kind NOT IN ('person', 'place')")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_entries_kind ON entries(kind)")
    conn.commit()


def guestbook_sign(conn: sqlite3.Connection, name: str, note: str) -> int:
    cursor = conn.execute(
        "INSERT INTO guestbook (created_at, name, note, published) VALUES (?, ?, ?, 1)",
        (_now(), name, note),
    )
    conn.commit()
    return int(cursor.lastrowid)


def guestbook_entries(conn: sqlite3.Connection, *, published_only: bool = True,
                      limit: int = 300) -> list[dict]:
    where = " WHERE published = 1" if published_only else ""
    rows = conn.execute(
        f"SELECT * FROM guestbook{where} ORDER BY created_at DESC, id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    return [dict(row) for row in rows]


def guestbook_count(conn: sqlite3.Connection) -> int:
    return int(conn.execute("SELECT COUNT(*) FROM guestbook WHERE published = 1").fetchone()[0])


def guestbook_delete(conn: sqlite3.Connection, entry_id: int) -> None:
    conn.execute("DELETE FROM guestbook WHERE id = ?", (entry_id,))
    conn.commit()


def guestbook_toggle(conn: sqlite3.Connection, entry_id: int) -> None:
    conn.execute(
        "UPDATE guestbook SET published = CASE WHEN published = 1 THEN 0 ELSE 1 END "
        "WHERE id = ?",
        (entry_id,),
    )
    conn.commit()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _insert_channels(conn: sqlite3.Connection, entry_id: int,
                     channels: list[dict]) -> None:
    for index, channel in enumerate(channels):
        conn.execute(
            """
            INSERT INTO channels (entry_id, kind, label, value, sort_order)
            VALUES (?, ?, ?, ?, ?)
            """,
            (entry_id, channel.get("kind", "contact"), channel["label"],
             channel["value"], channel.get("sort_order", index * 10)),
        )


def create_entry(conn: sqlite3.Connection, data: dict, channels: list[dict]) -> int:
    stamp = _now()
    cursor = conn.execute(
        """
        INSERT INTO entries
            (created_at, updated_at, name, kind, category, description,
             location, published, submitter_contact, admin_note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            stamp, stamp, data["name"], data.get("kind", "person"),
            data.get("category", "Neighbours"),
            data.get("description", ""), data.get("location", ""),
            1 if data.get("published", True) else 0,
            data.get("submitter_contact", ""), data.get("admin_note", ""),
        ),
    )
    entry_id = int(cursor.lastrowid)
    _insert_channels(conn, entry_id, channels)
    conn.commit()
    return entry_id


def update_entry(conn: sqlite3.Connection, entry_id: int, data: dict,
                 channels: list[dict]) -> None:
    conn.execute(
        """
        UPDATE entries SET updated_at = ?, name = ?, kind = ?, category = ?,
            description = ?, location = ?, published = ?, submitter_contact = ?,
            admin_note = ?
        WHERE id = ?
        """,
        (
            _now(), data["name"], data.get("kind", "person"),
            data.get("category", "Neighbours"),
            data.get("description", ""), data.get("location", ""),
            1 if data.get("published", True) else 0,
            data.get("submitter_contact", ""), data.get("admin_note", ""),
            entry_id,
        ),
    )
    conn.execute("DELETE FROM channels WHERE entry_id = ?", (entry_id,))
    _insert_channels(conn, entry_id, channels)
    conn.commit()


def set_published(conn: sqlite3.Connection, entry_id: int, published: bool) -> None:
    conn.execute(
        "UPDATE entries SET published = ?, updated_at = ? WHERE id = ?",
        (1 if published else 0, _now(), entry_id),
    )
    conn.commit()


def delete_entry(conn: sqlite3.Connection, entry_id: int) -> None:
    conn.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
    conn.commit()


def channels_for(conn: sqlite3.Connection, entry_id: int) -> list[dict]:
    rows = conn.execute(
        "SELECT kind, label, value, sort_order FROM channels WHERE entry_id = ? "
        "ORDER BY sort_order, id",
        (entry_id,),
    ).fetchall()
    return [dict(row) for row in rows]


def _entry(row: sqlite3.Row, channels: list[dict]) -> dict:
    entry = dict(row)
    entry["published"] = bool(entry["published"])
    entry["channels"] = channels
    return entry


def get_entry(conn: sqlite3.Connection, entry_id: int,
              published_only: bool = False) -> dict | None:
    row = conn.execute("SELECT * FROM entries WHERE id = ?", (entry_id,)).fetchone()
    if row is None:
        return None
    if published_only and not row["published"]:
        return None
    return _entry(row, channels_for(conn, entry_id))


def list_entries(conn: sqlite3.Connection, *, q: str = "", category: str = "",
                 kind: str = "", published_only: bool = True, order: str = "name",
                 limit: int = 300) -> list[dict]:
    clauses = []
    params: list[object] = []
    if published_only:
        clauses.append("e.published = 1")
    if kind:
        clauses.append("e.kind = ?")
        params.append(kind)
    if category:
        clauses.append("e.category = ?")
        params.append(category)
    if q:
        like = f"%{q.strip()}%"
        clauses.append(
            "(e.name LIKE ? OR e.description LIKE ? OR e.location LIKE ? "
            "OR e.id IN (SELECT entry_id FROM channels WHERE value LIKE ?))"
        )
        params.extend([like, like, like, like])
    where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
    ordering = "e.created_at DESC, e.id DESC" if order == "created" else "e.name COLLATE NOCASE ASC, e.id ASC"
    params.append(limit)
    rows = conn.execute(
        f"SELECT e.* FROM entries e{where} ORDER BY {ordering} LIMIT ?",
        params,
    ).fetchall()
    return [_entry(row, channels_for(conn, row["id"])) for row in rows]


def counts(conn: sqlite3.Connection, kind: str | None = None) -> dict[str, int]:
    where = " WHERE kind = ?" if kind else ""
    params = (kind,) if kind else ()
    total = int(conn.execute(f"SELECT COUNT(*) FROM entries{where}", params).fetchone()[0])
    published_where = " WHERE published = 1"
    if kind:
        published_where += " AND kind = ?"
    published = int(conn.execute(f"SELECT COUNT(*) FROM entries{published_where}", params).fetchone()[0])
    return {"total": total, "published": published, "hidden": total - published}
