"""Public map view."""
from __future__ import annotations

import json
import re

from .. import db, web
from . import page_context, redirect


def register(add):
    add("GET", re.compile(r"^/$"), index)
    add("GET", re.compile(r"^/map$"), index)
    add("GET", re.compile(r"^/place/(?P<slug>[^/]+)$"), place_detail)
    add("GET", re.compile(r"^/api/places$"), api_places)
    add("GET", re.compile(r"^/api/layers$"), api_layers)


def index(conn, req, **_):
    places = db.rows(conn, "SELECT p.*, c.name AS category_name, c.colour AS category_colour FROM places p LEFT JOIN categories c ON c.id=p.category_id WHERE p.hidden=0 ORDER BY p.sort_order, p.name")
    layers = db.rows(conn, "SELECT * FROM map_layers ORDER BY sort_order, name")
    shapes = {}
    for s in db.rows(conn, "SELECT * FROM place_shapes"):
        shapes.setdefault(s["place_id"], []).append(dict(s))
    places_list = []
    for p in places:
        d = dict(p)
        d["shapes"] = shapes.get(p["id"], [])
        d["specs"] = [dict(r) for r in db.rows(conn, "SELECT * FROM place_specs WHERE place_id=? ORDER BY sort_order,id", (p["id"],))]
        d["photos"] = [dict(r) for r in db.rows(conn, "SELECT * FROM place_photos WHERE place_id=? ORDER BY sort_order,id", (p["id"],))]
        d["records"] = [dict(r) for r in db.rows(conn, "SELECT * FROM place_records WHERE place_id=? ORDER BY occurred_on DESC, id DESC", (p["id"],))]
        places_list.append(d)
    bbox = db.content(conn, "map_bbox", {})
    ring = db.content(conn, "parcel_ring", [])
    ctx = page_context(conn, req, places=places_list, layers=[dict(l) for l in layers],
                       bbox=bbox, ring=ring, title="Property Map")
    return 200, "text/html; charset=utf-8", web.render("map.html", **ctx)


def place_detail(conn, req, slug, **_):
    row = db.one(conn, "SELECT p.*, c.name AS category_name, c.colour AS category_colour FROM places p LEFT JOIN categories c ON c.id=p.category_id WHERE p.slug=?", (slug,))
    if not row:
        return 404, "text/html; charset=utf-8", "not found"
    p = dict(row)
    p["shapes"] = [dict(s) for s in db.rows(conn, "SELECT * FROM place_shapes WHERE place_id=? ORDER BY sort_order,id", (row["id"],))]
    p["specs"] = [dict(s) for r in [] for s in []] or [dict(r) for r in db.rows(conn, "SELECT * FROM place_specs WHERE place_id=? ORDER BY sort_order,id", (row["id"],))]
    p["photos"] = [dict(r) for r in db.rows(conn, "SELECT * FROM place_photos WHERE place_id=? ORDER BY sort_order,id", (row["id"],))]
    p["records"] = [dict(r) for r in db.rows(conn, "SELECT * FROM place_records WHERE place_id=? ORDER BY occurred_on DESC, id DESC", (row["id"],))]
    ctx = page_context(conn, req, place=p, title=p["name"])
    return 200, "text/html; charset=utf-8", web.render("place.html", **ctx)


def api_places(conn, req, **_):
    places = db.rows(conn, "SELECT id,slug,name,category_id,kind,short_desc,status,hidden FROM places")
    out = []
    for p in places:
        d = dict(p)
        d["shapes"] = [dict(s) for s in db.rows(conn, "SELECT shape_type,coords,colour FROM place_shapes WHERE place_id=?", (p["id"],))]
        out.append(d)
    return 200, "application/json; charset=utf-8", json.dumps(out)


def api_layers(conn, req, **_):
    layers = db.rows(conn, "SELECT * FROM map_layers ORDER BY sort_order,name")
    out = []
    for l in layers:
        d = dict(l)
        d["features"] = [dict(f) for f in db.rows(conn, "SELECT name,feature_type,coords,colour,note FROM layer_features WHERE layer_id=?", (l["id"],))]
        out.append(d)
    return 200, "application/json; charset=utf-8", json.dumps(out)
