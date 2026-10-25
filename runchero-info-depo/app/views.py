"""Request handlers.

Read-only by design. Every handler renders a template or streams a file from
the archive; nothing in this module can write to the database or the disk.
"""
from __future__ import annotations

import html
import json
import re
import sqlite3
from pathlib import Path

from . import calculators, config, db, md, web
from .seed import collections as collection_data
from .seed.content import TOPIC_MAP
from .seed.formulas import COMMON as COMMON_FORMULAS

SOURCE_LABELS = {
    "ai-organized": "AI-ORGANISED INDEX",
    "book": "PUBLIC-DOMAIN BOOK",
    "manual": "FACTORY MANUAL",
    "forum": "FORUM",
    "website": "WEBSITE",
    "archive": "ARCHIVE",
    "dataset": "DATASET",
    "other": "OTHER",
}

NAV = [
    {"slug": "grow", "label": "Grow", "icon": "seedling", "href": "/grow"},
    {"slug": "animals", "label": "Animals", "icon": "cow", "href": "/animals"},
    {"slug": "farm", "label": "Farm", "icon": "wheat", "href": "/farm"},
    {"slug": "kitchen", "label": "Kitchen", "icon": "jar", "href": "/kitchen"},
    {"slug": "workshop", "label": "Workshop", "icon": "wrench", "href": "/workshop"},
    {"slug": "formulas", "label": "Formulas", "icon": "notes", "href": "/formulas"},
    {"slug": "conversions", "label": "Conversions", "icon": "clock", "href": "/conversions"},
    {"slug": "vehicles", "label": "Equipment", "icon": "tractor", "href": "/vehicles"},
    {"slug": "library", "label": "Library", "icon": "book", "href": "/library"},
    {"slug": "sources", "label": "Sources", "icon": "info", "href": "/sources"},
]

ROLE_LABELS = {
    "growing": "Growing & culture",
    "soil": "Soil, compost & fertility",
    "plant-health": "Pests, disease & plant health",
    "propagation": "Seed, grafting & propagation",
    "cooking": "Cooking & kitchen",
    "preserving": "Preserving, canning & storing",
    "dairy": "Milk, butter & cheese",
    "health": "Health & veterinary care",
    "breeds": "Breeds, selection & judging",
    "feed": "Feed, pasture & forage",
    "husbandry": "Husbandry & housing",
    "kitchen": "Slaughter, butchery & cooking",
    "mechanic": "Mechanics & engines",
    "building": "Building, fencing & woodwork",
    "water": "Water, wells & irrigation",
    "health-home": "Home health & medicine",
    "survival": "Survival & shelter",
    "reference": "Reference & general",
}

ROLE_ORDER = {role: index for index, role in enumerate(ROLE_LABELS)}

EQUIPMENT_KIND_LABELS = {
    "tractor": "Tractors",
    "machine": "Implements",
    "atv": "ATVs & quads",
    "chainsaw": "Chainsaws",
    "mower": "Mowers",
    "truck": "Trucks & transport",
    "utv": "Utility vehicles",
}
EQUIPMENT_KIND_DESCRIPTIONS = {
    "tractor": "Browse tractor manufacturers, model specifications and factory manuals.",
    "machine": "Browse implements and powered machinery used for field and yard work.",
    "atv": "Browse all-terrain vehicles and quads used around the farm.",
    "chainsaw": "Browse chainsaws and small-engine equipment.",
    "mower": "Browse mowers and grass-cutting equipment.",
    "truck": "Browse road vehicles and transport equipment.",
    "utv": "Browse utility vehicles and farm 4x4s.",
}
EQUIPMENT_KIND_ICONS = {
    "tractor": "tractor",
    "machine": "tool",
    "atv": "truck",
    "chainsaw": "saw",
    "mower": "tool",
    "truck": "truck",
    "utv": "truck",
}


# --------------------------------------------------------------------------
# shared context
# --------------------------------------------------------------------------
def base_context(conn: sqlite3.Connection, **extra) -> dict:
    cats = db.categories(conn)
    nav_cats = [c for c in cats
                if c["kind"] == "article" and c["parent_id"] is None]
    context = {
        "conn": conn,
        "nav": NAV,
        "equipment_kind_labels": EQUIPMENT_KIND_LABELS,
        "equipment_kind_descriptions": EQUIPMENT_KIND_DESCRIPTIONS,
        "equipment_kind_icons": EQUIPMENT_KIND_ICONS,
        "nav_categories": nav_cats,
        "library_categories": [c for c in cats if c["kind"] in ("library", "community")],
        "stats": db.stats(conn),
        "category_counts": db.counts_by_category(conn),
        "active": "",
        "active_topics": TOPIC_MAP.get(extra.get("active", ""), []),
        "query": "",
        "source_labels": SOURCE_LABELS,
        "page_sources": [],
    }
    context.update(extra)
    return context


def article_url(row) -> str:
    return f"/a/{row['slug']}"


KITCHEN_SUBGROUP_ORDER = [
    "foods", "baking", "preserving", "dairy", "drinks", "nutrition",
    "cooking", "library", "overview",
]

