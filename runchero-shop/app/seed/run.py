"""Seed the shop: catalog, packing options, shares, packages, terms, slots.

Idempotent. Prices come from live USDA feeds when the box has internet, and
from documented reference prices when it does not, so the shop boots offline
with honest numbers either way.
"""
from __future__ import annotations

import json
from typing import Any

from .. import db
from ..services import fulfillment, market, pricing, products, variants
from .icons import CUT_ICONS

# --------------------------------------------------------------------------
# catalog: nine primals, the sections inside them, then the cuts
# --------------------------------------------------------------------------

PRIMALS = [
    ("chuck", "Chuck", "cow", "meat",
     "Hard-working shoulder muscle. The best pot roast on the animal, and "
     "the flat iron and Denver steaks hiding inside it.", 1),
    ("rib", "Rib", "cow", "sun",
     "The luxury seats. Ribeye, prime rib, and the back ribs.", 2),
    ("loin", "Loin", "cow", "sky",
     "Strip, tenderloin, T-bone, porterhouse. The tender stretch along the "
     "backbone.", 3),
    ("round", "Round", "cow", "teal",
     "The leg. Lean, built for roasts and London broil.", 4),
    ("sirloin", "Sirloin", "cow", "grass",
     "The hip: top sirloin, tri-tip, petite sirloin. Flavor per dollar.", 5),
    ("brisket", "Brisket", "cow", "soil",
     "The breast. Low and slow, or point it at the smoker.", 6),
    ("ground", "Ground", "cow", "tomato",
     "Ground by us, the day it is cut. Choose your leanness.", 7),
    ("variety", "Variety", "cow", "plum",
     "Liver, oxtail, bones, tongue. The old cooking, back in style.", 8),
    ("deli", "Deli & Prepared", "cow", "orange",
     "Smoked, dried, and sliced. Made from the same herd.", 9),
]

SECTIONS = [
    ("steaks", "Steaks", 1),
    ("roasts", "Roasts", 2),
    ("ground", "Ground", 3),
    ("ribs", "Ribs", 4),
    ("stew", "Stew & Stir-fry", 5),
    ("bones", "Bones & Extras", 6),
    ("prepared", "Prepared", 7),
]

