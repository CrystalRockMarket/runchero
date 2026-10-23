# Runchero Information Depo (demo)

An offline farm directory that runs entirely on this machine. Colourful pixel art,
plain-language fixes for tractors, farming and animals, plus an archive of **real
public domain books** you can read in the browser or take away as text files.

Everything works with no internet connection once it has been seeded.

```
./run.py --seed          # fill the database, fetch the books, draw the pixel art
./run.py                 # serve on http://localhost:8080
```

Open <http://localhost:8080> on a phone or a desktop. The layout collapses to a
single column on small screens.

---

## What is inside

| Part | What it holds |
|------|---------------|
| **Fixes & Notes** | 159 community articles: fault finding, servicing, crops, soil, growing, livestock, workshop, kitchen and safety. Cross linked with `[[wiki-links]]`, tables and step-by-step procedures. |
| **Formula Shelf** | 359 formulas in 22 topics, ordered from the most-used everyday sums to advanced maths, statistics, finance, surveying, electrical and weather. Each one says what the symbols mean, what the units are, how to use it, and gives a worked example. |
| **Machines** | 51 tractors, trucks, mowers and quads with engine, drive, power and the known weak points. The tractor index lists 65 brands; Ford is fully populated, the rest are ready for data. |
| **Library · Archive** | 1 489 real books from Project Gutenberg, 444 737 pages, 682 MB of plain text, across ten shelves and themed filters. Search, read in the browser, or download the `.txt`. |
| **Library · Community** | The notes, grouped by shelf. |
| **Library · Submit** | The submission form, deliberately switched off in this build. |
| **Topic Depots** | Wheat, cattle, soil, hay, solar, workshop, kitchen and more: each depot gathers every note, book, formula and machine on one subject. |
| **Conversions** | 16 collapsible reference drawers covering cooking, temperature, length, area, volume, weight, seed, fertiliser, spray, livestock, weather, energy, workshop, garden, preserving, fuel and quick sums. |
| **Glossary** | 54 terms linked from notes and search. |

## Routes

| URL | Page |
|-----|------|
| `/` | Dashboard |
| `/section/<slug>` | A shelf of notes, with topic depots |
| `/a/<slug>` | One note |
| `/vehicles`, `/vehicles?type=…&make=…`, `/vehicles/<slug>` | Type to brand to model index and detail |
| `/library` | Library landing page |
| `/library/archive`, `/library/archive/<slug>` | The book archive |
| `/library/community`, `/library/community/<slug>` | Community notes |
| `/library/submit` | Submission form (disabled) |
| `/hub/<slug>` | Topic depot gathering notes, books, formulas and machines |
| `/conversions` | Collapsible conversion reference |
| `/formulas`, `/formulas?topic=…&q=…` | The formula shelf |
| `/search?q=…&kind=article,book,formula` | Full text search |
| `/read/<slug>` | Read a book in the browser |
| `/download/<slug>` | Download the plain text file |
| `/api/search?q=…`, `/api/stats` | JSON endpoints |

## How it is built

No frameworks, no package installs, no build step.

* **Python 3.12** standard library only - `http.server.ThreadingHTTPServer` does the
  serving, `sqlite3` does the storage.
* **Jinja2** for the templates (the one third-party library, already installed).
* **Pillow** draws every icon, cover, logo and banner. There are no image downloads
  and no web fonts: the 5x7 bitmap font in `app/pixel/font5x7.py` is the typeface.
* **SQLite with FTS5** gives the search box its speed and snippets.

```
app/config.py      paths, site name, read-only switch
app/palette.py     the 29 colours the whole site is drawn from
app/pixel/         bitmap font, 43 icons, PIL drawing helpers
app/db.py          schema, queries, FTS5 index
app/md.py          safe markdown subset with wiki links
app/web.py         Jinja environment, filters and the wiki-link resolver
app/views.py       one function per page
app/httpd.py       routes, static files, the server itself
app/seed/          categories, machines, articles, notes, books, formulas, the seeding script
app/templates/     17 templates
app/static/        css, js, service worker, generated images
tools/             asset builder, Gutenberg fetcher, smoke test, ASCII preview
```

Full detail in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Data locations

| What | Where |
|------|-------|
| Database | `/home/barn/data/runchero.db` |
| Book files | `/home/barn/archive/books/*.txt` |
| Upload inbox (unused) | `/home/barn/archive/inbox/` |
| Images | `app/static/img/` (generated) |

## Provenance and manuals

- Every page shows a source panel. Kinds: `ai-generated`, `ai-organized`,
  `book`, `manual`, `forum`, `website`, `archive`, `dataset`, `other`.
- `/sources` lists every source and its citation count.
- Search supports `?source=...`.
- Twenty-five public-domain Ford manuals live under the `lib-manuals` category
  and link to `book_vehicles`.
- `/read/<slug>` paginates a book and supports in-book search.
- Formula calculators appear where a formula is a single clean equation; they
  are convenience only and tell the user to double-check.
## Commands

```bash
./run.py --seed                     # seed everything, then serve
./run.py --port 9000                # serve on another port
python3 -m app.seed.run             # seed only (stop the server first)
python3 -m app.seed.run --no-fetch  # seed without touching the network
python3 -m app.seed.run --all-books # publish the whole 1 196 book catalogue
python3 tools/build_assets.py       # redraw the icons, covers, logo and banner
python3 tools/fetch_gutenberg.py    # top up the Project Gutenberg catalogue
python3 tools/check_links.py        # every [[wiki-slug]] in the depot resolves
python3 tools/smoke.py              # check every route against a running server
python3 tools/preview.py app/static/img/icons/cow.png   # check the art in a terminal
./tools/depot.sh start|stop|restart # run it in the background
```

The library is published in two sizes. A plain reseed keeps the curated shelves and
whatever extra books are already on disk, so a bigger archive is never thrown away.
`--all-books` publishes the whole catalogue. The plain text files are downloaded
once, fingerprinted with SHA-256, and kept in `/home/barn/archive/books/`.

## Read-only build

`RID_READ_ONLY` defaults to `1`. The server answers every POST with `405` and the
submission page explains that submissions are switched off. Nothing is written to
the database at runtime - not even a read counter - so the depot can be put on a
USB stick and served from anywhere.

## Books

All 1 196 titles are public domain and come from Project Gutenberg
(<https://www.gutenberg.org>). The plain text files are downloaded once, fingerprinted
with SHA-256, and kept in `/home/barn/archive/books/`. The catalogue lives in
`app/seed/books.py` and `app/seed/books_extra.py`; the covers are generated locally
by `tools/build_assets.py`, so the archive never depends on an image server.

## Wiki links

Every note, and every formula, is written in Markdown with `[[wiki-slug]]` links.
The resolver in `app/web.py` turns a slug into a link to the note, the book, the
shelf, the machine, the formula or the glossary term that carries it.
`tools/check_links.py` walks the whole depot and fails if any link points at
nothing, and `tools/smoke.py` checks the rendered pages on a running server.
