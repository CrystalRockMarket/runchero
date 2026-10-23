# Runchero Co-op Shop

A shared storefront for independent co-op businesses in Shelby County:
Runchero Beef, Fermentation Station, and Runchero Freeze-Dried. Each business
has its own catalog, pricing, comparisons, and social links; pickup location
and hours, cart, checkout, customer accounts, and admin login are shared.

It runs on the Python standard library. There is no web framework, no build
step, and no package install beyond Jinja2 and Pillow. The whole thing is
Python, SQLite, and HTML.

```
app/
  httpd.py        the server: routing, sessions, CSRF, static files
  web.py          Jinja environment, signed sessions, request object
  db.py           schema, connection handling, migrations
  config.py       every path and setting, all overridable by env var
  views/          one module per area of the site
  services/       business logic, no HTTP knowledge
  seed/           the demo data: cuts, packages, shares, packing, market
  jobs/           scheduled work (market refresh, slot top up, integrity)
  templates/      Jinja templates
  static/         css, pixel art icons, logo
  pixel/          the icon generator
tools/
  shop.sh         start, stop, restart, seed, status
  smoke.py        end to end checks against a running server
  backup.py       consistent database backups
  build_assets.py exports every icon and favicon
```

## Running it

```bash
./tools/shop.sh seed       # create and populate the database
./tools/shop.sh start      # serve on 127.0.0.1:8081
./tools/shop.sh status
./tools/shop.sh stop
```

The server writes its PID to `/home/barn/run/runchero-shop.pid` and logs to
`/home/barn/logs/runchero-shop.log`. The database lives at
`/home/barn/data/runchero-shop.db`. This shop is a separate process from the
Runchero Information Depo and never reads or writes the depot's files.

Configuration is all environment variables, so the same code runs on the farm
box or a laptop. The ones that matter most:

| Variable | Default | What it does |
| --- | --- | --- |
| `RBS_PORT` | `8081` | port to listen on |
| `RBS_DB_PATH` | `/home/barn/data/runchero-shop.db` | database file |
| `RBS_ADMIN_USER` | `runchero` | admin login name |
| `RBS_ADMIN_PASSWORD` | generated and printed at seed time | admin password |
| `RBS_PAYMENT_PROVIDER` | `mock` | `mock` or `stripe` |
| `RBS_SITE_URL` | empty | public URL, used for canonical links and the sitemap |
| `RBS_AMS_API_KEY` | empty | optional USDA AMS API key for regional detail |
| `RBS_CONTACT_EMAIL` | `hello@runchero.example` | public contact address shown on the contact page |

## Checking it

```bash
RBS_ADMIN_PASSWORD=<password> python3 tools/smoke.py http://127.0.0.1:8081
```

The smoke test walks all three catalogs, cuts, packages, shares, campaigns,
product-only and mixed carts, packing, checkout, receipts, uploads, scoped
admins, customer accounts, and pricing preview/apply/revert. Admin checks are
skipped unless `RBS_ADMIN_PASSWORD` is set.

## How it is put together

**Routing.** `app/httpd.py` matches the request path against a list of
regular expressions built in `app/views/`. Views get a
connection, the request, and any named groups from the pattern.

**Sessions and CSRF.** The session cookie is a signed JSON blob. The CSRF
token is derived from the session, so every form carries a hidden `_csrf`
field and every POST checks it. A missing or stale token bounces the visitor
back to the form with an explanation instead of silently doing nothing.

**Accounts.** Customers sign up with an email and password, then keep their
contact details, fulfillment default, address, delivery notes, preferred
monthly processing day, and contact method on the `customers` table. Password
hashes use PBKDF2-SHA256 through the same helper as the admin console, and
the session cookie carries only the customer id. Orders link by
`customer_id`, with an email fallback so guest orders show up in the history
of an account created later. There is no mailer in this build: sign-up and
email changes mark the address verified immediately and say so on the page,
so a real verification flow can be added later without changing the UI.