#: (slug, name, primal, section, ams series key, fallback local price/lb,
#:  unit, unit_lbs, tags, serving, blurb, icon, featured)
CUTS: list[tuple] = [
    # -- chuck ------------------------------------------------------------
    ("chuck-roast-bone-in", "Chuck Roast, Bone-In", "chuck", "roasts",
     "ams:Chuck Roast, Bone-In, Regular", 7.02, "lb", 3.5, "roast,sunday",
     "Feeds 4-6", "Pot roast the way your grandmother made it.", "cow", 1),
    ("chuck-roast-boneless", "Chuck Roast, Boneless", "chuck", "roasts",
     "ams:Chuck Roast, Boneless, Regular", 6.62, "lb", 3.0, "roast",
     "Feeds 4-6", "Rolled and tied, ready for the Dutch oven.", "cow", 1),
    ("chuck-steak-bone-in", "Chuck Steak, Bone-In", "chuck", "steaks",
     "ams:Chuck Steak, Bone-In, Regular", 6.99, "lb", 1.0, "steak,budget",
     "1 steak", "A weeknight steak that takes a marinade happily.", "cow", 0),
    ("chuck-steak-boneless", "Chuck Steak, Boneless", "chuck", "steaks",
     "", 7.49, "lb", 0.8, "steak,budget", "1 steak",
     "Leaner than the bone-in, quick on a flat top.", "cow", 0),
    ("chuck-eye-steak", "Chuck Eye Steak", "chuck", "steaks",
     "ams:Chuck Eye Steak, Regular", 6.99, "lb", 0.7, "steak,value",
     "1 steak", "The poor man's ribeye, and honestly close.", "cow", 1),
    ("flat-iron-steak", "Flat Iron Steak", "chuck", "steaks",
     "ams:Flat Iron Steak, Regular", 12.99, "lb", 0.7, "steak,grill",
     "1-2 steaks", "Second most tender cut on the animal.", "cow", 1),
    ("denver-steak", "Denver Steak", "chuck", "steaks",
     "", 12.99, "lb", 0.7, "steak,grill", "1-2 steaks",
     "Chuck's other secret. Well marbled, cheap by reputation.", "cow", 0),
    ("chuck-tender-roast", "Chuck Tender Roast", "chuck", "roasts",
     "", 7.29, "lb", 2.5, "roast", "Feeds 4",
     "The mock tender. Slice it thin for sandwiches after.", "cow", 0),
    ("country-style-ribs", "Country Style Ribs", "chuck", "ribs",
     "", 8.99, "lb", 2.0, "ribs,smoker", "Feeds 3",
     "Not ribs at all: chuck sliced rib-style. Braise them.", "cow", 0),
    ("stew-meat", "Beef Stew Meat", "chuck", "stew",
     "ams:Stew Meat, Regular", 9.98, "lb", 1.5, "stew,slowcooker",
     "Feeds 4", "Hand-cubed chuck. Half the work of stew is done.", "cow", 1),
    ("cube-steak", "Cube Steak", "chuck", "steaks",
     "ams:Cube Steak, Regular", 6.99, "lb", 0.6, "steak,chickenfried",
     "1 steak", "Country fried steak, chicken fried steak, tonight.", "cow", 0),
    ("beef-shin", "Beef Shin, Cross-Cut", "chuck", "stew",
     "", 5.49, "lb", 1.5, "stew,osso", "Feeds 3",
     "Osso buco cut. Marrow in the middle, collagen all through.", "cow", 0),
    # -- rib --------------------------------------------------------------
    ("ribeye-steak-bone-in", "Ribeye Steak, Bone-In", "rib", "steaks",
     "ams:Ribeye Steak, Bone-In, Regular", 16.35, "lb", 1.1, "steak,grill",
     "1 steak", "The cowboy cut. Marbling that carries the flavor.", "cow", 1),
    ("ribeye-steak-boneless", "Ribeye Steak, Boneless", "rib", "steaks",
     "ams:Ribeye Steak, Boneless, Regular", 19.99, "lb", 0.9, "steak,grill",
     "1-2 steaks", "All ribeye, no bone to work around.", "cow", 1),
    ("prime-rib-roast", "Prime Rib Roast, Bone-In", "rib", "roasts",
     "", 14.99, "lb", 5.0, "roast,holiday", "Feeds 6-8",
     "The holiday centerpiece. Order early, we cut these to request.", "cow", 1),
    ("ribeye-roast-boneless", "Ribeye Roast, Boneless", "rib", "roasts",
     "ams:Ribeye Roast, Boneless, Regular", 8.99, "lb", 4.0, "roast",
     "Feeds 6", "A rolled ribeye roast, easier to slice than bone-in.", "cow", 0),
    ("beef-back-ribs", "Beef Back Ribs", "rib", "ribs",
     "", 6.99, "lb", 3.0, "ribs,smoker", "Feeds 2-3",
     "Leftovers from the ribeye roast, and proud of it.", "cow", 0),
    ("beef-short-ribs", "Beef Short Ribs", "rib", "ribs",
     "ams:Short Ribs, Regular", 10.99, "lb", 2.5, "ribs,slowcooker,smoker",
     "Feeds 3", "English cut. Braise until they give up.", "cow", 1),
    ("rib-fingers", "Rib Fingers", "rib", "steaks",
     "", 9.99, "lb", 1.0, "steak,grill", "Feeds 2",
     "The meat between the rib bones. Grill hot and fast.", "cow", 0),
    # -- loin -------------------------------------------------------------
    ("strip-steak-bone-in", "Strip Steak, Bone-In", "loin", "steaks",
     "ams:Strip Steak, Bone-In, Regular", 8.99, "lb", 1.0, "steak,grill",
     "1 steak", "The Kansas City strip. Firm, beefy, honest.", "cow", 1),
    ("strip-steak-boneless", "Strip Steak, Boneless", "loin", "steaks",
     "ams:Strip Steak, Boneless, Regular", 15.97, "lb", 0.9, "steak,grill",
     "1-2 steaks", "The New York strip. Steakhouse default.", "cow", 1),
    ("filet-mignon", "Filet Mignon", "loin", "steaks",
     "ams:Filet Mignon, Regular", 23.98, "lb", 0.5, "steak,premium",
     "2 medallions", "The tenderloin, cut into medallions.", "cow", 1),
    ("whole-tenderloin", "Whole Tenderloin", "loin", "roasts",
     "ams:Tenderloin, Regular", 17.15, "lb", 4.5, "roast,holiday,premium",
     "Feeds 6-8", "The whole PSMO. Cheaper per pound than medallions.", "cow", 0),
    ("t-bone-steak", "T-Bone Steak", "loin", "steaks",
     "ams:T-Bone Steak, Regular", 12.71, "lb", 1.2, "steak,grill",
     "1 steak", "Strip on one side of the bone, tenderloin on the other.", "cow", 1),
    ("porterhouse-steak", "Porterhouse Steak", "loin", "steaks",
     "ams:Porterhouse Steak, Regular", 15.71, "lb", 1.5, "steak,grill,premium",
     "1 steak, feeds 2", "The T-bone's big brother, with a real filet side.", "cow", 1),
    ("strip-roast", "Strip Roast, Bone-In", "loin", "roasts",
     "ams:Strip Roast, Bone-In, Regular", 4.99, "lb", 4.0, "roast",
     "Feeds 6", "A whole striploin, roasted whole and sliced thin.", "cow", 0),
    ("flank-steak", "Flank Steak", "loin", "steaks",
     "ams:Flank Steak, Regular", 12.99, "lb", 1.2, "steak,fajitas",
     "Feeds 3", "London broil's home cut. Slice across the grain.", "cow", 1),
    ("skirt-steak", "Skirt Steak", "loin", "steaks",
     "ams:Skirt Steak, Regular", 13.29, "lb", 1.0, "steak,fajitas,grill",
     "Feeds 2-3", "The fajita cut. Char it hard, slice it thin.", "cow", 1),
    ("hanger-steak", "Hanger Steak", "loin", "steaks",
     "", 16.99, "lb", 0.8, "steak,grill", "Feeds 2",
     "One per animal. The butcher's secret kept badly.", "cow", 0),
    ("bavette-steak", "Bavette (Flap) Steak", "loin", "steaks",
     "", 13.99, "lb", 1.0, "steak,grill", "Feeds 2-3",
     "The bistro cut in Paris. Takes a sauce like it was born for it.", "cow", 0),
    ("picanha", "Picanha (Coulotte)", "loin", "steaks",
     "", 15.99, "lb", 1.2, "steak,grill,smoker", "Feeds 3",
     "The Brazilian rump cap. Fat cap on, rotisserie ready.", "cow", 0),
    ("filet-tips", "Filet Tips", "loin", "stew",
     "", 12.99, "lb", 1.0, "stew,stirfry,premium", "Feeds 2-3",
     "Tenderloin ends and trim. Stroganoff without the sticker shock.", "cow", 0),
    # -- round ------------------------------------------------------------
    ("top-round-roast", "Top Round Roast", "round", "roasts",
     "ams:Top Round Roast, Regular", 8.02, "lb", 3.0, "roast,deli",
     "Feeds 5", "The deli roast beef cut. Slice it thin for lunches.", "cow", 1),
    ("top-round-steak", "Top Round Steak", "round", "steaks",
     "ams:Top Round Steak, Regular", 5.99, "lb", 0.9, "steak,budget",
     "1 steak", "London broil's cousin. Marinate, then slice thin.", "cow", 0),
    ("bottom-round-roast", "Bottom Round Roast", "round", "roasts",
     "ams:Bottom Round Roast, Regular", 7.99, "lb", 3.0, "roast,slowcooker",
     "Feeds 5", "The pot roast for people who want less fat.", "cow", 0),
    ("bottom-round-steak", "Bottom Round Steak", "round", "steaks",
     "ams:Bottom Round Steak, Regular", 6.99, "lb", 0.8, "steak,budget",
     "1 steak", "Swiss steak territory. Pound it, flour it, braise it.", "cow", 0),
    ("eye-of-round-roast", "Eye of Round Roast", "round", "roasts",
     "ams:Eye of Round Roast, Regular", 6.99, "lb", 2.5, "roast,deli",
     "Feeds 4", "The leanest roast on the animal. Slice it paper thin.", "cow", 0),
    ("eye-of-round-steak", "Eye of Round Steak", "round", "steaks",
     "ams:Eye of Round Steak, Regular", 7.68, "lb", 0.7, "steak,budget",
     "1 steak", "Breakfast steak country. Chicken fry it.", "cow", 0),
    ("rump-roast", "Rump Roast", "round", "roasts",
     "ams:Rump Roast, Regular", 7.36, "lb", 3.0, "roast,slowcooker",
     "Feeds 5", "Three muscles in one roast. Braise it whole.", "cow", 0),
    ("sirloin-tip-roast", "Sirloin Tip Roast (Knuckle)", "round", "roasts",
     "ams:Sirloin Tip Roast, Regular", 6.99, "lb", 2.5, "roast",
     "Feeds 4", "Kentucky's favorite roast, and for good reason.", "cow", 1),
    ("london-broil", "London Broil", "round", "steaks",
     "ams:London Broil, Regular", 8.99, "lb", 1.5, "steak,budget,marinate",
     "Feeds 3", "Marinated top round, broiled hot and sliced thin.", "cow", 0),
    # -- sirloin ----------------------------------------------------------
    ("top-sirloin-steak", "Top Sirloin Steak, Boneless", "sirloin", "steaks",
     "ams:Top Sirloin Steak, Boneless, Regular", 10.04, "lb", 0.9,
     "steak,grill", "1-2 steaks",
     "The steak for every Saturday. Beefy and forgiving.", "cow", 1),
    ("sirloin-steak-bone-in", "Sirloin Steak, Bone-In", "sirloin", "steaks",
     "ams:Sirloin Steak, Bone-In, Regular", 8.99, "lb", 1.0, "steak,grill",
     "1 steak", "The bone adds a little something. Cheaper, too.", "cow", 0),
    ("sirloin-steak-boneless", "Sirloin Steak, Boneless", "sirloin", "steaks",
     "ams:Sirloin Steak, Boneless, Regular", 11.99, "lb", 0.8, "steak,grill",
     "1-2 steaks", "A smaller portion with all the flavor.", "cow", 0),
    ("petite-sirloin", "Petite Sirloin", "sirloin", "steaks",
     "ams:Petite Sirloin/Ball Tip Steak, Regular", 7.99, "lb", 0.6,
     "steak,budget", "1 steak",
     "The petite cut. A single-serving steak that grills in six minutes.", "cow", 0),
    ("sirloin-roast", "Sirloin Roast, Boneless", "sirloin", "roasts",
     "ams:Sirloin Roast, Boneless, Regular", 11.99, "lb", 3.0, "roast",
     "Feeds 5", "Tri-tip's big roast cousin.", "cow", 0),
    ("tri-tip-roast", "Tri-Tip Roast", "sirloin", "roasts",
     "ams:Tri-Tip Roast, Regular", 9.99, "lb", 2.0, "roast,smoker,grill",
     "Feeds 4", "The California cut. Fat cap on, smoke or grill.", "cow", 1),
    ("tri-tip-steak", "Tri-Tip Steak", "sirloin", "steaks",
     "ams:Tri-Tip Steak, Regular", 6.99, "lb", 0.9, "steak,grill",
     "1-2 steaks", "Tri-tip sliced into steaks for the week.", "cow", 0),
    ("ball-tip-steak", "Ball Tip Steak", "sirloin", "steaks",
     "ams:Petite Sirloin/Ball Tip Steak, Regular", 7.99, "lb", 0.7,
     "steak,budget", "1 steak", "The petite sirloin's other name.", "cow", 0),
    # -- brisket ----------------------------------------------------------
    ("brisket-whole", "Brisket, Whole Packer", "brisket", "roasts",
     "ams:Brisket, Whole, Regular", 5.28, "lb", 12.0, "smoker,roast",
     "Feeds a crowd", "The full packer, flat and point. Low and slow.", "cow", 1),
    ("brisket-flat", "Brisket, Flat", "brisket", "roasts",
     "", 6.99, "lb", 6.0, "smoker,roast", "Feeds 6",
     "The lean half of the brisket. Slices clean for sandwiches.", "cow", 0),
    ("brisket-point", "Brisket, Point", "brisket", "roasts",
     "", 5.99, "lb", 5.0, "smoker", "Feeds 5",
     "The fatty half. Burnt ends start here.", "cow", 0),
    # -- ground -----------------------------------------------------------
    ("ground-beef-70-30", "Ground Beef 70/30", "ground", "ground",
     "ams:Ground Beef 70-79%, 1-2 Lbs", 4.98, "lb", 1.0, "ground,burger",
     "1 lb pack", "The burger blend. Fat is flavor.", "cow", 1),
    ("ground-beef-80-20", "Ground Beef 80/20", "ground", "ground",
     "ams:Ground Beef 80-89%, 1-2 Lbs", 6.53, "lb", 1.0, "ground,burger",
     "1 lb pack", "The everyday grind. Burgers to bolognese.", "cow", 1),
    ("ground-beef-90-10", "Ground Beef 90/10", "ground", "ground",
     "ams:Ground Beef 90% or More, 1-2 Lbs", 7.10, "lb", 1.0, "ground,lean",
     "1 lb pack", "The lean grind. Tacos, chili, weeknights.", "cow", 1),
    ("ground-chuck", "Ground Chuck, 100% Beef", "ground", "ground",
     "bls:APU0000703111", 6.48, "lb", 1.0, "ground,chuck", "1 lb pack",
     "Ground from the chuck only, the day it is cut.", "cow", 0),
    ("ground-beef-family-pack", "Ground Beef 80/20, Family Pack", "ground",
     "ground", "ams:Ground Beef 80-89%, 5-9 Lbs", 4.00, "lb", 5.0,
     "ground,family", "5 lb pack",
     "Five pounds of the everyday grind in one wrap.", "cow", 1),
    ("ground-beef-bulk-10lb", "Ground Beef 80/20, 10 lb Box", "ground",
     "ground", "ams:Ground Beef 80-89%, 10 Lbs or more", 4.00, "lb", 10.0,
     "ground,family,freezer", "10 lb box",
     "Ten pounds, ten wraps. Fill the freezer.", "cow", 0),
    ("ground-beef-patties", "Ground Beef Patties", "ground", "ground",
     "ams:Ground Beef Patties, 1-2 Lbs", 6.99, "lb", 1.5, "ground,burger",
     "4 quarter-pound patties", "Pre-formed, pre-separated, grill-ready.", "cow", 0),
    ("premium-grind-patties", "Premium Grind Patties", "ground", "ground",
     "ams:Premium Grind Patties, 1-2 Lbs", 10.94, "lb", 1.5,
     "ground,burger,premium", "4 patties",
     "Chuck and sirloin ground together, patted by hand.", "cow", 0),
    # -- variety ----------------------------------------------------------
    ("beef-liver", "Beef Liver", "variety", "bones",
     "", 4.49, "lb", 1.0, "variety,liver", "Feeds 3",
     "Slice it thin, flour it, onions on top.", "cow", 0),
    ("oxtail", "Oxtail", "variety", "bones",
     "", 12.99, "lb", 2.0, "variety,stew,slowcooker", "Feeds 3",
     "The soup that made oxtail famous. Collagen for days.", "cow", 1),
    ("marrow-bones", "Marrow Bones", "variety", "bones",
     "", 3.99, "lb", 2.0, "variety,bones", "3-4 bones",
     "Roast them, scoop the marrow, spread it on toast.", "cow", 0),
    ("beef-tongue", "Beef Tongue", "variety", "bones",
     "", 9.99, "lb", 2.5, "variety", "Feeds 5",
     "Slow-poached, peeled, sliced cold. A delicacy.", "cow", 0),
    ("beef-heart", "Beef Heart", "variety", "bones",
     "", 5.49, "lb", 1.5, "variety,grill", "Feeds 3",
     "Skewer it, grill it rare. Dense and mineral.", "cow", 0),
    ("beef-kidney", "Beef Kidney", "variety", "bones",
     "", 4.99, "lb", 1.0, "variety", "Feeds 2",
     "Steak and kidney pie, for the traditionalists.", "cow", 0),
    ("beef-cheek", "Beef Cheek", "variety", "stew",
     "", 8.99, "lb", 1.5, "stew,slowcooker", "Feeds 3",
     "The braising cut that restaurants fight over.", "cow", 1),
    ("soup-bones", "Soup Bones", "variety", "bones",
     "", 2.49, "lb", 2.0, "bones,broth", "2 lb pack",
     "The start of every good pot of broth.", "cow", 0),
    ("beef-suet", "Beef Suet", "variety", "bones",
     "", 2.99, "lb", 1.0, "variety,broth", "1 lb",
     "Render it for tallow, or feed the birds in winter.", "cow", 0),
    # -- deli -------------------------------------------------------------
    ("deli-roast-beef", "Sliced Roast Beef", "deli", "prepared",
     "ams:Service Deli Roast Beef Cat 1", 12.78, "lb", 1.0, "deli,sandwich",
     "Feeds 4", "Roasted from our own top round, sliced thin.", "cow", 1),
    ("deli-corned-beef", "Sliced Corned Beef", "deli", "prepared",
     "ams:Service Deli Corned Beef", 13.99, "lb", 1.0, "deli,sandwich",
     "Feeds 4", "Corned in house, steamed and sliced.", "cow", 0),
    ("beef-jerky", "Beef Jerky", "deli", "prepared",
     "", 24.99, "each", 0.25, "deli,snack", "4 oz pack",
     "Dried in the smokehouse, cut from the round.", "cow", 1),
    ("summer-sausage", "Summer Sausage", "deli", "prepared",
     "", 12.99, "each", 1.0, "deli,snack", "1 lb roll",
     "The picnic roll. Smoked, cured, shelf stable.", "cow", 0),
    ("snack-sticks", "Beef Snack Sticks", "deli", "prepared",
     "", 7.99, "each", 0.4, "deli,snack", "8 sticks",
     "The lunchbox favorite, in five flavors.", "cow", 0),
    ("beef-bologna", "Smoked Beef Bologna", "deli", "prepared",
     "", 6.99, "lb", 1.0, "deli,sandwich", "Feeds 5",
     "Old fashioned ring bologna, smoked over hickory.", "cow", 0),
    ("beef-bacon", "Beef Bacon", "deli", "prepared",
     "", 9.99, "lb", 1.0, "deli,breakfast", "1 lb",
     "Cured and smoked navels. Breakfast, solved.", "cow", 0),
]

