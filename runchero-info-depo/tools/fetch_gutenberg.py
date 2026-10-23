#!/usr/bin/env python3
"""Pull a big shelf of relevant public domain books from Project Gutenberg.

The depot only had a curated handful of books. This tool reads the Project
Gutenberg catalogue, keeps the titles that are actually useful on a farm and
in a workshop, downloads them into the archive and writes a catalogue module
the seeder can use.

    python3 tools/fetch_gutenberg.py --limit 1200
    python3 tools/fetch_gutenberg.py --limit 1200 --workers 16 --dry-run

The download is resumable: a file that is already in the archive is left
alone, so the tool can be interrupted and run again.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import json
import re
import shutil
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import config  # noqa: E402

CATALOG_URL = "https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv.gz"
CACHE = Path("/tmp/opencode/pg_catalog.csv.gz")
TEXT_URL = "https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt"
ALT_URL = "https://www.gutenberg.org/files/{id}/{id}-0.txt"
USER_AGENT = ("Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 "
              "Firefox/128.0 (Runchero Information Depo archive fetcher)")
MAX_BYTES = 8 * 1024 * 1024

# --------------------------------------------------------------------------
# what we keep
# --------------------------------------------------------------------------
GROUPS: dict[str, list[str]] = {
    "agriculture": [
        "agriculture", "agronomy", "horticulture", "soil", "fertiliz", "irrigation",
        "drainage", "crop", "weeds", "cultivation", "grain", "wheat", "corn",
        "maize", "potato", "fruit culture", "sugar beet", "cotton", "tobacco",
        "forage", "farming", "plantation", "orchard", "vineyard", "pesticid",
        "herbicide", "seeds", "planting", "harvest", "tillage", "plough", "manure",
        "compost", "mushroom", "flora", "plant", "botany", "algae", "lichen",
        "fungus", "moss", "tree", "forestry", "graft", "pruning", "herb", "flower",
        "garden", "greenhouse", "nursery", "weeding", "farming", "agricultur",
    ],
    "livestock": [
        "animal husbandry", "cattle", "sheep", "swine", "hog", "poultry",
        "chicken", "horse", "goat", "dairy", "beekeeping", "bee", "veterinary",
        "livestock", "camel", "sheepdog", "pigeon", "turkey", "duck", "geese",
        "stock raising", "breeding", "mammal", "zoolog", "barn", "oxen",
    ],
    "machinery": [
        "machinery", "mechanic", "steam", "engine", "tractor", "railway",
        "train", "locomotive", "iron and steel", "machine tool", "automobil",
        "motor car", "boiler", "foundry", "forge", "blacksmith", "turning",
        "lathe", "milling", "gear", "agricultural machinery", "farm machinery",
        "carts", "wagons", "locomotion", "shipbuilding", "motor", "traction",
        "threshing", "harvesting machine",
    ],
    "rural": [
        "country life", "rural", "village", "manor", "estate", "landscape",
        "weather", "climate", "meteorolog", "geolog", "mining", "coal", "ore",
        "quarry", "fishing", "angler", "sport", "hunting", "forest", "woods",
        "wild", "nature", "natural history", "birds of", "flowers of", "fungi of",
        "bryolog", "household", "cottage", "chimney", "rural life",
    ],
    "craft": [
        "carpentry", "woodwork", "building", "construction", "architect",
        "plumb", "gas fitting", "electrical", "painting", "drawing", "draught",
        "sketch", "design", "sculptur", "masonry", "brick", "tile", "roof",
        "engraving", "printing", "bookbinding", "tailor", "sewing", "leather",
        "tannery", "glass", "pottery", "weaving", "textile", "surveying",
        "estimating", "quantities", "bricklayer", "plaster", "furniture",
        "engineering", "mechanical", "lumber", "timber", "joinery", "carpenter",
        "ironwork", "wrought iron", "tools", "hand tools", "welding", "gas",
    ],
    "kitchen": [
        "cookery", "cooking", "culinary", "cook-book", "cookbook", "food",
        "preserv", "canning", "pickl", "baking", "bread", "pastry", "confection",
        "sugar", "syrup", "wine", "beer", "brew", "ale", "cider", "coffee",
        "tea", "chocolate", "butter", "cheese", "milk", "meat", "butcher",
        "sausage", "pork", "bacon", "ham", "honey", "kitchen", "nutrition",
        "diet", "spice", "vinegar", "oil", "sauce", "pudding", "soup",
        "food--preservation", "food supply", "ferment", "lactic", "cheesemaking",
        "egg", "poultry for the table", "vegetable cookery",
    ],
    "science": [
        "mathemat", "arithmetic", "algebra", "geometry", "trigonometr",
        "calculus", "mensuration", "chemistr", "physics", "astronom",
        "mechanics", "weights and measures", "tables", "statistic", "probabilit",
        "electricity", "magnetism", "heat", "sound", "optics", "chemical",
        "element", "laborator", "experiment", "theorem", "equation", "logarithm",
        "quadratic", "calculating", "spectrum", "scientific tables", "surveying",
        "spherical", "triangle", "circle", "sphere", "cube", "conic", "solid",
        "rectangle", "geometry of", "metric system", "money", "compound interest",
    ],
    "health": [
        "medicin", "surger", "pharmac", "anatom", "physiolog", "hygien",
        "nurs", "first aid", "firstaid", "homeopathic", "disease", "patholog",
        "therapeut", "dietet", "fracture", "wound", "poison", "antitoxin",
        "materia medica", "dentistr", "invalid", "gymnastic", "massage",
        "water cure", "bacteriolog", "milk hygiene", "inspection",
    ],
    "money": [
        "econom", "political economy", "bookkeep", "account", "banking",
        "finance", "credit", "price", "cost", "wage", "labour", "capital",
        "trade", "commerce", "insurance", "tax", "tariff", "cooperation",
        "co-operative", "cooperative", "pension", "money and banking",
    ],
    "survival": [
        "survival", "foraging", "wild food", "woodcraft", "camping", "outdoor",
        "homestead", "off grid", "preparedness", "bushcraft", "shelter",
        "trapping", "hunting", "fishing", "forag", "edible", "poisonous plants",
        "first aid", "nursing", "medicine", "hygiene", "sanitation", "water supply",
        "solar", "hydroelectric", "wind power", "renewable", "energy",
    ],
}

DOMAIN_PREFIX = (
    "agriculture", "horticulture", "animal husbandry", "fish culture",
    "aquaculture", "dairying", "poultry", "veterinary", "beekeeping",
    "sericulture", "silk", "machinery", "mechanics", "steam", "electrical",
    "engineering", "carpentry", "building", "construction", "plumbing",
    "blacksmith", "metalworking", "iron and steel", "coal", "mining", "cookery",
    "cooking", "food", "preserv", "baking", "baker", "confection", "wine",
    "beer", "coffee", "tea", "sugar", "butchery", "bacteriolog", "mathematics",
    "arithmetic", "algebra", "geometry", "trigonometry", "calculus",
    "mensuration", "chemistry", "physics", "astronomy", "weights and measures",
    "tables", "statistics", "electricity", "magnetism", "heat", "sound",
    "optics", "medicine", "surgery", "pharmacy", "anatomy", "physiology",
    "hygiene", "nursing", "first aid", "economics", "bookkeeping", "accounting",
    "botany", "zoology", "entomology", "ornithology", "ichthyology",
    "meteorology", "geology", "agronomy", "farming", "gymnastics", "dentistry",
    "horticultur", "forestry", "dairymen's", "food--", "farm", "bees",
)

BAD = (
    "fiction", "poetry", "poems", "drama", "humor", "humour", "comic",
    "juvenile", "fairy", "romance", "novel", "anthology", "sermons", "hymns",
    "genealog", "encyclop", "dictionary of", "adventure", "trials",
    "letters of", "correspondence", "biography of", "travels", "voyages",
    "and the loves of", "love stories",
)

BAD_TITLE = re.compile(
    r"follies|outline of a natural|anecdotes of|amusements in|reminiscences of|"
    r"the story of the [a-z ]{0,12} of the|sketches of|random ramblings|"
    r"the making of a|trifles|scraps|thoughts and", re.I)

#: group -> (library category slug, cover motif, cover base, cover accent)
SHELF = {
    "agriculture": ("lib-agriculture", "wheat", "soil", "sun"),
    "livestock": ("lib-livestock", "cow", "tomato2", "cream"),
    "machinery": ("lib-machinery", "engine", "sky2", "silver"),
    "rural": ("lib-rural", "book", "grass", "brown"),
    "craft": ("lib-craft", "wrench", "teal2", "cream"),
    "kitchen": ("lib-kitchen", "jar", "orange", "plum"),
    "science": ("lib-science", "info", "navy", "cyan"),
    "health": ("lib-health", "firstaid", "teal", "white"),
    "money": ("lib-money", "tag", "brown", "sun2"),
    "survival": ("lib-survival", "shield", "tomato", "cream"),
}

ROTATE = [
    ("sky", "sky2"), ("grass", "grass2"), ("soil", "soil2"), ("cream", "paper2"),
    ("navy", "cyan"), ("brown", "orange"), ("teal", "teal2"), ("plum", "pink"),
]


# --------------------------------------------------------------------------
# catalogue
# --------------------------------------------------------------------------
def load_catalog() -> list[dict]:
    if not CACHE.exists():
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        print("fetching the Gutenberg catalogue...")
        with urllib.request.urlopen(
                urllib.request.Request(CATALOG_URL, headers={"User-Agent": USER_AGENT}),
                timeout=120) as response:
            CACHE.write_bytes(response.read())
    with gzip.open(CACHE, "rt", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def split_fields(value: str) -> list[str]:
    return [part.strip() for part in (value or "").split(";") if part.strip()]


BAD_HEAD = (
    "periodicals", "journal", "transactions", "proceedings", "bulletin",
    "societies", "association", "catalog", "bibliography", "directories",
    "year books", "yearbook", "annual report", "reports of", "memorials",
)

BAD_TITLE = re.compile(
    r"follies|anecdotes of|amusements in|reminiscences of|"
    r"trifles|scraps|thoughts and|journal|transactions|proceedings|"
    r"bulletin|annual report|volume [ivxlcdm]+|vol\. [ivxlcdm]+|"
    r"a century's progress|adobe days|canal days|oxford days|"
    r"a walk from|journey in|tour through|start in life", re.I)


def core_head(subject: str) -> str:
    """The leading subject head, e.g. 'Agriculture -- Wheat' -> 'Agriculture'."""
    head = subject.split(" -- ")[0].strip()
    return head


def classify(row: dict) -> tuple[str, int] | None:
    """Return (group, score) for a catalogue row, or None to skip it."""
    if row.get("Language") != "en" or row.get("Type") != "Text":
        return None
    subjects = split_fields(row.get("Subjects", ""))
    bookshelves = split_fields(row.get("Bookshelves", ""))
    if not any(s.lower().startswith(DOMAIN_PREFIX) for s in subjects):
        return None
    heads = [core_head(s) for s in subjects]
    if any(h.lower() in BAD_HEAD for h in heads):
        return None
    subject_blob = "; ".join(subjects).lower()
    shelf_blob = "; ".join(bookshelves).lower()
    blob = f"{subject_blob}; {shelf_blob}"
    if any(bad in blob for bad in BAD):
        return None
    if BAD_TITLE.search(row.get("Title", "")):
        return None
    head_blob = "; ".join(heads).lower()
    best_group, best_score = None, 0
    for group, words in GROUPS.items():
        core = sum(1 for word in words if word in head_blob)
        extra = sum(1 for word in words if word in subject_blob) - core
        score = core * 3 + extra
        if score > best_score:
            best_group, best_score = group, score
    if best_group is None or best_score < 3:
        return None
    return best_group, best_score


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return re.sub(r"-{2,}", "-", slug)[:70].strip("-")


SKIP_TAIL = {
    "history", "early works to 1800", "early works to 1850", "periodicals",
    "juvenile literature", "juvenile", "dictionaries", "dictionary",
    "bibliography", "indexes", "catalogs", "exhibitions", "pictorial works",
    "handbooks and manuals", "handbooks", "manuals", "textbooks", "textbooks and manuals",
}


def summarise(title: str, subjects: list[str]) -> str:
    """Build a shelf blurb out of the catalogue subjects."""
    cleaned: list[str] = []
    for subject in subjects:
        parts = [p.strip() for p in subject.split(" -- ") if p.strip()]
        for part in reversed(parts):
            if part.lower() in SKIP_TAIL or len(part) < 3:
                continue
            if part.lower() in title.lower():
                continue
            if part.lower() in {c.lower() for c in cleaned}:
                continue
            cleaned.append(part[0].lower() + part[1:] if part[:1].isupper() else part)
            break
        if len(cleaned) == 3:
            break
    if not cleaned:
        return (f"A public domain volume held in the depot archive: {title}. "
                "Readable offline, free to copy.")
    joined = ", ".join(cleaned[:-1]) + (" and " + cleaned[-1] if len(cleaned) > 1 else "")
    return (f"Subjects: {joined}. A public domain volume in the offline archive, "
            "readable on the depot or downloadable as plain text.")


# --------------------------------------------------------------------------
# downloading
# --------------------------------------------------------------------------
def fetch_one(gid: int, target: Path) -> str:
    if target.exists() and target.stat().st_size > 0:
        return "cached"
    last: Exception | None = None
    for template in (TEXT_URL, ALT_URL):
        url = template.format(id=gid)
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=90) as response:
                data = response.read(MAX_BYTES)
            if not data:
                raise RuntimeError("empty file")
            target.write_bytes(data)
            return "fetched"
        except (urllib.error.URLError, OSError, TimeoutError, RuntimeError) as error:
            last = error
            time.sleep(1.0)
    raise RuntimeError(f"{gid}: {last}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fill the depot archive")
    parser.add_argument("--limit", type=int, default=1200,
                        help="how many books to keep (default 1200)")
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--dry-run", action="store_true",
                        help="list the books without downloading")
    parser.add_argument("--per-group", type=int, default=0,
                        help="cap each shelf (0 = no cap)")
    args = parser.parse_args(argv)

    config.ensure_dirs()
    archive = config.ARCHIVE_DIR / "books"
    archive.mkdir(parents=True, exist_ok=True)

    print("reading the catalogue...")
    rows = load_catalog()
    from app.seed import books as curated_books
    skip_ids = {entry[0] for entry in curated_books.BOOKS}
    skip_slugs = {entry[1] for entry in curated_books.BOOKS}
    picked: list[dict] = []
    counts: dict[str, int] = {}
    for row in rows:
        result = classify(row)
        if result is None:
            continue
        group, score = result
        if args.per_group and counts.get(group, 0) >= args.per_group:
            continue
        try:
            gid = int(row["Text#"])
        except (TypeError, ValueError):
            continue
        if gid in skip_ids:
            continue
        title = row.get("Title", "").strip()
        if not title or slugify(title) in skip_slugs:
            continue
        picked.append({
            "gid": gid, "group": group, "score": score, "title": title,
            "author": (row.get("Authors", "") or "Unknown").strip(),
            "subjects": split_fields(row.get("Subjects", "")),
        })
        counts[group] = counts.get(group, 0) + 1

    # keep the best scoring book on each shelf first
    picked.sort(key=lambda item: (item["group"], -item["score"], item["title"]))
    per_group_cap = args.per_group or max(1, args.limit // max(1, len(GROUPS)))
    kept: list[dict] = []
    seen_group: dict[str, int] = {}
    for item in picked:
        if seen_group.get(item["group"], 0) >= per_group_cap:
            continue
        seen_group[item["group"]] = seen_group.get(item["group"], 0) + 1
        kept.append(item)
    # fill any spare capacity with the rest of the list
    if len(kept) < args.limit:
        chosen = {(item["gid"]) for item in kept}
        for item in picked:
            if len(kept) >= args.limit:
                break
            if item["gid"] in chosen:
                continue
            chosen.add(item["gid"])
            kept.append(item)
    kept = kept[:args.limit]
    kept.sort(key=lambda item: (item["group"], item["title"]))

    print("shelves:", {g: c for g, c in sorted(seen_group.items())})
    print(f"{len(kept)} books selected")
    if args.dry_run:
        for item in kept[:40]:
            print(f"  [{item['group']:11s}] {item['gid']:>6}  {item['title'][:64]}")
        return 0

    # --------------------------------------------------------------------------
    # download
    # --------------------------------------------------------------------------
    failures: list[tuple[int, str]] = []
    done = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {}
        for item in kept:
            slug = slugify(item["title"])
            target = archive / f"{slug}.txt"
            futures[pool.submit(fetch_one, item["gid"], target)] = item
        for future in as_completed(futures):
            item = futures[future]
            done += 1
            try:
                future.result()
            except Exception as error:  # noqa: BLE001 - keep going
                failures.append((item["gid"], str(error)))
            if done % 100 == 0:
                print(f"  {done}/{len(kept)} ({len(failures)} failed)")
    if failures:
        print(f"{len(failures)} downloads failed:", failures[:10])

    # --------------------------------------------------------------------------
    # write the catalogue module
    # --------------------------------------------------------------------------
    from app.seed.run import guess_year  # reuse the seeder's title page reader

    entries: list[str] = []
    used_slugs: dict[str, int] = {}
    for item in kept:
        slug = slugify(item["title"])
        target = archive / f"{slug}.txt"
        if not target.exists():
            continue
        if slug in used_slugs:
            used_slugs[slug] += 1
            slug = f"{slug}-{used_slugs[slug]}"
        else:
            used_slugs[slug] = 1
        shelf, motif, base, accent = SHELF[item["group"]]
        rot_a, rot_b = ROTATE[used_slugs.get(slug, 0) % len(ROTATE)]
        text = target.read_text(encoding="utf-8", errors="replace")
        year = guess_year(text[:4000]) or ""
        summary = summarise(item["title"], item["subjects"])
        author = item["author"].split(";")[0].strip() or "Unknown"
        entries.append(
            f"    ({item['gid']}, {slug!r},\n"
            f"     {item['title']!r},\n"
            f"     {author!r}, {shelf!r},\n"
            f"     {summary!r},\n"
            f"     {motif!r}, {rot_a!r}, {rot_b!r}, {year or ''}),"
        )

    out = ROOT / "app" / "seed" / "books_extra.py"
    out.write_text(
        '"""Extra shelves of Gutenberg books, filled in by tools/fetch_gutenberg.py.\n\n'
        "Generated file: run ``python3 tools/fetch_gutenberg.py`` to refresh it.\n"
        "Each entry is (gutenberg_id, slug, title, author, category, summary,\n"
        "motif, base, accent, year).\n"
        '"""\n\n'
        "from __future__ import annotations\n\n"
        "BOOKS: list[tuple] = [\n"
        + "\n".join(entries)
        + "\n]\n",
        encoding="utf-8")
    print(f"wrote {out} with {len(entries)} books")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