SHELF_INDEXES = {
    "farm": {
        "name": "Farm & Soil",
        "short": "Farm",
        "icon": "wheat",
        "blurb": ("An index of the archive's soil, compost, water, hay, grain, "
                  "pasture, fencing and seed-saving sources. Shelves are grouped "
                  "by subject. Every card opens a depot of real books; nothing "
                  "here is written advice."),
        "href": "/farm",
        "placeholder": "Filter by subject, tool, author...",
        "button": "FILTER FARM",
        "sort_label": "SUBJECT",
        "sub_order": ["soil", "water", "hay-grain", "pasture-fencing",
                      "seeds", "overview"],
        "archive_cat": "lib-agriculture",
        "book_categories": ("lib-agriculture",),
        "books_label": "ALL FARM BOOKS",
        "books_anchor": "farm-books",
        "books_list_id": "farm-books-list",
        "books_intro": ("The complete local farming shelf. Filter the list by "
                        "title or author, then open a record to read the book here."),
        "extra_chips": (("soil", "SOIL & COMPOST"),
                        ("irrigation", "WATER & IRRIGATION")),
        "empty": "No farm shelves match that filter. Try a plainer word.",
    },
    "workshop": {
        "name": "Workshop & Making",
        "short": "Workshop",
        "icon": "wrench",
        "blurb": ("An index of the archive's woodwork, metalwork, mechanics, "
                  "building, plumbing and electrical sources. Shelves are grouped "
                  "by trade. Every card opens a depot of real books and factory "
                  "manuals; nothing here is written advice."),
        "href": "/workshop",
        "placeholder": "Filter by trade, tool, author...",
        "button": "FILTER WORKSHOP",
        "sort_label": "TRADE",
        "sub_order": ["wood", "metal", "mechanical", "building",
                      "electrical", "overview"],
        "archive_cat": "lib-craft",
        "book_categories": ("lib-craft", "lib-manuals"),
        "books_label": "ALL WORKSHOP BOOKS",
        "books_anchor": "workshop-books",
        "books_list_id": "workshop-books-list",
        "books_intro": ("The complete local workshop shelf, including factory "
                        "manuals. Filter by title or author, then open a record "
                        "to read it here."),
        "extra_chips": (("woodwork", "WOODWORK"),
                        ("metalwork", "METALWORK")),
        "empty": "No workshop shelves match that filter. Try a plainer word.",
    },
    "survival": {
        "name": "Survival & Preparedness",
        "short": "Survival",
        "icon": "shield",
        "blurb": ("An index of the archive's foraging, wild food, water, shelter, "
                  "first-aid and off-grid sources. Shelves are grouped by subject. "
                  "Every card opens a depot of real books and reports; nothing here "
                  "is written advice."),
        "href": "/survival",
        "placeholder": "Filter by subject, skill, author...",
        "button": "FILTER SURVIVAL",
        "sort_label": "SUBJECT",
        "sub_order": ["food-water", "shelter", "first-aid", "overview"],
        "archive_cat": "lib-survival",
        "book_categories": ("lib-survival",),
        "books_label": "ALL SURVIVAL BOOKS",
        "books_anchor": "survival-books",
        "books_list_id": "survival-books-list",
        "books_intro": ("The complete local survival shelf. Filter the list by "
                        "title or author, then open a record to read the book here."),
        "extra_chips": (("first-aid", "FIRST AID"),
                        ("foraging", "FORAGING")),
        "empty": "No survival shelves match that filter. Try a plainer word.",
    },
    "home": {
        "name": "Home & Health",
        "short": "Home",
        "icon": "firstaid",
        "blurb": ("An index of the archive's home health, medicine, hygiene and "
                  "household sources. Shelves are grouped by subject. Every card "
                  "opens a depot of real books and reports; nothing here is "
                  "written advice."),
        "href": "/home",
        "placeholder": "Filter by subject, remedy, author...",
        "button": "FILTER HOME",
        "sort_label": "SUBJECT",
        "sub_order": ["health"],
        "archive_cat": "lib-health",
        "book_categories": ("lib-health",),
        "books_label": "ALL HOME BOOKS",
        "books_anchor": "home-books",
        "books_list_id": "home-books-list",
        "books_intro": ("The complete local home and health shelf. Filter the "
                        "list by title or author, then open a record to read the "
                        "book here."),
        "extra_chips": (("home-health", "HOME & HEALTH"),),
        "empty": "No home shelves match that filter. Try a plainer word.",
    },
}


def _shelf_sort(items, sort: str, sub_order: list[str]) -> tuple[list, str]:
    if sort == "name":
        items.sort(key=lambda item: item["name"].lower())
    elif sort == "sources":
        items.sort(key=lambda item: (-item["source_count"], item["name"].lower()))
    else:
        sort = "group"
        rank = {slug: index for index, slug in enumerate(sub_order)}
        items.sort(key=lambda item: (rank.get(item["subgroup_slug"], 999),
                                     item["name"].lower()))
    return items, sort


def _books_for(conn: sqlite3.Connection, categories, query: str = ""):
    seen: dict[str, object] = {}
    for category in categories:
        for book in db.books(conn, category_slug=category):
            seen.setdefault(book["slug"], book)
    books = sorted(seen.values(), key=lambda book: book["title"])
    if query:
        needle = query.lower()
        books = [book for book in books
                 if needle in (book["title"] + " " + (book["author"] or "")).lower()]
    return books


def _grouped(items, order: dict[str, str],
             sub_order: list[str] | None = None) -> list[dict]:
    """Group collection rows into group -> subgroup -> items for templates."""
    groups: dict[str, dict] = {}
    for item in items:
        group_slug = item["group_slug"]
        if group_slug not in groups:
            groups[group_slug] = {
                "slug": group_slug,
                "name": order.get(group_slug, item["group_name"]),
                "items": 0,
                "subgroups": {},
            }
        group = groups[group_slug]
        group["items"] += 1
        sub_slug = item["subgroup_slug"]
        sub = group["subgroups"].setdefault(
            sub_slug, {"slug": sub_slug, "name": item["subgroup_name"], "items": []})
        sub["items"].append(item)
    ordered = sorted(groups.values(),
                     key=lambda g: (list(order).index(g["slug"])
                                    if g["slug"] in order else 999, g["name"]))
    for group in ordered:
        if sub_order:
            group["subgroups"] = sorted(
                group["subgroups"].values(),
                key=lambda sub: (sub_order.index(sub["slug"])
                                 if sub["slug"] in sub_order else 999,
                                 sub["name"]))
        else:
            group["subgroups"] = sorted(
                group["subgroups"].values(),
                key=lambda sub: (-len(sub["items"]), sub["name"]))
    return ordered


