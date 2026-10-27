# Runchero Links

A small community tool that turns Amazon product links and searches into tagged
affiliate links. Paste a product link, paste a whole list, or search Amazon and
open the tagged search in a new tab. It also explains, in plain language, what a
qualifying purchase could earn.

It is stateless: no accounts, no cookies, no database, no history. Links are
converted in memory and forgotten.

```
app/
  httpd.py             standard-library server, routes, security headers
  web.py               Jinja environment and request object
  views.py             pages and JSON API
  services/amazon.py   URL validation and conversion rules
  services/resolve.py  a.co / amzn.to resolver and rate limit
  templates/           home, results, how, error
  static/              pixel CSS, fonts, icons, copy/estimator JS
tools/
  links.sh             start, stop, restart, status
  smoke.py             end-to-end checks
tests/
  test_amazon.py       conversion unit tests
```

## Run

```bash
./tools/links.sh start      # serve on 0.0.0.0:8091
./tools/links.sh status
./tools/links.sh stop
```

Open <http://localhost:8091>, or `http://<this-machine-LAN-IP>:8091` from
another device on the same network.

The server writes its PID to `/home/barn/run/runchero-links.pid` and logs to
`/home/barn/logs/runchero-links.log`.

## Configuration

| Variable | Default | What it does |
| --- | --- | --- |
| `RLK_AFFILIATE_TAG` | `runchero-20` | Amazon Associate tag added to links |
| `RLK_HOST` | `0.0.0.0` | listen address |
| `RLK_PORT` | `8091` | listen port |
| `RLK_COMMISSION_RATE` | `3.0` | starting estimate in the earnings panel |
| `RLK_RESOLVE_TIMEOUT` | `5` | seconds allowed for a short-link lookup |
| `RLK_RESOLVE_PER_MINUTE` | `30` | short-link lookups allowed per device per minute |

The demo tag is `runchero-20`. Set the real tag when the Associate account is
ready; no code change is needed.

## How a link is converted

1. Accept only `http`/`https` links on `amazon.com` (including `www`, `m`,
   `smile`) or a short host (`a.co`, `amzn.to`).
2. Reject usernames, passwords, unexpected ports, and lookalike hosts such as
   `amazon.com.evil.com`.
3. Find the 10-character ASIN in `/dp/<ASIN>`, `/gp/product/<ASIN>`,
   `/gp/aw/d/<ASIN>`, or `/<name>/dp/<ASIN>` and rebuild it as `/dp/<ASIN>`.
4. For searches, keep `k`, `i`, `node`, `rh`, and `field-keywords`; drop the rest.
5. Remove tracking parameters: `tag`, `linkCode`, `linkId`, `ref`, `ref_`, `th`,
   `psc`, `social_share`, `sprefix`, `crid`, `qid`, `pf_rd_*`, `pd_rd_*`, and
   related fields.
6. Add `tag=runchero-20`.
7. Return the link. Nothing is shortened, masked, or redirected.

Short links are followed by the server with a five-second timeout and a cap of
five redirects. Every hop must remain inside Amazon-owned hosts. If the lookup
fails, the page asks for the full product link instead.

## What could it earn?

The estimator is deliberately simple and adjustable:

- order total default $60
- orders per month default 10
- commission rate default 3% (range 1–10%)

At those defaults: $1.80 per qualifying order, $18.00 per month, $216.00 per
year. Amazon's real rates depend on the category, rates change, returns can
reverse a commission, and not every click or purchase qualifies. The page says
all of that next to the numbers.

## Rules and safety

- The affiliate relationship is disclosed in the footer and beside the tool.
- Outbound links carry `rel="nofollow sponsored noopener noreferrer"`.
- There is no open-redirect endpoint and no link cloaking.
- Security headers: CSP, `X-Content-Type-Options`, `Referrer-Policy: no-referrer`,
  `X-Frame-Options: DENY`, `Permissions-Policy`.
- Request logs record the page and status, not pasted links or searches.
- Short-link lookups are rate limited per device.

## Check it

```bash
python3 -m unittest discover -s tests -v
./tools/links.sh start
python3 tools/smoke.py
```

See `docs/how-it-works.md` for the longer explanation shown on the `/how` page.
