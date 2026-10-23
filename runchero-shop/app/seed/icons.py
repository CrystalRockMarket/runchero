"""Which pixel sprite belongs to which cut.

The sprite names match ``app/pixel/meat.py``. A cut that has no sprite of
its own borrows the closest one: a top round steak and a bottom round steak
are the same shape, a bone-in chuck roast and a bone-in rib roast are both a
roast with a bone along the edge.
"""
from __future__ import annotations

CUT_ICONS: dict[str, str] = {
    # -- chuck ------------------------------------------------------------
    "chuck-roast-bone-in": "roast_bone",
    "chuck-roast-boneless": "roast_chunk",
    "chuck-tender-roast": "roast_chunk",
    "chuck-steak-bone-in": "chuck_steak",
    "chuck-steak-boneless": "chuck_steak",
    "chuck-eye-steak": "chuck_eye",
    "flat-iron-steak": "flat_iron",
    "denver-steak": "denver",
    "cube-steak": "cube_steak",
    "country-style-ribs": "country_ribs",
    "stew-meat": "stew_chunks",
    "beef-shin": "shin",

    # -- rib --------------------------------------------------------------
    "ribeye-steak-bone-in": "ribeye",
    "ribeye-steak-boneless": "ribeye_boneless",
    "rib-fingers": "rib_fingers",
    "prime-rib-roast": "roast_bone",
    "ribeye-roast-boneless": "roast_chunk",
    "beef-back-ribs": "ribs_rack",
    "beef-short-ribs": "ribs_short",

    # -- loin -------------------------------------------------------------
    "strip-steak-bone-in": "striploin",
    "strip-steak-boneless": "striploin_boneless",
    "filet-mignon": "tenderloin",
    "t-bone-steak": "tbone",
    "porterhouse-steak": "porterhouse",
    "flank-steak": "flank",
    "skirt-steak": "skirt",
    "hanger-steak": "hanger",
    "bavette-steak": "bavette",
    "picanha": "picanha",
    "whole-tenderloin": "tenderloin_whole",
    "strip-roast": "roast_bone",
    "filet-tips": "filet_tips",

    # -- round ------------------------------------------------------------
    "top-round-steak": "round_steak",
    "bottom-round-steak": "round_steak",
    "eye-of-round-steak": "eye_round",
    "london-broil": "london_broil",
    "top-round-roast": "roast_round",
    "bottom-round-roast": "roast_round",
    "eye-of-round-roast": "roast_eye",
    "rump-roast": "rump_roast",
    "sirloin-tip-roast": "ball_tip",

    # -- sirloin ----------------------------------------------------------
    "top-sirloin-steak": "sirloin",
    "sirloin-steak-bone-in": "sirloin_bone",
    "sirloin-steak-boneless": "sirloin_boneless",
    "petite-sirloin": "petite_sirloin",
    "tri-tip-steak": "tri_tip",
    "ball-tip-steak": "ball_tip",
    "sirloin-roast": "roast_chunk",
    "tri-tip-roast": "tri_tip",

    # -- brisket ----------------------------------------------------------
    "brisket-whole": "brisket_whole",
    "brisket-flat": "brisket_flat",
    "brisket-point": "brisket_point",

    # -- ground -----------------------------------------------------------
    "ground-beef-70-30": "ground",
    "ground-beef-80-20": "ground",
    "ground-beef-90-10": "ground",
    "ground-chuck": "ground",
    "ground-beef-family-pack": "ground",
    "ground-beef-bulk-10lb": "ground",
    "ground-beef-patties": "patties",
    "premium-grind-patties": "patties",

    # -- variety ----------------------------------------------------------
    "beef-cheek": "cheek",
    "beef-liver": "liver",
    "oxtail": "oxtail",
    "marrow-bones": "marrow_bone",
    "beef-tongue": "tongue",
    "beef-heart": "heart",
    "beef-kidney": "kidney",
    "soup-bones": "soup_bones",
    "beef-suet": "suet",

    # -- deli and prepared ------------------------------------------------
    "deli-roast-beef": "sliced_roast",
    "deli-corned-beef": "corned_beef",
    "beef-jerky": "jerky",
    "summer-sausage": "sausage",
    "snack-sticks": "snack_sticks",
    "beef-bologna": "bologna",
    "beef-bacon": "bacon",
}
