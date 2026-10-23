#!/usr/bin/env bash
# Take a consistent backup of the shop database.
#
#   ./tools/backup.sh            # one backup, keep the last 14
#   ./tools/backup.sh --list     # show what is on disk
#
# Backups go to $RBS_BACKUP_DIR (default /home/barn/backups), outside the
# project directory, so a redeploy cannot eat them.
set -euo pipefail
cd "$(dirname "$0")/.."
exec python3 tools/backup.py "$@"
