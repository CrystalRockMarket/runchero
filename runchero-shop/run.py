#!/usr/bin/env python3
"""Start the Runchero Beef shop.

    ./run.py              serve on 0.0.0.0:8081
    ./run.py --seed       seed the database first, then serve
    ./run.py job market   run the daily market job instead of serving
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.httpd import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
