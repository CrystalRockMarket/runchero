# Runchero Property Map

Interactive pixel-art map of the Runchero Farms property (Shelby County, KY,
parcel 025-00-012). Click a building or area to see photos, specs, construction
notes, maintenance log, and events. Admin console to add/edit places, layers,
categories, settings, and records.

## Run

```bash
./tools/map.sh seed      # create + populate database
./tools/map.sh start     # serve on 0.0.0.0:8082
./tools/map.sh status
./tools/map.sh stop
```

Admin login: `runchero` / (set `RMP_ADMIN_PASSWORD` at seed time, or reset in db).

## Data

- Database: `/home/barn/data/runchero-map.db`
- Parcel geometry: Shelby County PVA (ArcGIS), reference only.
- Satellite imagery: Esri World Imagery (used for planning; map itself is pixel art).

## Stack

Python 3 standard library + Jinja2 + Pillow. SQLite storage. No framework,
no build step, no internet required at runtime.
