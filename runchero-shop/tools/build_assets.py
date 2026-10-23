#!/usr/bin/env python3
"""Build the static art: export every icon as a PNG at the sizes the theme
uses, plus the shop logo and favicon.

    python3 tools/build_assets.py

Idempotent: safe to re-run any time the icon set changes.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import db, config  # noqa: E402
from app.pixel import draw, icons  # noqa: E402
from app.pixel.font5x7 import GLYPH_HEIGHT, GLYPH_WIDTH  # noqa: E402

OUT = config.STATIC_DIR / "img" / "icons"
SCALES = {1: None, 2: "@2x", 3: "@3x", 4: "@4x"}


def cow_mark() -> Image.Image:
    """Draw a larger, transparent Holstein-style pixel cow for the brand."""
    img = Image.new("RGBA", (128, 96), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    ink = (27, 27, 35, 255)
    cream = (253, 246, 227, 255)
    white = (255, 255, 255, 255)
    pink = (242, 138, 178, 255)
    grass = (108, 194, 74, 255)
    sun = (255, 210, 74, 255)

    # Tail and tuft.
    d.line([(24, 44), (16, 52), (16, 68), (12, 72)], fill=ink, width=4)
    d.rectangle((8, 68, 16, 76), fill=ink)
    d.rectangle((12, 72, 20, 80), fill=ink)

    # Legs behind the barrel, then hooves.
    for x in (32, 56, 84, 100):
        d.rectangle((x, 62, x + 12, 88), fill=ink)
        d.rectangle((x + 4, 66, x + 8, 80), fill=cream)
        d.rectangle((x, 82, x + 12, 92), fill=ink)
    # Udder peeking between the legs.
    d.rectangle((68, 64, 84, 76), fill=pink)
    d.rectangle((72, 72, 76, 80), fill=pink)
    d.rectangle((80, 72, 84, 80), fill=pink)

    # Main body, with squared pixel-art silhouette and Holstein patches.
    d.rectangle((24, 28, 104, 72), fill=ink)
    d.rectangle((28, 32, 100, 68), fill=white)
    d.polygon([(36, 32), (56, 32), (56, 40), (64, 40), (64, 56),
               (56, 56), (56, 64), (40, 64), (40, 56), (32, 56),
               (32, 40), (36, 40)], fill=ink)
    d.polygon([(72, 32), (88, 32), (88, 40), (96, 40), (96, 52),
               (88, 52), (88, 60), (76, 60), (76, 52), (68, 52),
               (68, 40), (72, 40)], fill=ink)
    d.rectangle((44, 60, 52, 68), fill=ink)

    # Neck and head facing right.
    d.rectangle((88, 36, 112, 64), fill=ink)
    d.rectangle((92, 40, 108, 60), fill=cream)
    d.rectangle((100, 28, 124, 56), fill=ink)
    d.rectangle((104, 32, 120, 52), fill=white)
    # Ear, horns, eye, and muzzle.
    d.polygon([(100, 32), (92, 28), (92, 36), (100, 40)], fill=ink)
    d.rectangle((104, 20, 108, 32), fill=ink)
    d.rectangle((108, 20, 112, 28), fill=sun)
    d.rectangle((116, 24, 120, 32), fill=ink)
    d.rectangle((112, 36, 116, 40), fill=ink)
    d.rectangle((116, 40, 128, 56), fill=ink)
    d.rectangle((120, 44, 124, 52), fill=pink)
    d.rectangle((124, 44, 128, 52), fill=pink)
    # Cream cheek and collar accent.
    d.rectangle((96, 48, 112, 60), fill=cream)
    d.rectangle((88, 60, 108, 64), fill=grass)

    # Ground detail.
    d.rectangle((20, 92, 108, 96), fill=grass)
    d.rectangle((28, 88, 36, 92), fill=grass)
    d.rectangle((92, 88, 100, 92), fill=grass)
    return img


def export_icons() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    for name in sorted(icons.ICONS):
        for scale, suffix in SCALES.items():
            img = draw.icon_image(name, scale)
            target = OUT / (f"{name}{suffix or ''}.png")
            draw.save(img, target)
            count += 1
    return count


def export_logo() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    # Wordmark on the shop's ink background so it sits cleanly in the topbar.
    img = draw.new_canvas(300, 64, "ink2")
    mark = cow_mark()
    mark.thumbnail((68, 56), Image.Resampling.NEAREST)
    img.alpha_composite(mark, (5, 4))
    draw.draw_text(img, 82, 15, "RUNCHERO", colour="cream", scale=3, spacing=2)
    draw.draw_text(img, 84, 42, "BEEF", colour="grass3", scale=2, spacing=3)
    draw.save(img, OUT / "logo.png")

    mark = cow_mark()
    draw.save(mark, OUT / "cow-mark.png")

    # Favicons use the larger brand cow, nearest-neighbour scaled to keep its
    # stepped pixel edges crisp at every browser-requested size.
    mark = cow_mark()
    for size in (32, 64, 180, 192, 512):
        canvas = draw.new_canvas(size, size, "ink")
        thumb = mark.copy()
        thumb.thumbnail((size - 8, size - 8), Image.Resampling.NEAREST)
        canvas.alpha_composite(thumb, ((size - thumb.width) // 2,
                                       (size - thumb.height) // 2))
        draw.save(canvas, OUT / f"favicon-{size}.png")

def export_cover(filename: str, title: str, subtitle: str) -> None:
    """Build a high-resolution pixel-art social card for one co-op store."""
    img = draw.new_canvas(1200, 630, "ink")
    mark = cow_mark().resize((320, 240), Image.Resampling.NEAREST)
    img.alpha_composite(mark, (440, 28))
    width = draw.text_width(title, scale=4, spacing=2)
    draw.draw_text(img, (1200 - width) // 2, 326, title, colour="cream",
                   scale=4, spacing=2)
    width = draw.text_width(subtitle, scale=3, spacing=2)
    draw.draw_text(img, (1200 - width) // 2, 414, subtitle, colour="grass3",
                   scale=3, spacing=2)
    draw.save(img, config.STATIC_DIR / "img" / filename)


def main() -> int:
    config.ensure_dirs()
    made = export_icons()
    export_logo()
    export_cover("og-cover.png", "RUNCHERO BEEF", "LOCALLY GROWN. CUT FOR YOUR TABLE.")
    export_cover("og-fermentation.png", "FERMENTATION STATION",
                 "SMALL-BATCH FERMENTED FOODS")
    export_cover("og-freeze-dried.png", "RUNCHERO FREEZE-DRIED",
                 "FARM-GROWN. JUST ADD HOT WATER.")
    print(f"exported {made} high-resolution pixel icons, logo, favicons, and store social cards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
