# Architecture

## The shape of it

```
browser  ──HTTP──▶  app/httpd.py  ──▶  app/views.py  ──▶  app/db.py (SQLite)
                          │                   │
                          │                   └──▶  app/md.py, app/web.py (Jinja)
                          └──▶  app/static/  (css, js, generated pixel art)
```

No framework, no ORM, no package installs. The only third-party libraries are
Jinja2 (templates) and Pillow (drawing the pixel art). Everything else is the
Python 3.12 standard library.

## Layers

### `app/config.py`
Single source of truth for paths and identity. Every path can be moved with an
environment variable, which is what keeps the database and the archive out of the
source tree:

| Setting | Default | Environment variable |
|---------|---------|---------------------|
| Data directory | `/home/barn/data` | `RID_DATA_DIR` |
| Archive directory | `/home/barn/archive` | `RID_ARCHIVE_DIR` |
| Database file | `<data>/runchero.db` | - |
| Book files | `<archive>/books/` | - |
| Upload inbox (unused) | `<archive>/inbox/` | - |
| Port | `8080` | - |
| Read-only | `true` | `RID_READ_ONLY` |
| Site name | `Runchero Information Depo` | `RID_SITE_NAME` |

### `app/palette.py`
The 29 colours used by the CSS, the icons and the generated images. The CSS custom
properties are produced from the same table, so the page and the artwork can never
drift apart. `shade()` and `mix()` build the derived tones.

### `app/pixel/`
* `font5x7.py` - a 5x7 bitmap font for every word that is drawn into an image.
* `icons.py` - 43 icons, each a 16x16 grid of characters. `icons.validate()` checks
  that every icon is 16 rows of 16 characters and only uses colours from the
  palette legend. It is part of the test pass.
* `draw.py` - PIL helpers: `dither_rect`, `vertical_gradient`, `draw_text`,
  `stamp_icon`, `make_cover`, `make_logo`, `make_hero`, `make_icon_sheet`.

Covers are generated locally from the book metadata, so the archive needs no image
server and every book gets a jacket that matches the site palette.

### `app/db.py`
SQLite with the FTS5 module. Schema version 2. Tables:

| Table | Holds |
|-------|-------|
| `meta` | schema version and build info |
| `categories` | shelves, with `kind` = `article` or `library`, and a parent for sub-shelves |
| `books.theme` | the library theme used by the archive filter; populated during seeding from the shelf |
| `vehicles` | 51 machines; 65 tractor brands are listed in `content.TRACTOR_BRANDS` as menu placeholders |
| `articles` | community notes, with `featured`, `views`, `read_minutes` |
| `article_vehicles` | many-to-many between notes and machines |
| `sources` | provenance records: kind, name, url, license, notes |
| `citations` | many-to-many between sources and pages (`page_kind`, `page_slug`) |
| `book_vehicles` | many-to-many between factory manuals and machines |
| `books` | archive records: author, year, pages, bytes, sha256, relative path |
| `submissions` | queued submissions (unused in the read-only build) |
| `glossary` | 54 terms |
| `calendar` | 12 months of farm work |
| `formula_topics` | the 22 topics the formula shelf is sorted into |
| `formulas` | 359 formulas: expression, symbols, units, guidance, worked example |
| `search_fts` | FTS5 index over article titles, summaries, bodies, book metadata and formulas |

`db.reindex()` rebuilds the FTS table. It is called at the end of every seed.

### `app/calculators.py`
A conservative single-equation parser. It accepts 87 of 359 formulas and returns a JavaScript expression plus labels, default values and a warning. Formulas that are tables, prose or multi-step are skipped, so the page never shows a broken calculator.

### `app/md.py`
A deliberately small markdown renderer: headings, paragraphs, lists, tables, bold,
italic, code, blockquotes, rules and `[[wiki-slug]]` links. Links are resolved
against the database; anything that is not a known slug is rendered as plain text.
The same renderer is used for the guidance on the formula shelf, so the links in a
formula work exactly like the links in a note.
URLs are filtered to `http`, `https` and `mailto`.

### `app/static/sw.js`
Offline shell cache version `runchero-depo-v3`; includes `/sources`, reader assets and formula calculator assets.

### `app/web.py`
The Jinja environment. Filters: `filesize`, `prettydate`, `monthname`, `wikilink`,
`slugify`. `make_resolver()` turns a slug into a URL, so a wiki link knows whether
it points at a note, a book, a shelf, a machine, a formula or a glossary term.
Formula links land on `/formulas?q=<slug>#formula-<slug>`, and glossary links land
on `/search?q=<term>` because the reference page was removed.

### `app/views.py`
One function per page. It also builds provenance labels, page source lists, reader pagination/search and calculator metadata for formulas. Each returns either a rendered template (the handler wraps
it in `200 text/html`) or a `(status, content_type, body)` tuple. `not_found()`
returns a real `404` with the error page, so crawlers and browsers both see the
right status code.

### `app/httpd.py`
`ThreadingHTTPServer` with a table of `(method, pattern, handler)` tuples. Static
files are served from `app/static/` with path traversal blocked and a safe content
type per extension. Every response carries `X-Content-Type-Options: nosniff` and a
referrer policy. `POST` always returns `405` with a read-only notice.

Query parameters are parsed with `parse_qs` and joined with commas, so a form can
send the same name twice (`kind=article&kind=book`).

The navigation is deliberately shallow, but each top-level section opens into
topic depots. `/vehicles` is a type list, `/vehicles?type=tractor` is the brand
list (all 65 names, with model counts), and `/vehicles?type=tractor&make=Ford`
is the model list. `/hub/<slug>` gathers notes, books, formulas and machines on
one subject, and `/conversions` is a set of native `<details>` drawers so the
page stays cheap to open on an old device. The removed reference page is not
routed; glossary links go to `/search?q=<term>` instead.

