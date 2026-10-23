#!/usr/bin/env python3
"""Consistent backups of the shop database.

The database is the whole store: cuts, prices, orders, households, the
market history. A copy taken while a request is writing can be corrupt, so
this uses SQLite's online backup API, which produces a consistent snapshot
without stopping the shop.

    python3 tools/backup.py            # take one backup
    python3 tools/backup.py --list     # show what is on disk
    python3 tools/backup.py --prune 7  # keep the last 7 backups

Backups land outside the project directory so a redeploy cannot eat them.
"""
from __future__ import annotations

import argparse
import os
import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import config  # noqa: E402

DEFAULT_KEEP = 14


def backup_dir() -> Path:
    return Path(os.environ.get("RBS_BACKUP_DIR", "/home/barn/backups")).resolve()


def take_backup(db_path: Path, out_dir: Path) -> Path:
    if not db_path.exists():
        raise SystemExit(f"no database at {db_path}")
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    target = out_dir / f"runchero-shop-{stamp}.db"
    src = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    dst = sqlite3.connect(target)
    try:
        with dst:
            src.backup(dst)
    finally:
        dst.close()
        src.close()
    # The WAL may still hold unmerged pages; the backup above includes them,
    # but a standalone .db is easier to restore than a db plus wal pair.
    for suffix in ("-wal", "-shm"):
        extra = Path(str(db_path) + suffix)
        if extra.exists():
            shutil.copy2(extra, Path(str(target) + suffix))
    return target


def list_backups(out_dir: Path) -> list[Path]:
    if not out_dir.exists():
        return []
    return sorted(out_dir.glob("runchero-shop-*.db"))


def prune(out_dir: Path, keep: int) -> list[Path]:
    removed = []
    files = list_backups(out_dir)
    for old in files[:-keep] if keep > 0 else files:
        for path in (old, Path(str(old) + "-wal"), Path(str(old) + "-shm")):
            if path.exists():
                path.unlink()
                removed.append(path)
    return removed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=str(config.DB_PATH))
    parser.add_argument("--out", default=None)
    parser.add_argument("--keep", type=int, default=DEFAULT_KEEP)
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--prune", type=int, metavar="N",
                        help="keep only the newest N backups")
    args = parser.parse_args()

    out_dir = Path(args.out).resolve() if args.out else backup_dir()

    if args.list:
        for path in list_backups(out_dir):
            size = path.stat().st_size / 1024
            print(f"{path.name}  {size:,.0f} KB")
        return 0

    if args.prune is not None:
        removed = prune(out_dir, args.prune)
        for path in removed:
            print(f"removed {path.name}")
        return 0

    target = take_backup(Path(args.db), out_dir)
    size = target.stat().st_size / 1024
    print(f"backup: {target} ({size:,.0f} KB)")
    prune(out_dir, args.keep)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
