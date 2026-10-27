"""SQLite storage for community app requests."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

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
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            name TEXT NOT NULL DEFAULT '',
            contact TEXT NOT NULL DEFAULT '',
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'new',
            admin_note TEXT NOT NULL DEFAULT ''
        );
        CREATE INDEX IF NOT EXISTS idx_requests_status ON requests(status);
        CREATE INDEX IF NOT EXISTS idx_requests_created ON requests(created_at);
        """
    )
    conn.commit()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def create_request(conn: sqlite3.Connection, *, name: str, contact: str,
                   title: str, description: str, category: str) -> int:
    stamp = _now()
    cursor = conn.execute(
        """
        INSERT INTO requests
            (created_at, updated_at, name, contact, title, description, category, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'new')
        """,
        (stamp, stamp, name, contact, title, description, category),
    )
    conn.commit()
    return int(cursor.lastrowid)


def list_requests(conn: sqlite3.Connection, status: str | None = None,
                  query: str = "", limit: int = 200) -> list[sqlite3.Row]:
    clauses: list[str] = []
    params: list[object] = []
    if status and status in config.STATUSES:
        clauses.append("status = ?")
        params.append(status)
    if query:
        like = f"%{query.strip()}%"
        clauses.append("(title LIKE ? OR description LIKE ? OR name LIKE ? OR contact LIKE ?)")
        params.extend([like, like, like, like])
    where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
    params.append(limit)
    return conn.execute(
        f"SELECT * FROM requests{where} ORDER BY created_at DESC, id DESC LIMIT ?",
        params,
    ).fetchall()


def get_request(conn: sqlite3.Connection, request_id: int) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM requests WHERE id = ?", (request_id,)
    ).fetchone()


def update_request(conn: sqlite3.Connection, request_id: int, *,
                   status: str, note: str) -> None:
    conn.execute(
        "UPDATE requests SET status = ?, admin_note = ?, updated_at = ? WHERE id = ?",
        (status, note, _now(), request_id),
    )
    conn.commit()


def delete_request(conn: sqlite3.Connection, request_id: int) -> None:
    conn.execute("DELETE FROM requests WHERE id = ?", (request_id,))
    conn.commit()


def counts(conn: sqlite3.Connection) -> dict[str, int]:
    result = {status: 0 for status in config.STATUSES}
    for row in conn.execute("SELECT status, COUNT(*) AS n FROM requests GROUP BY status"):
        result[row["status"]] = int(row["n"])
    result["total"] = sum(result[status] for status in config.STATUSES)
    return result


def export_rows(conn: sqlite3.Connection) -> Iterable[sqlite3.Row]:
    return conn.execute("SELECT * FROM requests ORDER BY id")
