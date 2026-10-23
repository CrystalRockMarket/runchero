#!/usr/bin/env python3
"""Generate every pixel-art asset the site uses.

Run it after changing the palette, the icon set or the book catalogue:

    python3 tools/build_assets.py

Everything is drawn locally with PIL. No downloads, no fonts to install.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import config, palette  # noqa: E402
from app.pixel import draw, icons  # noqa: E402
from app.seed import books as book_catalogue  # noqa: E402
from app.seed import books_deep  # noqa: E402
from app.seed import books_extra  # noqa: E402
from app.seed import manuals as manual_catalogue  # noqa: E402

IMG = config.STATIC_DIR / "img"


def build_icons() -> int:
    folder = IMG / "icons"
    folder.mkdir(parents=True, exist_ok=True)
    for name in icons.ICONS:
        draw.save(draw.icon_image(name, 1), folder / f"{name}.png")
    return len(icons.ICONS)


def build_app_icons() -> None:
    """Square marks for the web manifest."""
    for size in (192, 512):
        mark = draw.icon_image("depot", 1).resize((size, size), 0)
        # NEAREST keeps the pixels square
        from PIL import Image
        mark = draw.icon_image("depot", 1).resize((size, size), Image.NEAREST)
        draw.save(mark, IMG / f"icon-{size}.png")


def build_logo() -> None:
    logo = draw.make_logo("Runchero", "Information Depo", width=214, height=42)
    draw.save(logo, IMG / "logo.png")


def build_hero() -> None:
    hero = draw.make_hero(width=320, height=84)
    draw.save(hero, IMG / "hero.png")


def build_tiles() -> None:
    folder = IMG / "tiles"
    folder.mkdir(parents=True, exist_ok=True)
    for index, (a, b) in enumerate([
        ("sky", "sky2"), ("grass", "grass2"), ("soil", "soil2"), ("cream", "paper2")
    ]):
        tile = draw.new_canvas(8, 8)
        draw.dither_rect(tile, 0, 0, 8, 8, a, b, pattern=index % 4, cell=1)
        draw.save(tile, folder / f"dither-{index}.png")


def build_covers(curated_only: bool = True) -> int:
    folder = IMG / "covers"
    folder.mkdir(parents=True, exist_ok=True)
    count = 0
    for entry in [*book_catalogue.BOOKS, *books_extra.BOOKS, *books_deep.BOOKS]:
        _, slug, title, author, _cat, _summary, motif, base, accent, year = entry
        if curated_only and slug not in book_catalogue.CURATED:
            continue
        cover = draw.make_cover(
            title=title,
            author=author,
            year=str(year),
            base=base,
            accent=accent,
            motif=motif,
            stamp="PD",
        )
        draw.save(cover, folder / f"{slug}.png")
        count += 1
    for item in manual_catalogue.MANUALS:
        cover = draw.make_cover(
            title=item["title"],
            author=item["author"],
            year=str(item["year"] or ""),
            base="sky2",
            accent="sun",
            motif="tractor",
            stamp="PD",
        )
        draw.save(cover, folder / f"{item['slug']}.png")
        count += 1
    return count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Draw the pixel art")
    parser.add_argument("--all-books", action="store_true",
                        help="draw a cover for every book, not just the curated ones")
    args = parser.parse_args(argv)

    config.ensure_dirs()
    icons_made = build_icons()
    build_app_icons()
    build_logo()
    build_hero()
    build_tiles()
    covers = build_covers(curated_only=not args.all_books)
    print(f"icons   : {icons_made}")
    print(f"covers  : {covers}")
    print(f"palette : {len(palette.PALETTE)} colours")
    print(f"written : {IMG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
