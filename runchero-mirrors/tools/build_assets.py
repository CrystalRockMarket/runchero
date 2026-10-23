#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from app import config
from app.pixel import draw, icons

IMG = config.STATIC_DIR / "img"


def build_icons():
    folder = IMG / "icons"
    folder.mkdir(parents=True, exist_ok=True)
    for name in icons.ICONS:
        draw.save(draw.icon_image(name, 1), folder / f"{name}.png")
    return len(icons.ICONS)


def main():
    config.ensure_dirs()
    n = build_icons()
    print(f"icons: {n}")


if __name__ == "__main__":
    raise SystemExit(main())
