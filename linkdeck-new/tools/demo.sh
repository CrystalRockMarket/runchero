#!/usr/bin/env bash
# Manage the public demo instance with a stable config.
# Usage: bash tools/demo.sh {start|stop|restart|status}
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

export LD_DB_PATH="${LD_DB_PATH:-/home/barn/data/linkdeck-demo.db}"
export LD_ADMIN_PASSWORD="${LD_ADMIN_PASSWORD:-demo-admin-2026}"
export LD_SECRET_KEY="${LD_SECRET_KEY:-2rKeMN8tE1UBVOa8h8rjZv8pnR4YqBTE314a5YttSTQE9dbF45BVvQbU}"
export LD_HOST="${LD_HOST:-0.0.0.0}"
export LD_PORT="${LD_PORT:-8092}"
export LD_FRONTEND_BASE_URL="${LD_FRONTEND_BASE_URL:-http://192.168.1.179:8092}"

exec bash "$ROOT/tools/start.sh" "${1:-start}"