# --------------------------------------------------------------------------
# packages, shares, packing options
# --------------------------------------------------------------------------

PACKAGES: list[dict] = [
    {"slug": "steak-night", "name": "Steak Night Box", "badge": "Deal of the week",
     "blurb": "Two ribeyes, two strips, four filet medallions. The box that "
              "makes a Saturday.", "icon": "ribeye", "featured": 1, "deal_rank": 1,
     "items": [("ribeye-steak-bone-in", 2.2), ("strip-steak-boneless", 1.8),
               ("filet-mignon", 1.0)]},
    {"slug": "freezer-filler", "name": "Freezer Filler", "badge": "Best value",
     "blurb": "Twenty pounds: ground, roasts, and stew meat. A month of "
              "dinners in one drop.", "icon": "roast_chunk", "featured": 1,
     "deal_rank": 2,
     "items": [("ground-beef-family-pack", 5.0), ("chuck-roast-boneless", 3.0),
               ("sirloin-tip-roast", 2.5), ("stew-meat", 1.5),
               ("ground-beef-90-10", 1.0)]},
    {"slug": "burger-block", "name": "Burger Block", "badge": "Grill season",
     "blurb": "Ten pounds of 80/20 in ten wraps. The block that carries a "
              "summer.", "icon": "patties", "featured": 1, "deal_rank": 3,
     "items": [("ground-beef-bulk-10lb", 10.0)]},
    {"slug": "family-favorites", "name": "Family Favorites", "badge": "",
     "blurb": "Roast night, taco night, and stew night, covered.",
     "icon": "country_ribs", "featured": 1, "deal_rank": 4,
     "items": [("chuck-roast-bone-in", 3.5), ("ground-beef-90-10", 2.0),
               ("sirloin-tip-roast", 2.5), ("beef-short-ribs", 2.0)]},
]

