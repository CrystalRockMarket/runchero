#!/usr/bin/env python3
"""Bulk download ALL relevant Project Gutenberg books for an offline farming community.

This script:
1. Fetches the full Gutenberg catalogue (~70k books)
2. Filters to farming/rural/craft/health/survival topics (same logic as fetch_gutenberg.py)
3. Downloads ALL matching books to ~/archive/books/ (resumable, skips existing)
4. Optionally watches ~/archive/books/ and auto-seeds new files into the depot

Usage:
    python3 tools/bulk_gutenberg.py                    # one-shot bulk download
    python3 tools/bulk_gutenberg.py --watch            # download then watch for new files
    python3 tools/bulk_gutenberg.py --watch-only       # just watch, no initial download
    python3 tools/bulk_gutenberg.py --dry-run          # show what would be downloaded
    python3 tools/bulk_gutenberg.py --limit 500        # cap at 500 books

Time estimates (on typical broadband):
    ~1,200 books: 30-60 minutes (sequential) / 5-10 minutes (16 workers)
    ~3,000 books: 60-120 minutes / 15-25 minutes
    ~7,000 books: 2-4 hours / 30-60 minutes
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    Observer = None
    FileSystemEventHandler = object

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import config  # noqa: E402

CATALOG_URL = "https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv.gz"
CACHE = Path("/tmp/pg_catalog.csv.gz")
TEXT_URL = "https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt"
ALT_URL = "https://www.gutenberg.org/files/{id}/{id}-0.txt"
USER_AGENT = ("Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 "
              "Firefox/128.0 (Runchero Bulk Gutenberg Fetcher)")
MAX_BYTES = 8 * 1024 * 1024
DEFAULT_WORKERS = 16

# =============================================================================
# Classification (copied from fetch_gutenberg.py - keep in sync)
# =============================================================================

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

SKIP_TAIL = {
    "history", "early works to 1800", "early works to 1850", "periodicals",
    "juvenile literature", "juvenile", "dictionaries", "dictionary",
    "bibliography", "indexes", "catalogs", "exhibitions", "pictorial works",
    "handbooks and manuals", "handbooks", "manuals", "textbooks", "textbooks and manuals",
}


def load_catalog() -> list[dict]:
    if not CACHE.exists():
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        print("fetching the Gutenberg catalogue (~30 MB)...")
        with urllib.request.urlopen(
                urllib.request.Request(CATALOG_URL, headers={"User-Agent": USER_AGENT}),
                timeout=180) as response:
            CACHE.write_bytes(response.read())
    with gzip.open(CACHE, "rt", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def split_fields(value: str) -> list[str]:
    return [part.strip() for part in (value or "").split(";") if part.strip()]


def core_head(subject: str) -> str:
    head = subject.split(" -- ")[0].strip()
    return head


def classify(row: dict) -> tuple[str, int] | None:
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


# =============================================================================
# Downloading
# =============================================================================

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


# =============================================================================
# Auto-seed watcher
# =============================================================================

class ArchiveWatcher(FileSystemEventHandler):
    def __init__(self, debounce_sec: float = 2.0):
        self.debounce_sec = debounce_sec
        self.pending: dict[Path, float] = {}
        self.last_seed = 0.0

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".txt"):
            self.pending[Path(event.src_path)] = time.time()

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".txt"):
            self.pending[Path(event.src_path)] = time.time()

    def process_pending(self):
        now = time.time()
        ready = [p for p, t in self.pending.items() if now - t >= self.debounce_sec]
        if not ready:
            return
        for p in ready:
            del self.pending[p]
        self.seed_new_files(ready)

    def seed_new_files(self, paths: list[Path]):
        print(f"\n[watcher] {len(paths)} new book file(s) detected, seeding...")
        try:
            from app import db
            from app.seed import run as seed_run
            config.ensure_dirs()
            conn = db.connect()
            db.init_db(conn)
            category_ids = seed_run.seed_categories(conn)
            fetched, cached, shelved = seed_run.seed_books(conn, category_ids, fetch=False, everything=True)
            db.reindex(conn)
            conn.commit()
            conn.close()
            print(f"[watcher] seeded: {fetched} fetched, {cached} cached, {shelved} on shelves")
        except Exception as e:
            print(f"[watcher] seed failed: {e}")


def run_watcher(archive_dir: Path):
    if not WATCHDOG_AVAILABLE:
        print("[watcher] watchdog not installed. Install with: sudo apt install python3-watchdog")
        return
    print(f"[watcher] monitoring {archive_dir} for new .txt files...")
    handler = ArchiveWatcher()
    observer = Observer()
    observer.schedule(handler, str(archive_dir), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
            handler.process_pending()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


# =============================================================================
# Main
# =============================================================================

def estimate_time(book_count: int, workers: int) -> str:
    # Rough estimate: ~2-3 sec/book sequential, ~0.5 sec with 16 workers
    if workers <= 1:
        secs = book_count * 2.5
    else:
        secs = book_count * 0.5 / (workers / 16) + 30
    if secs < 60:
        return f"~{int(secs)} seconds"
    elif secs < 3600:
        return f"~{int(secs/60)} minutes"
    else:
        return f"~{secs/3600:.1f} hours"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bulk download relevant Gutenberg books for offline farming depot")
    parser.add_argument("--limit", type=int, default=0, help="max books to download (0 = all matching)")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS, help=f"parallel downloads (default {DEFAULT_WORKERS})")
    parser.add_argument("--dry-run", action="store_true", help="list books without downloading")
    parser.add_argument("--watch", action="store_true", help="after download, watch ~/archive/books/ and auto-seed")
    parser.add_argument("--watch-only", action="store_true", help="skip download, just watch and auto-seed")
    parser.add_argument("--per-group", type=int, default=0, help="cap per topic group (0 = no cap)")
    args = parser.parse_args(argv)

    config.ensure_dirs()
    archive = config.ARCHIVE_DIR / "books"
    archive.mkdir(parents=True, exist_ok=True)

    # Load existing catalogue to skip already-downloaded
    from app.seed import books as curated_books
    skip_ids = {entry[0] for entry in curated_books.BOOKS}
    skip_slugs = {entry[1] for entry in curated_books.BOOKS}
    existing_files = {f.stem for f in archive.glob("*.txt")}

    print("reading the catalogue...")
    rows = load_catalog()
    print(f"  {len(rows):,} total entries in Gutenberg catalogue")

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
        if not title or slugify(title) in skip_slugs or slugify(title) in existing_files:
            continue
        picked.append({
            "gid": gid, "group": group, "score": score, "title": title,
            "author": (row.get("Authors", "") or "Unknown").strip(),
            "subjects": split_fields(row.get("Subjects", "")),
        })
        counts[group] = counts.get(group, 0) + 1

    picked.sort(key=lambda item: (item["group"], -item["score"], item["title"]))

    if args.limit:
        per_group_cap = max(1, args.limit // max(1, len(GROUPS)))
        kept: list[dict] = []
        seen_group: dict[str, int] = {}
        for item in picked:
            if seen_group.get(item["group"], 0) >= per_group_cap:
                continue
            seen_group[item["group"]] = seen_group.get(item["group"], 0) + 1
            kept.append(item)
        if len(kept) < args.limit:
            chosen = {item["gid"] for item in kept}
            for item in picked:
                if len(kept) >= args.limit:
                    break
                if item["gid"] in chosen:
                    continue
                chosen.add(item["gid"])
                kept.append(item)
        picked = kept[:args.limit]

    print("\nSelected by shelf:")
    for group in sorted(counts.keys()):
        gcount = sum(1 for b in picked if b["group"] == group)
        print(f"  {group:12s}: {gcount:,}")
    print(f"\nTotal: {len(picked):,} books")
    print(f"Estimated time: {estimate_time(len(picked), args.workers)} with {args.workers} workers")

    if args.dry_run:
        for item in picked[:50]:
            print(f"  [{item['group']:11s}] {item['gid']:>6}  {item['title'][:70]}")
        if len(picked) > 50:
            print(f"  ... and {len(picked) - 50} more")
        return 0

    if not picked:
        print("Nothing to download.")
    else:
        print("\nDownloading...")
        failures: list[tuple[int, str]] = []
        done = 0
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {}
            for item in picked:
                slug = slugify(item["title"])
                target = archive / f"{slug}.txt"
                futures[pool.submit(fetch_one, item["gid"], target)] = item
            for future in as_completed(futures):
                item = futures[future]
                done += 1
                try:
                    future.result()
                except Exception as error:
                    failures.append((item["gid"], str(error)))
                if done % 50 == 0 or done == len(picked):
                    print(f"  {done}/{len(picked)} ({len(failures)} failed)")
        if failures:
            print(f"\n{len(failures)} downloads failed (first 10):")
            for gid, err in failures[:10]:
                print(f"  {gid}: {err}")

    # Auto-seed after download
    if picked and not args.watch_only:
        print("\nSeeding depot database...")
        try:
            from app import db
            from app.seed import run as seed_run
            conn = db.connect()
            db.init_db(conn)
            category_ids = seed_run.seed_categories(conn)
            fetched, cached, shelved = seed_run.seed_books(conn, category_ids, fetch=False, everything=True)
            db.reindex(conn)
            conn.commit()
            conn.close()
            print(f"Seeded: {fetched} fetched, {cached} cached, {shelved} on shelves")
        except Exception as e:
            print(f"Seed failed: {e}")

    if args.watch or args.watch_only:
        run_watcher(archive)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())