**Co-op stores.** The beef catalog keeps its specialized cuts, packages,
shares, and campaigns. Fermentation Station and Runchero Freeze-Dried use the
generic `stores` and `products` tables, while their line items share checkout
and pickup. Product comparisons store the competitor, comparable package,
source URL, and check date; freeze-dried research notes are in
`docs/coop-pricing-research.md`. Re-seeding adds missing example products but
does not overwrite admin-edited prices or copy.

**Store administration.** Existing admins can create additional admins and
grant full access or checked access to one or more stores. Full-access admins
manage access grants; store-scoped admins can edit products and social links
only for assigned stores, and their order list is filtered to those stores.
Product forms support price, stock, description, comparison source, and image
upload. Uploaded raster images are verified and re-encoded as PNG under
`app/static/img/uploads/<store>/`; files are limited to 2 MB and stored outside
SQLite.

**Packing.** Packing options are grouped: `wrap`, `portioning`, `bagging`,
`gift`, `labeling`, and a line level `ground_pack` that only applies to
ground cuts. Order level choices apply to the whole order; the ground pack
choice is per line. Charges are priced per pound or per item depending on
the option, which is why the receipt shows a packing line that changes when
you switch pack sizes.

**Prices.** Every cut has a base price and a market series key. The admin
pricing console can preview a change against the current USDA series, apply
it, and revert it by audit id. Applying a change writes a row to `price_audits`
with the before and after numbers.

**Market prices.** `app/jobs/market_daily.py` pulls USDA AMS, ERS, and BLS
series over plain HTTP and stores them in `market_prices`. The shop
works without the optional AMS API key: the keyless feeds cover national
weekly and monthly prices, and the key only adds regional detail. The shop
never invents a local chain price. Where a local price is needed it is
entered by hand in the admin console and recorded in `local_observations`.
`/data-sources` explains every feed, links the raw public reports, and states
the pricing rule. It is linked from the footer, not the main nav.

**Cut artwork.** `app/pixel/meat.py` generates a 16x16 sprite for each cut
shape (steaks, roasts, ribs, ground, offal, deli) from the same palette as the
rest of the pixel art. `app/seed/icons.py` maps every cut slug to a sprite;
`tools/build_assets.py` exports the 1x/2x/3x PNGs.

**Shop sorting.** `/shop` accepts `sort=featured|price-asc|price-desc|deal|name`,
alongside the existing `primal`, `tag`, and `q` filters. `deal` ranks by the
percent under the live benchmark and is what the landing page links to.

**Fulfillment.** Orders reserve a pickup slot: the pounds in the order come
out of that window's capacity (1500 lb per pickup window). Slots are
generated for the next 28 days, for both pickup and delivery windows. The
daily job tops up the slots that are running low.

## Whole cow drops

A whole cow is sold as several household shares, not one sale, because of the
retail exemption for beef for home use. The rules the shop follows:

- No single sale may be more than half of a carcass.
- At least 75% of the carcass must go to households.
- The cow is butchered once, on one day, to one cut sheet that every
  household sees before their meat is wrapped.

A campaign splits a cow into `household_target` shares. A household holds a
place by name and email, and gets its own order and cut sheet later. The
campaign pages are at `/campaigns`.

## Money and honesty rules

- Savings badges always compare the cut price against the market benchmark
  for that cut, before packing options are added, and the page says so.
- The mock payment provider never charges a card and every receipt and
  badge says so.
- Kentucky beef for home use is tax exempt; the site says where the
  exemption comes from rather than hiding it.
- The minimum order is $99. Delivery is $15 and free over $159.

## Accessibility and SEO

Semantic headings, native form controls, visible focus rings, a skip link,
44 pixel touch targets, live regions for flash messages, errors next to the
field that caused them, and a reduced motion mode. Every page has a unique
title, a description, canonical link, and Open Graph tags, and
`/sitemap.xml` and `/robots.txt` are generated from live data.

## Backups

```bash
./tools/backup.sh            # one consistent snapshot
./tools/backup.sh --list     # what is on disk
./tools/backup.sh --prune 7  # keep the newest seven
```

The backup uses SQLite's online backup API, so it never catches the database
half written. Backups land in `/home/barn/backups`, outside the project
directory.
