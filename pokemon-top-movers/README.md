# Pokémon Top Movers (n8n + Postgres + Gotenberg)

Nightly Pokémon TCG price snapshots and a daily "Top Movers" image, built with
n8n. Pulls every card from the pokemontcg.io API, stores TCGplayer market prices
per variant in Postgres, then renders a 1080×1350 image of the biggest gainers
and drops with Gotenberg and (optionally) posts it to a Facebook Page.

```
pokemon-top-movers.n8n.json    the n8n workflow (import this)
docker-compose.pokemon-n8n.yml  all-in-docker stack (postgres + gotenberg + n8n)
n8n.service                     systemd unit for a native n8n install
```

## How it works

1. **Nightly snapshot (3 AM)** — pulls all cards (120 pages × 250, throttled),
   flattens TCGplayer market prices per variant (holo and reverse holo tracked
   separately), writes rows to Postgres. Re-runs are safe (`skipOnConflict`).
2. **Daily movers (8 AM)** — SQL compares the latest snapshot to the one
   `windowDays` earlier, keeps cards at/above `minPrice` (default `$5`), and
   returns the top gainers and fallers.
3. **Build HTML** — a Code node lays out the image: hero card, four more
   gainers, three biggest drops, using official card art and real numbers.
4. **Render** — Gotenberg screenshots the HTML to PNG.
5. **Save / Share** — writes `top-movers_<date>_<n>d.png` to `/data/output`,
   then posts to Facebook (optional).

## Two ways to run

### A. All-in-Docker

```bash
docker compose -f docker-compose.pokemon-n8n.yml up -d
```

Open n8n on port `5678`. Postgres and Gotenberg are reachable inside the compose
network as hosts `postgres` and `gotenberg`.

### B. n8n native + Postgres native + Gotenberg in Docker (this deployment)

Used on the `el-comms0001` host so n8n runs under systemd and is exposed over
Tailscale HTTPS.

- **n8n** — installed with Node 24 (`n8n` needs Node ≥ 24; the system Node 26
  breaks native deps). Managed by `n8n.service`, listens on `127.0.0.1:5678`.
- **Postgres** — native `postgresql 16` on `127.0.0.1:5432`, role `cards`,
  database `cardsdb`.
- **Gotenberg** — Docker container on `127.0.0.1:3000` (upstream no longer ships
  standalone binaries and the image bundles Chromium).
- **Name aliases** — `/etc/hosts` maps `gotenberg` and `postgres` to `127.0.0.1`
  so the workflow's `http://gotenberg:3000` and the `postgres` credential host
  work unchanged.
- **HTTPS** — `tailscale serve --bg --https=8443 http://127.0.0.1:5678`
  → `https://<tailnet-host>:8443/`.

#### Install n8n (native)

```bash
brew install node@24
/home/linuxbrew/.linuxbrew/opt/node@24/bin/npm install -g n8n --ignore-scripts
/home/linuxbrew/.linuxbrew/opt/node@24/bin/npm install -g sqlite3 --allow-scripts=sqlite3
sudo cp n8n.service /etc/systemd/system/n8n.service
sudo systemctl daemon-reload
sudo systemctl enable --now n8n
```

`n8n.service` sets `N8N_USER_FOLDER`, port, `WEBHOOK_URL`/`N8N_EDITOR_BASE_URL`
(tailnet `:8443`), `N8N_RESTRICT_FILE_ACCESS_TO=/data/output`, and a `NODE_PATH`
pointing at n8n's `node_modules`.

#### Postgres (native)

```bash
sudo apt-get install -y postgresql postgresql-contrib
sudo -u postgres psql -c "CREATE ROLE cards LOGIN PASSWORD 'change-me';"
sudo -u postgres createdb -O cards cardsdb
PGPASSWORD=change-me psql -h 127.0.0.1 -U cards -d cardsdb -f init_table.sql
```

The `card_prices` table is pre-created; the workflow's init node is idempotent.

#### Gotenberg (Docker)

```bash
docker run -d --name gotenberg --restart unless-stopped \
  -p 127.0.0.1:3000:3000 gotenberg/gotenberg:8
```

#### Hostname aliases

```bash
# /etc/hosts
127.0.0.1 gotenberg postgres
```

#### Tailscale HTTPS

```bash
sudo tailscale serve --bg --https=8443 http://127.0.0.1:5678
```

> Port `:443` could not be used: a k3s/CNI iptables rule DNATs all `tcp dport
> 443` to the cluster ingress pod, hijacking it before tailscaled sees it (it
> returns a Go `404 page not found`). `:8443` avoids the conflict without
> touching the cluster ingress.

## Setup after import

1. Import `pokemon-top-movers.n8n.json` into n8n.
2. Create the **Postgres** credential → host `postgres`, port `5432`, db
   `cardsdb`, user `cards`, password `change-me`; attach to the three Postgres
   nodes.
3. Add a **Facebook Graph API** credential to *Post to Facebook* (Page token +
   Page ID).
4. Paste a free pokemontcg.io API key into the **Config Snapshot** node.
5. Run **Run once: init DB**, then the snapshot branch once.
6. Wait at least `windowDays` between snapshots; the movers branch errors
   clearly until two comparable snapshots exist. Set `windowDays` to `7` in
   **Config Movers** for a weekly post.

## Gotenberg API note

Route: `POST /forms/chromium/screenshot/html`.

The HTML part must be sent with **filename `index.html`** (field name can be
`files`). The *Build HTML* node already names its binary `index.html`, so the
render node is correct. `width`, `height`, `format=png`, and `waitDelay` are
honored; the screenshot is full-page, and the workflow's `body { margin:0;
height:1350px; overflow:hidden }` keeps the output exactly 1080×1350.

## Caveats

- Prices from this API lag ~a day; the free API has no history, so your own
  nightly snapshots are the history.
- The Facebook node needs a valid Page token/Page ID before it will post.
- For a weekly winners-and-losers post, duplicate the movers branch with
  `windowDays = 7` and a Monday cron.