# --------------------------------------------------------------------------
# pages
# --------------------------------------------------------------------------
def home(conn: sqlite3.Connection, **_) -> str:
    all_collections = db.collections(conn)
    featured = [c for c in all_collections if c["featured"]]
    crops = [c for c in all_collections if c["kind"] == "crop"]
    animals = [c for c in all_collections if c["kind"] == "animal"]
    topics = [c for c in all_collections if c["kind"] == "topic"]
    latest_books = db.rows(
        conn, "SELECT * FROM books WHERE format != 'MANUAL' "
              "ORDER BY added_at DESC, title LIMIT 6")
    recent_crop = db.recent_collection_books(conn, "crop", limit=4)
    recent_animal = db.recent_collection_books(conn, "animal", limit=4)
    return web.render("home.html", **base_context(
        conn, active="home", featured=featured, recent_crop=recent_crop,
        recent_animal=recent_animal, latest_books=latest_books,
        grow_groups=_grouped(crops, collection_data.CROP_GROUPS),
        animal_groups=_grouped(animals, collection_data.ANIMAL_GROUPS),
        topic_groups=_grouped(topics, collection_data.TOPIC_GROUPS),
        page_sources=db.sources_for(conn, "page", "home"),
    ))


def grow(conn: sqlite3.Connection, **kwargs) -> str:
    query = (kwargs.get("q", "") or "").strip()
    items = db.collections(conn, kind="crop", query=query or None)
    featured = [c for c in db.collections(conn, kind="crop") if c["featured"]]
    return web.render("grow.html", **base_context(
        conn, active="grow", query=query, collections=items,
        featured=featured,
        groups=_grouped(items, collection_data.CROP_GROUPS),
        books=_books_for(conn, ("lib-agriculture", "lib-rural"), query),
        recent=db.recent_collection_books(conn, "crop", limit=8),
        page_sources=db.sources_for(conn, "page", "grow"),
    ))


def animals(conn: sqlite3.Connection, **kwargs) -> str:
    query = (kwargs.get("q", "") or "").strip()
    items = db.collections(conn, kind="animal", query=query or None)
    featured = [c for c in db.collections(conn, kind="animal") if c["featured"]]
    return web.render("animals.html", **base_context(
        conn, active="animals", query=query, collections=items,
        featured=featured,
        groups=_grouped(items, collection_data.ANIMAL_GROUPS),
        books=_books_for(conn, ("lib-livestock",), query),
        recent=db.recent_collection_books(conn, "animal", limit=8),
        page_sources=db.sources_for(conn, "page", "animals"),
    ))


def topics(conn: sqlite3.Connection, **kwargs) -> str:
    query = (kwargs.get("q", "") or "").strip()
    items = db.collections(conn, kind="topic", query=query or None)
    return web.render("topics.html", **base_context(
        conn, active="", query=query, collections=items,
        groups=_grouped(items, collection_data.TOPIC_GROUPS),
        page_sources=db.sources_for(conn, "page", "collections"),
    ))


def kitchen(conn: sqlite3.Connection, **kwargs) -> str:
    query = (kwargs.get("q", "") or "").strip()
    sort = (kwargs.get("sort", "") or "food").strip()
    items = list(db.collections(conn, kind="topic", group="kitchen",
                                query=query or None))
    items, sort = _shelf_sort(items, "group" if sort == "food" else sort,
                              KITCHEN_SUBGROUP_ORDER)
    return web.render("kitchen.html", **base_context(
        conn, active="kitchen", query=query, sort=sort, collections=items,
        groups=_grouped(items, collection_data.TOPIC_GROUPS,
                        KITCHEN_SUBGROUP_ORDER),
        books=_books_for(conn, ("lib-kitchen",), query),
        books_label="ALL COOKBOOKS",
        books_anchor="cookbook-shelf",
        books_list_id="cookbook-list",
        books_intro=("The complete local cookery shelf. Filter the list by title "
                     "or author, then open a record to read the book here."),
        books_aria="Filter the cookbook list",
        books_placeholder="Filter cookbooks by title or author...",
        page_sources=db.sources_for(conn, "page", "kitchen"),
    ))


def group_index(conn: sqlite3.Connection, group: str, **kwargs) -> str:
    meta = SHELF_INDEXES[group]
    query = (kwargs.get("q", "") or "").strip()
    sort = (kwargs.get("sort", "") or "group").strip()
    items = list(db.collections(conn, kind="topic", group=group,
                                query=query or None))
    items, sort = _shelf_sort(items, sort, meta["sub_order"])
    return web.render("shelf_group.html", **base_context(
        conn, active=group, query=query, sort=sort, collections=items,
        group_slug=group, meta=meta,
        groups=_grouped(items, collection_data.TOPIC_GROUPS,
                        meta["sub_order"]),
        books=_books_for(conn, meta["book_categories"], query),
        books_label=meta["books_label"],
        books_anchor=meta["books_anchor"],
        books_list_id=meta["books_list_id"],
        books_intro=meta["books_intro"],
        page_sources=db.sources_for(conn, "page", group),
    ))


def collection_page(conn: sqlite3.Connection, slug: str, expected_kind: str = "",
                    **_) -> str:
    row = db.collection_by_slug(conn, slug)
    if row is None:
        return not_found(conn)
    if expected_kind and row["kind"] != expected_kind:
        return redirect(f"/topic/{slug}" if row["kind"] == "topic"
                        else f"/{row['kind']}s/{slug}")
    books = db.collection_books(conn, row["id"])
    shelves: dict[str, list] = {}
    for book in books:
        shelves.setdefault(book["role"], []).append(book)
    ordered_shelves = sorted(
        shelves.items(), key=lambda pair: (ROLE_ORDER.get(pair[0], 99), pair[0]))
    related = db.collection_related(conn, row)
    children = db.collection_children(conn, row)
    kind_slug = {"crop": "grow", "animal": "animals", "topic": "collections"}[row["kind"]]
    back_href = {"crop": "/grow", "animal": "/animals"}.get(row["kind"], "/collections")
    back_label = {"crop": "Grow", "animal": "Animals"}.get(row["kind"], "Topics")
    if row["kind"] == "topic":
        group = row["group_slug"]
        if group == "kitchen":
            kind_slug, back_href, back_label = "kitchen", "/kitchen", "Kitchen"
        elif group in SHELF_INDEXES:
            kind_slug = group
            back_href = SHELF_INDEXES[group]["href"]
            back_label = SHELF_INDEXES[group]["short"]
    return web.render("collection.html", **base_context(
        conn, active=kind_slug, collection=row, books=books,
        shelves=ordered_shelves, role_labels=ROLE_LABELS,
        related=related, children=children,
        back_href=back_href, back_label=back_label,
        page_sources=db.sources_for(conn, "collection", slug),
    ))


