# Runchero Hub

A community directory page for the Runchero projects. Each card shows a real
screenshot of the app, a plain-language description of what it gives the
community, topic tags, and a direct link.

It also has an anonymous idea queue: anyone on the local network can propose a
new community app without making an account. A volunteer admin reviews the
queue in a small password-protected panel.

```
app/
  httpd.py             standard-library server, routes, security headers
  web.py               Jinja environment, signed cookies, CSRF
  views.py             directory, requests, admin, health
  projects.py          the allowlisted project list
  db.py                SQLite storage for app requests
  limits.py            in-memory rate limiter
  templates/           base, home, request, thanks, admin, login, error
  static/              pixel CSS, fonts, icons, screenshots, JS
tools/
  hub.sh               start, stop, restart, status, backup
  smoke.py             end-to-end checks on a throwaway database
tests/
  test_projects.py     allowlist and exclusion checks
  test_db.py           request storage checks
```

## Run

```bash
./tools/hub.sh start      # serve on 0.0.0.0:8092
./tools/hub.sh status
./tools/hub.sh backup     # snapshot the request database
./tools/hub.sh stop
```

Open <http://localhost:8092>, or `http://<LAN-IP>:8092` from another device.

The request database lives at `/home/barn/data/runchero-hub.db`; snapshots go
to `/home/barn/data/backups/`. The code is backed up by the `~/projects` git
cron, but the database is deliberately kept out of git.

## Configuration

| Variable | Default | What it does |
| --- | --- | --- |
| `RHUB_PORT` | `8092` | listen port |
| `RHUB_HOST` | `0.0.0.0` | listen address |
| `RHUB_DB_PATH` | `/home/barn/data/runchero-hub.db` | request database |
| `RHUB_ADMIN_USER` | `runchero` | admin username |
| `RHUB_ADMIN_PASSWORD` | `runchero` | admin password — change before sharing |
| `RHUB_SUBMISSIONS_PER_HOUR` | `5` | anonymous submissions per device |
| `RHUB_LINK_HOST` | empty | force project links to one host instead of the request host |

## Project allowlist

Only the projects in `app/projects.py` appear. `earth.love`, `games-earth`, and
the other excluded tokens are filtered out even if someone edits the list
carelessly, and the tests assert they never appear.

## Request rules

- No account or sign-up.
- CSRF token, hidden honeypot field, length caps, and a per-device rate limit.
- Name and contact are optional and admin-only.
- Requests are never published automatically.
- Admin can change status (`new`, `reviewing`, `planned`, `built`, `declined`),
  leave a private note, or delete an entry.

## Check it

```bash
python3 -m unittest discover -s tests -v
python3 tools/smoke.py
```

The smoke test starts its own server on port 8095 with a temporary database, so
it never touches real requests.
