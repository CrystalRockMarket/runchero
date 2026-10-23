"""Place CRUD (admin)."""
from __future__ import annotations

import json
import re

from .. import db, web
from . import page_context, redirect, flash


def register(add):
    add("GET", re.compile(r"^/admin/places$"), list_places)
    add("GET", re.compile(r"^/admin/places/new$"), new_form)
    add("POST", re.compile(r"^/admin/places/new$"), create)
    add("GET", re.compile(r"^/admin/place/(?P<id>\d+)$"), edit_form)
    add("POST", re.compile(r"^/admin/place/(?P<id>\d+)$"), update)
    add("POST", re.compile(r"^/admin/place/(?P<id>\d+)/delete$"), delete)


def _admin_guard(conn, req):
    if not req.session_get("admin_id"):
        return redirect("/admin/login")
    return None


def list_places(conn, req, **_):
    g = _admin_guard(conn, req)
    if g: return g
    places = db.rows(conn, "SELECT p.*, c.name AS catname FROM places p LEFT JOIN categories c ON c.id=p.category_id ORDER BY p.sort_order,p.name")
    ctx = page_context(conn, req, places=[dict(p) for p in places], title="Places")
    return 200, "text/html; charset=utf-8", web.render("admin/places.html", **ctx)


def new_form(conn, req, **_):
    g = _admin_guard(conn, req)
    if g: return g
    cats = db.rows(conn, "SELECT * FROM categories ORDER BY sort_order,name")
    ctx = page_context(conn, req, categories=[dict(c) for c in cats], place=None, title="New Place")
    return 200, "text/html; charset=utf-8", web.render("admin/place_edit.html", **ctx)


def create(conn, req, **_):
    g = _admin_guard(conn, req)
    if g: return g
    if not req.csrf_ok():
        return redirect("/admin/places")
    f = req.form
    slug = (f.get("slug") or "").strip().lower().replace(" ", "-")
    name = (f.get("name") or "").strip()
    if not slug or not name:
        flash(req, "Slug and name required.", "error")
        return redirect("/admin/places/new")
    cat_id = f.get("category_id") or None
    conn.execute("""INSERT INTO places(slug,name,category_id,kind,short_desc,year_built,construction,dimensions,area_acres,status,notes,hidden)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                (slug, name, cat_id, f.get("kind","building"), f.get("short_desc",""), f.get("year_built",""),
                 f.get("construction",""), f.get("dimensions",""), float(f.get("area_acres") or 0),
                 f.get("status","active"), f.get("notes",""), 1 if f.get("hidden")=="1" else 0))
    conn.commit()
    pid = db.scalar(conn, "SELECT id FROM places WHERE slug=?", (slug,))
    db.log_audit(conn, "place.create", "place", pid, json.dumps({"slug":slug,"name":name}), actor=req.session_get("admin_name") or "admin")
    conn.commit()
    flash(req, f"Created {name}.", "ok")
    return redirect(f"/admin/place/{pid}")


def edit_form(conn, req, id, **_):
    g = _admin_guard(conn, req)
    if g: return g
    row = db.one(conn, "SELECT * FROM places WHERE id=?", (id,))
    if not row:
        return redirect("/admin/places")
    p = dict(row)
    p["specs"] = [dict(r) for r in db.rows(conn, "SELECT * FROM place_specs WHERE place_id=? ORDER BY sort_order,id", (id,))]
    p["photos"] = [dict(r) for r in db.rows(conn, "SELECT * FROM place_photos WHERE place_id=? ORDER BY sort_order,id", (id,))]
    p["records"] = [dict(r) for r in db.rows(conn, "SELECT * FROM place_records WHERE place_id=? ORDER BY occurred_on DESC,id DESC", (id,))]
    p["shapes"] = [dict(r) for r in db.rows(conn, "SELECT * FROM place_shapes WHERE place_id=? ORDER BY sort_order,id", (id,))]
    cats = db.rows(conn, "SELECT * FROM categories ORDER BY sort_order,name")
    ctx = page_context(conn, req, place=p, categories=[dict(c) for c in cats], title=f"Edit {p['name']}")
    return 200, "text/html; charset=utf-8", web.render("admin/place_edit.html", **ctx)


def update(conn, req, id, **_):
    g = _admin_guard(conn, req)
    if g: return g
    if not req.csrf_ok():
        return redirect(f"/admin/place/{id}")
    f = req.form
    cat_id = f.get("category_id") or None
    conn.execute("""UPDATE places SET name=?,category_id=?,kind=?,short_desc=?,year_built=?,construction=?,
                    dimensions=?,area_acres=?,status=?,notes=?,hidden=?,updated_at=datetime('now') WHERE id=?""",
                (f.get("name",""), cat_id, f.get("kind","building"), f.get("short_desc",""), f.get("year_built",""),
                 f.get("construction",""), f.get("dimensions",""), float(f.get("area_acres") or 0),
                 f.get("status","active"), f.get("notes",""), 1 if f.get("hidden")=="1" else 0, id))
    # specs replace
    conn.execute("DELETE FROM place_specs WHERE place_id=?", (id,))
    for i, key in enumerate(req.getlist("spec_key")):
        val = req.getlist("spec_value")[i] if i < len(req.getlist("spec_value")) else ""
        if key.strip():
            conn.execute("INSERT INTO place_specs(place_id,key,value,sort_order) VALUES(?,?,?,?)", (id, key.strip(), val.strip(), i))
    # photos: append new paths
    for path in [p for p in (req.form.get("new_photo_path") or "").splitlines() if p.strip()]:
        cap = req.form.get("new_photo_caption","")
        conn.execute("INSERT INTO place_photos(place_id,path,caption) VALUES(?,?,?)", (id, path.strip(), cap.strip()))
    # records append
    rtitle = (req.form.get("new_record_title") or "").strip()
    if rtitle:
        conn.execute("INSERT INTO place_records(place_id,kind,title,body,occurred_on,actor) VALUES(?,?,?,?,?,?)",
                     (id, req.form.get("new_record_kind","note"), rtitle, req.form.get("new_record_body",""), req.form.get("new_record_date",""), req.session_get("admin_name") or "admin"))
    # shape coords update
    coords_json = req.form.get("shape_coords")
    if coords_json:
        try:
            coords = json.loads(coords_json)
            conn.execute("DELETE FROM place_shapes WHERE place_id=?", (id,))
            conn.execute("INSERT INTO place_shapes(place_id,shape_type,coords) VALUES(?,?,?)", (id, "polygon", json.dumps(coords)))
        except Exception:
            pass
    conn.commit()
    db.log_audit(conn, "place.update", "place", id, json.dumps({"name": f.get("name","")}), actor=req.session_get("admin_name") or "admin")
    conn.commit()
    flash(req, "Saved.", "ok")
    return redirect(f"/admin/place/{id}")


def delete(conn, req, id, **_):
    g = _admin_guard(conn, req)
    if g: return g
    if not req.csrf_ok():
        return redirect("/admin/places")
    row = db.one(conn, "SELECT name FROM places WHERE id=?", (id,))
    name = row["name"] if row else id
    conn.execute("DELETE FROM places WHERE id=?", (id,))
    conn.commit()
    db.log_audit(conn, "place.delete", "place", id, json.dumps({"name": name}), actor=req.session_get("admin_name") or "admin")
    conn.commit()
    flash(req, f"Deleted {name}.", "ok")
    return redirect("/admin/places")
