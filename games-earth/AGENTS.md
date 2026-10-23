# AGENTS.md — build conventions for this repo

## Commands
- `python3 tools/build_assets.py` — regenerate all pixel art + CSS vars (run after touching `pixel/*`)
- `python3 tools/preview.py <png>` — ASCII preview of a generated image
- `python3 tools/serve.py` — local preview server (EL engine + static web root) on :8077
- `python3 tools/seed_content.py` — write the starter content tree under `domain/`
- `python3 tools/smoke.py` — crawl the preview server and verify every route
- `python3 tools/lint_oml.py` — check every template for balanced OML and resolved includes

## Layout
- `pixel/` — palette, 5x7 font, 16x16 icons, PIL helpers (no other module imports from here except `tools/`)
- `tools/` — build/preview/serve/seed/smoke scripts (run from project root)
- `cgi/` — project CGI programs installed to `/usr/lib/cgi-bin` at deploy time
- `domain/` — the standalone EL domain tree; this is the deliverable
  - `domain/_WEB/` — document root (static files only)
  - `domain/_ROOT/_TEMPLATES/` — OML templates (the redesign)
  - `domain/LANGS/ENG/` — flat-file content tree
- `docs/` — architecture, content format, deploy

## Rules
- Palette source of truth is `pixel/palette.py`; never hard-code hex in CSS/art
- Never write into `/LOVE` (read-only for `barn`); games.earth data is reference-only
- Templates are OML: tokens use `#NAME#`, comments `<!--- ... --->`
- All art stays hard-edged: no border-radius, no blur shadows, 4px grid