def redirect(location: str) -> tuple[int, dict, str]:
    return 301, {"Location": location, "Content-Length": "0"}, ""



def old_section(conn: sqlite3.Connection, slug: str, **_) -> tuple[int, dict, str]:
    if slug.startswith("vehicle"):
        return redirect("/vehicles")
    target = {
        "farming": "/grow",
        "growing": "/grow",
        "animals": "/animals",
        "kitchen": "/kitchen",
        "workshop": "/workshop",
        "survival": "/survival",
        "vehicles": "/vehicles",
    }.get(slug, "/collections")
    return redirect(target)


def old_article(conn: sqlite3.Connection, slug: str, **_) -> tuple[int, dict, str]:
    return redirect(f"/search?q={slug.replace('-', ' ')}")


def old_hub(conn: sqlite3.Connection, slug: str, **_) -> tuple[int, dict, str]:
    row = db.one(conn, "SELECT slug FROM collections WHERE slug = ? AND kind='topic'",
                 (slug,))
    return redirect(f"/topic/{slug}" if row else f"/search?q={slug.replace('-', ' ')}")


def section(conn: sqlite3.Connection, slug: str, **kwargs) -> str:
    if slug == "vehicles":
        return vehicle_index(conn, **kwargs)
    cat = db.one(conn, "SELECT * FROM categories WHERE slug = ?", (slug,))
    if cat is None:
        return not_found(conn)
    children = db.rows(conn, "SELECT * FROM categories WHERE parent_id = ? "
                             "ORDER BY sort_order, name", (cat["id"],))
    articles = db.articles(conn, slug)
    vehicles = db.rows(conn, "SELECT * FROM vehicles WHERE category_id = ? "
                             "ORDER BY make, model", (cat["id"],))
    hubs = TOPIC_MAP.get(slug, [])
    return web.render("section.html", **base_context(
        conn, active=slug, cat=cat, children=children, articles=articles,
        vehicles=vehicles, hubs=hubs,
        child_counts=db.counts_by_category(conn),
        page_sources=db.sources_for(conn, "page", f"section-{slug}"),
    ))


def article(conn: sqlite3.Connection, slug: str, **_) -> str:
    row = db.article_by_slug(conn, slug)
    if row is None:
        return not_found(conn)
    resolver = web.make_resolver(conn)
    body_html = md.render(row["body"], resolver)
    related = db.rows(conn,
                       "SELECT a.*, c.name AS category_name, c.slug AS category_slug "
                       "FROM articles a LEFT JOIN categories c ON c.id=a.category_id "
                       "WHERE a.id != ? AND (a.category_id = ? OR a.tags LIKE ?) "
                       "LIMIT 5",
                       (row["id"], row["category_id"], f"%{row['tags'].split(',')[0]}%"))
    vehicle = None
    if row["vehicle_id"]:
        vehicle = db.one(conn, "SELECT * FROM vehicles WHERE id = ?", (row["vehicle_id"],))
    # No write here on purpose: the depot is read-only at runtime, so the read
    # counter stays as the seed left it.
    return web.render("article.html", **base_context(
        conn, active=row["category_slug"] or "", article=row,
        body_html=body_html, related=related, vehicle=vehicle,
        page_sources=db.sources_for(conn, "article", slug),
    ))


def vehicle_index(conn: sqlite3.Connection, **kwargs) -> str:
    items = db.vehicles(conn)
    vehicle_type = (kwargs.get("type", "") or "").strip().lower()
    make = (kwargs.get("make", "") or "").strip()
    # normalise make case against the data
    if make:
        make = next((m["make"] for m in items if m["make"].lower() == make.lower()), make)

    kinds: dict[str, list[dict]] = {}
    for item in items:
        kinds.setdefault(item["kind"], []).append(dict(item))

    grouped: dict[str, dict[str, list]] = {}
    for kind, machines in kinds.items():
        by_make: dict[str, list] = {}
        for machine in machines:
            by_make.setdefault(machine["make"], []).append(machine)
        grouped[kind] = by_make

    # Every tractor brand we intend to cover, even without model data yet.
    try:
        from app.seed.content import TRACTOR_BRANDS
    except Exception:
        TRACTOR_BRANDS = []
    tractor_brands = []
    for brand in TRACTOR_BRANDS:
        models = [m for m in items if m["kind"] == "tractor" and m["make"] == brand]
        tractor_brands.append({"name": brand, "count": len(models),
                               "models": models})

    ford = [m for m in items if m["make"] == "Ford" and m["kind"] == "tractor"]

    # Filtered views: type page -> brands, brand page -> models.
    if vehicle_type and not make:
        brands_for_type = []
        if vehicle_type == "tractor":
            brands_for_type = tractor_brands
        else:
            makes = sorted({m["make"] for m in items if m["kind"] == vehicle_type})
            brands_for_type = [{"name": m, "count": len(grouped.get(vehicle_type, {}).get(m, [])),
                               "models": grouped.get(vehicle_type, {}).get(m, [])}
                              for m in makes]
        brands_for_type.sort(key=lambda b: (not bool(b["count"]),
                                            b["name"].lower() != "ford",
                                            b["name"].lower()))
        available_brands = [brand for brand in brands_for_type if brand["count"]]
        planned_brands = [brand for brand in brands_for_type if not brand["count"]]
        return web.render("vehicles.html", **base_context(
            conn, active="vehicles", vehicles=items, kinds=kinds, grouped=grouped,
            ford=ford, view="type", vehicle_type=vehicle_type,
            brands=brands_for_type, make="",
            available_brands=available_brands, planned_brands=planned_brands,
            tractor_brand_count=len(tractor_brands),
            page_sources=db.sources_for(conn, "page", "vehicles")))
    if make:
        type_for_make = vehicle_type or next((m["kind"] for m in items if m["make"] == make), "tractor")
        models = [m for m in items if m["make"] == make and (not vehicle_type or m["kind"] == vehicle_type)]
        return web.render("vehicles.html", **base_context(
            conn, active="vehicles", vehicles=items, kinds=kinds, grouped=grouped,
            ford=ford, view="brand", vehicle_type=type_for_make, make=make,
            brands=[], models=models,
            tractor_brand_count=len(tractor_brands),
            page_sources=db.sources_for(conn, "page", "vehicles")))
    return web.render("vehicles.html", **base_context(
        conn, active="vehicles", vehicles=items, kinds=kinds, grouped=grouped,
        ford=ford, view="index", vehicle_type="", make="", brands=[], models=[],
        tractor_brand_count=len(tractor_brands),
        page_sources=db.sources_for(conn, "page", "vehicles")))


