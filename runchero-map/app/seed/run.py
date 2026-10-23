"""Seed the Runchero property map: categories, places, shapes, layers, admin."""
from __future__ import annotations

import json
from pathlib import Path

from .. import db, config
from ..services import auth

DATA_DIR = Path(__file__).resolve().parent / "data"


def _load_json(name):
    p = DATA_DIR / name
    if p.exists():
        return json.loads(p.read_text())
    return None


def seed(conn):
    report = {}
    # categories
    categories = [
        ("barn", "Barn", "wood", "home", 1),
        ("shop", "Shop / Workshop", "orange", "wrench", 2),
        ("house", "House / Residence", "plum", "home", 3),
        ("storage", "Storage", "grey", "box", 4),
        ("field", "Field / Pasture", "grass", "grass", 5),
        ("pond", "Pond / Water", "sky", "droplet", 6),
        ("road", "Road / Drive", "grey2", "tractor", 7),
        ("fence", "Fence / Gate", "brown", "fence", 8),
        ("utility", "Utility", "teal", "gear", 9),
        ("other", "Other", "silver", "tag", 10),
    ]
    for slug, name, colour, icon, so in categories:
        conn.execute(
            "INSERT INTO categories(slug,name,colour,icon,sort_order) VALUES(?,?,?,?,?) "
            "ON CONFLICT(slug) DO UPDATE SET name=excluded.name, colour=excluded.colour, icon=excluded.icon, sort_order=excluded.sort_order",
            (slug, name, colour, icon, so))
    report["categories"] = len(categories)

    # map layers
    layers = [
        ("boundary", "Property Boundary", "Parcel outline from county PVA", 1),
        ("fences", "Fences", "All fence lines", 1),
        ("water", "Water", "Creek, pond, drainage", 1),
        ("power", "Power / Utilities", "Overhead and buried", 1),
        ("fields", "Fields / Pastures", "Pasture and crop divisions", 1),
        ("roads", "Roads / Drives", "Farm roads and access", 1),
    ]
    for slug, name, desc, vis in layers:
        conn.execute(
            "INSERT INTO map_layers(slug,name,description,visible,sort_order) VALUES(?,?,?,?,?) "
            "ON CONFLICT(slug) DO UPDATE SET name=excluded.name, description=excluded.description, visible=excluded.visible",
            (slug, name, desc, vis, 0))
    report["layers"] = len(layers)

    # places (initial seed: a handful of representative structures)
    places = [
        ("main-barn", "Main Barn", "barn", "building", "Post-frame barn, hay storage and equipment bay", 1998,
         "Post-frame, metal roof, concrete floor", "40 x 80 ft", 0.0,
         "active", "Hay storage, equipment bay, loft storage."),
        ("shop", "Farm Shop", "shop", "building", "Workshop and repair bay", 2005,
         "Pole barn, concrete slab", "30 x 50 ft", 0.0, "active", "Tools, welder, tractor service."),
        ("farmhouse", "Farmhouse", "house", "building", "Primary residence", 1972,
         "Wood frame, brick veneer", "28 x 44 ft", 0.0, "active", "Family residence."),
        ("equipment-shed", "Equipment Shed", "storage", "building", "Covered equipment storage", 2010,
         "Pole barn, gravel floor", "60 x 40 ft", 0.0, "active", "Tractors, implements, trucks."),
        ("hay-barn", "Hay Barn", "barn", "building", "Open hay storage", 2000,
         "Pole barn, open sides", "50 x 60 ft", 0.0, "active", "Round bale storage."),
        ("pond", "Farm Pond", "pond", "water", "Stock pond", "", "", "", 1.2,
         "active", "Water for livestock; stocked with bass."),
        ("north-pasture", "North Pasture", "field", "field", "Cool-season grass pasture", "", "", "", 45.0,
         "active", "Rotational grazing."),
        ("south-field", "South Field", "field", "field", "Hay and crop field", "", "", "", 60.0,
         "active", "Hay production."),
    ]
    place_ids = {}
    for (slug, name, cat, kind, short, year, construction, dims, acres, status, notes) in places:
        cat_id = conn.execute("SELECT id FROM categories WHERE slug=?", (cat,)).fetchone()[0]
        conn.execute(
            """INSERT INTO places(slug,name,category_id,kind,short_desc,year_built,construction,dimensions,area_acres,status,notes)
               VALUES(?,?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(slug) DO UPDATE SET name=excluded.name, category_id=excluded.category_id,
               kind=excluded.kind, short_desc=excluded.short_desc, year_built=excluded.year_built,
               construction=excluded.construction, dimensions=excluded.dimensions, area_acres=excluded.area_acres,
               status=excluded.status, notes=excluded.notes""",
            (slug, name, cat_id, kind, short, str(year), construction, dims, acres, status, notes))
        pid = conn.execute("SELECT id FROM places WHERE slug=?", (slug,)).fetchone()[0]
        place_ids[slug] = pid
    report["places"] = len(places)

    # place specs
    specs = {
        "main-barn": [("Roof", "Metal"), ("Floor", "Concrete"), ("Power", "200A panel"), ("Water", "Well nearby")],
        "shop": [("Power", "100A"), ("Heat", "Wood stove"), ("Lift", "None")],
        "farmhouse": [("Bedrooms", "3"), ("Baths", "2"), ("Heat", "Propane")],
    }
    for slug, items in specs.items():
        pid = place_ids[slug]
        for k, v in items:
            conn.execute("INSERT INTO place_specs(place_id,key,value) VALUES(?,?,?)", (pid, k, v))

    # records (sample)
    records = [
        ("main-barn", "construction", "Barn erected", "Post-frame barn built by local crew; concrete slab poured.", "1998-06-15", "owner"),
        ("main-barn", "maintenance", "Roof screws replaced", "Replaced 40 loose roof screws on south slope.", "2024-03-10", "owner"),
        ("shop", "maintenance", "Welder serviced", "MIG welder tuned and tips replaced.", "2024-08-02", "owner"),
        ("pond", "event", "Stocked bass", "Added 200 fingerling largemouth.", "2023-04-20", "owner"),
    ]
    for slug, kind, title, body, date, actor in records:
        pid = place_ids[slug]
        conn.execute("INSERT INTO place_records(place_id,kind,title,body,occurred_on,actor) VALUES(?,?,?,?,?,?)",
                     (pid, kind, title, body, date, actor))

    # boundary layer feature from parcel geojson
    parcel = _load_json("parcel.geojson")
    if parcel and parcel.get("features"):
        ring = parcel["features"][0]["geometry"]["coordinates"][0]
        # convert lon/lat ring to pixel coords on a 960x640 canvas covering bbox
        import math
        lons = [p[0] for p in ring]; lats = [p[1] for p in ring]
        minx, maxx = min(lons), max(lons); miny, maxy = min(lats), max(lats)
        # pad
        pad_x = (maxx-minx)*0.05; pad_y=(maxy-miny)*0.05
        minx-=pad_x; maxx+=pad_x; miny-=pad_y; maxy+=pad_y
        W, H = 960, 640
        def to_px(lon, lat):
            x = (lon-minx)/(maxx-minx)*W
            y = (maxy-lat)/(maxy-miny)*H
            return [round(x,1), round(y,1)]
        pxring = [to_px(lon,lat) for lon,lat in ring]
        layer_id = conn.execute("SELECT id FROM map_layers WHERE slug='boundary'").fetchone()[0]
        conn.execute("INSERT INTO layer_features(layer_id,name,feature_type,coords,colour,note) VALUES(?,?,?,?,?,?)",
                     (layer_id, "Parcel 025-00-012", "polygon", json.dumps(pxring), "ink", "County PVA parcel outline (reference, not legal survey)"))
        # store bbox in site_content
        db.set_content(conn, "map_bbox", {"minx":minx,"maxx":maxx,"miny":miny,"maxy":maxy,"W":W,"H":H})
        db.set_content(conn, "parcel_ring", pxring)
        report["boundary_vertices"] = len(pxring)

    # property centroid for placing seed shapes (approx center of parcel)
    # place shapes: simple rectangles for buildings, placed roughly
    # We'll place them as placeholder polygons near center; admin can move.
    cx, cy = 480, 320
    def rect(x,y,w,h):
        return [[x,y],[x+w,y],[x+w,y+h],[x,y+h]]
    shape_map = {
        "main-barn": rect(cx-120, cy-60, 120, 60),
        "shop": rect(cx+20, cy-50, 90, 50),
        "farmhouse": rect(cx-200, cy+40, 80, 60),
        "equipment-shed": rect(cx+10, cy+60, 110, 60),
        "hay-barn": rect(cx-100, cy+120, 90, 50),
        "pond": [[cx+180,cy+80],[cx+260,cy+60],[cx+280,cy+140],[cx+200,cy+160]],
        "north-pasture": rect(60,60,300,200),
        "south-field": rect(60,360,420,220),
    }
    for slug, coords in shape_map.items():
        pid = place_ids[slug]
        conn.execute("INSERT INTO place_shapes(place_id,shape_type,coords) VALUES(?,?,?)",
                     (pid, "polygon", json.dumps(coords)))

    # admin account
    generated = auth.ensure_admin(conn)
    report["admin_generated_password"] = generated

    # site content defaults already written by map_content on first request
    db.set_content(conn, "map_bbox", db.content(conn, "map_bbox", {}))
    report["places_seeded"] = len(places)
    return report


def run_seed():
    conn = db.connect()
    db.init_db(conn)
    rep = seed(conn)
    conn.commit()
    conn.close()
    return rep
