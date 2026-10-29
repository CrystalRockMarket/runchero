# LinkDeck

A production-shaped, VPS-ready link-sharing site. Visitors get a fairly-shuffled
deck of affiliate/referral offers; signed-in users submit links, track clicks,
and see estimated earnings; admins moderate submissions from a dashboard.

Built with FastAPI, SQLAlchemy 2.0 (async), SQLite, Jinja2 and vanilla JS.

## Features

- **Public deck** – weighted fair shuffle, category filters, top/new modes.
- **Anonymous submissions** – no account needed; links queue for review.
- **Accounts** – Google / Facebook OAuth and passwordless email magic links.
- **User dashboard** – per-user offers, click + unique-visitor stats, estimated
  earnings, promo codes, recent clicks.
- **Click tracking** – server-side events with hashed IPs, referrer and UA.
- **Voting** – "worked / didn't work" with per-voter dedup.
- **Admin panel** – global stats, approve/reject offers, user + click listings.
- **Security** – bcrypt password hashing, opaque server-side session tokens,
  HttpOnly/SameSite cookies, CSP + hardening headers, rate limiting, no secrets
  in URLs (magic tokens are stored hashed).

## Quick start (dev)

```bash
cd /home/barn/projects/linkdeck-new
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

export LD_ADMIN_PASSWORD='choose-a-strong-password'
python run.py --port 8096 --reload
```

Open http://localhost:8096. Admin login is at `/admin`.

Run the smoke test (uses a throwaway DB):

```bash
python tools/smoke_test.py
```

### Manage a background server

```bash
tools/start.sh start     # uses venv, writes pidfile + log
tools/start.sh status
tools/start.sh restart
tools/start.sh stop
```

## Configuration

All settings are environment variables (optionally via `.env`). See
`.env.example`. Highlights:

| Variable | Default | Purpose |
| --- | --- | --- |
| `LD_SECRET_KEY` | dev-secret | JWT/session signing key – **set this in production** |
| `LD_ADMIN_PASSWORD` | *(empty)* | Creates the default admin on first boot |
| `LD_DB_PATH` | `/home/barn/data/linkdeck.db` | SQLite database path |
| `LD_HOST` / `LD_PORT` | `0.0.0.0` / `8096` | Bind address |
| `LD_FRONTEND_BASE_URL` | `http://localhost:8096` | Used in magic links / redirects |
| `LD_GOOGLE_CLIENT_ID` / `LD_GOOGLE_CLIENT_SECRET` | *(empty)* | Enables Google login |
| `LD_FACEBOOK_APP_ID` / `LD_FACEBOOK_APP_SECRET` | *(empty)* | Enables Facebook login |
| `LD_SMTP_HOST` / `LD_SMTP_USER` / `LD_SMTP_PASSWORD` | *(empty)* | Enables real magic-link email |
| `LD_ALLOW_ANONYMOUS_OFFER` | `1` | Allow submissions without login |

When SMTP is not configured, `/auth/magic/send` returns a `dev_link` in the JSON
response (and the login page renders it) so the flow is testable locally.

## API overview

Public:
- `GET /api/offers?category=&mode=shuffle|top|new|one`
- `POST /api/offers` – submit (optionally authenticated)
- `POST /api/click/{offer_id}`
- `POST /api/vote/{offer_id}?is_up=&voter_key=`
- `GET /api/stats/offer/{offer_id}`, `/api/stats/global`, `/api/stats/leaderboard`

Auth (`/auth`):
- `GET /google`, `/google/callback`, `/facebook`, `/facebook/callback`
- `POST /magic/send`, `GET /magic/verify?token=`
- `POST /admin/login`, `GET /me`, `POST|GET /logout`

Admin (`/api/admin`, requires an admin session):
- `POST /offers/{id}/status` `{ "status": "active|rejected|pending|flagged" }`
- `DELETE /offers/{id}`, `GET /stats`, `GET /clicks`

## Production notes

- Run behind a TLS-terminating reverse proxy (Caddy/nginx) and set
  `LD_FRONTEND_BASE_URL=https://your-domain`; session cookies become `Secure`.
- Set a strong `LD_SECRET_KEY` and `LD_ADMIN_PASSWORD`; leave `DEBUG` off
  (disables `/docs`).
- SQLite is fine for small deployments; point `LD_DB_PATH` at persistent storage
  and back it up. Swap the engine URL in `app/db.py` for Postgres if needed.
- Multiple uvicorn workers are supported (`run.py --workers N`); all state lives
  in the database, not process memory.
- Error tracking: run under systemd with `Restart=always`.
