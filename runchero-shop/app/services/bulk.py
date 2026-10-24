"""Made-to-order bulk lots for the Fermentation Station storefront.

The bulk page lists only 25, 50, and 100 lb lots. Prices are derived from the
pint price already stored on each product, so a price change in the catalog
flows through to the bulk page without a second table to maintain.
"""
from __future__ import annotations

from typing import Any

#: (pounds, discount, label)
BULK_TIERS: list[tuple[int, float, str]] = [
    (25, 0.20, "25 lb"),
    (50, 0.25, "50 lb"),
    (100, 0.30, "100 lb"),
]

#: Lead time from confirmed order to ready-for-pickup, with a short note.
LEAD_TIMES: dict[str, tuple[str, str]] = {
    "sauerkraut": ("5 weeks", "Four-week ferment, then packed"),
    "kimchi": ("3 weeks", "Two-week ferment, then packed"),
    "kombucha-classic": ("3 weeks", "Fourteen-day brew, then bottled"),
    "kombucha-ginger": ("3 weeks", "Fourteen-day brew plus ginger secondary"),
    "fermented-pickles": ("4 weeks", "Three-week ferment, then packed"),
    "fermented-mustard": ("5 weeks", "Four-week ferment, then packed"),
    "fermented-hot-sauce": ("4 weeks", "Three-week ferment, then bottled"),
    "apple-cider-vinegar": ("8 weeks", "Six-week ferment plus mother"),
    "miso-paste": ("6 months", "Aged six months before packing"),
    "tempeh": ("1 week", "Fresh culture, then packed"),
}

#: Packaging and holding instructions, by item.
PACKAGING: dict[str, dict[str, str]] = {
    "sauerkraut": {
        "pack": "5-gallon bucket", "hold": "Refrigerated",
        "group": "vegetable",
    },
    "kimchi": {
        "pack": "5-gallon bucket", "hold": "Refrigerated",
        "group": "vegetable",
    },
    "kombucha-classic": {
        "pack": "5-gallon keg", "hold": "Refrigerated",
        "group": "liquid",
    },
    "kombucha-ginger": {
        "pack": "5-gallon keg", "hold": "Refrigerated",
        "group": "liquid",
    },
    "fermented-pickles": {
        "pack": "5-gallon bucket", "hold": "Refrigerated",
        "group": "vegetable",
    },
    "fermented-mustard": {
        "pack": "5-gallon bucket", "hold": "Cool",
        "group": "vegetable",
    },
    "fermented-hot-sauce": {
        "pack": "5-gallon keg", "hold": "Cool",
        "group": "liquid",
    },
    "apple-cider-vinegar": {
        "pack": "5-gallon keg", "hold": "Cool",
        "group": "liquid",
    },
    "miso-paste": {
        "pack": "5-gallon bucket", "hold": "Cool",
        "group": "miso",
    },
    "tempeh": {
        "pack": "1-lb frozen blocks", "hold": "Frozen",
        "group": "tempeh",
    },
}

#: What each packaging group looks like at 25, 50, and 100 lb.
GROUP_NOTES: dict[str, dict[str, str]] = {
    "vegetable": {
        "title": "Fermented vegetables",
        "body": "Food-grade 5-gallon buckets with gasketed lids. A 25 lb "
                "lot is one bucket, 50 lb is two, and 100 lb is four. Each "
                "bucket is labeled with the item, net weight, pack date, and "
                "best-by date.",
    },
    "liquid": {
        "title": "Liquids",
        "body": "Food-grade 5-gallon kegs. A 25 lb lot is about 3 gallons "
                "(one keg), 50 lb is about 6 gallons (two kegs), and 100 lb "
                "is about 12 gallons (three kegs). We confirm the container "
                "with you when you order.",
    },
    "miso": {
        "title": "Miso",
        "body": "Food-grade 5-gallon buckets. A 25 lb lot is one bucket, "
                "50 lb is two, and 100 lb is four. Miso is dense and keeps "
                "well; we pack it tight and label the age and pack date.",
    },
    "tempeh": {
        "title": "Tempeh",
        "body": "Vacuum-sealed 1-lb blocks in an insulated case, kept frozen. "
                "A 25 lb lot is 25 blocks, 50 lb is 50 blocks, and 100 lb is "
                "100 blocks.",
    },
}

DEFAULT_INFO = {
    "lead": "Confirm with us",
    "lead_note": "Batch time depends on the item",
    "pack": "Food-grade container",
    "hold": "Chilled",
    "group": "vegetable",
}


def info_for(slug: str) -> dict[str, str]:
    """Lead time and packaging for one bulk item."""
    lead, note = LEAD_TIMES.get(slug, ("Confirm with us",
                                       "Batch time depends on the item"))
    info = dict(DEFAULT_INFO)
    info.update(PACKAGING.get(slug, {}))
    info["lead"] = lead
    info["lead_note"] = note
    return info


def tiers_for(pint_price: float, pint_lbs: float) -> list[dict[str, Any]]:
    """Price 25, 50, and 100 lb lots from the pint price."""
    per_lb = float(pint_price) / (float(pint_lbs) or 1.04)
    rows: list[dict[str, Any]] = []
    for lbs, discount, label in BULK_TIERS:
        price = round(per_lb * lbs * (1.0 - discount), 2)
        rows.append({
            "lbs": lbs,
            "label": label,
            "price": price,
            "per_lb": round(price / lbs, 2),
            "save_pct": int(round(discount * 100)),
        })
    return rows
