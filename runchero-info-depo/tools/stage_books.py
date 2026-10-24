#!/usr/bin/env python3
"""Stage books for later integration into the depot.

Drop files in /home/barn/archive/staging/ or pass paths. This tool:
- normalizes filenames to slugs
- extracts basic metadata (title from filename/content if possible)
- records them in archive/import_queue/manifest.jsonl with source info
- does NOT modify the database or site files - safe to run while another AI is working

Later, run with --integrate to add staged books to books_from_staged.py
and they'll be picked up on next seed.

Usage:
    python3 tools/stage_books.py /path/to/book.txt /path/to/book.pdf
    python3 tools/stage_books.py --scan
    python3 tools/stage_books.py --integrate  # prepares for next seed (non-destructive)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import config

STAGING = config.ARCHIVE_DIR / "staging"
QUEUE = config.ARCHIVE_DIR / "import_queue"
BOOKS = config.ARCHIVE_DIR / "books"
PDFS = BOOKS / "pdfs"
MANIFEST = QUEUE / "manifest.jsonl"
INTEGRATED = QUEUE / "integrated.json"


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return re.sub(r"-{2,}", "-", slug)[:80].strip("-")


def detect_title(path: Path) -> str:
    name = path.stem.replace("-", " ").replace("_", " ")
    # try to read first line if text
    if path.suffix.lower() in (".txt", ".md"):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")[:500]
            for line in text.splitlines():
                line = line.strip()
                if line and len(line) > 3 and not line.startswith(("#", "[", "---")):
                    return line[:200]
        except Exception:
            pass
    return name.title()


def stage_file(path: Path, source_url: str = "", license_info: str = "", 
               category: str = "lib-rural", topic: str = "") -> dict:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    if path.name.startswith(".") or path.name.lower().startswith("readme"):
        raise ValueError("README and hidden files are not staged")
    
    title = detect_title(path)
    slug = slugify(title)
    
    # copy to books dir
    if path.suffix.lower() == ".pdf":
        dest = PDFS / f"{slug}.pdf"
        if dest.exists():
            h = hashlib.sha256(path.read_bytes()).hexdigest()[:8]
            slug = f"{slug}-{h}"
            dest = PDFS / f"{slug}.pdf"
    else:
        dest = BOOKS / f"{slug}.txt"
        if dest.exists():
            h = hashlib.sha256(path.read_bytes()).hexdigest()[:8]
            slug = f"{slug}-{h}"
            dest = BOOKS / f"{slug}.txt"
    
    shutil.copy2(path, dest)
    data = dest.read_bytes()
    
    record = {
        "slug": slug,
        "title": title,
        "original_path": str(path),
        "staged_path": str(dest),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "suffix": path.suffix.lower(),
        "source_url": source_url,
        "license": license_info,
        "category": category,
        "topic": topic,
        "staged_at": datetime.now(timezone.utc).isoformat(),
        "status": "staged",
    }
    return record


def scan_staging() -> list[dict]:
    STAGING.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    PDFS.mkdir(parents=True, exist_ok=True)
    
    staged = []
    for path in STAGING.iterdir():
        if (path.is_file() and path.suffix.lower() in ('.txt', '.pdf', '.md')
                and not path.name.startswith('.')
                and not path.name.lower().startswith('readme')):
            try:
                rec = stage_file(path)
                staged.append(rec)
                # move to processed
                processed = STAGING / "processed"
                processed.mkdir(exist_ok=True)
                shutil.move(str(path), str(processed / path.name))
            except Exception as e:
                print(f"ERR {path}: {e}")
    return staged


def load_manifest() -> list[dict]:
    if not MANIFEST.exists():
        return []
    recs = []
    for line in MANIFEST.read_text(encoding='utf-8').splitlines():
        if line.strip():
            recs.append(json.loads(line))
    return recs


def write_manifest(recs: list[dict]):
    with MANIFEST.open('w', encoding='utf-8') as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')


def integrate() -> int:
    """Generate books_from_staged.py for seeder to pick up. Non-destructive."""
    recs = load_manifest()
    if not recs:
        print("nothing staged")
        return 0

    integrated = json.loads(INTEGRATED.read_text()) if INTEGRATED.exists() else []
    integrated_slugs = {i['slug'] for i in integrated}

    new_recs = [r for r in recs if r['slug'] not in integrated_slugs]
    if not new_recs:
        print("all staged books already integrated")
        return 0

    lines = []
    integrated_now = []
    for rec in new_recs:
        if rec.get('suffix') != '.txt':
            print(f"kept for later (PDF support pending): {rec['slug']}")
            continue
        title = rec['title'].replace("'", "\\'")
        author = rec.get('author', 'Unknown').replace("'", "\\'")
        slug = rec['slug']
        cat = rec.get('category', 'lib-rural')
        source_url = rec.get('source_url', '')
        license_info = rec.get('license', 'Public domain / source metadata only')
        motif = {'lib-livestock':'cow','lib-agriculture':'wheat','lib-machinery':'engine','lib-craft':'wrench','lib-kitchen':'jar','lib-health':'firstaid','lib-survival':'shield'}.get(cat,'book')
        summary = f"Staged from {rec.get('original_path','unknown')}. Source: {source_url or 'see manifest'}. License: {license_info}."
        gid = 0
        lines.append(f"    ({gid}, {slug!r}, {title!r}, {author!r}, {cat!r}, {summary!r}, {motif!r}, 'sky', 'sky2', ''),")
        integrated_now.append(rec)

    if not integrated_now:
        print("no text files ready to integrate")
        return 0

    out = ROOT / "app" / "seed" / "books_from_staged.py"
    content = f'''"""Books staged via tools/stage_books.py for later integration.

Only source metadata is recorded. No AI-generated descriptions.
Generated: {datetime.now(timezone.utc).isoformat()}
"""

from __future__ import annotations

BOOKS: list[tuple] = [
''' + '\n'.join(lines) + '\n]\n'
    tmp = out.with_suffix(".py.tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(out)

    integrated.extend(integrated_now)
    INTEGRATED.write_text(json.dumps(integrated, indent=2), encoding="utf-8")

    print(f"integrated {len(integrated_now)} books into {out}")
    print("run: python3 -m app.seed.run --no-fetch to add them to the site")
    return len(integrated_now)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Stage books for later integration')
    parser.add_argument('files', nargs='*')
    parser.add_argument('--scan', action='store_true')
    parser.add_argument('--integrate', action='store_true')
    parser.add_argument('--source-url', default='')
    parser.add_argument('--license', default='')
    parser.add_argument('--category', default='lib-rural')
    args = parser.parse_args(argv)
    
    config.ensure_dirs()
    STAGING.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    PDFS.mkdir(parents=True, exist_ok=True)
    
    recs = load_manifest()
    
    if args.integrate:
        return integrate()
    
    if args.scan or not args.files:
        staged = scan_staging()
        for s in staged:
            recs.append(s)
            print(f"staged: {s['slug']} ({s['bytes']} bytes)")
    else:
        for f in args.files:
            try:
                rec = stage_file(f, args.source_url, args.license, args.category)
                recs.append(rec)
                print(f"staged: {rec['slug']} ({rec['bytes']} bytes)")
            except Exception as e:
                print(f"ERR {f}: {e}")
    
    write_manifest(recs)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
