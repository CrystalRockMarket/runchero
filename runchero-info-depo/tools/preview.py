#!/usr/bin/env python3
"""Print a pixel-art PNG as ASCII so it can be checked in a terminal.

    python3 tools/preview.py app/static/img/logo.png
    python3 tools/preview.py app/static/img/icons/cow.png --chars " .:-=+*#%@"
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image

RAMP = " .:-=+*#%@"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ASCII preview of a pixel image")
    parser.add_argument("path")
    parser.add_argument("--chars", default=RAMP)
    parser.add_argument("--max-width", type=int, default=200)
    args = parser.parse_args(argv)

    path = Path(args.path)
    if not path.exists():
        print(f"missing: {path}")
        return 1
    image = Image.open(path).convert("RGBA")
    ramp = args.chars
    try:
        for y in range(image.height):
            row = []
            for x in range(image.width):
                r, g, b, a = image.getpixel((x, y))
                if a < 32:
                    row.append(" ")
                    continue
                lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
                row.append(ramp[min(len(ramp) - 1, int(lum * len(ramp)))])
            print("".join(row))
    except BrokenPipeError:
        pass
    print(f"\n{path.name}: {image.width}x{image.height}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
