"""Where the depot's information comes from.

The depot does not host AI-written articles. Its pages are AI-organised
indexes: they point at books, reports and manuals that are read in full from
the local archive. Nothing here invents a citation. A source appears on a page
only when there is a real archive file, publication URL or scan behind it.
"""
from __future__ import annotations

AI_VEHICLE = {
    "slug": "depot-ai-vehicle-data",
    "title": "Runchero equipment index",
    "author": "Runchero",
    "kind": "ai-organized",
    "url": "",
    "license": "",
    "note": "Equipment records organised with AI. Use the factory manual for "
            "exact settings, torques, fluids and serial number breaks.",
}
AI_FORMULA = {
    "slug": "depot-ai-formula-shelf",
    "title": "Runchero formula index",
    "author": "Runchero",
    "kind": "ai-organized",
    "url": "",
    "license": "",
    "note": "Formulas collected and indexed with AI. The calculators are "
            "convenience tools; double-check every result before using it.",
}
AI_TOPIC = {
    "slug": "depot-ai-topic-map",
    "title": "Runchero depot index",
    "author": "Runchero",
    "kind": "ai-organized",
    "url": "",
    "license": "",
    "note": "The grouping, labels and cross-links on this page are AI-organised "
            "from the archive's books and manuals. The information itself is "
            "read from those sources.",
}
AI_REFERENCE = {
    "slug": "depot-ai-reference-pages",
    "title": "Runchero reference index",
    "author": "Runchero",
    "kind": "ai-organized",
    "url": "",
    "license": "",
    "note": "Conversion tables and reference layouts compiled with AI from "
            "standard public reference values. Verify safety-critical or "
            "expensive calculations independently.",
}

AI_SOURCES = [AI_VEHICLE, AI_FORMULA, AI_TOPIC, AI_REFERENCE]

#: Static pages that carry the "AI-organised index" provenance footer.
STATIC_PAGES = [
    ("page", "home", AI_TOPIC["slug"]),
    ("page", "grow", AI_TOPIC["slug"]),
    ("page", "animals", AI_TOPIC["slug"]),
    ("page", "farm", AI_TOPIC["slug"]),
    ("page", "kitchen", AI_TOPIC["slug"]),
    ("page", "workshop", AI_TOPIC["slug"]),
    ("page", "survival", AI_TOPIC["slug"]),
    ("page", "vehicles", AI_TOPIC["slug"]),
    ("page", "library", AI_TOPIC["slug"]),
    ("page", "archive", AI_TOPIC["slug"]),
    ("page", "search", AI_TOPIC["slug"]),
    ("page", "formulas", AI_FORMULA["slug"]),
    ("page", "conversions", AI_REFERENCE["slug"]),
    ("page", "sources", AI_TOPIC["slug"]),
    ("page", "reader", AI_TOPIC["slug"]),
    ("page", "library-manuals", AI_VEHICLE["slug"]),
]
