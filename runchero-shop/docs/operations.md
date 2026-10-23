# Operations runbook

Everything the shop needs day to day, in the order it usually comes up.

## Service control

```bash
./tools/shop.sh status     # is it running, what is the pid
./tools/shop.sh start      # start it, waits for the pid file
./tools/shop.sh stop       # stop it
./tools/shop.sh restart    # stop then start
./tools/shop.sh seed       # create or refresh the demo data
```

`start` waits for the server to write `/home/barn/run/runchero-shop.pid`
after it binds the port, so a `start` that returns is a `start` that
worked. Logs go to `/home/barn/logs/runchero-shop.log`.

Never kill it with `pkill -f` using a pattern that also matches the command
line running the kill. It takes the calling shell with it. Use
`./tools/shop.sh stop`, or kill the pid in the pid file.

## Data

| What | Where |
| --- | --- |
| Database | `/home/barn/data/runchero-shop.db` |
| Backups | `/home/barn/backups` |
| Logs | `/home/barn/logs/runchero-shop.log` |
| Pid | `/home/barn/run/runchero-shop.pid` |

The database is the entire store. Cuts, prices, orders, households,
subscriptions, market history, audit rows: it is all in there. Back it up.

```bash
./tools/backup.sh
```

Restoring is the reverse: stop the shop, copy the backup over
`runchero-shop.db`, remove any stale `-wal` and `-shm` files, start the shop,
and check `/admin/integrity`.

## Scheduled work

`app/jobs/market_daily.py` does three things:

1. pulls USDA AMS, ERS, and BLS series and writes `market_prices`,
2. tops up pickup slots that are running low,
3. writes a claim integrity report, so you can see when a price no longer
   matches the market.

It is meant to run from cron once a day:

```cron
15 6 * * * cd /home/barn/projects/runchero-shop && python3 app/jobs/market_daily.py >> /home/barn/logs/market-job.log 2>&1
```

If the job cannot reach the network it logs the failure and leaves the last
good market rows in place. The shop keeps selling at the prices it has.

## The admin console

`/admin` covers:

- **dashboard** — orders, revenue, low stock, market freshness
- **pricing** — preview a change against the current market series, apply
  it, revert it by audit id
- **integrity** — cuts whose price no longer matches the market
- **market** — the observations, manual entry of local prices, a manual
  refresh
- **orders** — every order with its packing choices and payment state

The admin password is set at seed time and printed once. To change it, set
`RBS_ADMIN_PASSWORD` and restart, or set it directly in the database:

```sql
UPDATE admin_user SET password_hash = '<hash>' WHERE username = 'runchero';
```

## When something looks wrong

| Symptom | Look at |
| --- | --- |
| Page is a plain 500 | `tail -50 /home/barn/logs/runchero-shop.log` |
| "database is locked" | another writer is holding the lock; check for a stuck job |
| Cart says the session expired | the secret key changed, so old cookies no longer verify |
| Market prices went stale | the daily job failed; `/admin/market` shows the error |
| Missing icons | `python3 tools/build_assets.py` |

## Checks after any change

```bash
RBS_ADMIN_PASSWORD=<password> python3 tools/smoke.py http://127.0.0.1:8081
```

It should report zero failures. It covers the catalog, cart, packing,
checkout, receipt, subscriptions, campaigns, and the admin console.
