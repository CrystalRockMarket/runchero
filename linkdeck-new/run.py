#!/usr/bin/env python3
"""Dev entry point: python run.py [--port 8092] [--reload]"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import uvicorn

from app.config import settings


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the LinkDeck server")
    parser.add_argument("--host", default=settings.HOST)
    parser.add_argument("--port", type=int, default=settings.PORT)
    parser.add_argument("--reload", action="store_true")
    parser.add_argument("--workers", type=int, default=1)
    args = parser.parse_args()

    uvicorn.run(
        "app.httpd:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        workers=None if args.reload else args.workers,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )


if __name__ == "__main__":
    main()