"""Pixel rendering helpers built on PIL.

Everything in the app is drawn on a logical pixel grid. Images are never
resampled with a smooth filter, so edges stay hard when a browser scales them
with ``image-rendering: pixelated``.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

from PIL import Image, ImageDraw

from . import palette
from . import font5x7

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
def save(img: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "PNG", optimize=True)


# --------------------------------------------------------------------------
# composites
# --------------------------------------------------------------------------
def make_logo(wordmark: str, sub: str = "", mark: str = "arcade",
              width: int = 220, height: int = 44,
              text_colour: str = "paper",
              sub_colour: str = "silver") -> Image.Image:
    """Pixel wordmark: a mark plus the name in the bitmap font.

    Defaults assume the dark site chrome: cream text on transparency.
    """
    img = new_canvas(width, height)
    draw = ImageDraw.Draw(img)

    mark_w = 0
    text_x = 8
    draw_text(img, text_x, 8, wordmark.upper(), colour=text_colour, scale=3, spacing=1)
    if sub:
        draw_text(img, text_x + 1, 32, sub.upper(), colour=sub_colour, scale=1, spacing=1)
    return img


def make_hero(width: int = 320, height: int = 96) -> Image.Image:
    """A wide pixel-art arcade scene used as the site banner."""
    img = new_canvas(width, height, "navy")
    draw = ImageDraw.Draw(img)

    # night sky bands
    for i in range(4):
        colour = "navy" if i % 2 == 0 else "ink2"
        draw.rectangle([0, i * height // 8, width, (i + 1) * height // 8 - 1],
                       fill=_rgba(colour))
    dither_rect(img, 0, 0, width, height // 3, "navy", "ink2", pattern=1, cell=1)

    # stars
    for sx, sy in ((14, 10), (46, 20), (88, 8), (132, 18), (196, 10),
                   (248, 22), (288, 12), (310, 30), (70, 34), (170, 6)):
        draw_rect(draw, sx, sy, 1, 1, "white")

    # moon
    stamp_icon(img, "moon", width - 52, 6, 2)

    # floor
    floor_y = height - 26
    draw.rectangle([0, floor_y, width, height], fill=_rgba("ink2"))
    dither_rect(img, 0, floor_y, width, 6, "ink2", "ink", pattern=2, cell=1)
    for gx in range(0, width, 8):
        draw.rectangle([gx, floor_y + 10, gx + 2, floor_y + 11], fill=_rgba("navy"))

    # arcade cabinet, a stack of tiles, a die, cards and a trophy on the floor
    stamp_icon(img, "arcade", 26, floor_y - 34, 2)
    stamp_icon(img, "tiles", 84, floor_y - 20, 1)
    stamp_icon(img, "dice", 132, floor_y - 18, 1)
    stamp_icon(img, "cards", 156, floor_y - 18, 1)
    stamp_icon(img, "trophy", 198, floor_y - 18, 1)
    stamp_icon(img, "controller", 234, floor_y - 18, 1)

    # floating sparkles
    for sx, sy in ((112, 34), (186, 26), (272, 40)):
        stamp_icon(img, "spark", sx, sy, 1)

    return img


def make_badge(text: str, fill: str = "sun", text_colour: str = "ink",
               pad: int = 3) -> Image.Image:
    """A small pixel badge: a coloured chip with text in it."""
    width = text_width(text, 1) + pad * 2
    height = font5x7.GLYPH_HEIGHT + pad * 2
    img = new_canvas(width, height, fill)
    draw = ImageDraw.Draw(img)
    draw_rect(draw, 0, 0, width, height, "ink")
    draw_text(img, pad, pad, text, colour=text_colour, scale=1)
    return img


def make_dither_tile(size: int = 16, colour_a: str = "navy",
                     colour_b: str = "ink2", pattern: int = 1) -> Image.Image:
    """A seamless dither tile, used as a CSS background image."""
    img = new_canvas(size, size)
    dither_rect(img, 0, 0, size, size, colour_a, colour_b, pattern=pattern, cell=1)
    return img