SHARES = [
    ("eighth", "Eighth Share", 100, 79, 535, 75, 6.77, 1,
     "About 79 lb of take-home beef. Fits a small chest freezer.", 4),
    ("quarter", "Quarter Share", 200, 158, 1030, 150, 6.52, 1,
     "The classic quarter: steaks, roasts, and ground for a household.", 3),
    ("half", "Half Share", 400, 315, 2020, 250, 6.41, 1,
     "A side of beef, cut exactly how you like it.", 2),
    ("whole-drop", "Whole Cow, Multi-Household Drop", 800, 630, 3960, 300, 6.29, 4,
     "A whole cow split across households, each with its own order, cut "
     "sheet, and packing choices. No single sale exceeds half a carcass, "
     "which is how the retail exemption works.", 1),
]

PACKING_GROUPS = [
    ("wrap", "Wrapping", "Paper or vacuum sealed. Paper breathes and is "
     "traditional; vacuum seal is best for the freezer.", "order", 1),
    ("portioning", "Portioning", "Whole cuts, or steaks cut to your "
     "thickness and portioned.", "order", 2),
    ("bagging", "Bagging", "Bulk packaging means fewer bags; individual "
     "means every portion is labeled.", "order", 3),
    ("ground_pack", "Ground Beef Pack Size", "How the grind is wrapped.",
     "line", 4),
    ("gift", "Gift Wrap", "A kraft box and a hand written card.", "order", 5),
    ("labeling", "Labels", "Every wrap carries the cut and the pack date.",
     "order", 6),
]

#: (group, code, label, description, price_mode, amount, is_default, icon)
PACKING_OPTIONS = [
    ("wrap", "vacuum", "Vacuum sealed (plastic)", "",
     "per_lb", 0.0, 1, "box"),
    ("wrap", "paper", "Butcher paper", "Breathes, traditional, great for "
     "display. Best eaten within three weeks.", "per_lb", 0.75, 0, "box"),
    ("wrap", "paper_vacuum", "Butcher paper + vacuum", "Paper on the "
     "outside, sealed inside. Best of both.", "per_lb", 1.25, 0, "box"),
    ("portioning", "whole", "Whole cut", "", "per_lb", 0.0, 1, "cow"),
    ("portioning", "steak_8", "Portioned 8 oz steaks", "", "per_unit", 1.50, 0,
     "cow"),
    ("portioning", "steak_10", "Portioned 10 oz steaks", "", "per_unit", 1.75,
     0, "cow"),
    ("portioning", "steak_12", "Portioned 12 oz steaks", "", "per_unit", 2.00,
     0, "cow"),
    ("portioning", "meal", "Meal-ready portions", "Cubed and portioned for "
     "stir-fry, stew, and tacos.", "per_lb", 0.90, 0, "cow"),
    ("bagging", "bulk", "Bulk packaging", "", "per_lb", 0.0, 1, "box"),
    ("bagging", "individual", "Individually portioned and labeled", "",
     "per_unit", 0.25, 0, "box"),
    ("ground_pack", "lb5", "5 lb packs", "", "per_lb", 0.0, 1, "box"),
    ("ground_pack", "lb1", "1 lb packs", "More wraps, easier to thaw one "
     "meal at a time.", "per_lb", 0.50, 0, "box"),
    ("ground_pack", "lb2", "2 lb packs", "", "per_lb", 0.30, 0, "box"),
    ("ground_pack", "lb10", "One 10 lb box", "Cheaper by the wrap.", "percent",
     -5.0, 0, "box"),
    ("gift", "no", "No gift wrap", "", "flat", 0.0, 1, "box"),
    ("gift", "yes", "Kraft box + handwritten card", "", "flat", 6.0, 0, "box"),
    ("labeling", "standard", "Standard labels", "Cut and pack date on every "
     "wrap.", "per_lb", 0.0, 1, "list"),
    ("labeling", "custom", "Custom labels", "Your name on every wrap, for "
     "the shared freezer.", "per_lb", 0.0, 0, "list"),
]

#: Options that only make sense for certain cuts. Ground beef is sold in
#: packs, so the pack size only applies to cuts tagged "ground".
PACKING_APPLIES_TO = {
    ("ground_pack", "lb1"): '["ground"]',
    ("ground_pack", "lb2"): '["ground"]',
    ("ground_pack", "lb5"): '["ground"]',
    ("ground_pack", "lb10"): '["ground"]',
}

TERMS_BODY = """## Ordering

These terms cover every order placed through this shop. By checking the box
at checkout you accept the version linked on that order, and the version
number is stored with your receipt.

## Eligibility and household limits

One cow share per household per drop, unless we say otherwise in writing.
Shares and limited drops exist so neighbors can buy good beef affordably,
not so anyone can corner a drop.

## Fair play

These clauses exist to keep the line fair for everyone:

- Do not split an order to dodge the order minimum or the delivery threshold.
- Do not buy shares or limited drops for resale or redistribution.
- Do not create duplicate accounts to reset subscription history or
  stacking limits.
- Do not subscribe and cancel in cycles to farm the subscriber discount.
- Do not hoard stock across multiple simultaneous orders when we are low.
- Pick up your order in your window. Repeated no-shows lose pickup
  privileges.
- Do not misrepresent our beef: what we sell is what we raise, and we will
  not tolerate claims we did not make.

We read these plainly and enforce them with a warning first wherever we can.

## Subscriptions

A subscription is meat you asked for, on a cadence you chose, at a price
shown before you confirm. You can skip, pause, change cadence, or cancel
from your manage link at any time, without calling anyone. Cancellation
takes effect at the end of the paid period.

## Payment

Cards are charged when the order is placed. Share deposits reserve your
portion of a drop and are credited against the balance.

## Delivery and pickup

We deliver on Wednesdays and Saturdays to Shelby, Henry, Spencer, Nelson,
and Jefferson counties. Wednesday orders close Tuesday 11:59pm; Saturday
orders close Friday 11:59pm. Beef arrives cold-chained at or below 41
degrees F and goes straight into your fridge or freezer. Once it is in your
hands, storage and handling are yours.

## Food safety

Our beef is processed at a USDA inspected facility and carries the
inspection mark, the safe handling statement, and a use-by or freeze-by date.
Follow it. Raw beef is raw beef.

## Refunds

If an order is wrong or lost in our care, we replace it or refund it. If a
drop is cancelled, deposits are refunded in full. Otherwise beef is
perishable: once it leaves our cooler in good order, it is yours.

## Kentucky

These terms run under Kentucky law. Sales tax: packaged raw beef for home
consumption is exempt from Kentucky sales tax, and your receipt shows no
sales tax line for that reason.

## Changes

We version these terms. When they change, the new version governs new
orders and the old version stays attached to old ones.
"""

SOCIAL_LINKS = [
    ("beef", "Runchero on Facebook", "https://www.facebook.com/runchero", "facebook",
     "Drop announcements, first pick on shares.", "chat", 1),
]


# --------------------------------------------------------------------------
# co-op stores
# --------------------------------------------------------------------------

