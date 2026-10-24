# Runchero Mirrors

A local-network website depot. Neighbours paste a website address, the app copies
it with HTTrack, and the finished copy stays readable on the local network even
when the internet does not.

Built for non-technical users: a plain-language walkthrough, a live **Currently
working** page with pause/resume/stop, polite default crawl speeds, and a
pixel-art Runchero interface.

## Quick start

```bash
cd /home/barn/projects/runchero-mirrors

./tools/mirrors.sh seed     # initialize the database and folders
./tools/mirrors.sh start    # serve on 0.0.0.0:8090
./tools/mirrors.sh status
./tools/mirrors.sh restart
./tools/mirrors.sh stop
```

Open `http://localhost:8090`, or `http://<this-machine-LAN-IP>:8090` from another
device.

HTTrack is **vendored** in `vendor/httrack/`, so the app works without a
system-wide install or sudo. To use a system HTTrack instead, set
`RMM_HTTRACK_BIN` (and `RMM_HTTRACK_LIB` if needed).

## How it works

1. **Add a site** (`/add`) - Enter an `http://` or `https://` address, optionally
   add a friendly name and note, and choose a crawl pace. The form checks the URL
   and shows red error text when it is missing a protocol or is already saved.
2. **Watch it work** (`/working`) - Shows the active crawl plus anything queued.
   Pages, files, bytes, speed, elapsed time, and last activity update every few
   seconds. Pause freezes the HTTrack process; Resume continues it; Stop discards
   the partial copy from the browse list.
3. **Browse saved copies** (`/browse`) - Completed mirrors open at
   `/mirror/<slug>/`. Links, images, CSS, fonts, and other files are served from
   the saved copy, not the live internet.

The default pace is deliberately **Very slow** (12 KB/s, 2-5 pages per minute on
most sites). Slower is kinder to the remote server and produces a more complete
archive.

## Defaults and paths

| Item | Default |
| --- | --- |
| Listen address | `0.0.0.0:8090` |
| SQLite database | `/home/barn/data/runchero-mirrors.db` |
| Saved sites | `/home/barn/mirrors/<slug>/` |
| HTTrack cache and logs | `/home/barn/mirrors/.cache/` |
| App log | `/home/barn/logs/runchero-mirrors.log` |
| PID file | `/home/barn/run/runchero-mirrors.pid` |

Common environment overrides: `RMM_HOST`, `RMM_PORT`, `RMM_DATA_DIR`,
`RMM_DB_PATH`, `RMM_MIRRORS_ROOT`, `RMM_RUN_DIR`, `RMM_LOG_DIR`,
`RMM_DEFAULT_SPEED`, `RMM_MAX_QUEUE`, `RMM_MAX_CONCURRENT`,
`RMM_ALLOW_PRIVATE_HOSTS`, `RMM_SECRET_KEY`.

By default, private and local addresses (`localhost`, `*.local`, RFC1918 IPs)
are blocked to prevent the crawler from being pointed at the local network. On a
trusted network set `RMM_ALLOW_PRIVATE_HOSTS=1`.

## Speeds and limits

| Profile | Rate | Depth | Socket(s) | Total size cap |
| --- | --- | --- | --- | --- |
| Very slow (default) | 12 KB/s | 4 | 1 | 750 MB |
| Slow | 24 KB/s | 5 | 1 | 1 GB |
| Medium | 50 KB/s | 6 | 2 | 1.5 GB |

One crawl runs at a time; up to 20 jobs can wait in the queue. Each crawl has a
12-hour ceiling (10 hours for Medium). A retry starts from a clean copy.

## Notes and troubleshooting

- **LAN access fails:** this machine's firewall may not allow port 8090. Run
  `sudo ufw allow 8090/tcp` (an administrator is needed). Check with
  `./tools/mirrors.sh status`.
- **App will not start:** read `/home/barn/logs/runchero-mirrors.log`. A crash left
  mid-download is marked failed on the next start; use **Retry** on the dashboard.
- **A site saves no pages:** verify the address opens in a browser and does not
  block automated visitors. HTTrack's log is linked from the Currently working
  page.
- **HTTrack options:** use `--depth`, `--max-rate`, and `-I0`. Do not use
  `--max-depth`, `--rate`, or `-%i0`; those are invalid and make HTTrack print its
  help text.
- **Finished mirror shows the wrong front page:** the app detects the site entry
  inside HTTrack's `<host>/...` layout and never serves HTTrack's top-level portal
  page.
