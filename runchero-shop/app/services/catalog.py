"""Catalog reads: primals, cuts, packages, and shares."""
from __future__ import annotations

import json
from typing import Any

from .. import db


def primals(conn: db.sqlite3.Connection) -> list[db.sqlite3.Row]:
    return db.rows(conn, "SELECT * FROM primals ORDER BY sort_order, name")


def sections(conn: db.sqlite3.Connection) -> list[db.sqlite3.Row]:
    return db.rows(conn, "SELECT * FROM sections ORDER BY sort_order, name")


def cuts(conn: db.sqlite3.Connection, *, active_only: bool = True,
         primal_slug: str | None = None, section_slug: str | None = None,
         tag: str | None = None, search: str | None = None,
         featured: bool = False, limit: int | None = None) -> list[db.sqlite3.Row]:
    sql = [
        "SELECT c.*, p.slug AS primal_slug, p.name AS primal_name,",
        "       p.icon AS primal_icon, s.slug AS section_slug, s.name AS section_name",
        "FROM cuts c",
        "LEFT JOIN primals p ON p.id = c.primal_id",
        "LEFT JOIN sections s ON s.id = c.section_id",
        "WHERE 1=1",
    ]
    params: list[Any] = []
    if active_only:
        sql.append("AND c.active = 1")
    if primal_slug:
        sql.append("AND p.slug = ?")
        params.append(primal_slug)
    if section_slug:
        sql.append("AND s.slug = ?")
        params.append(section_slug)
    if tag:
        sql.append("AND (',' || c.tags || ',') LIKE ?")
        params.append(f"%,{tag},%")
    if featured:
        sql.append("AND c.featured = 1")
    if search:
        sql.append("AND (c.name LIKE ? OR c.blurb LIKE ? OR c.tags LIKE ?)")
        like = f"%{search}%"
        params.extend([like, like, like])
    sql.append("ORDER BY c.sort_order, c.name")
    if limit:
        sql.append("LIMIT ?")
        params.append(limit)
    return db.rows(conn, " ".join(sql), params)


def cut_by_slug(conn: db.sqlite3.Connection, slug: str) -> db.sqlite3.Row | None:
    return db.one(conn,
                  "SELECT c.*, p.slug AS primal_slug, p.name AS primal_name,"
                  "       p.icon AS primal_icon, s.slug AS section_slug,"
                  "       s.name AS section_name "
                  "FROM cuts c "
                  "LEFT JOIN primals p ON p.id = c.primal_id "
                  "LEFT JOIN sections s ON s.id = c.section_id "
                  "WHERE c.slug = ?",
                  (slug,))


def packages(conn: db.sqlite3.Connection, *, featured: bool = False,
             limit: int | None = None) -> list[db.sqlite3.Row]:
    sql = "SELECT * FROM packages WHERE active = 1"
    params: list[Any] = []
    if featured:
        sql += " AND featured = 1"
    sql += " ORDER BY deal_rank, sort_order, name"
    if limit:
        sql += " LIMIT ?"
        params.append(limit)
    return db.rows(conn, sql, params)


def package_by_slug(conn: db.sqlite3.Connection, slug: str) -> db.sqlite3.Row | None:
    return db.one(conn, "SELECT * FROM packages WHERE slug = ? AND active = 1",
                  (slug,))


def package_items(conn: db.sqlite3.Connection, package_id: int) -> list[db.sqlite3.Row]:
    return db.rows(conn,
                   "SELECT pi.*, c.slug AS cut_slug, c.name AS cut_name, "
                   "       c.unit, c.unit_lbs, c.icon, c.local_price, "
                   "       c.runchero_price, c.price_per_lb "
                   "FROM package_items pi JOIN cuts c ON c.id = pi.cut_id "
                   "WHERE pi.package_id = ? ORDER BY pi.id",
                   (package_id,))


def shares(conn: db.sqlite3.Connection) -> list[db.sqlite3.Row]:
    return db.rows(conn, "SELECT * FROM shares WHERE active = 1 ORDER BY sort_order")


def share_by_slug(conn: db.sqlite3.Connection, slug: str) -> db.sqlite3.Row | None:
    return db.one(conn, "SELECT * FROM shares WHERE slug = ? AND active = 1",
                  (slug,))


def share_contents(conn: db.sqlite3.Connection, takehome_lbs: float,
                   price_per_lb: float) -> list[dict[str, Any]]:
    """A rough breakdown of what a share contains, for the share page."""
    plan = [
        ("Steaks", 0.20), ("Roasts", 0.30), ("Ground beef", 0.22),
        ("Stir-fry & stew meat", 0.08), ("Brisket & ribs", 0.08),
        ("Bones, fat, and extras", 0.12),
    ]
    out = []
    for label, share in plan:
        lbs = takehome_lbs * share
        out.append({
            "label": label,
            "lbs": round(lbs, 1),
            "value": round(lbs * price_per_lb, 2),
        })
    return out


def tag_list(conn: db.sqlite3.Connection) -> list[str]:
    tags: set[str] = set()
    for row in conn.execute("SELECT tags FROM cuts WHERE active = 1"):
        for tag in (row["tags"] or "").split(","):
            tag = tag.strip()
            if tag:
                tags.add(tag)
    return sorted(tags)


def social_links(conn: db.sqlite3.Connection,
                 store_slug: str = "beef") -> list[db.sqlite3.Row]:
    return db.rows(conn,
                   "SELECT * FROM social_links WHERE active = 1 AND store_slug = ? "
                   "ORDER BY sort_order", (store_slug,))
