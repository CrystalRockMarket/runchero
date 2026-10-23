# Runchero Mirrors

Local-network app for submitting websites to download with HTTrack and browsing them as finished mirrors. Designed for non-technical users with a step-by-step guided walkthrough, pixel art UI in the Runchero style, and a live status view of queued/running/completed mirrors.

## Quick start

```bash
./tools/mirrors.sh seed   # initialize database and directories
./tools/mirrors.sh start  # serve on 0.0.0.0:8090
./tools/mirrors.sh status
./tools/mirrors.sh stop
```

Browse: http://localhost:8090 (or your local IP on port 8090). HTTrack must be available (bundled or installed).

## How it works

1. **Add a site** - Guided walkthrough explains each step in plain language. Enter URL, optional name/notes, and click Start.
2. **Watch progress** - Dashboard shows queued, currently downloading, and completed mirrors with running time, saved pages/files, and status.
3. **Browse finished mirrors** - Completed sites are viewable/browsable through the app. Files are stored under `/home/barn/mirrors` by default (configurable).
