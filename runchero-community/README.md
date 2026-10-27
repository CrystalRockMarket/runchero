# Runchero Community Directory

A community noticeboard for the Runchero local network. Neighbours can add
themselves, a business, a group, or a service without making an account. Every
listing shows the public ways to get in touch: phone, email, Facebook,
Instagram, website, address, and up to three custom contact rows or links.

Anonymous listings are published immediately and then **locked**. Only a
signed-in admin can edit, hide, or delete an entry.

```
app/
  httpd.py             standard-library server, routes, security headers
  web.py               Jinja environment, signed cookies, CSRF
  views.py             directory, listing form, admin, health
  channels.py          contact/link validation, normalisation, display
  db.py                SQLite storage for entries and channels
  config.py            settings, limits, kinds, categories
  limits.py            in-memory rate limiter
  templates/           base, home, entry, add, added, admin, login, error
  static/              pixel CSS, fonts, icons, JS
tools/
  community.sh         start, stop, restart, status, backup
  smoke.py             end-to-end checks on a throwaway database
tests/
  test_db.py           storage, search, filters, cascade checks
  test_channels.py     contact/link validation and display checks
```

## Run

```bash
./tools/community.sh start      # serve on 0.0.0.0:8093
./tools/community.sh status
./tools/community.sh backup     # snapshot the listing database
./tools/community.sh stop
```

Open <http://localhost:8093>, or `http://<LAN-IP>:8093` from another device.

The database lives at `/home/barn/data/runchero-community.db`; snapshots go to
`/home/barn/data/backups/`. The code is backed up by the `~/projects` git cron,
but the database is deliberately kept out of git.

## Configuration

| Variable | Default | What it does |
| --- | --- | --- |
| `RDIR_PORT` | `8093` | listen port |
| `RDIR_HOST` | `0.0.0.0` | listen address |
| `RDIR_DB_PATH` | `/home/barn/data/runchero-community.db` | listing database |
| `RDIR_ADMIN_USER` | `runchero` | admin username |
| `RDIR_ADMIN_PASSWORD` | `runchero` | admin password — change before sharing |
| `RDIR_SUBMISSIONS_PER_HOUR` | `5` | anonymous listings per device |
| `RDIR_SECRET_KEY` | empty | signing key; otherwise generated on first run |
| `RDIR_SECURE_COOKIES` | `0` | set to `1` when serving over HTTPS |

## Listing rules

- No account or sign-up for submitters.
- CSRF token, hidden honeypot field, length caps, and a per-device rate limit.
- At least one public contact detail is required.
- Listings are public immediately and locked after submission.
- Only an admin can edit, hide, or delete an entry.
- Submitter contact and admin notes are private and never shown publicly.
- Custom values beginning with `https://` are rendered as links; everything else
  is shown as plain contact text.

## Schema

`entries` stores the listing (name, kind, category, description, location,
published flag, private submitter contact, private admin note, timestamps).

`channels` stores one row per public contact method (kind `contact` or `link`,
label, value, sort order) and cascades on delete.

## Check it

```bash
python3 -m unittest discover -s tests -v
python3 tools/smoke.py
```

The smoke test starts its own server on port 8094 with a temporary database, so
it never touches real listings.