def vehicle(conn: sqlite3.Connection, slug: str, **_) -> str:
    row = db.vehicle_by_slug(conn, slug)
    if row is None:
        return not_found(conn)
    # Factory manuals are linked explicitly by the seeder; other books are a
    # loose title/summary match, so they stay in a separate background list.
    manuals = db.rows(conn,
                      "SELECT b.* FROM books b "
                      "JOIN book_vehicles bv ON bv.book_id = b.id "
                      "WHERE bv.vehicle_id = ? ORDER BY b.year, b.title",
                      (row["id"],))
    books = db.rows(conn,
                    "SELECT b.*, c.name AS category_name FROM books b "
                    "LEFT JOIN categories c ON c.id=b.category_id "
                    "WHERE b.format != 'MANUAL' AND (b.title LIKE ? OR b.summary LIKE ?) "
                    "ORDER BY b.title LIMIT 12",
                    (f"%{row['make']} {row['model']}%", f"%{row['model']}%"))
    return web.render("vehicle.html", **base_context(
        conn, active="vehicles", vehicle=row, books=books, manuals=manuals,
        page_sources=db.sources_for(conn, "vehicle", slug)))


def library(conn: sqlite3.Connection, **_) -> str:
    archive = db.books(conn, limit=60)
    items = db.collections(conn)
    themes = db.rows(conn, "SELECT COALESCE(theme,'general') theme, COUNT(*) n "
                           "FROM books GROUP BY theme ORDER BY n DESC")
    return web.render("library.html", **base_context(
        conn, active="library", archive=archive,
        collections=items,
        featured=[c for c in items if c["featured"]],
        formats=db.rows(conn, "SELECT format, COUNT(*) n FROM books GROUP BY format"),
        themes=themes,
        page_sources=db.sources_for(conn, "page", "library"),
    ))


