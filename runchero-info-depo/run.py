#!/usr/bin/env python3
"""Start the Runchero Information Depo.

    ./run.py              serve on 0.0.0.0:8080
    ./run.py --seed       seed the database and archive first, then serve
    ./run.py --port 9000  serve somewhere else
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.httpd import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