STORES = [
    ("beef", "Runchero Beef", "Locally grown beef, cut for your table.",
     "Beef raised in Shelby County and cut to order. Priced about 20% under "
     "the published grocery average.", "cow", "meat", 1),
    ("fermentation", "Fermentation Station",
     "Small-batch fermented foods from the garden.",
     "Sauerkraut, kimchi, kombucha, and pickles fermented in small batches "
     "from garden and farm produce. Live cultures, real salt, time.", "jar", "grass", 2),
    ("freeze-dried", "Runchero Freeze-Dried",
     "Farm-grown freeze-dried foods and ready meals.",
     "Farm-grown freeze-dried vegetables by the pound and pre-portioned meals. "
     "Meals are designed for a 20+ year shelf life when sealed and stored "
     "as directed; just add hot water.", "download", "sky", 3),
]

FERMENTED_PRODUCTS = [
    # (slug, name, kind, unit, price, compare_at, serving, stock, blurb, image)
    ("sauerkraut", "Classic Sauerkraut", "item", "jar", 12.0, 0,
     "16 oz jar", 24,
     "Cabbage and sea salt fermented four weeks in a salt brine. Live "
     "lactobacillus cultures plus vitamin C and fiber: sauerkraut's benefit "
     "is gut digestion and immune support from a vegetable lacto-ferment — "
     "different from kombucha, which is a fermented tea.",
     "https://placehold.co/400x400/e9e2d4/2f3140?text=Sauerkraut"),
    ("kimchi", "Napa Cabbage Kimchi", "item", "jar", 14.0, 0,
     "16 oz jar", 18,
     "Napa cabbage, gochugaru, garlic, ginger and fish sauce. Spicy and "
     "alive with lactic-acid bacteria and vitamins A, B and C from the "
     "cabbage and chili.",
     "https://placehold.co/400x400/e9e2d4/2f3140?text=Kimchi"),
    ("kombucha-classic", "Kombucha, Classic", "item", "bottle", 6.0, 0,
     "16 oz bottle", 30,
     "Black tea and cane sugar fermented 14 days with a SCOBY. Kombucha's "
     "benefit comes from fermented-tea acids and B vitamins — a tea-culture "
     "ferment, not the salt-brine vegetable ferment of sauerkraut or "
     "mustard.",
     "https://placehold.co/400x400/e9e2d4/2f3140?text=Kombucha"),
    ("kombucha-ginger", "Kombucha, Ginger", "item", "bottle", 6.5, 0,
     "16 oz bottle", 30,
     "Classic kombucha secondary-fermented with fresh ginger. The same "
     "fermented-tea probiotics and B vitamins, with ginger's zing.",
     "https://placehold.co/400x400/e9e2d4/2f3140?text=Kombucha+Ginger"),
    ("fermented-pickles", "Fermented Dill Pickles", "item", "jar", 11.0, 0,
     "quart jar", 12,
     "Kirby cucumbers, dill, garlic, salt brine — no vinegar. "
     "Lacto-fermented pickles stay crisp while adding gut-friendly "
     "lactobacillus cultures.",
     "https://placehold.co/400x400/e9e2d4/2f3140?text=Pickles"),
    ("fermented-mustard", "Fermented Mustard", "item", "jar", 10.0, 0,
     "8 oz jar", 20,
     "Mustard seed fermented with salt and time. Fermentation mellows the "
     "heat and creates live cultures — a condiment with probiotic benefits, "
     "unlike vinegar mustards. Different benefits than kombucha: this is a "
     "salt-brined seed ferment.",
     "https://placehold.co/400x400/e9e2d4/2f3140?text=Mustard"),
    ("fermented-hot-sauce", "Fermented Hot Sauce", "item", "bottle", 9.0, 0,
     "5 oz bottle", 24,
     "Fresno and habanero peppers fermented 3 weeks. Fermentation tames the "
     "burn and adds live cultures; bright heat with gut benefits.",
     "https://placehold.co/400x400/e9e2d4/2f3140?text=Hot+Sauce"),
    ("apple-cider-vinegar", "Raw Apple Cider Vinegar", "item", "bottle", 8.0,
     0, "16 oz bottle", 24,
     "Unfiltered, with the mother. Raw ACV carries acetic acid and trace "
     "probiotics from apple fermentation.",
     "https://placehold.co/400x400/e9e2d4/2f3140?text=Apple+Cider+Vinegar"),
    ("miso-paste", "Miso Paste", "item", "jar", 13.0, 0,
     "12 oz jar", 15,
     "Soybean and rice koji aged 6 months. Miso fermentation uses koji mold "
     "to break down soy into digestible, savory umami — a koji ferment, "
     "distinct from lacto-brine ferments.",
     "https://placehold.co/400x400/e9e2d4/2f3140?text=Miso"),
    ("tempeh", "Tempeh", "item", "pack", 9.0, 0,
     "8 oz block", 18,
     "Cultured soybean cake. Rhizopus fermentation binds whole soybeans "
     "into a firm, digestible cake with complete plant protein.",
     "https://placehold.co/400x400/e9e2d4/2f3140?text=Tempeh"),
]

EVENTS = [
    ("Sauerkraut Workshop",
     "Hands-on lacto-fermentation: slice, salt, and pack your own jar of "
     "sauerkraut to take home. All jars, weights and cabbage provided.",
     "2026-11-14", "10:00", "12:00",
     "The Crea, 601 Main St, Shelbyville, KY 40065", 12),
    ("Kombucha Brewing 101",
     "Start your own continuous brew: SCOBY care, sweet tea, secondary "
     "fermentation and bottling. Take a SCOBY starter home.",
     "2026-11-21", "14:00", "16:00",
     "The Crea, 601 Main St, Shelbyville, KY 40065", 12),
    ("Fermented Mustard & Hot Sauce",
     "Grind mustard seed and ferment peppers. Leave with a jar of mustard "
     "and a bottle of hot sauce, plus the recipes.",
     "2026-12-05", "10:00", "12:00",
     "The Crea, 601 Main St, Shelbyville, KY 40065", 12),
    ("Canning the Harvest",
     "Water-bath canning for garden surplus: tomatoes, pickles and jam. "
     "Jars, lids and produce provided.",
     "2026-12-12", "09:00", "12:00",
     "The Crea, 601 Main St, Shelbyville, KY 40065", 10),
    ("Winter Fermentation Circle",
     "Share ferments, trade starters and plan spring plantings. Bring a jar "
     "of something you made; coffee and tea on the house.",
     "2027-01-10", "14:00", "16:00",
     "The Crea, 601 Main St, Shelbyville, KY 40065", 20),
]

