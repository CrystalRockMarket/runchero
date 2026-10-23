#!/usr/bin/env python3
"""Preview a generated PNG as ASCII art in the terminal.

    python3 tools/preview.py domain/_WEB/_PIXEL/icons/dice.png
    python3 tools/preview.py domain/_WEB/_PIXEL/hero.png --width 100
    python3 tools/preview.py domain/_WEB/_PIXEL/logo.png --bg light

Pixels are mapped to the nearest character in a ramp, so you can eyeball the
art without leaving the terminal.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image

RAMP = ".:-=+*#%@"
LIGHT_BG = (253, 246, 227)
DARK_BG = (27, 27, 35)


def to_ascii(img: Image.Image, width: int, bg: tuple[int, int, int] | None) -> str:
    if img.width > width:
        ratio = width / img.width
        height = max(1, int(img.height * ratio / 2))
        img = img.resize((width, height), Image.NEAREST)

    if bg is not None:
        flat = Image.new("RGB", img.size, bg)
        flat.paste(img, mask=img.split()[3] if img.mode == "RGBA" else None)
        img = flat

    out = []
    pixels = img.convert("RGB").load()
    for y in range(img.height):
        row = []
        for x in range(img.width):
            r, g, b = pixels[x, y]
            lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            index = int(lum * (len(RAMP) - 1))
            row.append(RAMP[index])
        out.append("".join(row))
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--width", type=int, default=64)
    parser.add_argument("--bg", choices=["dark", "light", "none"], default="dark",
                        help="background to composite the art onto")
    args = parser.parse_args()

    if not args.path.exists():
        print(f"no such file: {args.path}", file=sys.stderr)
        return 1

    img = Image.open(args.path)
    bg = {"dark": DARK_BG, "light": LIGHT_BG, "none": None}[args.bg]
    print(f"# {args.path} ({img.width}x{img.height})")
    print(to_ascii(img, args.width, bg))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
