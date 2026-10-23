"""Community calculators: the sums a small farm actually needs.

Every entry is a single clean equation, so each one gets a quick calculator
on the formulas page. Results are convenience only - double-check before you
mix feed, pour concrete or calibrate a sprayer.
"""

from __future__ import annotations

FORMULAS: list[dict] = [
    # ------------------------------------------------------------------ livestock
    {
        "slug": "feed-ration-calculator",
        "name": "Daily feed ration",
        "topic": "livestock",
        "expression": "F = W x R / 100",
        "symbols": "F = feed per day (kg); W = live weight (kg); R = ration (% of bodyweight)",
        "units": "kg per day",
        "how": "Multiply the animal's liveweight by the ration percentage, then "
               "divide by 100. A 600 kg cow on a 2.5% ration needs 15 kg of feed "
               "a day. Split between forage and concentrate as the ration sheet "
               "says.",
        "example": "600 kg cow x 2.5% / 100 = 15 kg feed per day.",
        "tags": "feed,ration,livestock,cattle,sheep,pigs",
    },
    {
        "slug": "liveweight-from-heart-girth",
        "name": "Liveweight from heart girth",
        "topic": "livestock",
        "expression": "W = G x G x L / 300",
        "symbols": "W = liveweight (kg); G = heart girth (cm); L = body length (cm)",
        "units": "kg",
        "how": "Measure around the chest just behind the front legs (heart girth) "
               "and from the point of shoulder to the pin bone (body length), both "
               "in centimetres. Square the girth, multiply by length, divide by "
               "300. Best for cattle; less accurate for very fat or very thin "
               "stock.",
        "example": "Girth 190 cm x length 150 cm: 190 x 190 x 150 / 300 = "
                   "1,805 kg estimate.",
        "tags": "liveweight,cattle,weighing,girth",
    },
    {
        "slug": "hay-bale-weight",
        "name": "Hay bale weight",
        "topic": "livestock",
        "expression": "W = L x W x H x D",
        "symbols": "W = weight (kg); L = length (m); W = width (m); "
                   "H = height (m); D = density (kg per m3)",
        "units": "kg per bale",
        "how": "Measure the bale in metres, multiply length x width x height to "
               "get cubic metres, then multiply by density. A small square bale "
               "is about 100-150 kg/m3; a big round bale is denser, about "
               "200-250 kg/m3.",
        "example": "1.2 x 0.7 x 0.4 m x 130 kg/m3 = about 44 kg per small bale.",
        "tags": "hay,bale,weight,storage,feed",
    },
    # ------------------------------------------------------------------ agronomy
    {
        "slug": "seed-rate-calculator",
        "name": "Seed rate",
        "topic": "agronomy",
        "expression": "S = A x P / 1000",
        "symbols": "S = seed needed (kg); A = area (hectares); "
                   "P = plants per m2 x 1000 (seed rate kg/ha ÷ 1000)",
        "units": "kg of seed",
        "how": "Convert your target plants per square metre into kg per hectare "
               "(check the seed bag or the seed-rate table), then multiply by the "
               "area in hectares. This gives total kilograms of seed to buy. See "
               "also the [[seed-saving]] depot for saving your own seed.",
        "example": "2 ha at 35 plants per m2 (about 200 kg/ha): 2 x 200 = "
                   "400 kg of seed.",
        "tags": "seed,rate,drilling,sowing,crops",
    },
    {
        "slug": "sprayer-calibration",
        "name": "Sprayer output calibration",
        "topic": "agronomy",
        "expression": "O = (F x 600) / (S x W)",
        "symbols": "O = output (litres per hectare); F = flow per nozzle "
                   "(litres per minute); S = speed (km per hour); "
                   "W = nozzle spacing (metres)",
        "units": "litres per hectare",
        "how": "Catch the output from one nozzle for one minute to get flow. "
               "Measure your forward speed and the nozzle spacing on the boom. "
               "This tells you how many litres per hectare you are putting down, "
               "so you can mix the right amount of chemical in the tank.",
        "example": "1.5 L/min x 600 / (8 km/h x 0.5 m) = 225 L/ha.",
        "tags": "sprayer,calibration,spraying,chemical,agronomy",
    },
    # ------------------------------------------------------------------ workshop
    {
        "slug": "board-feet-calculator",
        "name": "Board feet of timber",
        "topic": "workshop",
        "expression": "BF = T x W x L / 12",
        "symbols": "BF = board feet; T = thickness (inches); W = width (inches); "
                   "L = length (feet)",
        "units": "board feet",
        "how": "Multiply thickness x width x length, then divide by 12. This is "
               "how sawn timber is measured and sold. A 2-inch plank 8 inches "
               "wide and 10 feet long is 13.3 board feet.",
        "example": "2 x 8 x 10 / 12 = 13.3 board feet.",
        "tags": "timber,lumber,board feet,sawmill",
    },
    {
        "slug": "fence-post-calculator",
        "name": "Fence posts needed",
        "topic": "workshop",
        "expression": "N = (D x 1000 / S) + 1",
        "symbols": "N = number of posts; D = fence length (metres); "
                   "S = post spacing (metres)",
        "units": "posts",
        "how": "Divide the fence length by the post spacing, then add one for "
               "the end post. Round up to the next whole post. Add strainer "
               "posts at corners and gates separately.",
        "example": "100 m fence at 3 m spacing: 100 / 3 + 1 = 34 posts.",
        "tags": "fence,posts,fencing,perimeter",
    },
    # ------------------------------------------------------------------ construction
    {
        "slug": "concrete-calculator",
        "name": "Concrete volume",
        "topic": "construction",
        "expression": "V = L x W x D",
        "symbols": "V = volume (cubic metres); L = length (m); W = width (m); "
                   "D = depth (m)",
        "units": "m3",
        "how": "Multiply length x width x depth in metres. Add 5-10% for waste "
               "and over-excavation. A cubic metre of concrete weighs about "
               "2.4 tonnes, so plan your delivery and your wheelbarrows.",
        "example": "A shed base 4 x 3 x 0.15 m = 1.8 m3 of concrete.",
        "tags": "concrete,volume,foundation,shed",
    },
    {
        "slug": "water-tank-volume",
        "name": "Water tank volume",
        "topic": "construction",
        "expression": "V = pi x r2 x h",
        "symbols": "V = volume (litres); r = radius (metres); h = height (m)",
        "units": "litres",
        "how": "For a round tank: area of the circle (pi x radius squared) times "
               "height, then multiply by 1000 to get litres from cubic metres. "
               "A 2-metre diameter tank 2 metres high holds about 6,283 litres.",
        "example": "r = 1 m, h = 2 m: 3.14159 x 1 x 2 = 6.28 m3 = 6,283 litres.",
        "tags": "water,tank,volume,storage,rainwater",
    },
    # ------------------------------------------------------------------ workshop / chainsaw
    {
        "slug": "chainsaw-chain-file-size",
        "name": "Chainsaw chain file size",
        "topic": "workshop",
        "expression": "Fs = P x 25.4",
        "symbols": "Fs = round file size (mm); P = chain pitch (inches)",
        "units": "mm",
        "how": "Chain pitch is stamped on the drive link or the bar. Multiply "
               "the pitch in inches by 25.4 to get the matching round file "
               "diameter in millimetres. Common: 3/8 inch pitch = 9.5 mm file; "
               "0.325 inch = 8.3 mm file; 0.404 inch = 10.3 mm file.",
        "example": "3/8 inch = 0.375 x 25.4 = 9.5 mm round file.",
        "tags": "chainsaw,chain,file,sharpening",
    },
    # ------------------------------------------------------------------ growing
    {
        "slug": "plant-spacing-calculator",
        "name": "Plants per area",
        "topic": "growing",
        "expression": "N = (L x W x 10000) / (RxC)",
        "symbols": "N = number of plants; L = row length (m); W = row width (m); "
                   "R = row spacing (m); C = in-row spacing (m)",
        "units": "plants",
        "how": "Work out the total area in square metres, then divide by the "
               "area each plant needs (row spacing x in-row spacing). This tells "
               "you how many plants to order for a plot or field.",
        "example": "20 x 10 m plot, rows 0.75 m apart, plants 0.3 m apart: "
                   "20000 / 0.225 = 88,888 plants.",
        "tags": "spacing,plants,plot,garden,crops",
    },
]


def register_formulas() -> list[dict]:
    return FORMULAS