FREEZE_DRIED_PRODUCTS = [
    # veggies by the lb
    ("fd-corn", "Freeze-Dried Sweet Corn", "veg", "lb", 23.99, 25.69, "1 lb bag; compare package weights",
     40, "Farm-grown sweet corn, freeze-dried. Rehydrates in 5 minutes."),
    ("fd-peas", "Freeze-Dried Green Peas", "veg", "lb", 24.99, 28.48, "1 lb bag; compare package weights",
     40, "Sweet green peas, freeze-dried. Crunchy snack or soup add-in."),
    ("fd-strawberries", "Freeze-Dried Strawberries", "veg", "lb", 29.99, 26.00, "1 lb bag; compare package weights",
     25, "Whole strawberries, sliced. Intense flavor, no sugar added."),
    ("fd-apples", "Freeze-Dried Apples", "veg", "lb", 34.99, 56.25, "1 lb bag; compare package weights",
     30, "Cinnamon-dusted apple slices. Crisp and light."),
    ("fd-mushrooms", "Freeze-Dried Mushrooms", "veg", "lb", 79.99, 86.71, "1 lb bag; compare package weights",
     20, "Mixed mushrooms, sliced. Earthy, rehydrates for soups and sauces."),
    ("fd-spinach", "Freeze-Dried Spinach", "veg", "lb", 49.99, 74.19, "1 lb bag; compare package weights",
     20, "Farm-grown spinach, freeze-dried. Stir into anything."),
    ("fd-bell-peppers", "Freeze-Dried Bell Peppers", "veg", "lb", 49.99, 51.74, "1 lb bag; compare package weights",
     25, "Mixed color bell peppers, diced. Sweet and bright."),
    ("fd-green-beans", "Freeze-Dried Green Beans", "veg", "lb", 39.99, 43.94, "1 lb bag; compare package weights",
      30, "Farm-grown green beans, freeze-dried. Snackable or ready for soups and sides."),
    ("fd-broccoli", "Freeze-Dried Broccoli Florets", "veg", "lb", 59.99, 77.17, "1 lb bag; compare package weights",
      24, "Farm-grown broccoli florets, no stems, freeze-dried for soups and trail meals."),
    ("fd-cauliflower", "Freeze-Dried Cauliflower", "veg", "lb", 65.99, 94.14, "1 lb bag; compare package weights",
      24, "Farm-grown cauliflower florets and stems, ready for soups, curries, and casseroles."),
    # hiker meals
    ("fd-curry", "Homemade Curry Meal", "meal", "pouch", 12.49, 12.49, "one pre-portioned meal pouch; add hot water",
     200, "Farm-grown vegetables in a coconut curry sauce over rice. Just add hot water."),
    ("fd-chili", "Three-Bean Chili", "meal", "pouch", 11.99, 12.49, "one pre-portioned meal pouch; add hot water",
     200, "Kidney, black, and pinto beans with tomatoes and spice."),
    ("fd-beef-stew", "Beef Stew", "meal", "pouch", 12.99, 12.49, "one pre-portioned meal pouch; add hot water",
     200, "Beef, potatoes, carrots, and gravy. Hearty trail meal."),
    ("fd-pasta-primavera", "Pasta Primavera", "meal", "pouch", 11.99, 12.49, "one pre-portioned meal pouch; add hot water",
     200, "Pasta with garden vegetables in a light herb sauce."),
    ("fd-pad-thai", "Pad Thai", "meal", "pouch", 12.99, 12.99, "one pre-portioned meal pouch; add hot water",
     200, "Rice noodles with peanuts, lime, and vegetables."),
    ("fd-risotto", "Mushroom Risotto", "meal", "pouch", 12.49, 12.49, "one pre-portioned meal pouch; add hot water",
     200, "Arborio rice with mushrooms and parmesan."),
    ("fd-shepherds-pie", "Shepherd's Pie", "meal", "pouch", 13.49, 12.49, "one pre-portioned meal pouch; add hot water",
     200, "Ground beef, vegetables, and mashed potato topping."),
    ("fd-enchiladas", "Vegetable Enchiladas", "meal", "pouch", 11.99, 12.49, "one pre-portioned meal pouch; add hot water",
     200, "Corn tortillas with beans, peppers, and enchilada sauce."),
    ("fd-stroganoff", "Beef Stroganoff", "meal", "pouch", 12.99, 12.49, "one pre-portioned meal pouch; add hot water",
     200, "Beef and noodles in a creamy mushroom sauce."),
    ("fd-mac-cheese", "Mac and Cheese", "meal", "pouch", 10.99, 12.49, "one pre-portioned meal pouch; add hot water",
     200, "Elbow pasta in a sharp cheddar sauce."),
    ("fd-oatmeal", "Apple Cinnamon Oatmeal", "meal", "pouch", 8.99, 10.99, "one pre-portioned breakfast pouch; add hot water",
     300, "Rolled oats with dried apple and cinnamon. Breakfast on the trail."),
    ("fd-rice-pudding", "Rice Pudding", "meal", "pouch", 8.99, 10.99, "one pre-portioned dessert pouch; add hot water",
     300, "Creamy rice pudding with raisins. Dessert or breakfast."),
    # huge lots
    ("fd-meal-lot-100", "Hiker Meal Lot (100 pouches)", "meal", "lot", 1099.0, 1249.0, "100 pre-portioned meal pouches",
     5, "Mixed case of 100 freeze-dried meals. Best value for expeditions."),
    ("fd-meal-lot-50", "Hiker Meal Lot (50 pouches)", "meal", "lot", 574.50, 624.50, "50 pre-portioned meal pouches",
     8, "Mixed case of 50 freeze-dried meals."),
]

def _seed_stores(conn) -> None:
    for slug, name, tagline, desc, icon, accent, order in STORES:
        conn.execute(
            "INSERT INTO stores(slug, name, tagline, description, icon, accent, "
            "sort_order, active) VALUES(?, ?, ?, ?, ?, ?, ?, 1) "
            "ON CONFLICT(slug) DO UPDATE SET name = excluded.name, "
            "tagline = excluded.tagline, description = excluded.description, "
            "icon = excluded.icon, accent = excluded.accent, "
            "sort_order = excluded.sort_order",
            (slug, name, tagline, desc, icon, accent, order))


def _apply_store_icon(conn, store_slug: str, slug: str, icon: str) -> None:
    """Keep seeded icons current and drop old placeholder images.

    Admin uploads are preserved: only the placehold.co stand-ins are cleared.
    """
    conn.execute("UPDATE products SET icon = ? WHERE store_slug = ? AND slug = ?",
                 (icon, store_slug, slug))
    conn.execute(
        "UPDATE products SET image = '' WHERE store_slug = ? AND slug = ? "
        "AND image LIKE 'https://placehold.co/%'", (store_slug, slug))
    conn.commit()


