"""The formula shelf.

Every formula is a plain dict so the seeder can drop it straight into the
database and the formulas page can filter it by topic.

    slug, name, topic, expression, symbols, units, how, example, tags
"""

from __future__ import annotations

from .advanced import FORMULAS as ADVANCED
from .community import FORMULAS as COMMUNITY
from .core import FORMULAS as CORE
from .kitchen import FORMULAS as KITCHEN
from .land import FORMULAS as LAND
from .making import FORMULAS as MAKING
from .science import FORMULAS as SCIENCE

# Topic order drives the order of the shelves on the formulas page. It runs
# from the everyday to the specialist: the sums most people need first, the
# advanced maths and surveying shelves at the end.
TOPICS: list[dict] = [
    {"slug": "measurement", "name": "Measurement", "blurb": "Area, volume, "
     "length and the conversions in between."},
    {"slug": "kitchen", "name": "Kitchen", "blurb": "Baking, preserving, "
     "cooking and feeding the house."},
    {"slug": "maths", "name": "Maths", "blurb": "Percentages, ratios, "
     "averages and the rule of three."},
    {"slug": "money", "name": "Money", "blurb": "Pricing, margins, payback "
     "and working out whether a job is worth doing."},
    {"slug": "agronomy", "name": "Agronomy", "blurb": "Seed rates, "
     "fertiliser, spraying, irrigation and harvests."},
    {"slug": "livestock", "name": "Livestock", "blurb": "Feed, growth, "
     "breeding and the numbers behind a healthy herd."},
    {"slug": "growing", "name": "Growing", "blurb": "Spacing, sowing, "
     "watering and the vegetable plot."},
    {"slug": "workshop", "name": "Workshop", "blurb": "Torque, cutting, "
     "concrete, timber and the machines on the yard."},
    {"slug": "construction", "name": "Construction", "blurb": "Foundations, "
     "walls, insulation and drainage."},
    {"slug": "energy", "name": "Energy", "blurb": "Fuel, electricity, heat "
     "loss and solar."},
    {"slug": "physics", "name": "Physics", "blurb": "Force, power, heat and "
     "the way machines move."},
    {"slug": "chemistry", "name": "Chemistry", "blurb": "pH, concentration and "
     "mixing without surprises."},
    {"slug": "health", "name": "Health", "blurb": "Body mass, dosage and the "
     "everyday numbers of staying well."},
    {"slug": "data", "name": "Data", "blurb": "Averages, spread and what the "
     "numbers are really telling you."},
    {"slug": "geometry", "name": "Geometry", "blurb": "Shapes, perimeters, "
     "surface areas and volumes for setting out."},
    {"slug": "trigonometry", "name": "Trigonometry", "blurb": "Angles, "
     "distances, bearings and the maths of anything sloping."},
    {"slug": "advanced-maths", "name": "Advanced maths", "blurb": "Algebra, "
     "series, logs and calculus when the straight line runs out."},
    {"slug": "statistics", "name": "Statistics", "blurb": "Samples, spread, "
     "confidence and reading trial results honestly."},
    {"slug": "finance", "name": "Finance", "blurb": "Loans, annuities, "
     "depreciation and comparing investments properly."},
    {"slug": "surveying", "name": "Surveying", "blurb": "Levels, bearings, "
     "earthworks and areas from coordinates."},
    {"slug": "electrical", "name": "Electrical", "blurb": "Cable, batteries, "
     "inverters and the sums behind an off-grid supply."},
    {"slug": "meteorology", "name": "Weather", "blurb": "Rain, humidity, "
     "wind chill and growing degree days."},
]

# The fastest route into the shelf. The formulas page puts these first inside
# each topic, and the "most used" strip links straight to them.
COMMON: list[str] = [
    "area-of-a-rectangle", "volume-of-a-cylinder", "percentage-change",
    "rule-of-three", "bakers-percentage", "hydration", "seed-rate-from-target-population",
    "plants-per-hectare", "sprayer-volume-rate", "fertiliser-nitrogen-requirement",
    "irrigation-depth", "average-daily-gain", "feed-conversion-ratio",
    "stocking-rate", "dry-matter-intake", "grain-storage-mass", "hay-bales-per-hectare",
    "fuel-consumption", "kg-to-pounds", "celsius-to-fahrenheit",
    "litres-to-imperial-gallons", "acres-and-hectares", "area-of-a-circle",
    "volume-of-a-box", "mass-from-volume-and-density", "row-and-plant-spacing",
    "watering-a-bed", "safe-cooking-temperature", "brine-percentage",
    "jam-setting-point", "stock-ratio", "bolt-torque", "concrete-bags",
    "fence-post-spacing", "board-feet", "pulley-mechanics", "gear-ratio",
    "rainwater-harvesting", "solar-array-output", "ohms-law", "electrical-power",
    "heat-loss-through-walls", "drug-dose-by-weight", "gestation-and-due-date",
    "break-even", "gross-margin", "payback-period", "weighted-average",
    "standard-deviation", "pythagoras-hypotenuse",
    "feed-ration-calculator", "liveweight-from-heart-girth",
    "sprayer-calibration", "board-feet-calculator", "fence-post-calculator",
    "concrete-calculator", "water-tank-volume", "chainsaw-chain-file-size",
    "plant-spacing-calculator",
]

FORMULAS: list[dict] = [*CORE, *SCIENCE, *LAND, *MAKING, *KITCHEN, *ADVANCED, *COMMUNITY]

__all__ = ["FORMULAS", "TOPICS", "COMMON"]
