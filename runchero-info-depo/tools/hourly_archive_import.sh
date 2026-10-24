#!/usr/bin/env bash
# Hourly scan for books dropped into /home/barn/archive/staging/
# - Only processes .txt/.pdf/.md files (README.md and hidden files ignored)
# - Copies them into /home/barn/archive/books/ (or pdfs/) with no AI summaries
# - Updates app/seed/books_from_staged.py with source metadata only
# - Safe to run alongside other work; uses a lock to avoid races

set -euo pipefail

LOCK="/tmp/runchero-hourly-archive-import.lock"
PROJECT="/home/barn/projects/runchero-info-depo"
STAGING="/home/barn/archive/staging"
LOG="/home/barn/archive/import_queue/hourly.log"

mkdir -p /home/barn/archive/import_queue "$STAGING" "$STAGING/processed"

exec 200>"$LOCK"
flock -n 200 || exit 0

{
  echo "[$(date -Iseconds)] starting hourly archive import"
  cd "$PROJECT"
  # Scan for new files and stage them
  python3 tools/stage_books.py --scan
  # Integrate staged text files into the site's book catalogue
  python3 tools/stage_books.py --integrate
  echo "[$(date -Iseconds)] finished"
} >> "$LOG" 2>&1
