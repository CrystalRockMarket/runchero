"""Pixel rendering helpers built on PIL.

Everything in the app is drawn on a logical pixel grid. Images are never
resampled with a smooth filter, so edges stay hard when a browser scales them
with ``image-rendering: pixelated``.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

from PIL import Image, ImageDraw

from .. import palette
from . import font5x7, icons

Image.MAX_IMAGE_PIXELS = None


# --------------------------------------------------------------------------
# canvas helpers
# --------------------------------------------------------------------------
def new_canvas(width: int, height: int, bg: str | None = None) -> Image.Image:
    """Create an RGBA canvas, optionally filled with a palette colour."""
    if bg is None:
        return Image.new("RGBA", (width, height), (0, 0, 0, 0))
    return Image.new("RGBA", (width, height), palette.rgb(bg) + (255,))


def _rgba(colour: str, alpha: int = 255) -> tuple[int, int, int, int]:
    return palette.rgb(colour) + (alpha,)


def draw_rect(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int,
              colour: str) -> None:
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=_rgba(colour))


def draw_bevel(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int,
               top: str = "white", bottom: str = "grey2", fill: str | None = None,
               thickness: int = 1) -> None:
    """Classic 90s bevel: light top/left, dark bottom/right."""
    if fill:
        draw_rect(draw, x, y, w, h, fill)
    for i in range(thickness):
        draw.line([x + i, y + i, x + w - 1 - i, y + i], fill=_rgba(top))
        draw.line([x + i, y + i, x + i, y + h - 1 - i], fill=_rgba(top))
        draw.line([x + i, y + h - 1 - i, x + w - 1 - i, y + h - 1 - i], fill=_rgba(bottom))
        draw.line([x + w - 1 - i, y + i, x + w - 1 - i, y + h - 1 - i], fill=_rgba(bottom))


# --------------------------------------------------------------------------
# dithering
# --------------------------------------------------------------------------
#: 4 classic 2x2 dither patterns. Each is a 4x4 tile of on/off cells.
DITHER_TILES = {
    0: (0b0000, 0b0000, 0b0000, 0b0000),
    1: (0b1010, 0b0101, 0b1010, 0b0101),
    2: (0b1000, 0b0100, 0b0010, 0b0001),
    3: (0b1100, 0b1001, 0b1010, 0b0110),
}


def dither_rect(img: Image.Image, x: int, y: int, w: int, h: int,
                colour_a: str, colour_b: str, pattern: int = 1,
                cell: int = 2) -> None:
    """Fill a rectangle with a two-tone dither pattern."""
    draw = ImageDraw.Draw(img)
    tile = DITHER_TILES[pattern % len(DITHER_TILES)]
    for row in range(h):
        for col in range(w):
            bits = tile[row % 4]
            if bits & (1 << (col % 4)):
                draw.rectangle(
                    [x + col, y + row, x + col + cell - 1, y + row + cell - 1],
                    fill=_rgba(colour_a),
                )
            else:
                draw.rectangle(
                    [x + col, y + row, x + col + cell - 1, y + row + cell - 1],
                    fill=_rgba(colour_b),
                )


def vertical_gradient(img: Image.Image, x: int, y: int, w: int, h: int,
                      top: str, bottom: str, bands: int = 8) -> None:
    """Cheap pixel-art gradient: a few hard bands, dithered at the seams."""
    draw = ImageDraw.Draw(img)
    band_h = max(1, h // bands)
    for i in range(bands):
        top_y = y + i * band_h
        bot_y = y + (i + 1) * band_h if i < bands - 1 else y + h
        draw.rectangle([x, top_y, x + w - 1, bot_y - 1], fill=_rgba(top))
    draw.rectangle([x, y + h - band_h, x + w - 1, y + h - 1], fill=_rgba(bottom))


# --------------------------------------------------------------------------
# text
# --------------------------------------------------------------------------
def text_width(text: str, scale: int = 1, spacing: int = 1) -> int:
    if not text:
        return 0
    advance = (font5x7.GLYPH_WIDTH + spacing) * scale
    return len(text) * advance - spacing * scale


def draw_text(img: Image.Image, x: int, y: int, text: str, colour: str = "ink",
              scale: int = 1, spacing: int = 1) -> int:
    """Draw text with the 5x7 bitmap font. Returns the advance width."""
    draw = ImageDraw.Draw(img)
    advance = (font5x7.GLYPH_WIDTH + spacing) * scale
    cursor = x
    for char in text:
        rows = font5x7.glyph(char)
        for row_index, row in enumerate(rows):
            for col_index, cell in enumerate(row):
                if cell != "#":
                    continue
                px = cursor + col_index * scale
                py = y + row_index * scale
                draw.rectangle(
                    [px, py, px + scale - 1, py + scale - 1],
                    fill=_rgba(colour),
                )
        cursor += advance
    return cursor - x


def wrap_text(text: str, max_chars: int) -> list[str]:
    """Greedy word wrap using the monospace bitmap font."""
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                lines.append(current)
            if len(word) > max_chars:
                chunk = word
                while len(chunk) > max_chars:
                    lines.append(chunk[:max_chars])
                    chunk = chunk[max_chars:]
                current = chunk
            else:
                current = word
    if current:
        lines.append(current)
    return lines


def draw_text_block(img: Image.Image, x: int, y: int, lines: Iterable[str],
                    colour: str = "ink", scale: int = 1, spacing: int = 1,
                    line_gap: int = 2, align: str = "left",
                    max_width: int | None = None) -> int:
    """Draw multiple lines, returns the total height consumed."""
    height = 0
    for line in lines:
        width = text_width(line, scale, spacing)
        offset = 0
        if align == "center" and max_width:
            offset = (max_width - width) // 2
        elif align == "right" and max_width:
            offset = max_width - width
        draw_text(img, x + offset, y + height, line, colour, scale, spacing)
        height += font5x7.GLYPH_HEIGHT * scale + line_gap * scale
    return height


# --------------------------------------------------------------------------
# icons
# --------------------------------------------------------------------------
def icon_image(name: str, scale: int = 1) -> Image.Image:
    """Render one icon from its character map into an RGBA image."""
    rows = icons.ICONS.get(name)
    if rows is None:
        rows = icons.ICONS["info"]
    size = icons.ICON_SIZE
    img = Image.new("RGBA", (size * scale, size * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for row_index, row in enumerate(rows):
        for col_index, cell in enumerate(row):
            if cell == ".":
                continue
            colour = palette.ICON_LEGEND.get(cell)
            if colour is None:
                continue
            px = col_index * scale
            py = row_index * scale
            draw.rectangle([px, py, px + scale - 1, py + scale - 1],
                           fill=_rgba(colour))
    return img


def stamp_icon(img: Image.Image, name: str, x: int, y: int, scale: int = 1) -> None:
    """Draw an icon onto an existing canvas at integer position."""
    icon = icon_image(name, scale)
    img.alpha_composite(icon, (x, y))


def save(img: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "PNG", optimize=True)


# --------------------------------------------------------------------------
# composites
# --------------------------------------------------------------------------
def make_cover(title: str, author: str, year: str, base: str, accent: str,
               motif: str = "book", width: int = 120, height: int = 160,
               stamp: str | None = None) -> Image.Image:
    """Generate a pixel-art book cover.

    Covers are produced locally rather than downloaded so the archive stays
    self-contained and every book has a matching jacket.
    """
    img = new_canvas(width, height, base)
    draw = ImageDraw.Draw(img)

    # subtle vertical banding + dither corner
    vertical_gradient(img, 0, 0, width, height, base, palette.shade(base, 0.82),
                      bands=6)
    dither_rect(img, 0, height - 26, width, 26, accent, base, pattern=1)

    # frame
    draw_rect(draw, 0, 0, width, height, "ink")
    draw_rect(draw, 2, 2, width - 4, height - 4, accent)
    draw_rect(draw, 4, 4, width - 8, height - 8, base)

    # motif
    motif_scale = 5
    motif_w = icons.ICON_SIZE * motif_scale
    stamp_icon(img, motif, (width - motif_w) // 2, 16, motif_scale)

    # title
    title_scale = 2 if len(title) <= 26 else 1
    max_chars = max(8, (width - 16) // ((font5x7.GLYPH_WIDTH + 1) * title_scale))
    lines = wrap_text(title.upper(), max_chars)
    while len(lines) > 4 and title_scale > 1:
        title_scale = 1
        max_chars = (width - 16) // (font5x7.GLYPH_WIDTH + 1)
        lines = wrap_text(title.upper(), max_chars)
    lines = lines[:5]

    block_height = len(lines) * (font5x7.GLYPH_HEIGHT * title_scale + 2 * title_scale)
    title_y = 16 + motif_w + 12
    draw_text_block(img, 8, title_y, lines, colour="ink", scale=title_scale,
                    spacing=1, line_gap=2, align="center", max_width=width - 16)

    # rule
    rule_y = title_y + block_height + 4
    draw_rect(draw, 12, rule_y, width - 24, 1, accent)

    # author + year
    author_lines = wrap_text(author.upper(), 20)[:2]
    draw_text_block(img, 8, rule_y + 6, author_lines, colour="ink2", scale=1,
                    spacing=1, line_gap=1, align="center", max_width=width - 16)
    if year:
        draw_text(img, 8, height - 14, year, colour="ink2", scale=1)

    if stamp:
        stamp_w = text_width(stamp, 1) + 6
        draw_rect(draw, width - stamp_w - 6, 6, stamp_w, 11, "ink")
        draw_text(img, width - stamp_w - 3, 8, stamp, colour="white", scale=1)

    return img


def make_logo(wordmark: str, sub: str = "", width: int = 200,
              height: int = 40) -> Image.Image:
    """Pixel wordmark: a depot mark plus the name in the bitmap font."""
    img = new_canvas(width, height)
    draw = ImageDraw.Draw(img)

    mark_scale = 2
    mark_w = icons.ICON_SIZE * mark_scale
    stamp_icon(img, "depot", 0, (height - mark_w) // 2, mark_scale)

    text_x = mark_w + 6
    draw_text(img, text_x, 6, wordmark.upper(), colour="ink", scale=3, spacing=1)
    if sub:
        draw_text(img, text_x + 1, 30, sub.upper(), colour="ink2", scale=1, spacing=1)
    return img


def make_hero(width: int = 320, height: int = 80) -> Image.Image:
    """A wide pixel-art farm scene used as the dashboard banner."""
    img = new_canvas(width, height, "sky")
    draw = ImageDraw.Draw(img)

    # sky gradient bands
    for i in range(4):
        colour = "sky" if i % 2 == 0 else "sky2"
        draw.rectangle([0, i * height // 8, width, (i + 1) * height // 8 - 1],
                       fill=_rgba(colour))
    dither_rect(img, 0, 0, width, height // 4, "sky", "sky2", pattern=1, cell=1)

    # sun
    stamp_icon(img, "sun", width - 40, 8, 2)

    # clouds
    for cx, cy in ((28, 12), (110, 20), (200, 8)):
        draw_rect(draw, cx, cy, 22, 6, "white")
        draw_rect(draw, cx + 4, cy - 3, 12, 4, "white")
        dither_rect(img, cx + 2, cy + 4, 18, 3, "sky", "white", pattern=3, cell=1)

    # hills
    draw.rectangle([0, height - 34, width, height - 18], fill=_rgba("grass"))
    dither_rect(img, 0, height - 34, width, 8, "grass", "grass2", pattern=2, cell=1)
    draw.rectangle([0, height - 18, width, height], fill=_rgba("soil"))

    # ground texture
    for gx in range(0, width, 7):
        draw.rectangle([gx, height - 14, gx + 1, height - 12], fill=_rgba("soil2"))

    # barn + tractor on the hill
    stamp_icon(img, "depot", 40, height - 46, 2)
    stamp_icon(img, "tractor", 96, height - 40, 2)
    stamp_icon(img, "wheat", 160, height - 42, 2)
    stamp_icon(img, "cow", 200, height - 42, 2)
    stamp_icon(img, "hay", 250, height - 42, 2)
    stamp_icon(img, "tree" if "tree" in icons.ICONS else "wheat", 296, height - 42, 2)

    return img


def make_icon_sheet(names: Sequence[str], scale: int = 3,
                    columns: int = 8, cell: int = 22) -> Image.Image:
    """Contact sheet used while authoring the icon set."""
    rows = (len(names) + columns - 1) // columns
    img = new_canvas(columns * cell, rows * cell, "paper")
    draw = ImageDraw.Draw(img)
    for index, name in enumerate(names):
        x = (index % columns) * cell
        y = (index // columns) * cell
        stamp_icon(img, name, x + 2, y + 2, scale)
        draw_text(img, x + 1, y + 3 + icons.ICON_SIZE * scale, name[:6], "ink", 1)
    return img
