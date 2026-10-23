"""SQLite storage layer for the Runchero Beef shop.

One file on disk, no server, no daemon: the whole shop is a single database
plus a folder of static images. That keeps the backup story trivial and lets
the whole thing live on a stick.

The schema covers the full store: catalog, packing options, pricing rules and
their audit trail, market price observations, carts, orders, fulfillment
slots, subscriptions, share campaigns, and admin accounts.
"""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable, Iterator

from . import config

SCHEMA_VERSION = 5

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

-- ---------------------------------------------------------------------------
-- catalog
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS primals (
    id         INTEGER PRIMARY KEY,
    slug       TEXT UNIQUE NOT NULL,
    name       TEXT NOT NULL,
    icon       TEXT NOT NULL DEFAULT 'cow',
    accent     TEXT NOT NULL DEFAULT 'meat',
    blurb      TEXT NOT NULL DEFAULT '',
    sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS sections (
    id         INTEGER PRIMARY KEY,
    slug       TEXT UNIQUE NOT NULL,
    name       TEXT NOT NULL,
    blurb      TEXT NOT NULL DEFAULT '',
    sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS cuts (
    id                INTEGER PRIMARY KEY,
    slug              TEXT UNIQUE NOT NULL,
    name              TEXT NOT NULL,
    primal_id         INTEGER REFERENCES primals(id) ON DELETE SET NULL,
    section_id        INTEGER REFERENCES sections(id) ON DELETE SET NULL,
    local_price       REAL NOT NULL DEFAULT 0,
    runchero_price    REAL NOT NULL DEFAULT 0,
    unit              TEXT NOT NULL DEFAULT 'lb',
    unit_lbs          REAL NOT NULL DEFAULT 1,
    price_per_lb      REAL NOT NULL DEFAULT 0,
    market_series_key TEXT NOT NULL DEFAULT '',
    tags              TEXT NOT NULL DEFAULT '',
    serving           TEXT NOT NULL DEFAULT '',
    blurb             TEXT NOT NULL DEFAULT '',
    stock_lbs         REAL NOT NULL DEFAULT 0,
    icon              TEXT NOT NULL DEFAULT 'steak',
    featured          INTEGER NOT NULL DEFAULT 0,
    active            INTEGER NOT NULL DEFAULT 1,
    sort_order        INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_cuts_primal ON cuts(primal_id);
CREATE INDEX IF NOT EXISTS idx_cuts_section ON cuts(section_id);

CREATE TABLE IF NOT EXISTS packages (
    id           INTEGER PRIMARY KEY,
    slug         TEXT UNIQUE NOT NULL,
    name         TEXT NOT NULL,
    blurb        TEXT NOT NULL DEFAULT '',
    badge        TEXT NOT NULL DEFAULT '',
    price        REAL NOT NULL DEFAULT 0,
    compare_at   REAL NOT NULL DEFAULT 0,
    total_lbs    REAL NOT NULL DEFAULT 0,
    icon         TEXT NOT NULL DEFAULT 'box',
    featured     INTEGER NOT NULL DEFAULT 0,
    deal_rank    INTEGER NOT NULL DEFAULT 0,
    sort_order   INTEGER NOT NULL DEFAULT 0,
    active       INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS package_items (
    id         INTEGER PRIMARY KEY,
    package_id INTEGER NOT NULL REFERENCES packages(id) ON DELETE CASCADE,
    cut_id     INTEGER NOT NULL REFERENCES cuts(id) ON DELETE CASCADE,
    qty        REAL NOT NULL DEFAULT 1,
    note       TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_package_items_pkg ON package_items(package_id);

CREATE TABLE IF NOT EXISTS shares (
    id             INTEGER PRIMARY KEY,
    slug           TEXT UNIQUE NOT NULL,
    tier           TEXT NOT NULL,
    name           TEXT NOT NULL,
    hanging_lbs    REAL NOT NULL DEFAULT 0,
    takehome_lbs   REAL NOT NULL DEFAULT 0,
    price          REAL NOT NULL DEFAULT 0,
    deposit        REAL NOT NULL DEFAULT 0,
    price_per_lb   REAL NOT NULL DEFAULT 0,
    blurb          TEXT NOT NULL DEFAULT '',
    household_limit INTEGER NOT NULL DEFAULT 1,
    icon           TEXT NOT NULL DEFAULT 'cow',
    sort_order     INTEGER NOT NULL DEFAULT 0,
    active         INTEGER NOT NULL DEFAULT 1
);

-- ---------------------------------------------------------------------------
-- packing options: wrap style, portioning, bagging, gift wrap, extras
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS packing_groups (
    id         INTEGER PRIMARY KEY,
    code       TEXT UNIQUE NOT NULL,
    label      TEXT NOT NULL,
    blurb      TEXT NOT NULL DEFAULT '',
    scope      TEXT NOT NULL DEFAULT 'order',
    sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS packing_options (
    id         INTEGER PRIMARY KEY,
    group_code TEXT NOT NULL REFERENCES packing_groups(code) ON DELETE CASCADE,
    code       TEXT NOT NULL,
    label      TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    price_mode TEXT NOT NULL DEFAULT 'per_lb',
    amount     REAL NOT NULL DEFAULT 0,
    applies_to TEXT NOT NULL DEFAULT 'all',
    is_default INTEGER NOT NULL DEFAULT 0,
    icon       TEXT NOT NULL DEFAULT 'box',
    sort_order INTEGER NOT NULL DEFAULT 0,
    UNIQUE(group_code, code)
);

-- ---------------------------------------------------------------------------
-- pricing rules and their audit trail
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS price_rules (
    id           INTEGER PRIMARY KEY,
    scope_type   TEXT NOT NULL DEFAULT 'global',
    scope_value  TEXT NOT NULL DEFAULT '',
    discount_pct REAL NOT NULL DEFAULT 20,
    label        TEXT NOT NULL DEFAULT '',
    active       INTEGER NOT NULL DEFAULT 1,
    priority     INTEGER NOT NULL DEFAULT 0,
    created_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS price_audits (
    id          INTEGER PRIMARY KEY,
    action      TEXT NOT NULL,
    scope       TEXT NOT NULL DEFAULT '',
    target_json TEXT NOT NULL DEFAULT '{}',
    before_json TEXT NOT NULL DEFAULT '{}',
    after_json  TEXT NOT NULL DEFAULT '{}',
    summary     TEXT NOT NULL DEFAULT '',
    actor       TEXT NOT NULL DEFAULT 'system',
    draft_id    INTEGER,
    reverted_at TEXT,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_price_audits_created ON price_audits(created_at);

CREATE TABLE IF NOT EXISTS price_drafts (
    id           INTEGER PRIMARY KEY,
    scope        TEXT NOT NULL DEFAULT 'all',
    payload_json TEXT NOT NULL DEFAULT '{}',
    note         TEXT NOT NULL DEFAULT '',
    actor        TEXT NOT NULL DEFAULT 'system',
    published_at TEXT,
    created_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ---------------------------------------------------------------------------
-- market prices
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS market_prices (
    id          INTEGER PRIMARY KEY,
    series_key  TEXT NOT NULL,
    label       TEXT NOT NULL,
    source      TEXT NOT NULL,
    region      TEXT NOT NULL DEFAULT 'National',
    value       REAL NOT NULL DEFAULT 0,
    unit        TEXT NOT NULL DEFAULT 'lb',
    observed_at TEXT NOT NULL,
    fetched_at  TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(series_key, source, observed_at)
);
CREATE INDEX IF NOT EXISTS idx_market_series ON market_prices(series_key);

CREATE TABLE IF NOT EXISTS local_observations (
    id          INTEGER PRIMARY KEY,
    series_key  TEXT NOT NULL,
    store       TEXT NOT NULL,
    value       REAL NOT NULL DEFAULT 0,
    unit        TEXT NOT NULL DEFAULT 'lb',
    observed_at TEXT NOT NULL,
    note        TEXT NOT NULL DEFAULT '',
    actor       TEXT NOT NULL DEFAULT 'admin',
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_local_obs_series ON local_observations(series_key);

-- ---------------------------------------------------------------------------
-- carts
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS carts (
    id         TEXT PRIMARY KEY,
    email      TEXT NOT NULL DEFAULT '',
    packing_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS cart_items (
    id         INTEGER PRIMARY KEY,
    cart_id    TEXT NOT NULL REFERENCES carts(id) ON DELETE CASCADE,
    item_type  TEXT NOT NULL,
    ref_id     INTEGER NOT NULL,
    qty        REAL NOT NULL DEFAULT 1,
    packing_json TEXT NOT NULL DEFAULT '{}',
    note       TEXT NOT NULL DEFAULT '',
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_cart_items_cart ON cart_items(cart_id);

-- ---------------------------------------------------------------------------
-- fulfillment slots. Capacity is measured in pounds, not order count: a
-- 79 lb share and a 1 lb ground beef pack are not the same thing to haul.
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS slots (
    id           INTEGER PRIMARY KEY,
    kind         TEXT NOT NULL DEFAULT 'pickup',
    service_date TEXT NOT NULL,
    window_start TEXT NOT NULL,
    window_end   TEXT NOT NULL,
    capacity_lbs REAL NOT NULL DEFAULT 0,
    reserved_lbs REAL NOT NULL DEFAULT 0,
    cutoff_at    TEXT NOT NULL DEFAULT '',
    label        TEXT NOT NULL DEFAULT '',
    active       INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_slots_date ON slots(service_date, kind);

-- ---------------------------------------------------------------------------
-- orders
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS orders (
    id            INTEGER PRIMARY KEY,
    code          TEXT UNIQUE NOT NULL,
    email         TEXT NOT NULL DEFAULT '',
    phone         TEXT NOT NULL DEFAULT '',
    customer_name TEXT NOT NULL DEFAULT '',
    fulfillment   TEXT NOT NULL DEFAULT 'pickup',
    address_json  TEXT NOT NULL DEFAULT '{}',
    county        TEXT NOT NULL DEFAULT '',
    slot_id       INTEGER REFERENCES slots(id) ON DELETE SET NULL,
    subtotal      REAL NOT NULL DEFAULT 0,
    packing_total REAL NOT NULL DEFAULT 0,
    delivery_fee  REAL NOT NULL DEFAULT 0,
    discount_total REAL NOT NULL DEFAULT 0,
    tax_total     REAL NOT NULL DEFAULT 0,
    total         REAL NOT NULL DEFAULT 0,
    savings_total REAL NOT NULL DEFAULT 0,
    market_snapshot_json TEXT NOT NULL DEFAULT '{}',
    packing_json  TEXT NOT NULL DEFAULT '{}',
    terms_version TEXT NOT NULL DEFAULT '',
    payment_ref   TEXT NOT NULL DEFAULT '',
    payment_status TEXT NOT NULL DEFAULT 'pending',
    sub_id        INTEGER,
    customer_id   INTEGER REFERENCES customers(id) ON DELETE SET NULL,
    referral_code TEXT NOT NULL DEFAULT '',
    notes         TEXT NOT NULL DEFAULT '',
    status        TEXT NOT NULL DEFAULT 'placed',
    created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_orders_email ON orders(email);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);

CREATE TABLE IF NOT EXISTS order_items (
    id           INTEGER PRIMARY KEY,
    order_id     INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    item_type    TEXT NOT NULL,
    ref_id       INTEGER NOT NULL,
    store_slug   TEXT NOT NULL DEFAULT 'beef',
    name         TEXT NOT NULL,
    qty          REAL NOT NULL DEFAULT 1,
    unit         TEXT NOT NULL DEFAULT 'lb',
    unit_price   REAL NOT NULL DEFAULT 0,
    line_total   REAL NOT NULL DEFAULT 0,
    packing_total REAL NOT NULL DEFAULT 0,
    market_price REAL NOT NULL DEFAULT 0,
    savings      REAL NOT NULL DEFAULT 0,
    packing_json TEXT NOT NULL DEFAULT '{}',
    note         TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);

-- ---------------------------------------------------------------------------
-- subscriptions
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS subscribers (
    id            INTEGER PRIMARY KEY,
    email         TEXT UNIQUE NOT NULL,
    name          TEXT NOT NULL DEFAULT '',
    cadence       TEXT NOT NULL DEFAULT 'monthly',
    discount_pct  REAL NOT NULL DEFAULT 5,
    free_delivery INTEGER NOT NULL DEFAULT 1,
    status        TEXT NOT NULL DEFAULT 'active',
    token         TEXT UNIQUE NOT NULL,
    pack_profile_json TEXT NOT NULL DEFAULT '{}',
    next_date     TEXT NOT NULL DEFAULT '',
    created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS subscriptions (
    id            INTEGER PRIMARY KEY,
    subscriber_id INTEGER NOT NULL REFERENCES subscribers(id) ON DELETE CASCADE,
    order_id      INTEGER REFERENCES orders(id) ON DELETE SET NULL,
    items_json    TEXT NOT NULL DEFAULT '[]',
    status        TEXT NOT NULL DEFAULT 'active',
    cadence       TEXT NOT NULL DEFAULT 'monthly',
    skips         INTEGER NOT NULL DEFAULT 0,
    next_date     TEXT NOT NULL DEFAULT '',
    created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_subs_subscriber ON subscriptions(subscriber_id);

CREATE TABLE IF NOT EXISTS subscription_events (
    id            INTEGER PRIMARY KEY,
    subscription_id INTEGER NOT NULL REFERENCES subscriptions(id) ON DELETE CASCADE,
    event         TEXT NOT NULL,
    detail        TEXT NOT NULL DEFAULT '',
    created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ---------------------------------------------------------------------------
-- share campaigns: a whole cow is split across households so that no single
-- sale exceeds half a carcass.
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS share_campaigns (
    id            INTEGER PRIMARY KEY,
    slug          TEXT UNIQUE NOT NULL,
    name          TEXT NOT NULL,
    tier          TEXT NOT NULL DEFAULT 'whole',
    drop_date     TEXT NOT NULL DEFAULT '',
    total_lbs     REAL NOT NULL DEFAULT 0,
    price_per_household REAL NOT NULL DEFAULT 0,
    household_target INTEGER NOT NULL DEFAULT 4,
    share_tier    TEXT NOT NULL DEFAULT 'quarter',
    blurb         TEXT NOT NULL DEFAULT '',
    status        TEXT NOT NULL DEFAULT 'open',
    created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS campaign_households (
    id            INTEGER PRIMARY KEY,
    campaign_id   INTEGER NOT NULL REFERENCES share_campaigns(id) ON DELETE CASCADE,
    order_id      INTEGER REFERENCES orders(id) ON DELETE SET NULL,
    share_id      INTEGER REFERENCES shares(id) ON DELETE SET NULL,
    name          TEXT NOT NULL DEFAULT '',
    email         TEXT NOT NULL DEFAULT '',
    phone         TEXT NOT NULL DEFAULT '',
    status        TEXT NOT NULL DEFAULT 'reserved',
    note          TEXT NOT NULL DEFAULT '',
    created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_campaign_households_campaign ON campaign_households(campaign_id);

-- ---------------------------------------------------------------------------
-- site content, terms, social links, reviews, waitlist
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS site_content (
    key        TEXT PRIMARY KEY,
    value_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS terms_versions (
    id         INTEGER PRIMARY KEY,
    version    TEXT UNIQUE NOT NULL,
    title      TEXT NOT NULL,
    body       TEXT NOT NULL,
    effective  TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS social_links (
    id         INTEGER PRIMARY KEY,
    label      TEXT NOT NULL,
    url        TEXT NOT NULL,
    kind       TEXT NOT NULL DEFAULT 'sibling',
    blurb      TEXT NOT NULL DEFAULT '',
    icon       TEXT NOT NULL DEFAULT 'link',
    sort_order INTEGER NOT NULL DEFAULT 0,
    active     INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS reviews (
    id         INTEGER PRIMARY KEY,
    order_id   INTEGER REFERENCES orders(id) ON DELETE SET NULL,
    email      TEXT NOT NULL DEFAULT '',
    rating     INTEGER NOT NULL DEFAULT 5,
    body       TEXT NOT NULL DEFAULT '',
    cut_slug   TEXT NOT NULL DEFAULT '',
    published  INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS waitlist (
    id         INTEGER PRIMARY KEY,
    email      TEXT NOT NULL,
    item_type  TEXT NOT NULL DEFAULT 'cut',
    ref_id     INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(email, item_type, ref_id)
);

-- ---------------------------------------------------------------------------
-- admin and audit
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS admins (
    id       INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    passhash TEXT NOT NULL,
    role     TEXT NOT NULL DEFAULT 'owner',
    full_access INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ---------------------------------------------------------------------------
-- customer accounts. Email + password, with the profile and preferences the
-- account pages edit. Orders link by customer_id; older orders fall back to
-- the email on the order.
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS customers (
    id            INTEGER PRIMARY KEY,
    email         TEXT UNIQUE NOT NULL,
    passhash      TEXT NOT NULL,
    name          TEXT NOT NULL DEFAULT '',
    phone         TEXT NOT NULL DEFAULT '',
    email_verified INTEGER NOT NULL DEFAULT 0,
    verified_at   TEXT NOT NULL DEFAULT '',
    fulfillment   TEXT NOT NULL DEFAULT 'pickup',
    address_json  TEXT NOT NULL DEFAULT '{}',
    county        TEXT NOT NULL DEFAULT '',
    delivery_notes TEXT NOT NULL DEFAULT '',
    recurring_day INTEGER NOT NULL DEFAULT 0,
    contact_method TEXT NOT NULL DEFAULT 'email',
    market_updates INTEGER NOT NULL DEFAULT 0,
    created_at    TEXT NOT NULL DEFAULT (datetime('now')),
    last_login    TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);

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

-- ---------------------------------------------------------------------------
-- co-op stores and their products. Beef keeps its own specialised tables
-- (cuts, packages, shares, campaigns); every other business sells generic
-- products through these two tables so the admin, cart, and checkout stay
-- shared.
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS stores (
    slug        TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    tagline     TEXT NOT NULL DEFAULT '',
    description TEXT NOT NULL DEFAULT '',
    icon        TEXT NOT NULL DEFAULT 'box',
    accent      TEXT NOT NULL DEFAULT 'grass',
    sort_order  INTEGER NOT NULL DEFAULT 0,
    active      INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS products (
    id          INTEGER PRIMARY KEY,
    store_slug  TEXT NOT NULL REFERENCES stores(slug) ON DELETE CASCADE,
    slug        TEXT NOT NULL,
    name        TEXT NOT NULL,
    kind        TEXT NOT NULL DEFAULT 'item',
    unit        TEXT NOT NULL DEFAULT 'each',
    unit_lbs    REAL NOT NULL DEFAULT 0,
    price       REAL NOT NULL DEFAULT 0,
    compare_at  REAL NOT NULL DEFAULT 0,
    compare_brand TEXT NOT NULL DEFAULT '',
    compare_size TEXT NOT NULL DEFAULT '',
    compare_url TEXT NOT NULL DEFAULT '',
    compare_observed_at TEXT NOT NULL DEFAULT '',
    image       TEXT NOT NULL DEFAULT '',
    icon        TEXT NOT NULL DEFAULT 'box',
    blurb       TEXT NOT NULL DEFAULT '',
    serving     TEXT NOT NULL DEFAULT '',
    stock       REAL NOT NULL DEFAULT 0,
    tags        TEXT NOT NULL DEFAULT '',
    featured    INTEGER NOT NULL DEFAULT 0,
    active      INTEGER NOT NULL DEFAULT 1,
    sort_order  INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(store_slug, slug)
);
CREATE INDEX IF NOT EXISTS idx_products_store ON products(store_slug);
CREATE INDEX IF NOT EXISTS idx_products_active ON products(active);

-- ---------------------------------------------------------------------------
-- product variants: packaged sizes for the same item (pint, quart, half
-- gallon, 5 gallon, 10 gallon). Each variant carries its own price, stock
-- and optional benchmark comparison so the co-op can discount bulk sizes.
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS product_variants (
    id          INTEGER PRIMARY KEY,
    product_id  INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    size_label  TEXT NOT NULL DEFAULT 'Each',
    unit        TEXT NOT NULL DEFAULT 'each',
    unit_lbs    REAL NOT NULL DEFAULT 0,
    price       REAL NOT NULL DEFAULT 0,
    compare_at  REAL NOT NULL DEFAULT 0,
    stock       REAL NOT NULL DEFAULT 0,
    sort_order  INTEGER NOT NULL DEFAULT 0,
    active      INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_product_variants_product
    ON product_variants(product_id);
CREATE UNIQUE INDEX IF NOT EXISTS idx_product_variants_size
    ON product_variants(product_id, size_label);

-- ---------------------------------------------------------------------------
-- community events: canning / fermenting workshops and other co-op
-- gatherings, editable from the admin console.
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS events (
    id          INTEGER PRIMARY KEY,
    title       TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    event_date  TEXT NOT NULL DEFAULT '',
    start_time  TEXT NOT NULL DEFAULT '',
    end_time    TEXT NOT NULL DEFAULT '',
    location    TEXT NOT NULL DEFAULT '',
    capacity    INTEGER NOT NULL DEFAULT 0,
    active      INTEGER NOT NULL DEFAULT 1,
    sort_order  INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_events_date ON events(event_date);
CREATE UNIQUE INDEX IF NOT EXISTS idx_events_title ON events(title);

-- ---------------------------------------------------------------------------
-- per-store admin access. An admin with no rows here has full access (owner).
-- Otherwise they may only touch the stores listed for them.
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS admin_store_access (
    admin_id   INTEGER NOT NULL REFERENCES admins(id) ON DELETE CASCADE,
    store_slug TEXT NOT NULL REFERENCES stores(slug) ON DELETE CASCADE,
    PRIMARY KEY (admin_id, store_slug)
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
    _migrate(conn)
    conn.execute(
        "INSERT INTO meta(key, value) VALUES('schema_version', ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (str(SCHEMA_VERSION),),
    )
    conn.commit()


#: Columns added after the first release. CREATE TABLE IF NOT EXISTS will not
#: add a column to a table that already exists, so new ones are listed here
#: and applied with ALTER TABLE when the database is older.
_MIGRATIONS: tuple[tuple[str, str, str], ...] = (
    ("campaign_households", "share_id", "INTEGER REFERENCES shares(id) ON DELETE SET NULL"),
    ("orders", "customer_id", "INTEGER REFERENCES customers(id) ON DELETE SET NULL"),
    ("social_links", "store_slug", "TEXT NOT NULL DEFAULT 'beef'"),
    ("admins", "full_access", "INTEGER NOT NULL DEFAULT 1"),
    ("products", "icon", "TEXT NOT NULL DEFAULT 'box'"),
    ("products", "compare_brand", "TEXT NOT NULL DEFAULT ''"),
    ("products", "compare_size", "TEXT NOT NULL DEFAULT ''"),
    ("products", "compare_url", "TEXT NOT NULL DEFAULT ''"),
    ("products", "compare_observed_at", "TEXT NOT NULL DEFAULT ''"),
    ("order_items", "store_slug", "TEXT NOT NULL DEFAULT 'beef'"),
    ("cart_items", "variant_id", "INTEGER REFERENCES product_variants(id) ON DELETE SET NULL"),
    ("order_items", "variant_id", "INTEGER REFERENCES product_variants(id) ON DELETE SET NULL"),
)


def _migrate(conn: sqlite3.Connection) -> None:
    for table, column, declaration in _MIGRATIONS:
        try:
            existing = {row["name"] for row in conn.execute(
                f"PRAGMA table_info({table})")}
        except sqlite3.Error:
            continue
        if existing and column not in existing:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {declaration}")


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


def log_audit(conn: sqlite3.Connection, action: str, entity: str = "",
              entity_id: str = "", detail: str = "", actor: str = "system") -> None:
    conn.execute(
        "INSERT INTO audit_log(actor, action, entity, entity_id, detail_json) "
        "VALUES(?, ?, ?, ?, ?)",
        (actor, action, entity, str(entity_id), detail or "{}"),
    )


# --------------------------------------------------------------------------
# site content: small editable values the shop owner changes without a deploy
# --------------------------------------------------------------------------

def content(conn: sqlite3.Connection, key: str, default: Any = None) -> Any:
    import json
    row = one(conn, "SELECT value_json FROM site_content WHERE key = ?", (key,))
    if not row:
        return default
    try:
        return json.loads(row["value_json"])
    except (ValueError, TypeError):
        return default


def set_content(conn: sqlite3.Connection, key: str, value: Any) -> None:
    import json
    conn.execute(
        "INSERT INTO site_content(key, value_json) VALUES(?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value_json = excluded.value_json, "
        "updated_at = datetime('now')",
        (key, json.dumps(value)),
    )
    conn.commit()