def archive(conn: sqlite3.Connection, **kwargs) -> str:
    query = (kwargs.get("q", "") or "").strip()
    fmt = (kwargs.get("format", "") or "").strip()
    cat = (kwargs.get("cat", "") or "").strip()
    theme = (kwargs.get("theme", "") or "").strip()
    try:
        page = max(1, int(kwargs.get("page", 1) or 1))
    except (TypeError, ValueError):
        page = 1
    sql = ("SELECT b.*, c.name AS category_name, c.slug AS category_slug "
           "FROM books b LEFT JOIN categories c ON c.id=b.category_id WHERE 1=1")
    count_sql = ("SELECT COUNT(*) FROM books b LEFT JOIN categories c "
                 "ON c.id=b.category_id WHERE 1=1")
    params: list = []
    if query:
        sql += " AND (b.title LIKE ? OR b.author LIKE ? OR b.summary LIKE ?)"
        count_sql += " AND (b.title LIKE ? OR b.author LIKE ? OR b.summary LIKE ?)"
        params += [f"%{query}%"] * 3
    if fmt:
        sql += " AND b.format = ?"
        count_sql += " AND b.format = ?"
        params.append(fmt)
    if cat:
        sql += " AND c.slug = ?"
        count_sql += " AND c.slug = ?"
        params.append(cat)
    if theme:
        sql += " AND COALESCE(b.theme,'general') = ?"
        count_sql += " AND COALESCE(b.theme,'general') = ?"
        params.append(theme)
    total = db.scalar(conn, count_sql, list(params))
    per_page = 60
    pages = max(1, -(-total // per_page))
    page = min(page, pages)
    sql += " ORDER BY b.title LIMIT ? OFFSET ?"
    items = db.rows(conn, sql, [*params, per_page, (page - 1) * per_page])
    return web.render("archive.html", **base_context(
        conn, active="library", archive=items, query=query, fmt=fmt, cat=cat, theme=theme,
        formats=db.rows(conn, "SELECT format, COUNT(*) n FROM books GROUP BY format"),
        themes=db.rows(conn, "SELECT COALESCE(theme,'general') theme, COUNT(*) n "
                             "FROM books GROUP BY theme ORDER BY n DESC"),
        library_categories=db.rows(conn,
                                   "SELECT c.*, COUNT(b.id) n FROM categories c "
                                   "LEFT JOIN books b ON b.category_id=c.id "
                                   "WHERE c.kind='library' GROUP BY c.id "
                                   "ORDER BY c.sort_order"),
        total=total, page=page, pages=pages, per_page=per_page,
        page_sources=(db.sources_for(conn, "category", cat) if cat
                      else db.sources_for(conn, "page", "archive")),
    ))


def book(conn: sqlite3.Connection, slug: str, **_) -> str:
    row = db.book_by_slug(conn, slug)
    if row is None:
        return not_found(conn)
    path = config.ARCHIVE_DIR / row["rel_path"]
    exists = path.exists()
    related = db.rows(conn,
                       "SELECT b.*, c.name AS category_name FROM books b "
                       "LEFT JOIN categories c ON c.id=b.category_id "
                       "WHERE b.id != ? AND (b.category_id = ? OR b.author = ?) LIMIT 5",
                       (row["id"], row["category_id"], row["author"]))
    page_sources = db.sources_for(conn, "book", slug)
    if not page_sources:
        page_sources = [{
            "title": row["title"], "author": row["author"],
            "kind": "manual" if row["format"] == "MANUAL" else "book",
            "url": row["source_url"] or f"/library/archive/{row['slug']}",
            "license": row["license"], "book_slug": row["slug"],
            "role": "primary", "locator": "Full text in the local archive",
            "citation_note": "Bibliographic record from the archive catalogue.",
            "note": "",
        }]
    return web.render("book.html", **base_context(
        conn, active="library", book=row, exists=exists, related=related,
        page_sources=page_sources))


def community(conn: sqlite3.Connection, **kwargs) -> str:
    query = (kwargs.get("q", "") or "").strip()
    sql = ("SELECT a.*, c.name AS category_name, c.slug AS category_slug, "
           "c.icon AS category_icon FROM articles a "
           "LEFT JOIN categories c ON c.id=a.category_id "
           "WHERE a.status='published'")
    params: list = []
    if query:
        sql += " AND (a.title LIKE ? OR a.summary LIKE ? OR a.tags LIKE ?)"
        params += [f"%{query}%"] * 3
    sql += " ORDER BY c.sort_order, a.title"
    items = db.rows(conn, sql, params)
    grouped: dict[str, list] = {}
    for item in items:
        grouped.setdefault(item["category_slug"] or "other", []).append(item)
    shelves = db.rows(conn,
                      "SELECT c.*, COUNT(a.id) n FROM categories c "
                      "LEFT JOIN articles a ON a.category_id=c.id "
                      "AND a.status='published' "
                      "WHERE c.kind = 'article' "
                      "GROUP BY c.id ORDER BY c.sort_order")
    return web.render("community.html", **base_context(
        conn, active="community", items=items, grouped=grouped, query=query,
        library_categories=shelves,
        page_sources=db.sources_for(conn, "page", "community"),
    ))


def submit(conn: sqlite3.Connection, **_) -> str:
    pending = db.rows(conn, "SELECT * FROM submissions ORDER BY submitted_at DESC LIMIT 20")
    return web.render("submit.html", **base_context(
        conn, active="library", pending=pending,
        page_sources=db.sources_for(conn, "page", "submit")))


def formulas(conn: sqlite3.Connection, **kwargs) -> str:
    topic = (kwargs.get("topic", "") or "").strip()
    query = (kwargs.get("q", "") or "").strip()
    items = db.formulas(conn, topic=topic or None, query=query or None)
    topics = db.formula_topics(conn)
    counts = {row["topic"]: row["n"] for row in db.rows(
        conn, "SELECT topic, COUNT(*) n FROM formulas GROUP BY topic")}
    total = sum(counts.values())
    # Sort the shelves by everyday usefulness, then put the most-used formulas
    # at the top of each shelf. Topic order comes from the seed, not the DB.
    topic_order = {row["slug"]: i for i, row in enumerate(topics)}
    common_rank = {slug: i for i, slug in enumerate(COMMON_FORMULAS)}
    resolver = web.make_resolver(conn)
    prepared = []
    for item in items:
        item = dict(item)
        # The guidance and the worked example are Markdown, so the wiki links
        # inside them work like they do in an article.
        item["how_html"] = md.render(item["how"] or "", resolver)
        item["example_html"] = md.render(item["example"] or "", resolver)
        item["calculator"] = calculators.calculator_for(
            item["expression"], item["symbols"])
        prepared.append(item)
    prepared.sort(key=lambda x: (topic_order.get(x["topic"], 999),
                                 common_rank.get(x["slug"], 10_000), x["name"]))
    grouped: dict[str, list] = {}
    for item in prepared:
        grouped.setdefault(item["topic"], []).append(item)
    quick = []
    if not topic and not query:
        quick = sorted([item for item in prepared if item["slug"] in common_rank],
                       key=lambda x: common_rank[x["slug"]])[:16]
    names = {row["slug"]: row["name"] for row in topics}
    return web.render("formulas.html", **base_context(
        conn, active="formulas", formulas=prepared, grouped=grouped, topics=topics,
        counts=counts, total=total, topic=topic, query=query,
        topic_names=names, quick=quick, common_slugs=common_rank,
        page_sources=db.sources_for(conn, "page", "formulas"),
    ))


def search(conn: sqlite3.Connection, **kwargs) -> str:
    query = (kwargs.get("q", "") or "").strip()
    kind = (kwargs.get("kind", "") or "").strip()
    source = (kwargs.get("source", "") or "").strip()
    kinds = [k.strip() for k in kind.split(",") if k.strip()]
    metadata_kinds = [k for k in kinds if k != "section"]
    if kinds and not metadata_kinds:
        hits = []
    else:
        hits = (db.search(conn, query, ",".join(metadata_kinds) or None)
                if query else [])
    sections = []
    if query and (not kinds or "section" in kinds):
        if source == "manual":
            sections = db.search_sections(conn, query, kind="manual")
        elif source == "book":
            sections = db.search_sections(conn, query, kind="book")
        elif source in ("", "all"):
            sections = db.search_sections(conn, query)
    sections = [dict(row) for row in sections]
    for row in sections:
        row["snip_html"] = (html.escape(row["snip"] or "")
                            .replace("\x01", "<mark>").replace("\x02", "</mark>"))
    collections = []
    books = []
    formulas = []
    resolver = web.make_resolver(conn)
    for hit in hits:
        if hit["kind"] == "collection":
            row = db.one(
                conn,
                "SELECT c.*, (SELECT COUNT(*) FROM collection_books cb "
                "WHERE cb.collection_id = c.id) AS source_count "
                "FROM collections c WHERE c.id = ?", (hit["kind_id"],))
            if row:
                row = dict(row)
                row["snip"] = md.snippet(hit["snip"], resolver)
                collections.append(row)
        elif hit["kind"] == "formula":
            row = db.one(conn, "SELECT * FROM formulas WHERE id = ?", (hit["kind_id"],))
            if row:
                row = dict(row)
                row["excerpt_html"] = md.render(
                    (row["how"] or row["example"] or "").strip(), resolver)
                formulas.append(row)
        else:
            row = db.one(
                conn,
                "SELECT b.*, c.name AS category_name FROM books b "
                "LEFT JOIN categories c ON c.id=b.category_id WHERE b.id = ?",
                (hit["kind_id"],))
            if row:
                row = dict(row)
                row["snip"] = md.snippet(hit["snip"], resolver)
                books.append(row)

    if source == "manual":
        books = [b for b in books if b["format"] == "MANUAL"]
        collections = []
    elif source == "book":
        books = [b for b in books if b["format"] != "MANUAL"]
        collections = []
    elif source == "archive":
        books = [b for b in books if "archive.org" in (b["source_url"] or "")
                 or "Internet Archive" in (b["source"] or "")]
        collections = []
    elif source == "ai-organized":
        books = []
        formulas = []

    return web.render("search.html", **base_context(
        conn, active="", query=query, kind=kind, source=source,
        kinds=kinds, collections=collections, books=books, formulas=formulas,
        sections=sections,
        page_sources=db.sources_for(conn, "page", "search")))


READER_CHARS = 20_000
READER_MAX_BYTES = 4_000_000


def _reader_clean(raw: str, fmt: str) -> str:
    text = raw
    if fmt == "HTML":
        text = re.sub(r"(?s)<(script|style).*?</\1>", " ", text)
        text = re.sub(r"<[^>]+>", " ", text)
        text = html.unescape(text)
    start = text.find("*** START OF")
    if start != -1:
        newline = text.find("\n", start)
        if newline != -1:
            text = text[newline + 1:]
    end = text.find("*** END OF")
    if end != -1:
        text = text[:end]
    return text.strip() + "\n"


def _reader_pages(text: str, size: int = READER_CHARS) -> list[str]:
    pages: list[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + size)
        if end < len(text):
            cut = text.rfind("\n", start + size // 2, end)
            if cut > start:
                end = cut
        chunk = text[start:end].strip("\n")
        if chunk:
            pages.append(chunk)
        start = end
    return pages or [""]


def _page_label(text: str, index: int) -> str:
    for line in text.splitlines():
        clean = " ".join(line.split())
        if len(re.sub(r"[^A-Za-z0-9]", "", clean)) >= 4:
            return clean[:72]
    return f"Page {index}"


def _reader_markup(text: str, query: str) -> str:
    safe = html.escape(text)
    if not query:
        return safe
    needle = html.escape(query)
    try:
        return re.sub(re.escape(needle), lambda m: f"<mark>{m.group(0)}</mark>",
                      safe, flags=re.IGNORECASE)
    except re.error:
        return safe


def reader(conn: sqlite3.Connection, slug: str, **kwargs) -> str:
    row = db.book_by_slug(conn, slug)
    if row is None:
        return not_found(conn)
    path = config.ARCHIVE_DIR / row["rel_path"]
    text = ""
    truncated = False
    if path.exists() and row["format"] in ("TEXT", "HTML", "MANUAL"):
        raw = path.read_text(encoding="utf-8", errors="replace")
        if len(raw.encode("utf-8", errors="replace")) > READER_MAX_BYTES:
            raw = raw[:READER_MAX_BYTES]
            truncated = True
        text = _reader_clean(raw, row["format"])

    pages = _reader_pages(text) if text else []
    total = len(pages)
    query = (kwargs.get("q", "") or "").strip()
    hits: list[dict] = []
    if query and pages:
        for index, page in enumerate(pages, start=1):
            low = page.lower()
            needle = query.lower()
            count = low.count(needle)
            if count:
                pos = low.find(needle)
                left = max(0, pos - 70)
                right = min(len(page), pos + len(query) + 110)
                snippet = " ".join(page[left:right].split())
                hits.append({"page": index, "count": count, "snippet": snippet})
    raw_page = str(kwargs.get("page", "") or "").strip()
    try:
        page = max(1, int(raw_page)) if raw_page else 1
    except ValueError:
        page = 1
    if query and not raw_page and hits:
        page = hits[0]["page"]
    page = min(page, total) if total else 1
    current = pages[page - 1] if total else ""
    labels = [_page_label(item, n) for n, item in enumerate(pages, start=1)]
    page_sources = db.sources_for(conn, "book", slug)
    if not page_sources:
        page_sources = [{
            "title": row["title"], "author": row["author"],
            "kind": "manual" if row["format"] == "MANUAL" else "book",
            "url": row["source_url"] or f"/library/archive/{row['slug']}",
            "license": row["license"], "book_slug": row["slug"],
            "role": "primary", "locator": "Full text in the local archive",
            "citation_note": "Bibliographic record from the archive catalogue.",
            "note": "",
        }]
    return web.render("reader.html", **base_context(
        conn, active="library", book=row, text=current,
        text_html=_reader_markup(current, query), readable=bool(text),
        page=page, pages=total, labels=labels, query=query, hits=hits,
        truncated=truncated, page_sources=page_sources))


def sources(conn: sqlite3.Connection, **kwargs) -> str:
    counts = db.source_kind_counts(conn)
    kind = (kwargs.get("kind", "") or "").strip()
    if kind not in counts:
        kind = ""
    where = "WHERE s.kind = ? " if kind else ""
    params = (kind,) if kind else ()
    items = db.rows(conn,
                    "SELECT s.*, COUNT(c.id) n FROM sources s "
                    "LEFT JOIN citations c ON c.source_id=s.id "
                    f"{where}GROUP BY s.id ORDER BY s.kind, s.title", params)
    return web.render("sources.html", **base_context(
        conn, active="sources", source_counts=counts, source_total=sum(counts.values()),
        active_kind=kind, items=items,
        page_sources=db.sources_for(conn, "page", "sources")))


# --------------------------------------------------------------------------
# api
# --------------------------------------------------------------------------
def api_search(conn: sqlite3.Connection, **kwargs) -> tuple[int, str, str]:
    query = (kwargs.get("q", "") or "").strip()
    if not query:
        return 200, "application/json", json.dumps({"results": []})
    hits = db.search(conn, query, limit=12)
    results = []
    for hit in hits:
        if hit["kind"] == "collection":
            row = db.one(conn, "SELECT slug, name, kind, summary FROM collections WHERE id=?",
                         (hit["kind_id"],))
            if row:
                prefix = {"crop": "grow", "animal": "animals",
                          "topic": "topic"}[row["kind"]]
                results.append({"kind": "collection", "title": row["name"],
                                "summary": row["summary"],
                                "url": f"/{prefix}/{row['slug']}"})
        elif hit["kind"] == "formula":
            row = db.one(conn, "SELECT slug, name, topic FROM formulas WHERE id=?",
                         (hit["kind_id"],))
            if row:
                results.append({"kind": "formula", "title": row["name"],
                                "summary": row["topic"],
                                "url": f"/formulas?q={row['slug']}"})
        else:
            row = db.one(conn, "SELECT slug, title, author FROM books WHERE id=?",
                         (hit["kind_id"],))
            if row:
                results.append({"kind": "book", "title": row["title"],
                                "summary": row["author"],
                                "url": f"/library/archive/{row['slug']}"})
    return 200, "application/json", json.dumps({"query": query, "results": results})


def api_stats(conn: sqlite3.Connection, **_) -> tuple[int, str, str]:
    return 200, "application/json", json.dumps(db.stats(conn))


def conversions(conn: sqlite3.Connection, **_) -> str:
    return web.render("conversions.html", **base_context(
        conn, active="conversions",
        page_sources=db.sources_for(conn, "page", "conversions")))


def hub(conn: sqlite3.Connection, slug: str, **_) -> str:
    words = [w for w in slug.split("-") if len(w) > 2 and w not in
             ("and", "the", "for", "with", "from")]
    terms = list(dict.fromkeys([slug.replace("-", " "), *words]))
    def clauses(columns: list[str]) -> tuple[str, list]:
        ors, params = [], []
        for term in terms:
            like = f"%{term}%"
            ors.append("(" + " OR ".join(f"{c} LIKE ?" for c in columns) + ")")
            params.extend([like] * len(columns))
        return " OR ".join(ors), params

    a_sql, a_params = clauses(["a.title", "a.summary", "a.body", "a.tags"])
    articles = db.rows(conn,
        "SELECT a.*, c.name AS category_name, c.slug AS category_slug, "
        "c.icon AS category_icon FROM articles a "
        "LEFT JOIN categories c ON c.id=a.category_id "
        f"WHERE a.status='published' AND ({a_sql}) ORDER BY a.title", a_params)

    b_sql, b_params = clauses(["b.title", "b.author", "b.summary"])
    books = db.rows(conn,
        "SELECT b.*, c.name AS category_name FROM books b "
        "LEFT JOIN categories c ON c.id=b.category_id "
        f"WHERE {b_sql} ORDER BY b.title", b_params)

    f_sql, f_params = clauses(["name", "expression", "symbols", "how", "example", "tags"])
    formulas = db.rows(conn,
        f"SELECT * FROM formulas WHERE {f_sql} ORDER BY topic, name", f_params)

    v_sql, v_params = clauses(["make", "model", "notes"])
    vehicles = db.rows(conn,
        f"SELECT * FROM vehicles WHERE {v_sql} ORDER BY make, model", v_params)

    label = slug.replace("-", " ").title()
    parent = ""
    for section_slug, topics in TOPIC_MAP.items():
        for topic_slug, topic_name in topics:
            if topic_slug == slug:
                label, parent = topic_name, section_slug
                break
        if parent:
            break

    resolver = web.make_resolver(conn)
    formulas = [dict(item) for item in formulas]
    for item in formulas:
        item["how_html"] = md.render(item["how"] or "", resolver)
        item["example_html"] = md.render(item["example"] or "", resolver)

    return web.render("hub.html", **base_context(
        conn, active=parent or "", slug=slug, term=label, parent=parent,
        articles=articles, books=books, formulas=formulas, vehicles=vehicles,
        page_sources=db.sources_for(conn, "hub", slug)))


def not_found(conn: sqlite3.Connection, code: int = 404, message: str = "") -> tuple[int, str, str]:
    page = web.render("error.html", **base_context(conn, active="",
                                                   code=code,
                                                   message=message or "That page could not be found."))
    return code, "text/html; charset=utf-8", page


# --------------------------------------------------------------------------
# file streaming
# --------------------------------------------------------------------------
def download(conn: sqlite3.Connection, slug: str, **_) -> tuple[int, str, str] | tuple[int, dict, bytes]:
    row = db.book_by_slug(conn, slug)
    if row is None:
        return 404, "text/plain", "not found"
    path = (config.ARCHIVE_DIR / row["rel_path"]).resolve()
    try:
        path.relative_to(config.ARCHIVE_DIR.resolve())
    except ValueError:
        return 403, "text/plain", "forbidden"
    if not path.exists():
        return 404, "text/plain", "file missing from archive"
    data = path.read_bytes()
    headers = {
        "Content-Disposition": f'attachment; filename="{path.name}"',
        "X-Content-Type-Options": "nosniff",
    }
    return 200, headers, data  # type: ignore[return-value]


def robots(conn: sqlite3.Connection, **_) -> tuple[int, str, str]:
    return 200, "text/plain", "User-agent: *\nDisallow:\n"
