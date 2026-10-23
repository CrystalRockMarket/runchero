#!/usr/bin/env python3
"""Generate every pixel asset the site needs.

Run from the project root:

    python3 tools/build_assets.py

Outputs land in ``domain/_WEB/_PIXEL/`` (images) and
``domain/_WEB/_STYLES/EL_SS_PIXEL_vars.css`` (the palette custom properties).
The palette in ``pixel/palette.py`` is the single source of truth, so the CSS
and the artwork can never drift apart.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from PIL import Image  # noqa: E402

from pixel import draw, icons, palette  # noqa: E402

PIXEL_DIR = ROOT / "domain" / "_WEB" / "_PIXEL"
ICON_DIR = PIXEL_DIR / "icons"
STYLE_DIR = ROOT / "domain" / "_WEB" / "_STYLES"

SITE_NAME = "GAMES.EARTH"
SITE_SUB = "THE PIXEL DIRECTORY"
THEME_BG = "#1b1b23"
THEME_ACCENT = "#ffd24a"

#: Icons that get their own standalone PNG in ``_PIXEL/icons/``.
FEATURED = [
    "arcade", "board", "cards", "dice", "puzzle", "controller", "trophy",
    "medal", "crown", "flag", "target", "ladder", "tiles", "clock",
    "hourglass", "idea", "compass", "map", "book", "globe", "users",
]


def build_icons() -> list[Path]:
    """Every icon at 1x, 2x and 3x."""
    written: list[Path] = []
    for name, rows in icons.ICONS.items():
        img = Image.new("RGBA", (icons.ICON_SIZE, icons.ICON_SIZE), (0, 0, 0, 0))
        for row_index, row in enumerate(rows):
            for col_index, cell in enumerate(row):
                if cell == ".":
                    continue
                colour = palette.ICON_LEGEND.get(cell)
                if colour is None:
                    continue
                img.putpixel((col_index, row_index), palette.rgb(colour) + (255,))
        draw.save(img, ICON_DIR / f"{name}.png")
        written.append(ICON_DIR / f"{name}.png")
        for scale in (2, 3):
            big = img.resize(
                (icons.ICON_SIZE * scale, icons.ICON_SIZE * scale),
                Image.NEAREST,
            )
            path = ICON_DIR / f"{name}@{scale}x.png"
            draw.save(big, path)
            written.append(path)
    return written


def build_logo() -> list[Path]:
    """The wordmark, on a transparent background for the dark header."""
    written = []
    logo = draw.make_logo(SITE_NAME, SITE_SUB, mark="arcade", width=260, height=48)
    draw.save(logo, PIXEL_DIR / "logo.png")
    written.append(PIXEL_DIR / "logo.png")
    big = logo.resize((logo.width * 2, logo.height * 2), Image.NEAREST)
    draw.save(big, PIXEL_DIR / "logo@2x.png")
    written.append(PIXEL_DIR / "logo@2x.png")
    return written


def build_hero() -> list[Path]:
    written = []
    hero = draw.make_hero(320, 96)
    draw.save(hero, PIXEL_DIR / "hero.png")
    written.append(PIXEL_DIR / "hero.png")
    big = hero.resize((hero.width * 2, hero.height * 2), Image.NEAREST)
    draw.save(big, PIXEL_DIR / "hero@2x.png")
    written.append(PIXEL_DIR / "hero@2x.png")
    return written


def _favicon_base(mark: str = "arcade", size: int = 32) -> Image.Image:
    """A solid tile with a centred mark, sized for a favicon."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    from PIL import ImageDraw

    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, size - 1, size - 1], fill=palette.rgb("ink") + (255,))
    d.rectangle([1, 1, size - 2, size - 2], fill=palette.rgb("navy") + (255,))
    inner = int(size * 0.66)
    scale = max(1, inner // icons.ICON_SIZE)
    mark_img = draw.icon_image(mark, scale)
    img.alpha_composite(mark_img, ((size - mark_img.width) // 2,
                                   (size - mark_img.height) // 2))
    return img


def build_favicons() -> list[Path]:
    written = []
    for size in (16, 32, 48):
        path = PIXEL_DIR / f"favicon-{size}.png"
        draw.save(_favicon_base(size=size), path)
        written.append(path)
    draw.save(_favicon_base(size=32), PIXEL_DIR / "favicon.png")
    written.append(PIXEL_DIR / "favicon.png")

    # PWA icons: flat, full-bleed background, mark centred.
    for size in (192, 512):
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        from PIL import ImageDraw

        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, size - 1, size - 1], fill=palette.rgb("navy") + (255,))
        d.rectangle([0, 0, size - 1, size - 1], outline=palette.rgb("ink") + (255,),
                    width=max(2, size // 32))
        inner = int(size * 0.5)
        scale = max(1, inner // icons.ICON_SIZE)
        mark_img = draw.icon_image("arcade", scale)
        img.alpha_composite(mark_img, ((size - mark_img.width) // 2,
                                       (size - mark_img.height) // 2))
        path = PIXEL_DIR / f"icon-{size}.png"
        draw.save(img, path)
        written.append(path)

    # Maskable: mark kept inside the 80% safe zone, full-bleed background.
    size = 512
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    from PIL import ImageDraw

    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, size - 1, size - 1], fill=palette.rgb("navy") + (255,))
    safe = int(size * 0.60)
    scale = max(1, safe // icons.ICON_SIZE)
    mark_img = draw.icon_image("arcade", scale)
    img.alpha_composite(mark_img, ((size - mark_img.width) // 2,
                                   (size - mark_img.height) // 2))
    path = PIXEL_DIR / "icon-maskable-512.png"
    draw.save(img, path)
    written.append(path)
    return written


def build_tiles() -> list[Path]:
    written = []
    for name, (a, b) in {
        "dither-navy": ("navy", "ink2"),
        "dither-ink": ("ink", "ink2"),
        "dither-paper": ("paper2", "paper"),
    }.items():
        path = PIXEL_DIR / f"{name}.png"
        draw.save(draw.make_dither_tile(16, a, b, pattern=1), path)
        written.append(path)
    return written


def build_css_vars() -> Path:
    """Emit the palette as CSS custom properties."""
    STYLE_DIR.mkdir(parents=True, exist_ok=True)
    body = [
        "/* Generated by tools/build_assets.py - do not edit by hand.",
        " * Source of truth: pixel/palette.py",
        " */",
        ":root {",
        palette.css_vars(),
        "",
        "  /* semantic aliases */",
        palette.semantic_vars(),
        "}",
        "",
    ]
    path = STYLE_DIR / "EL_SS_PIXEL_vars.css"
    path.write_text("\n".join(body))
    return path


def main() -> int:
    print("building pixel assets...")
    groups = {
        "icons": build_icons(),
        "logo": build_logo(),
        "hero": build_hero(),
        "favicons": build_favicons(),
        "tiles": build_tiles(),
    }
    for name, paths in groups.items():
        print(f"  {name}: {len(paths)} file(s)")
    css = build_css_vars()
    print(f"  css vars: {css.relative_to(ROOT)}")
    total = sum(len(p) for p in groups.values())
    print(f"done: {total} images")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
