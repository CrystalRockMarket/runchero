"""Seed the depot.

    python3 -m app.seed.run            # fill the database and the archive
    python3 -m app.seed.run --no-fetch # skip the downloads (offline)

The script is idempotent: it can be run again at any time without duplicating
anything. Book files already present in the archive are left alone.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from .. import config, db
from . import books as book_data
from . import books_deep
from . import books_extra
from . import books_from_download
from . import books_from_staged
from . import collections as collection_data
from . import content
from . import formulas as formula_data
from . import manuals as manual_data
from . import sources as source_data

USER_AGENT = ("Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 "
              "Firefox/128.0 (Runchero Information Depo archive fetcher)")
TEXT_URL = "https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt"
ALT_URL = "https://www.gutenberg.org/files/{id}/{id}-0.txt"
MAX_BYTES = 6 * 1024 * 1024


# --------------------------------------------------------------------------
# fetching
# --------------------------------------------------------------------------
def _fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read(MAX_BYTES)


def fetch_text(gutenberg_id: int) -> bytes:
    last_error: Exception | None = None
    for template in (TEXT_URL, ALT_URL):
        url = template.format(id=gutenberg_id)
        try:
            return _fetch(url)
        except (urllib.error.URLError, OSError, TimeoutError) as error:
            last_error = error
            time.sleep(1.5)
    raise RuntimeError(f"could not fetch {gutenberg_id}: {last_error}")


def strip_boilerplate(raw: bytes) -> str:
    text = raw.decode("utf-8", errors="replace")
    start = text.find("*** START OF")
    if start != -1:
        end_of_header = text.find("\n", start)
        text = text[end_of_header + 1:] if end_of_header != -1 else text
    end = text.find("*** END OF")
    if end != -1:
        text = text[:end]
    return text.strip() + "\n"


def guess_year(text: str) -> int | None:
    """Find the publication year on the title page."""
    head = text[:4000]
    years = re.findall(r"\b(1[5-9]\d\d)\b", head)
    if not years:
        return None
    counts: dict[int, int] = {}
    for value in years:
        year = int(value)
        counts[year] = counts.get(year, 0) + 1
    best = max(counts, key=lambda y: (counts[y], -abs(y - 1900)))
    return best


def estimate_pages(text: str) -> int:
    words = len(text.split())
    return max(1, round(words / 250))


# --------------------------------------------------------------------------
# database writers
# --------------------------------------------------------------------------
def seed_categories(conn) -> dict[str, int]:
    for (slug, name, icon, accent, kind, parent, blurb, order) in content.CATEGORIES:
        conn.execute(
            "INSERT INTO categories(slug, name, icon, accent, kind, parent_id, blurb, sort_order) "
            "VALUES(?,?,?,?,?,NULL,?,?) ON CONFLICT(slug) DO UPDATE SET "
            "name=excluded.name, icon=excluded.icon, accent=excluded.accent, "
            "kind=excluded.kind, blurb=excluded.blurb, sort_order=excluded.sort_order",
            (slug, name, icon, accent, kind, blurb, order),
        )
    ids = {row["slug"]: row["id"] for row in
           db.rows(conn, "SELECT id, slug FROM categories")}
    for (slug, _n, _i, _a, _k, parent, _b, _o) in content.CATEGORIES:
        if parent:
            conn.execute("UPDATE categories SET parent_id = ? WHERE slug = ?",
                         (ids[parent], slug))
    return ids


def seed_vehicles(conn, category_ids) -> None:
    for (slug, kind, make, model, y_from, y_to, engine, drive, power,
         notes, cat) in content.VEHICLES:
        conn.execute(
            "INSERT INTO vehicles(slug, kind, make, model, year_from, year_to, "
            "engine, drive, power, notes, origin, category_id) VALUES(?,?,?,?,?,?,?,?,?,?,?,?) "
            "ON CONFLICT(slug) DO UPDATE SET kind=excluded.kind, make=excluded.make, "
            "model=excluded.model, year_from=excluded.year_from, year_to=excluded.year_to, "
            "engine=excluded.engine, drive=excluded.drive, power=excluded.power, "
            "notes=excluded.notes, category_id=excluded.category_id",
            (slug, kind, make, model, y_from, y_to, engine, drive, power, notes,
             "ai-organized", category_ids.get(cat)),
        )


def seed_glossary(conn) -> None:
    for term, definition, category, icon in content.GLOSSARY:
        conn.execute(
            "INSERT INTO glossary(term, definition, category, icon) VALUES(?,?,?,?) "
            "ON CONFLICT(term) DO UPDATE SET definition=excluded.definition, "
            "category=excluded.category, icon=excluded.icon",
            (term, definition, category, icon),
        )


def seed_calendar(conn) -> None:
    conn.execute("DELETE FROM calendar")
    for month, crop, task, icon in content.CALENDAR:
        conn.execute(
            "INSERT INTO calendar(month, region, crop, task, icon) VALUES(?,?,?,?,?)",
            (month, "temperate", crop, task, icon),
        )


def seed_books(conn, category_ids, fetch: bool = True,
               everything: bool = False) -> tuple[int, int, int]:
    archive = config.ARCHIVE_DIR / "books"
    archive.mkdir(parents=True, exist_ok=True)
    fetched = 0
    cached = 0
    deep_slugs = {b[1] for b in books_deep.BOOKS}
    catalogue = [*book_data.BOOKS, *books_deep.BOOKS, *books_extra.BOOKS, *books_from_download.BOOKS, *books_from_staged.BOOKS]
    if not everything:
        # The curated shelves, the demo deep-dives, plus any extra book already
        # on disk. That way a bigger archive is never thrown away by a reseed.
        catalogue = [b for b in catalogue
                     if b[1] in book_data.CURATED
                     or b[1] in deep_slugs
                     or b in books_from_download.BOOKS
                     or b in books_from_staged.BOOKS
                     or (archive / f"{b[1]}.txt").exists()]
    for (gid, slug, title, author, category, summary, motif, base, accent,
         year) in catalogue:
        target = archive / f"{slug}.txt"
        raw: bytes | None = None
        if target.exists() and target.stat().st_size > 0:
            raw = target.read_bytes()
            cached += 1
        elif fetch:
            try:
                raw = fetch_text(gid)
                target.write_bytes(raw)
                fetched += 1
                time.sleep(0.7)
            except Exception as error:  # noqa: BLE001 - keep seeding the rest
                print(f"  ! {slug}: {error}")
                raw = None
        text = strip_boilerplate(raw) if raw else ""
        digest = hashlib.sha256(raw).hexdigest() if raw else ""
        if not year:
            year = guess_year(text) if text else None
        theme = {
            "lib-agriculture": "farming", "lib-livestock": "livestock",
            "lib-machinery": "engineering", "lib-rural": "rural",
            "lib-craft": "making", "lib-kitchen": "cooking",
            "lib-science": "science", "lib-health": "health",
            "lib-money": "business", "lib-survival": "survival",
            "lib-manuals": "manuals",
        }.get(category, "general")
        conn.execute(
            "INSERT INTO books(slug, title, author, publisher, year, language, "
            "category_id, format, pages, bytes, sha256, rel_path, summary, source, "
            "source_url, license, motif, base, accent, theme) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
            "ON CONFLICT(slug) DO UPDATE SET title=excluded.title, author=excluded.author, "
            "year=excluded.year, category_id=excluded.category_id, pages=excluded.pages, "
            "bytes=excluded.bytes, sha256=excluded.sha256, rel_path=excluded.rel_path, "
            "summary=excluded.summary, motif=excluded.motif, base=excluded.base, "
            "accent=excluded.accent, theme=excluded.theme",
            (slug, title, author, "Project Gutenberg", year, "en",
             category_ids.get(category), "TEXT", estimate_pages(text) if text else None,
             len(raw) if raw else 0, digest, f"books/{slug}.txt", summary,
             "gutenberg", f"https://www.gutenberg.org/ebooks/{gid}",
             "Public domain (Project Gutenberg)", motif, base, accent, theme),
        )
    keep = {b[1] for b in catalogue}
    keep.update(m["slug"] for m in manual_data.MANUALS)
    for row in conn.execute("SELECT slug FROM books").fetchall():
        if row["slug"] not in keep:
            conn.execute("DELETE FROM books WHERE slug = ?", (row["slug"],))
    return fetched, cached, len(catalogue)


def seed_formulas(conn) -> int:
    for order, topic in enumerate(formula_data.TOPICS, start=1):
        conn.execute(
            "INSERT INTO formula_topics(slug, name, blurb, sort_order) "
            "VALUES(?,?,?,?) ON CONFLICT(slug) DO UPDATE SET name=excluded.name, "
            "blurb=excluded.blurb, sort_order=excluded.sort_order",
            (topic["slug"], topic["name"], topic["blurb"], order),
        )
    for item in formula_data.FORMULAS:
        conn.execute(
            "INSERT INTO formulas(slug, name, topic, expression, symbols, units, "
            "how, example, tags, origin) VALUES(?,?,?,?,?,?,?,?,?,?) "
            "ON CONFLICT(slug) DO UPDATE SET name=excluded.name, "
            "topic=excluded.topic, expression=excluded.expression, "
            "symbols=excluded.symbols, units=excluded.units, how=excluded.how, "
            "example=excluded.example, tags=excluded.tags",
            (item["slug"], item["name"], item["topic"], item["expression"],
             item["symbols"], item["units"], item["how"], item["example"],
             item["tags"], "ai-organized"),
        )
    return len(formula_data.FORMULAS)


# --------------------------------------------------------------------------
# manuals and provenance
# --------------------------------------------------------------------------
def seed_manuals(conn, category_ids) -> int:
    archive = config.ARCHIVE_DIR / "books"
    category_id = category_ids.get("lib-manuals")
    for item in manual_data.MANUALS:
        path = archive / item["file"]
        raw = path.read_bytes() if path.exists() else b""
        text = raw.decode("utf-8", errors="replace") if raw else ""
        digest = hashlib.sha256(raw).hexdigest() if raw else ""
        coverage = ", ".join(v.replace("ford-", "Ford ") for v in item["vehicles"])
        summary = item.get("summary") or (
            f"Factory service manual for {item['title']}. OCR text from a "
            "public-domain Internet Archive scan; open the original PDF for "
            "photographs, diagrams and exact specifications."
        )
        if coverage:
            summary += f" Covers {coverage}."
        conn.execute(
            "INSERT INTO books(slug, title, author, publisher, year, language, "
            "category_id, format, pages, bytes, sha256, rel_path, summary, source, "
            "source_url, license, motif, base, accent, theme) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
            "ON CONFLICT(slug) DO UPDATE SET title=excluded.title, "
            "author=excluded.author, publisher=excluded.publisher, year=excluded.year, "
            "category_id=excluded.category_id, format=excluded.format, pages=excluded.pages, "
            "bytes=excluded.bytes, sha256=excluded.sha256, rel_path=excluded.rel_path, "
            "summary=excluded.summary, source=excluded.source, source_url=excluded.source_url, "
            "license=excluded.license, motif=excluded.motif, base=excluded.base, "
            "accent=excluded.accent, theme=excluded.theme",
            (item["slug"], item["title"], item["author"],
             item.get("publisher", item["author"]),
             item["year"], "en", category_id, "MANUAL",
             estimate_pages(text) if text else None, len(raw), digest,
             f"books/{item['file']}", summary, "Internet Archive", item["pdf"],
             item.get("license", "Public Domain Mark 1.0 (Internet Archive)"),
             item.get("motif", "tractor"), item.get("base", "sky2"),
             item.get("accent", "sun"), "manuals"),
        )
        book_id = db.scalar(conn, "SELECT id FROM books WHERE slug = ?", (item["slug"],))
        conn.execute("DELETE FROM book_vehicles WHERE book_id = ?", (book_id,))
        for vehicle_slug in item["vehicles"]:
            vehicle_id = db.scalar(conn, "SELECT id FROM vehicles WHERE slug = ?",
                                   (vehicle_slug,))
            if vehicle_id:
                conn.execute(
                    "INSERT OR IGNORE INTO book_vehicles(book_id, vehicle_id) VALUES(?,?)",
                    (book_id, vehicle_id),
                )
    return len(manual_data.MANUALS)


def _upsert_source(conn, source: dict) -> int:
    conn.execute(
        "INSERT INTO sources(slug, title, author, kind, url, license, book_slug, note) "
        "VALUES(?,?,?,?,?,?,?,?) ON CONFLICT(slug) DO UPDATE SET "
        "title=excluded.title, author=excluded.author, kind=excluded.kind, "
        "url=excluded.url, license=excluded.license, book_slug=excluded.book_slug, "
        "note=excluded.note",
        (source["slug"], source["title"], source.get("author", ""),
         source.get("kind", "other"), source.get("url", ""),
         source.get("license", ""), source.get("book_slug", ""),
         source.get("note", "")),
    )
    return int(db.scalar(conn, "SELECT id FROM sources WHERE slug = ?", (source["slug"],)))


def _cite(conn, page_kind: str, page_slug: str, source_id: int,
          role: str = "background", locator: str = "", note: str = "") -> None:
    conn.execute(
        "DELETE FROM citations WHERE page_kind=? AND page_slug=? "
        "AND source_id=?",
        (page_kind, page_slug, source_id),
    )
    conn.execute(
        "INSERT INTO citations(page_kind, page_slug, source_id, role, "
        "locator, note) VALUES(?,?,?,?,?,?)",
        (page_kind, page_slug, source_id, role, locator, note),
    )


def seed_sources(conn) -> int:
    """Write provenance for the surviving indexes and the factory manuals."""
    conn.execute("DELETE FROM citations WHERE page_kind = 'article'")
    conn.execute("DELETE FROM sources WHERE kind = 'ai-generated'")

    ai = {source["slug"]: _upsert_source(conn, source)
          for source in source_data.AI_SOURCES}
    ai_vehicle = ai[source_data.AI_VEHICLE["slug"]]
    ai_formula = ai[source_data.AI_FORMULA["slug"]]
    ai_topic = ai[source_data.AI_TOPIC["slug"]]
    ai_reference = ai[source_data.AI_REFERENCE["slug"]]

    for row in conn.execute("SELECT slug FROM vehicles"):
        _cite(conn, "vehicle", row["slug"], ai_vehicle, "index",
              "AI-organised equipment record",
              "Settings must be checked against the factory manual.")
    for row in conn.execute("SELECT slug FROM formulas"):
        _cite(conn, "formula", row["slug"], ai_formula, "index",
              "AI-organised formula index",
              "Double-check any safety-critical result.")
    for page_kind, page_slug, source_slug in source_data.STATIC_PAGES:
        _cite(conn, page_kind, page_slug, ai[source_slug], "index",
              "AI-organised depot index",
              "The index is AI-organised; the linked sources are not.")
    _cite(conn, "page", "conversions", ai_reference, "index",
          "AI-organised conversion tables", "Verify safety-critical conversions.")

    # Factory manuals: one source record per scan, then citations to the book
    # record, every model it covers, the Ford tractor guide and the manuals shelf.
    for item in manual_data.MANUALS:
        license_label = item.get("license", "Public Domain Mark 1.0 (Internet Archive)")
        source = {
            "slug": f"manual-{item['slug']}",
            "title": item["title"],
            "author": item["author"],
            "kind": "manual",
            "url": item["pdf"],
            "license": license_label.replace(" (Internet Archive)", ""),
            "book_slug": item["slug"],
            "note": "Factory scan from the Internet Archive. Read the OCR text "
                    "in the local library or open the PDF for photographs and diagrams.",
        }
        source_id = _upsert_source(conn, source)
        _cite(conn, "book", item["slug"], source_id, "primary",
              "Full OCR text and PDF", "Primary factory source.")
        for vehicle_slug in item["vehicles"]:
            _cite(conn, "vehicle", vehicle_slug, source_id, "manual",
                  "Factory manual covering this model",
                  "Use the scan for exact settings, torques and part numbers.")
        hub_slug = item.get("hub")
        if not hub_slug and item["slug"].startswith("ford-manual-"):
            hub_slug = "ford-tractors"
        if hub_slug:
            _cite(conn, "hub", hub_slug, source_id, "manual",
                  "Factory manual for Ford tractors", "")
        _cite(conn, "category", "lib-manuals", source_id, "manual",
              "Manuals shelf", "")
        _cite(conn, "page", "library-manuals", source_id, "manual",
              "Manuals shelf", "")
    return len(manual_data.MANUALS)


# --------------------------------------------------------------------------
# organised depots
# --------------------------------------------------------------------------
_STOP_TERMS = {
    "and", "the", "for", "with", "from", "into", "book", "books", "guide",
    "manual", "manuals", "practical", "complete", "treatise", "history",
}

_ROLE_WORDS = {
    "growing": ("grow", "garden", "culture", "horticulture", "vegetable", "crop",
                "seed", "plant", "orchard", "vine"),
    "soil": ("soil", "compost", "manure", "fertility", "mould", "drainage"),
    "plant-health": ("disease", "pest", "insect", "blight", "fungus", "infest"),
    "propagation": ("seed", "propagat", "nursery", "graft", "cutting"),
    "cooking": ("cook", "recipe", "kitchen", "soup", "sauce", "sallet", "salad"),
    "preserving": ("preserv", "canning", "ketchup", "pickle", "jam",
                   "jelly", "bottl"),
    "dairy": ("dairy", "milk", "cheese", "butter", "cream", "bacteriolog"),
    "health": ("disease", "doctor", "veterinar", "health", "medicine",
               "cattle plague", "abortion"),
    "breeds": ("breed", "selection", "select", "age", "teeth", "ox", "cattle"),
    "feed": ("feed", "feeding", "pasture", "hay", "silage", "forage", "grain"),
    "kitchen": ("cook", "meat", "butcher", "sausage", "curing", "slaughter",
                "canning", "carving"),
    "mechanic": ("mechanic", "engine", "motor", "tractor", "repair"),
    "building": ("build", "barn", "shed", "fence", "carpent", "timber"),
    "water": ("water", "irrigat", "pump", "well", "drain"),
    "health-home": ("health", "medicine", "nurse", "hygiene", "first aid"),
    "survival": ("survival", "camp", "shelter", "forag", "emergency"),
}


def _role_for(item: dict, book) -> str:
    text = f"{book['title']} {book['summary']} {book['category']}".lower()
    kind = item["kind"]
    if kind == "crop":
        order = ("plant-health", "preserving", "cooking", "soil", "propagation")
        fallback = "growing"
    elif kind == "animal":
        order = ("health", "dairy", "kitchen", "feed", "breeds")
        fallback = "husbandry"
    else:
        group = item["group_slug"]
        if group == "kitchen":
            if item["slug"] == "butchery":
                order = ("kitchen", "preserving", "dairy", "cooking")
            elif item["slug"] == "dairy":
                order = ("dairy", "preserving", "kitchen", "cooking")
            else:
                order = ("preserving", "dairy", "kitchen", "cooking")
            fallback = "kitchen"
        elif group == "workshop":
            order = ("mechanic", "building", "water")
            fallback = "reference"
        elif group == "survival":
            order = ("survival", "health-home", "water", "building")
            fallback = "reference"
        elif group == "home":
            order = ("health-home", "kitchen", "water")
            fallback = "reference"
        else:
            order = ("soil", "water", "feed", "growing", "plant-health")
            fallback = "reference"
    for role in order:
        if any(word in text for word in _ROLE_WORDS[role]):
            return role
    return fallback


def _terms(item: dict) -> list[str]:
    raw = " ".join((item["name"], item["aliases"], item["keywords"])).lower()
    out: list[str] = []
    for piece in re.split(r"[,;/]+", raw):
        term = " ".join(piece.split()).strip(".-()")
        if len(term) >= 3 and term not in _STOP_TERMS and term not in out:
            out.append(term)
    return out


def _score_book(book, terms: list[str]) -> int:
    """Score a book on its catalogue title only.

    Matching summaries produced too many false links (a generic AI-generated
    catalogue blurb mentions "preserving" in passing). The title is the
    reliable signal for what a public-domain book is actually about.
    """
    title = book["title"].lower()
    score = 0
    for term in terms:
        if re.search(r"\b" + re.escape(term) + r"\b", title):
            score += 8
    return score


def seed_collections(conn, category_ids) -> int:
    """Build every depot index and point it at real archive books."""
    books = db.rows(
        conn,
        "SELECT b.*, c.slug AS category FROM books b "
        "LEFT JOIN categories c ON c.id = b.category_id",
    )
    by_slug = {b["slug"]: b for b in books}

    # Clear links first so a definition change never leaves stale rows behind.
    conn.execute("DELETE FROM collection_books")
    conn.execute("DELETE FROM citations WHERE page_kind = 'collection'")

    for order, item in enumerate(collection_data.COLLECTIONS, start=1):
        conn.execute(
            "INSERT INTO collections(slug, name, kind, group_slug, group_name, "
            "subgroup_slug, subgroup_name, icon, accent, summary, aliases, "
            "scientific, featured, sort_order) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
            "ON CONFLICT(slug) DO UPDATE SET name=excluded.name, kind=excluded.kind, "
            "group_slug=excluded.group_slug, group_name=excluded.group_name, "
            "subgroup_slug=excluded.subgroup_slug, subgroup_name=excluded.subgroup_name, "
            "icon=excluded.icon, accent=excluded.accent, summary=excluded.summary, "
            "aliases=excluded.aliases, scientific=excluded.scientific, "
            "featured=excluded.featured, sort_order=excluded.sort_order",
            (item["slug"], item["name"], item["kind"], item["group_slug"],
             item["group_name"], item["subgroup_slug"], item["subgroup_name"],
             item["icon"], item["accent"], item["summary"], item["aliases"],
             item["scientific"], item["featured"], order),
        )
        collection_id = int(db.scalar(
            conn, "SELECT id FROM collections WHERE slug = ?", (item["slug"],)))

        wanted: list[str] = []
        for slug in item["books"]:
            if slug in by_slug and slug not in wanted:
                wanted.append(slug)

        category = item.get("category", "")
        if category:
            for book in sorted(books, key=lambda row: row["title"]):
                if book["category"] == category and book["slug"] not in wanted:
                    wanted.append(book["slug"])

        terms = _terms(item)
        scored = []
        for book in books:
            if book["slug"] in wanted:
                continue
            if item["kind"] in ("crop", "animal") and book["category"] == "lib-manuals":
                continue
            score = _score_book(book, terms)
            if score:
                scored.append((score, book["slug"]))
        scored.sort(key=lambda pair: (-pair[0], pair[1]))
        limit = item.get("limit") or (34 if item["featured"] else 18)
        if category:
            limit = item.get("limit") or len(wanted)
        if len(wanted) > limit:
            wanted = wanted[:limit]
        for _score, slug in scored:
            if len(wanted) >= limit:
                break
            if slug not in wanted:
                wanted.append(slug)

        if len(wanted) < 5:
            fallback = {
                "crop": collection_data.FALLBACK_CROP_BOOKS,
                "animal": collection_data.FALLBACK_ANIMAL_BOOKS,
                "topic": collection_data.FALLBACK_TOPIC_BOOKS,
            }[item["kind"]]
            for slug in fallback:
                if slug in by_slug and slug not in wanted:
                    wanted.append(slug)

        for rank, slug in enumerate(wanted, start=1):
            book = by_slug[slug]
            role = _role_for(item, book)
            conn.execute(
                "INSERT OR REPLACE INTO collection_books(collection_id, book_id, "
                "role, note, rank) VALUES(?,?,?,?,?)",
                (collection_id, book["id"], role,
                 f"Indexed under {role.replace('-', ' ')}.", rank),
            )

            if book["source"] == "Internet Archive":
                source_slug = f"manual-{slug}"
            else:
                source_slug = f"book-{slug}"
            source_id = db.scalar(conn, "SELECT id FROM sources WHERE slug = ?",
                                  (source_slug,))
            if source_id is None:
                source_id = _upsert_source(conn, {
                    "slug": source_slug,
                    "title": book["title"],
                    "author": book["author"],
                    "kind": "book",
                    "url": book["source_url"] or f"/library/archive/{slug}",
                    "license": book["license"],
                    "book_slug": slug,
                    "note": "Public-domain source held in the local archive.",
                })
            _cite(conn, "collection", item["slug"], int(source_id), role,
                  "Indexed archive source", "")

    keep = {item["slug"] for item in collection_data.COLLECTIONS}
    for row in conn.execute("SELECT slug FROM collections").fetchall():
        if row["slug"] not in keep:
            conn.execute("DELETE FROM collections WHERE slug = ?", (row["slug"],))
    return len(collection_data.COLLECTIONS)


# --------------------------------------------------------------------------
# entry point
# --------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Seed the Runchero depot")
    parser.add_argument("--no-fetch", action="store_true",
                        help="do not download books (offline seeding)")
    parser.add_argument("--skip-assets", action="store_true",
                        help="do not regenerate the pixel art")
    parser.add_argument("--all-books", action="store_true",
                        help="publish the whole Gutenberg catalogue instead of "
                             "the books already on disk")
    parser.add_argument("--skip-sections", action="store_true",
                        help="do not build the chapter search index")
    parser.add_argument("--force-sections", action="store_true",
                        help="rebuild every chapter section from scratch")
    args = parser.parse_args(argv)

    config.ensure_dirs()
    conn = db.connect()
    db.init_db(conn)

    print("seeding shelves...")
    category_ids = seed_categories(conn)
    seed_vehicles(conn, category_ids)
    seed_glossary(conn)
    seed_calendar(conn)
    conn.execute("DELETE FROM articles")
    print(f"  {len(content.CATEGORIES)} categories, "
          f"{len(content.VEHICLES)} machines, {len(content.GLOSSARY)} glossary terms")

    formula_count = seed_formulas(conn)
    print(f"  {formula_count} formulas on the reference shelf")

    print("filling the archive...")
    fetched, cached, shelved = seed_books(conn, category_ids, fetch=not args.no_fetch,
                                           everything=args.all_books)
    print(f"  {fetched} downloaded, {cached} already on disk, "
          f"{shelved} books on the shelves")

    manual_count = seed_manuals(conn, category_ids)
    print(f"  {manual_count} manuals on the manuals shelf")
    seed_sources(conn)
    print("  provenance records written")

    depot_count = seed_collections(conn, category_ids)
    print(f"  {depot_count} organised depots linked to archive sources")

    if not args.skip_sections:
        print("indexing book chapters...")
        from ..sections import index_all
        section_books, section_count = index_all(
            conn, force=args.force_sections,
            progress=lambda book, n: None)
        print(f"  {section_count} chapter passages from {section_books} new books")

    if not args.skip_assets:
        print("drawing pixel art...")
        sys.path.insert(0, str(config.PROJECT_DIR))
        from tools import build_assets
        # Every published book gets a cover, otherwise the archive page shows
        # broken pictures.
        build_assets.main(["--all-books"])

    db.reindex(conn)
    conn.commit()

    stats = db.stats(conn)
    print("done:", stats)
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
