"""The pricing engine: the 20 percent rule, .x9 rounding, scoped actions.

The owner's promise is "priced under the local shelf." That promise lives
here, not in the seed data, so a repricing is one rule change instead of
ninety-two hand edits. Everything an admin action does is recorded before
and after, and publish-time checks refuse to let a cut drift above its
market benchmark without an explicit override.
"""
from __future__ import annotations

import json
from typing import Any

from .. import db


def round_to_x9(price: float) -> float:
    """Floor a price to the nearest cent ending in nine: 12.99, 13.09, 5.19."""
    if price <= 0:
        return 0.0
    cents = int(price * 100 + 1e-9)
    dimes = cents // 10
    high = dimes * 10 + 9
    if high <= cents:
        result = high
    else:
        result = (dimes - 1) * 10 + 9
    return max(0.0, result) / 100.0


def discount_for(conn: db.sqlite3.Connection, cut: db.sqlite3.Row) -> float:
    """The effective discount percent for one cut, most specific rule wins.

    Rule scopes, from most to least specific: tag, section, primal, band,
    global.
    """
    rules = db.rows(conn,
                    "SELECT * FROM price_rules WHERE active = 1 "
                    "ORDER BY priority DESC, id")
    best: tuple[int, float] | None = None
    for rule in rules:
        if _rule_matches(rule, cut):
            priority = int(rule["priority"])
            if best is None or priority > best[0]:
                best = (priority, float(rule["discount_pct"]))
    return best[1] if best else 20.0


def _rule_matches(rule: db.sqlite3.Row, cut: db.sqlite3.Row) -> bool:
    scope = rule["scope_type"]
    value = (rule["scope_value"] or "").strip()
    if scope == "global":
        return True
    if scope == "primal":
        return (cut["primal_slug"] or "") == value
    if scope == "section":
        return (cut["section_slug"] or "") == value
    if scope == "tag":
        tags = set((cut["tags"] or "").split(","))
        return value in tags
    if scope == "band":
        try:
            low, high = (float(v) for v in value.split("-", 1))
        except ValueError:
            return False
        return low <= float(cut["local_price"]) <= high
    return False


def computed_price(conn: db.sqlite3.Connection, cut: db.sqlite3.Row) -> float:
    """Our price for a cut under the current rules."""
    discount = discount_for(conn, cut)
    return round_to_x9(float(cut["local_price"]) * (1.0 - discount / 100.0))


def scope_cuts(conn: db.sqlite3.Connection, scope: str, value: str,
              search: str | None = None) -> list[db.sqlite3.Row]:
    """Which cuts an action applies to."""
    sql = ("SELECT c.*, p.slug AS primal_slug, p.name AS primal_name, "
           "s.slug AS section_slug, s.name AS section_name "
           "FROM cuts c LEFT JOIN primals p ON p.id = c.primal_id "
           "LEFT JOIN sections s ON s.id = c.section_id WHERE c.active = 1")
    params: list[Any] = []
    if scope == "primal" and value:
        sql += " AND p.slug = ?"
        params.append(value)
    elif scope == "section" and value:
        sql += " AND s.slug = ?"
        params.append(value)
    elif scope == "tag" and value:
        sql += " AND (',' || c.tags || ',') LIKE ?"
        params.append(f"%,{value},%")
    elif scope == "band" and value:
        try:
            low, high = (float(v) for v in value.split("-", 1))
            sql += " AND c.local_price BETWEEN ? AND ?"
            params.extend([low, high])
        except ValueError:
            pass
    if search:
        sql += " AND (c.name LIKE ? OR c.tags LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
    sql += " ORDER BY c.name"
    return db.rows(conn, sql, params)