def _seed_products(conn) -> int:
    # Premade CC0 pixel-art icons (tstamborski/pixelart-icons) chosen per item.
    icon_map = {
        # Fermentation Station
        "sauerkraut": "onion", "kimchi": "carrot",
        "kombucha-classic": "coffee", "kombucha-ginger": "lemon",
        "fermented-pickles": "potion-green", "fermented-mustard": "orange",
        "fermented-hot-sauce": "potion-red", "apple-cider-vinegar": "apple",
        "miso-paste": "coffee-alt", "tempeh": "egg-fried",
        # Freeze-Dried produce
        "fd-corn": "lemon", "fd-peas": "potion-green",
        "fd-strawberries": "cherries", "fd-apples": "apple-alt",
        "fd-mushrooms": "umbrella", "fd-spinach": "potion-green",
        "fd-bell-peppers": "orange", "fd-green-beans": "potion-green",
        "fd-broccoli": "tree", "fd-cauliflower": "flower",
        # Freeze-Dried ready meals
        "fd-curry": "carrot", "fd-chili": "potion-red",
        "fd-beef-stew": "salami", "fd-pasta-primavera": "onion",
        "fd-pad-thai": "lemon", "fd-risotto": "umbrella",
        "fd-shepherds-pie": "burger", "fd-enchiladas": "orange",
        "fd-stroganoff": "salami", "fd-mac-cheese": "egg-fried",
        "fd-oatmeal": "apple", "fd-rice-pudding": "cherries",
        # Bulk lots
        "fd-meal-lot-50": "box", "fd-meal-lot-100": "box",
    }
    comparisons = {
        "fd-corn": ("North Bay Trading", "8.5 oz bag: $13.65; $25.69/lb equivalent",
                    "https://www.northbaytrading.com/freeze-dried-super-sweet-corn"),
        "fd-peas": ("North Bay Trading", "4.5 oz bag: $8.01; $28.48/lb equivalent",
                    "https://www.northbaytrading.com/freeze-dried-peas"),
        "fd-strawberries": ("Vancouver Freeze Dry", "1 lb bag listed at $26.00 USD",
                            "https://vfdfoodsupply.com/en-us/products/freeze-dried-diced-strawberries-1"),
        "fd-apples": ("North Bay Trading", "1.2 lb bag for $67.50; $56.25/lb equivalent",
                      "https://www.northbaytrading.com/freeze-dried-apples"),
        "fd-spinach": ("North Bay Trading", "1 lb bag sale listing at $74.19",
                       "https://www.northbaytrading.com/freeze-dried-spinach"),
        "fd-green-beans": ("North Bay Trading", "1 lb bag listed at $43.94",
                           "https://www.northbaytrading.com/freeze-dried-green-beans"),
        "fd-mushrooms": ("North Bay Trading", "1 lb bag listed at $86.71",
                         "https://www.northbaytrading.com/freeze-dried-mushrooms"),
        "fd-broccoli": ("North Bay Trading", "1.25 lb bag sale listing at $96.46; $77.17/lb equivalent",
                        "https://www.northbaytrading.com/freeze-dried-broccoli-florets"),
        "fd-cauliflower": ("North Bay Trading", "14 oz bag listed at $82.37; $94.14/lb equivalent",
                           "https://www.northbaytrading.com/freeze-dried-cauliflower-florets"),
        "fd-bell-peppers": ("North Bay Trading", "16 oz bag listed at $51.74",
                            "https://www.northbaytrading.com/freeze-dried-green-bell-peppers"),
    }
    meal_url = "https://mountainhouse.com/collections/pouches"
    order = 0
    for item in FERMENTED_PRODUCTS:
        (slug, name, kind, unit, price, compare, serving, stock,
         blurb, _image) = item
        order += 1
        icon = icon_map.get(slug, "onion")
        pid = products.create(
            conn, store_slug="fermentation", slug=slug, name=name,
            kind=kind, unit=unit, unit_lbs=0.0, price=price,
            compare_at=compare, image="", icon=icon, blurb=blurb,
            serving=serving, stock=stock, tags="fermented",
            featured=0, active=True, sort_order=order)
        _apply_store_icon(conn, "fermentation", slug, icon)
        # Every item carries the full size ladder; larger pails cost less
        # per unit.
        variants.seed_standard_variants(conn, pid)

    order = 0
    for (slug, name, kind, unit, price, compare, serving, stock, blurb) in FREEZE_DRIED_PRODUCTS:
        order += 1
        icon = icon_map.get(slug, "box")
        brand, size, url = comparisons.get(
            slug, (("Mountain House" if kind == "meal" else ""),
                   ("per pouch; comparator package serving counts vary" if kind == "meal" else ""),
                   (meal_url if kind == "meal" else "")))
        if slug == "fd-meal-lot-100":
            size = "100 pouches × $12.49 each; Mountain House comparator"
        elif slug == "fd-meal-lot-50":
            size = "50 pouches × $12.49 each; Mountain House comparator"
        pid = products.create(
            conn, store_slug="freeze-dried", slug=slug, name=name,
            kind=kind, unit=unit,
            unit_lbs=1.0 if unit == "lb" else 0.0, price=price,
            compare_at=compare, image="", icon=icon, blurb=blurb,
            serving=serving, stock=stock, tags="freeze-dried",
            featured=0, active=True, sort_order=order)
        _apply_store_icon(conn, "freeze-dried", slug, icon)
        if unit == "lot":
            # A case lot is already the bulk size; give it a single option.
            conn.execute("DELETE FROM product_variants WHERE product_id = ?",
                         (pid,))
            lot_label = ("100-pouch lot" if slug.endswith("100")
                         else "50-pouch lot")
            variants.create(conn, pid, size_label=lot_label, unit="each",
                            unit_lbs=0, price=price, stock=stock,
                            sort_order=1, active=True)
        else:
            variants.seed_standard_variants(conn, pid)
    return int(conn.execute("SELECT COUNT(*) FROM products WHERE active = 1").fetchone()[0])


def _seed_events(conn) -> None:
    order = 0
    for (title, description, event_date, start_time, end_time,
         location, capacity) in EVENTS:
        order += 1
        conn.execute(
            "INSERT INTO events(title, description, event_date, start_time, "
            "end_time, location, capacity, active, sort_order) "
            "VALUES(?, ?, ?, ?, ?, ?, ?, 1, ?) "
            "ON CONFLICT(title) DO NOTHING",
            (title, description, event_date, start_time, end_time,
             location, capacity, order))

# --------------------------------------------------------------------------
# seeding
# --------------------------------------------------------------------------

def seed(conn: db.sqlite3.Connection) -> dict[str, Any]:
    report: dict[str, Any] = {}

    _seed_stores(conn)
    report["products"] = _seed_products(conn)
    report["stores"] = int(conn.execute(
        "SELECT COUNT(*) FROM stores WHERE active = 1").fetchone()[0])
    _seed_primals(conn)
    _seed_sections(conn)
    report["cuts"] = _seed_cuts(conn)
    report["packages"] = _seed_packages(conn)
    report["shares"] = _seed_shares(conn)
    report["campaigns"] = _seed_campaigns(conn)
    _seed_packing(conn)
    _seed_rules(conn)
    report["market"] = _seed_market(conn)
    report["slots"] = fulfillment.ensure_slots(conn)
    _seed_terms(conn)
    _seed_social(conn)
    _seed_content(conn)
    _seed_events(conn)
    _seed_admin(conn, report)
    conn.commit()
    return report


def _seed_primals(conn) -> None:
    for slug, name, icon, accent, blurb, order in PRIMALS:
        conn.execute(
            "INSERT INTO primals(slug, name, icon, accent, blurb, sort_order) "
            "VALUES(?, ?, ?, ?, ?, ?) "
            "ON CONFLICT(slug) DO UPDATE SET name = excluded.name, "
            "icon = excluded.icon, accent = excluded.accent, "
            "blurb = excluded.blurb, sort_order = excluded.sort_order",
            (slug, name, icon, accent, blurb, order))


def _seed_sections(conn) -> None:
    for slug, name, order in SECTIONS:
        conn.execute(
            "INSERT INTO sections(slug, name, sort_order) VALUES(?, ?, ?) "
            "ON CONFLICT(slug) DO UPDATE SET name = excluded.name",
            (slug, name, order))


def _seed_cuts(conn) -> int:
    primal_ids = {row["slug"]: row["id"]
                  for row in conn.execute("SELECT id, slug FROM primals")}
    section_ids = {row["slug"]: row["id"]
                   for row in conn.execute("SELECT id, slug FROM sections")}
    order = 0
    for (slug, name, primal, section, series, fallback, unit, unit_lbs,
         tags, serving, blurb, icon, featured) in CUTS:
        order += 1
        local = fallback
        if series:
            row = market.latest(conn, series)
            if row is not None:
                local = float(row["value"])
        ours = pricing.round_to_x9(local * 0.80)
        per_lb = ours
        # Every cut gets a sprite of its own where one exists.
        icon = CUT_ICONS.get(slug, icon)
        conn.execute(
            "INSERT INTO cuts(slug, name, primal_id, section_id, local_price, "
            "runchero_price, unit, unit_lbs, price_per_lb, "
            "market_series_key, tags, serving, blurb, stock_lbs, icon, "
            "featured, sort_order) "
            "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
            "ON CONFLICT(slug) DO UPDATE SET "
            "name = excluded.name, primal_id = excluded.primal_id, "
            "section_id = excluded.section_id, "
            "local_price = excluded.local_price, "
            "runchero_price = excluded.runchero_price, "
            "price_per_lb = excluded.price_per_lb, unit = excluded.unit, "
            "unit_lbs = excluded.unit_lbs, market_series_key = "
            "excluded.market_series_key, tags = excluded.tags, "
            "serving = excluded.serving, blurb = excluded.blurb, "
            "icon = excluded.icon, featured = excluded.featured, "
            "sort_order = excluded.sort_order",
            (slug, name, primal_ids[primal], section_ids[section], local,
             ours, unit, unit_lbs, per_lb, series, tags, serving, blurb,
             _stock_lbs(slug), icon, featured, order))
    return len(CUTS)


def _stock_lbs(slug: str) -> float:
    premium = ("filet", "porterhouse", "tenderloin", "ribeye-boneless",
               "hanger", "picanha")
    if any(key in slug for key in premium):
        return 18.0
    if "ground" in slug:
        return 240.0
    if "family-pack" in slug or "bulk" in slug:
        return 160.0
    if slug in ("stew-meat", "oxtail", "beef-cheek"):
        return 30.0
    return 60.0


