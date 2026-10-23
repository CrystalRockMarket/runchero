#!/usr/bin/env python3
"""Check every wiki link in the depot.

    python3 tools/check_links.py

Every note, and every formula, is written with `[[wiki-slug]]` links. A link that
points at nothing renders as a grey `[slug]` on the page, which is a dead end for
the reader. This walks the seed data and reports any link that does not resolve,
plus any note that links to itself.

Exit code is 1 when something is wrong, so it can be used as a check.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.seed import (articles, books, books_deep, books_extra, content,  # noqa: E402
                      collections as collection_data, formulas)
from app.seed import (notes_animals, notes_farming, notes_growing,  # noqa: E402
                      notes_kitchen, notes_reference, notes_vehicles,
                      notes_workshop, notes_yard)

NOTE_MODULES = (notes_vehicles, notes_farming, notes_animals, notes_workshop,
                notes_yard, notes_kitchen, notes_growing, notes_reference)

WIKI = re.compile(r"\[\[([^\]]+)\]\]")


def slug_of(term: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", term.strip().lower()).strip("-")


def target_of(inner: str) -> str:
    """`[[slug|label]]` points at the slug; the label is only the text."""
    return inner.split("|", 1)[0].strip() if "|" in inner else inner.strip()


def known_slugs(article_slugs: set[str]) -> dict[str, str]:
    """Every slug a link is allowed to point at, and what kind it is."""
    known: dict[str, str] = {s: "note" for s in article_slugs}
    for gid, slug, *rest in [*books.BOOKS, *books_extra.BOOKS,
                             *books_deep.BOOKS]:
        known.setdefault(slug, "book")
    for item in collection_data.COLLECTIONS:
        known.setdefault(item["slug"], "depot")
    for slug, *rest in content.CATEGORIES:
        known.setdefault(slug, "shelf")
    for vehicle in content.VEHICLES:
        known.setdefault(vehicle[0], "machine")
    for formula in formulas.FORMULAS:
        known.setdefault(formula["slug"], "formula")
    for term, definition, category, icon in content.GLOSSARY:
        known.setdefault(slug_of(term), "glossary term")
    return known


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check the wiki links in the depot")
    parser.add_argument("--verbose", action="store_true",
                        help="list every link, not just the broken ones")
    args = parser.parse_args(argv)

    items = list(articles.ARTICLES)
    for module in NOTE_MODULES:
        items.extend(module.NOTES)

    article_slugs = {item["slug"] for item in items}
    known = known_slugs(article_slugs)

    broken: list[tuple[str, str, str]] = []
    self_links: list[tuple[str, str]] = []
    total = 0

    def check(owner: str, field: str, text: str) -> None:
        nonlocal total
        for inner in WIKI.findall(text or ""):
            total += 1
            slug = target_of(inner)
            if slug == owner:
                self_links.append((owner, field))
            if slug not in known:
                broken.append((owner, field, slug))
            elif args.verbose:
                print(f"  {owner:40s} -> {known[slug]:14s} {slug}")

    for item in items:
        check(item["slug"], "note", item["body"])
    for formula in formulas.FORMULAS:
        for field in ("expression", "symbols", "units", "how", "example"):
            check(formula["slug"], "formula", formula.get(field) or "")

    print(f"{len(items)} notes and {len(formulas.FORMULAS)} formulas, "
          f"{total} wiki links checked")

    if broken:
        print(f"\n{len(broken)} broken link(s):")
        for owner, field, slug in sorted(set(broken)):
            print(f"  {slug:45s} in {owner} ({field})")
    if self_links:
        print(f"\n{len(self_links)} self link(s):")
        for owner, field in sorted(set(self_links)):
            print(f"  {owner} ({field})")

    if not broken and not self_links:
        print("every link resolves")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