def preview(conn: db.sqlite3.Connection, action: dict[str, Any]) -> list[dict[str, Any]]:
    """What an action would do, without doing it."""
    cuts = scope_cuts(conn, action.get("scope", "all"),
                      action.get("value", ""), action.get("search"))
    kind = action.get("kind", "rake")
    out: list[dict[str, Any]] = []
    for cut in cuts:
        old = float(cut["runchero_price"])
        local = float(cut["local_price"])
        if kind == "rake":
            discount = float(action.get("discount", 20.0))
            new = round_to_x9(local * (1.0 - discount / 100.0))
        elif kind == "percent":
            pct = float(action.get("percent", 0.0))
            new = round_to_x9(old * (1.0 - pct / 100.0))
        elif kind == "fixed":
            new = round_to_x9(float(action.get("price", old)))
        elif kind == "markdown":
            new = round_to_x9(old - float(action.get("amount", 0.0)))
        else:
            new = old
        out.append({
            "id": cut["id"], "slug": cut["slug"], "name": cut["name"],
            "local": local, "old": old, "new": new,
            "delta": round(new - old, 2),
        })
    return out


def apply(conn: db.sqlite3.Connection, action: dict[str, Any], actor: str,
          draft_id: int | None = None) -> dict[str, Any]:
    """Run an action, writing an audit row first."""
    rows = preview(conn, action)
    if not rows:
        return {"changed": 0, "rows": []}
    before = {row["id"]: row["old"] for row in rows}
    changed = 0
    for row in rows:
        if abs(row["new"] - row["old"]) < 0.005:
            continue
        conn.execute("UPDATE cuts SET runchero_price = ? WHERE id = ?",
                     (row["new"], row["id"]))
        changed += 1
    summary = {
        "action": action, "changed": changed,
        "rows": [{k: row[k] for k in ("id", "name", "old", "new", "delta")}
                 for row in rows if abs(row["delta"]) >= 0.005],
    }
    conn.execute(
        "INSERT INTO price_audits(action, scope, target_json, before_json, "
        "after_json, summary, actor, draft_id) "
        "VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
        (action.get("kind", "rake"),
         f"{action.get('scope', 'all')}:{action.get('value', '')}",
         json.dumps({k: action.get(k) for k in
                     ("scope", "value", "kind", "discount", "percent",
                      "price", "amount", "search")}),
         json.dumps({"cuts": before}),
         json.dumps({"cuts": {row["id"]: row["new"] for row in rows}}),
         json.dumps(summary), actor, draft_id))
    conn.commit()
    return summary


def audit_log(conn: db.sqlite3.Connection, limit: int = 40) -> list[db.sqlite3.Row]:
    return db.rows(conn, "SELECT * FROM price_audits ORDER BY id DESC LIMIT ?",
                   (limit,))


def revert(conn: db.sqlite3.Connection, audit_id: int, actor: str) -> bool:
    """Put prices back the way they were before one audited action."""
    row = db.one(conn, "SELECT * FROM price_audits WHERE id = ?", (audit_id,))
    if row is None or row["reverted_at"]:
        return False
    try:
        before = json.loads(row["before_json"])["cuts"]
    except (ValueError, TypeError, KeyError):
        return False
    for cut_id, price in before.items():
        conn.execute("UPDATE cuts SET runchero_price = ? WHERE id = ?",
                     (float(price), int(cut_id)))
    conn.execute("UPDATE price_audits SET reverted_at = datetime('now') "
                 "WHERE id = ?", (audit_id,))
    db.log_audit(conn, "price.revert", "price_audit", audit_id,
                 json.dumps({"by": actor}), actor=actor)
    conn.commit()
    return True


def claim_integrity(conn: db.sqlite3.Connection) -> list[db.sqlite3.Row]:
    """Cuts whose price no longer beats their market benchmark.

    The whole pitch is "priced under the local shelf," so any cut at or above
    its benchmark gets flagged here and its badge is suppressed on the shop
    page until someone repricing or explicitly overrides it.
    """
    from . import market
    rows = db.rows(conn,
                   "SELECT c.*, p.slug AS primal_slug, s.slug AS section_slug "
                   "FROM cuts c LEFT JOIN primals p ON p.id = c.primal_id "
                   "LEFT JOIN sections s ON s.id = c.section_id "
                   "WHERE c.active = 1 AND c.market_series_key != '' "
                   "ORDER BY c.name")
    out = []
    for cut in rows:
        comparison = market.compare(conn, cut)
        if comparison.get("available") and not comparison.get("under"):
            out.append(cut)
    return out