def _seed_packages(conn) -> int:
    cut_ids = {row["slug"]: row["id"]
               for row in conn.execute("SELECT id, slug FROM cuts")}
    cut_prices = {row["slug"]: float(row["runchero_price"])
                  for row in conn.execute("SELECT slug, runchero_price "
                                          "FROM cuts")}
    for index, package in enumerate(PACKAGES):
        subtotal = 0.0
        total_lbs = 0.0
        for slug, lbs in package["items"]:
            subtotal += cut_prices.get(slug, 0.0) * lbs
            total_lbs += lbs
        price = pricing.round_to_x9(subtotal * 0.92)
        compare = round(subtotal, 2)
        conn.execute(
            "INSERT INTO packages(slug, name, blurb, badge, price, "
            "compare_at, total_lbs, icon, featured, deal_rank, sort_order, "
            "active) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1) "
            "ON CONFLICT(slug) DO UPDATE SET name = excluded.name, "
            "blurb = excluded.blurb, badge = excluded.badge, "
            "price = excluded.price, compare_at = excluded.compare_at, "
            "total_lbs = excluded.total_lbs, icon = excluded.icon, "
            "featured = excluded.featured, deal_rank = excluded.deal_rank",
            (package["slug"], package["name"], package["blurb"],
             package["badge"], price, compare, round(total_lbs, 1),
             package["icon"], package["featured"], package["deal_rank"],
             index))
        row = conn.execute("SELECT id FROM packages WHERE slug = ?",
                           (package["slug"],)).fetchone()
        package_id = row["id"]
        conn.execute("DELETE FROM package_items WHERE package_id = ?",
                     (package_id,))
        for slug, lbs in package["items"]:
            conn.execute(
                "INSERT INTO package_items(package_id, cut_id, qty, note) "
                "VALUES(?, ?, ?, '')",
                (package_id, cut_ids[slug], lbs))
    return len(PACKAGES)


SHARE_ICONS = {
    "eighth": "burger",
    "quarter": "salami",
    "half": "hotdog",
    "whole-drop": "crate",
}


def _seed_shares(conn) -> int:
    for (tier, name, hanging, takehome, price, deposit, per_lb, limit,
         blurb, order) in SHARES:
        slug = f"share-{tier}"
        icon = SHARE_ICONS.get(tier, "salami")
        conn.execute(
            "INSERT INTO shares(slug, tier, name, hanging_lbs, takehome_lbs, "
            "price, deposit, price_per_lb, blurb, household_limit, icon, "
            "sort_order, active) "
            "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1) "
            "ON CONFLICT(slug) DO UPDATE SET name = excluded.name, "
            "hanging_lbs = excluded.hanging_lbs, "
            "takehome_lbs = excluded.takehome_lbs, price = excluded.price, "
            "deposit = excluded.deposit, price_per_lb = excluded.price_per_lb,"
            " blurb = excluded.blurb, household_limit = "
            "excluded.household_limit, icon = excluded.icon, "
            "sort_order = excluded.sort_order",
            (slug, tier, name, hanging, takehome, price, deposit, per_lb,
             blurb, limit, icon, order))
    return len(SHARES)


def _seed_campaigns(conn) -> int:
    """Open one whole cow campaign so the drop flow has something to show."""
    from ..services import campaigns as campaigns_service
    drops = campaigns_service.next_drop_dates(4)
    rows = [
        ("winter-cow-drop", "Winter Cow Drop", 4, 3960, 630, "quarter",
         drops[0] if drops else "",
         "Four households take a quarter each. One butcher day, one cut "
         "sheet, and every share wrapped the way that household asked."),
        ("spring-cow-drop", "Spring Cow Drop", 4, 3960, 630, "quarter",
         drops[1] if len(drops) > 1 else "",
         "Grass fed and ready for the grilling season. Four households, "
         "four quarters, one drop."),
    ]
    for slug, name, target, total_lbs, price, tier, drop_date, blurb in rows:
        conn.execute(
            "INSERT INTO share_campaigns(slug, name, tier, drop_date, "
            "total_lbs, price_per_household, household_target, share_tier, "
            "blurb, status) "
            "VALUES(?, ?, 'whole', ?, ?, ?, ?, ?, ?, 'open') "
            "ON CONFLICT(slug) DO UPDATE SET name = excluded.name, "
            "drop_date = excluded.drop_date, total_lbs = excluded.total_lbs, "
            "price_per_household = excluded.price_per_household, "
            "household_target = excluded.household_target, "
            "share_tier = excluded.share_tier, blurb = excluded.blurb",
            (slug, name, drop_date, total_lbs, price, target, tier, blurb))
    return len(rows)


def _seed_packing(conn) -> None:
    for code, label, blurb, scope, order in PACKING_GROUPS:
        conn.execute(
            "INSERT INTO packing_groups(code, label, blurb, scope, sort_order)"
            " VALUES(?, ?, ?, ?, ?) "
            "ON CONFLICT(code) DO UPDATE SET label = excluded.label, "
            "blurb = excluded.blurb, scope = excluded.scope",
            (code, label, blurb, scope, order))
    for group, code, label, description, mode, amount, default, icon \
            in PACKING_OPTIONS:
        conn.execute(
            "INSERT INTO packing_options(group_code, code, label, description,"
            " price_mode, amount, is_default, icon, applies_to, sort_order) "
            "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, "
            "(SELECT COALESCE(MAX(sort_order), 0) + 1 "
            "FROM packing_options WHERE group_code = ?)) "
            "ON CONFLICT(group_code, code) DO UPDATE SET "
            "label = excluded.label, description = excluded.description, "
            "price_mode = excluded.price_mode, amount = excluded.amount, "
            "is_default = excluded.is_default, applies_to = excluded.applies_to",
            (group, code, label, description, mode, amount, default, icon,
             PACKING_APPLIES_TO.get((group, code), "all"), group))


def _seed_rules(conn) -> None:
    """The owner's one promise: 20 percent under the local shelf price.

    Seeded once. Re-seeding must not stack up duplicate global rules.
    """
    existing = db.one(conn, "SELECT id FROM price_rules "
                            "WHERE scope_type = 'global' AND scope_value = ''")
    if existing is None:
        conn.execute(
            "INSERT INTO price_rules(scope_type, scope_value, discount_pct, "
            "label, active, priority) VALUES('global', '', 20, "
            "'20 percent under the local shelf price', 1, 0)")


def _seed_market(conn) -> dict[str, int]:
    """Pull live feeds. Offline, the fallbacks in the cut table stand in."""
    results = market.refresh(conn)
    return {result.provider: (len(result.observations) if result.ok
                              else -1) for result in results}


def _seed_terms(conn) -> None:
    conn.execute(
        "INSERT INTO terms_versions(version, title, body, effective) "
        "VALUES('1.0', 'Terms of Service', ?, date('now')) "
        "ON CONFLICT(version) DO NOTHING", (TERMS_BODY,))


def _seed_social(conn) -> None:
    """Keep the legitimate beef link; business-specific links are configured per store."""
    conn.execute("DELETE FROM social_links WHERE url LIKE '%runchero.example/%'")
    for store_slug, label, url, kind, blurb, icon, order in SOCIAL_LINKS:
        conn.execute(
            "DELETE FROM social_links WHERE store_slug = ? AND label = ? AND url = ?",
            (store_slug, label, url))
        conn.execute(
            "INSERT INTO social_links(store_slug, label, url, kind, blurb, icon, "
            "sort_order, active) VALUES(?, ?, ?, ?, ?, ?, ?, 1)",
            (store_slug, label, url, kind, blurb, icon, order))


def _seed_content(conn) -> None:
    from ..web import shop_content
    shop_content(conn)


def _seed_admin(conn, report) -> None:
    from ..services.auth import ensure_admin
    generated = ensure_admin(conn)
    if generated:
        report["admin_password"] = generated