### `app/seed/`
* `content.py` - 40 categories (including `lib-manuals`), 51 machines, 65 tractor brand names, 54 glossary terms, the topic-depot map and the calendar.
* `articles.py` - the 35 original community notes with their markdown bodies.
* `notes_*.py` - eight modules of further notes, one per shelf family:
  vehicles, farming, animals, workshop, yard, kitchen, growing and the old reference-style notes.
  The reference-style notes were reclassified onto farming, workshop, vehicles and survival shelves. Together with `articles.py` they make 159 notes.
* `books.py` - the curated Project Gutenberg titles: id, slug, title, author, shelf,
  summary, cover motif, colours and publication year.
* `manuals.py` - 25 public-domain Ford manuals with OCR text, PDF links and vehicle mappings.
* `sources.py` - AI sources, background book sources, static-page citations and `seed_sources()`.
* `books_extra.py` - 1 459 further titles in the same shape, generated by
  `tools/fetch_gutenberg.py` from the official `pg_catalog.csv.gz` feed.
* `formulas/` - 359 formulas split across six modules, with `__init__.py` holding
  the 22 topics in order and the `COMMON` list that puts the most-used formulas first.
* `run.py` - the seeding script. It is idempotent: categories, notes, machines and
  formulas are upserted by slug, and book files already in the archive are left alone.
  It also seeds `sources`, `citations` and `book_vehicles`; `seed_manuals` adds the
  25 Ford manuals from `app/seed/manuals.py` and links them to vehicles.
  A plain reseed publishes the curated shelves plus whatever extra books are already
  on disk, so a bigger archive is never thrown away; `--all-books` publishes the
  whole catalogue.
  It downloads the plain text, strips the Project Gutenberg header and footer,
  guesses the publication year from the title page, estimates the page count from
  the word count, and stores the SHA-256 of the file.

### `tools/`
* `build_assets.py` - draws every image the site uses.
* `preview.py` - prints a PNG as ASCII, which is how the artwork was checked
  without a browser.
* `fetch_gutenberg.py` - builds the extended book catalogue from the Project
  Gutenberg feed and downloads the plain text files.
* `check_links.py` - walks every note and formula and reports any `[[wiki-slug]]`
  that does not resolve, or that points at the note it sits in.
* `smoke.py` - checks every route against a running server, including manuals, sources, vehicle pages and conversions.

## Pixel art rules

1. **Palette only.** Every colour comes from `app/palette.py`.
2. **Integer scaling.** Icons are 16x16 and are displayed at 16px or 32px. Covers are
   120x160 and are displayed at 120px or 240px. The logo is 214x42 and is displayed
   at 42px. A non-integer scale would make the pixels uneven.
3. **`image-rendering: pixelated`** on every image, with `crisp-edges` as the
   fallback for older browsers.
4. **No web fonts.** Headings use the bitmap font drawn into the logo and headings
   are set in a monospace stack; the body uses the system sans.
5. **No gradients that are not dithered.** Large areas use a two-colour dither
   pattern, which is how the look stays in the 16-colour era.

## Search

`search_fts` is a contentless-ish FTS5 table with `kind` (`article`, `book` or `formula`) and
`kind_id` columns, so one query can return notes, books and formulas together.
`db.search()` accepts a kind or a comma separated list of kinds.

Snippets come from FTS5 `snippet()`. The highlight markers are `char(1)` and
`char(2)`, not `[` and `]`, because a `[` marker landing inside a `[[wiki-slug]]`
would break the link. `md.snippet()` then renders the fragment through the same
renderer as a note body: wiki links resolve into real links, everything is
HTML-escaped, and the markers become `<b>` and `</b>` at the very end. Markers
that fall inside a wiki link are dropped so the link stays whole.

Formula results do not use the FTS snippet at all: the guidance (`how`) or the
worked example is rendered in full, because a formula is short enough that a
fragment would read worse than the whole thing.

## Read-only build

`RID_READ_ONLY` is on by default:

* `do_POST` drains the request body and answers `405` with
  `Allow: GET, HEAD`.
* The submission page renders as a notice instead of a form.
* No runtime code writes to the database.

That makes the whole depot safe to copy onto a memory stick and serve from any
machine on the local network.

## Offline behaviour

* `app/static/sw.js` caches the shell (CSS, JS, logo, icons) on install and serves
  it cache-first.
* `manifest.webmanifest` makes the depot installable on a phone home screen.
* The books live on disk, so `/read/<slug>` and `/download/<slug>` need no network.
* The only thing that ever touches the internet is `python3 -m app.seed.run`, and
  only when it needs to fetch a book that is not already in the archive.

## Things to know

* **Project Gutenberg blocks scrapers.** The plain text files are fetched from
  `https://www.gutenberg.org/cache/epub/<id>/pg<id>.txt` with a normal user agent;
  the HTML pages are deliberately not scraped.
* **`gutendex.com` is unusable** from this machine (403 and TLS handshake
  failures), so the catalogue was built from the official feed
  `pg_catalog.csv.gz`.
* **Year detection is a heuristic.** `seed.run.guess_year()` reads the first few
  thousand characters of the title page and picks the most common four digit year
  between 1500 and 1999. A wrong year is harmless, but it is worth a glance.
* **Page counts are estimated** at 250 words per page, not counted from the file.
* **The read counter is static.** A note's view count is set by the seed and never
  incremented at runtime, because writing to the database would break the
  read-only promise and lock the file when several requests land at once.
* **One database connection per request thread.** SQLite refuses to share a
  connection between threads, so the connection lives in thread local storage.
