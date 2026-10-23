"""Formulas: agronomy, livestock and growing."""

from __future__ import annotations

FORMULAS: list[dict] = [
    # -------------------------------------------------------------- agronomy
    {
        "slug": "plants-per-hectare",
        "name": "Plants per hectare from spacing",
        "topic": "agronomy",
        "expression": "plants per hectare = 10,000 / (row spacing in m x "
                      "in-row spacing in m)",
        "symbols": "10,000 square metres to the hectare",
        "units": "plants/ha",
        "how": "Turn a spacing into a population, then into a seed rate. Work "
               "out what you want first, and the drill setting second.",
        "example": "Rows 30 cm apart with plants 10 cm apart in the row = "
                   "333,333 plants a hectare.",
        "tags": "spacing,population,plants,hectare,drilling",
    },
    {
        "slug": "seed-rate-from-target-population",
        "name": "Seed rate for a target plant population",
        "topic": "agronomy",
        "expression": "seed rate (kg/ha) = (target plants/ha x seed weight in g) "
                      "/ (germination x establishment) / 1,000,000",
        "symbols": "germination and establishment as decimals (0.95 and 0.90 "
                   "for example); seed weight in grams per seed",
        "units": "kg/ha",
        "how": "The proper way to buy seed. A bag says 80% germination, so you "
               "must buy 20% more seed than the target population needs, and "
               "more again for field losses.",
        "example": "Target 300,000 plants/ha, peas at 0.25 g a seed, 95% "
                   "germination, 90% establishment: (300,000 x 0.25) / "
                   "(0.95 x 0.90) / 1,000,000 = 87.7 kg/ha.",
        "tags": "seed rate,germination,population,drilling,peas",
    },
    {
        "slug": "seeds-per-metre-of-row",
        "name": "Seeds per metre of row",
        "topic": "agronomy",
        "expression": "seeds per metre = (seed rate in kg/ha x 1,000) / "
                      "(seeds per kg x row spacing in m)",
        "symbols": "seeds per kg is the label figure; row spacing in metres",
        "units": "seeds/m",
        "how": "The setting that goes on the drill. Work it out from the seed "
               "rate, then check it over a measured 10 m and count.",
        "example": "60 kg/ha of maize, 7,700 seeds/kg, rows 0.75 m apart = "
                   "104 seeds a metre.",
        "tags": "drill,seeds per metre,maize,setting",
    },
    {
        "slug": "metres-of-row-per-hectare",
        "name": "Row metres per hectare",
        "topic": "agronomy",
        "expression": "row metres per hectare = 10,000 / row spacing in m",
        "symbols": "one hectare of ground, however many times you drive over "
                   "it",
        "units": "m/ha",
        "how": "To work out how long it takes to drill a field, how much fuel "
               "you will burn, or how much fertiliser to put on through the "
               "drill.",
        "example": "Rows 25 cm apart = 40,000 m of row a hectare.",
        "tags": "rows,drilling,field,work rate",
    },
    {
        "slug": "fertiliser-nitrogen-requirement",
        "name": "Nitrogen needed for a target yield",
        "topic": "agronomy",
        "expression": "N product (kg/ha) = ((target N kg/ha - N already in the "
                      "soil and from manure) / N fraction in the product) x 100",
        "symbols": "urea is 46% N, ammonium nitrate 34.5%, farmyard manure "
                   "about 0.4% N with only a quarter available in year one",
        "units": "kg/ha",
        "how": "The calculation behind a fertiliser plan. Subtract what the "
               "soil and the manure already give you, then convert to the "
               "product you are actually buying.",
        "example": "Target 120 kg N/ha, soil and manure give 35, using urea: "
                   "(120 - 35) / 0.46 = 185 kg/ha of urea.",
        "tags": "fertiliser,nitrogen,urea,plan,manure",
    },
    {
        "slug": "lime-requirement",
        "name": "Lime requirement to raise soil pH",
        "topic": "agronomy",
        "expression": "lime (t/ha) = (buffer pH - target pH) x depth factor x "
                      "soil factor",
        "symbols": "a common field rule of thumb is 0.2 t/ha for each pH unit "
                   "per 15 cm of depth on a medium soil; a buffer (lime "
                   "requirement) test gives the figure directly",
        "units": "tonnes/ha",
        "how": "Lime is the one thing you cannot take back once it is spread, "
               "so use a buffer test rather than a pH test. See "
               "[[soil-ph-and-lime]].",
        "example": "Buffer pH 6.5, target 6.5, 20 cm deep: no lime needed. "
                   "Buffer 6.0 means about 0.4 t/ha on that soil.",
        "tags": "lime,ph,soil,buffer test,neutralise",
    },
    {
        "slug": "nitrogen-sulphur-ratio",
        "name": "Nitrogen to sulphur ratio in fertiliser",
        "topic": "agronomy",
        "expression": "for oilseed rape and cereals, aim for about 6 kg N for "
                      "every 1 kg S",
        "symbols": "most soils will release about 1 kg of sulphur for every "
                   "10 kg of nitrogen taken up by the crop",
        "units": "kg/ha",
        "how": "Oilseed rape and grass are hungry for sulphur. Too little "
               "sulphur and the crop cannot use the nitrogen you have paid "
               "for, so the response to extra N is poor.",
        "example": "For 90 kg N/ha, apply 15 kg S/ha as ammonium sulphate.",
        "tags": "sulphur,nitrogen,oilseed rape,fertiliser",
    },
    {
        "slug": "sprayer-volume-rate",
        "name": "Sprayer litres per hectare",
        "topic": "agronomy",
        "expression": "L/ha = (nozzle output in L/min x 600) / (speed in km/h x "
                      "boom width in m)",
        "symbols": "600 = 60 minutes in an hour x 1,000 m in a kilometre, "
                   "divided by 100 to change hectares to square metres",
        "units": "L/ha",
        "how": "Every sprayer book starts with this. Get the volume right and "
               "the dose per hectare is right. Measure a nozzle with a "
               "jug, and time the pass over 100 m.",
        "example": "A 2 L/min nozzle at 8 km/h on a 6 m boom: (2 x 600) / "
                   "(8 x 6) = 250 L/ha.",
        "tags": "sprayer,nozzle,volume rate,boom,herbicide",
    },
    {
        "slug": "sprayer-tank-quantity",
        "name": "Sprayer tank fill and dose",
        "topic": "agronomy",
        "expression": "tank volume (L) = area (ha) x L/ha ; "
                      "product in the tank (L or kg) = tank volume x rate per "
                      "hectare / 100",
        "symbols": "always measure the product into the tank, never guess",
        "units": "L, kg",
        "how": "Work out the fill for the area you are about to spray, then "
               "measure the product with a proper jug. Over-application is "
               "expensive, illegal and dangerous.",
        "example": "2 ha at 250 L/ha is a 500 L tank. At 2 L/ha of product "
                   "that is 10 L in the tank.",
        "tags": "sprayer,tank,dose,product,calibration",
    },
    {
        "slug": "irrigation-depth",
        "name": "Irrigation depth in millimetres",
        "topic": "agronomy",
        "expression": "depth (mm) = volume applied (m3/ha) / 10 ; "
                      "1 mm over 1 hectare = 10 m3 = 10,000 litres",
        "symbols": "mm of water is the standard unit for irrigation; 1 mm is "
                   "1 litre per square metre",
        "units": "mm, m3/ha, litres",
        "how": "The language of every irrigation schedule. 25 mm is a proper "
               "soaking for a root crop, 5 mm is just keeping the surface "
               "damp.",
        "example": "Applying 40 m3/ha is a depth of 4 mm, which is too little "
                   "to reach the roots in a loam.",
        "tags": "irrigation,mm,water,depth,schedule",
    },
    {
        "slug": "irrigation-requirement",
        "name": "Irrigation requirement (crop coefficient method)",
        "topic": "agronomy",
        "expression": "gross depth (mm) = (ET x Kc - effective rainfall) / "
                      "application efficiency",
        "symbols": "ET = evapotranspiration in mm/day (about 5-7 in summer); "
                   "Kc = crop coefficient (0.3 for seedlings, 0.6 for grass, "
                   "1.0 for full maize, 1.15 for tomatoes); efficiency 0.7-0.9 "
                   "for a sprinkler, 0.9-1.0 for drip",
        "units": "mm/day or mm/season",
        "how": "The basic scheduling method. Multiply the daily water use by "
               "the crop stage, take off the rain, and divide by how well your "
               "system actually delivers.",
        "example": "Full maize at 6 mm/day and Kc 1.0 over 10 days, no rain, "
                   "80% efficiency: (60 - 0) / 0.8 = 75 mm to apply.",
        "tags": "irrigation,evapotranspiration,kc,schedule,maize",
    },
    {
        "slug": "pump-flow-rate",
        "name": "Pump flow needed for an irrigation block",
        "topic": "agronomy",
        "expression": "flow (L/s) = (hectares x depth in mm x 10,000) / "
                      "(hours x 3,600)",
        "symbols": "10,000 L/ha/mm; 3,600 seconds in an hour",
        "units": "L/s, m3/h",
        "how": "To check that the pump and the pipes can deliver. A 1 hectare "
               "block needing 25 mm in 4 hours needs 17 L/s.",
        "example": "2 ha, 20 mm, in 6 hours: (2 x 20 x 10,000) / (6 x 3,600) "
                   "= 18.5 L/s.",
        "tags": "pump,flow,irrigation,pipe,borehole",
    },
    {
        "slug": "grain-yield-from-ears",
        "name": "Grain yield from the plant population",
        "topic": "agronomy",
        "expression": "yield (t/ha) = (plants/ha x ears per plant x grains per "
                      "ear x grain weight in g) / 1,000,000",
        "symbols": "grain weight: wheat 45 g, barley 45 g, oats 35 g, beans "
                   "1.5 g",
        "units": "t/ha",
        "how": "The way to work out what a crop is worth before you have "
               "even got the harvester in the field. Combine it with a per "
               "hectare count of plants and ears.",
        "example": "250,000 plants/ha, 1.6 ears, 60 grains, 45 g: "
                   "(250,000 x 1.6 x 60 x 45) / 1,000,000 = 108 t/ha.",
        "tags": "yield,wheat,barley,ears,estimate",
    },
    {
        "slug": "bushels-per-acre",
        "name": "Bushels per acre from a yield in pounds",
        "topic": "agronomy",
        "expression": "bushels/acre = (yield in lb/acre) / (lb per bushel)",
        "symbols": "lb per bushel: wheat 60, barley 48, maize 56, oats 32, "
                   "soybean 60, rye 56",
        "units": "bushels/acre",
        "how": "For converting the old imperial yields into today's tonnes a "
               "hectare, and for reading the old books on the shelf. A bushel "
               "is a volume, so the weight depends on the crop.",
        "example": "Wheat at 2,400 lb/acre: 2,400 / 60 = 40 bushels.",
        "tags": "bushels,acre,yield,wheat,conversion",
    },
    {
        "slug": "grain-storage-mass",
        "name": "Mass of grain in a bin",
        "topic": "agronomy",
        "expression": "mass (tonnes) = volume (m3) x bulk density (t/m3)",
        "symbols": "bulk density: wheat 0.75, barley 0.70, maize 0.72, oats "
                   "0.40, rapeseed 0.60, beans 0.75, wood chips 0.30",
        "units": "tonnes",
        "how": "To know how much grain is in the barn before you sell it, and "
               "to check a silo is big enough. Measure the heap or the bin "
               "and multiply.",
        "example": "A 6 m diameter, 4 m deep bin holds about 113 m3, which is "
                   "85 tonnes of wheat.",
        "tags": "storage,bulk density,bin,silo,tonnes",
    },
    {
        "slug": "grain-storage-space",
        "name": "Storage space for a crop",
        "topic": "agronomy",
        "expression": "volume (m3) = (tonnes / bulk density in t/m3)",
        "symbols": "add 15% for the space the grain does not fill evenly at "
                   "the sides and the top",
        "units": "m3",
        "how": "Before you harvest, work out where the crop is going to go, "
               "and whether the bin will hold it all.",
        "example": "60 tonnes of barley at 0.70 t/m3 = 86 m3, plus 15% = "
                   "99 m3 of bin space needed.",
        "tags": "storage,space,harvest,bin,barley",
    },
    {
        "slug": "grain-drying",
        "name": "Drying grain: air and heat",
        "topic": "agronomy",
        "expression": "moisture to remove (kg/ha) = (harvest moisture % - "
                      "target moisture %) x grain weight (kg/ha) / 100",
        "symbols": "a drying fan moves roughly 15-25 m3 of air per second per "
                   "kilowatt of heat; do not raise the air temperature more than "
                   "5 degrees C above the incoming air",
        "units": "kg of water, m3/s of air",
        "how": "Grain dried too fast or too hot goes cracked, and the cracks "
               "cost you in the mill. See [[storing-grain]].",
        "example": "Wheat at 22% harvested to 15% stored, 8 t/ha: "
                   "(22 - 15) x 8,000 / 100 = 560 kg of water a hectare.",
        "tags": "drying,moisture,air,fan,grain",
    },
    {
        "slug": "compost-carbon-nitrogen",
        "name": "Compost carbon to nitrogen ratio",
        "topic": "agronomy",
        "expression": "C:N ratio = kg of carbon / kg of nitrogen",
        "symbols": "aim for 25:1 to 30:1 in the heap; fresh manure is about "
                   "20:1, straw about 80:1, spent mushroom compost about 12:1",
        "units": "ratio",
        "how": "The rule that makes a heap work. Too much carbon and it sits "
               "there for a year; too little nitrogen and it goes sour and "
               "smells. See [[compost-heap]].",
        "example": "A heap of 100 kg straw at 80:1 needs about 2 kg of "
                   "nitrogen, which is 4.5 kg of urea.",
        "tags": "compost,carbon,nitrogen,heap,manure",
    },
    {
        "slug": "compost-nutrient-supply",
        "name": "Nutrients supplied by a manure or compost load",
        "topic": "agronomy",
        "expression": "available N (kg/ha) = (tonnes applied x N % x 100 x "
                      "availability factor) / 100",
        "symbols": "availability factor: 0.4 for farmyard manure in the first "
                   "year, 0.15 in the second, 0.6 for slurry injected, 0.2 for "
                   "compost",
        "units": "kg/ha",
        "how": "The part of the manure spreadsheet that matters. A load of "
               "manure looks like a big pile of nitrogen on the yard, and only "
               "a fraction of it is available to the crop this year.",
        "example": "10 t/ha of manure at 0.5% N with 40% availability: "
                   "(10 x 0.5 x 100 x 0.4) / 100 = 20 kg N/ha.",
        "tags": "manure,nitrogen,compost,availability,plan",
    },
    {
        "slug": "cover-crop-grazing-days",
        "name": "Grazing days from a cover crop",
        "topic": "agronomy",
        "expression": "grazing days = (dry matter kg/ha x grazeable fraction) / "
                      "(animals x intake per animal per day)",
        "symbols": "intake for a 500 kg cow is about 2% of body weight a day, "
                   "so 10 kg of dry matter; grazeable fraction is 0.5-0.7 for "
                   "most swards",
        "units": "days",
        "how": "Whether the cover crop is a real feed or just a cover. It "
               "depends on the dry matter, not the green weight, and on how "
               "much you leave behind.",
        "example": "4,000 kg DM/ha at 60% grazeable, 20 cows at 10 kg DM a "
                   "day: 2,400 / 200 = 12 days.",
        "tags": "cover crop,grazing,dry matter,feed,forage",
    },
    {
        "slug": "forage-dry-matter-yield",
        "name": "Forage dry matter yield",
        "topic": "agronomy",
        "expression": "DM yield (t/ha) = fresh yield (t/ha) x dry matter % / 100",
        "symbols": "grass at silage is usually 18-25% dry matter; hay is 85-88%",
        "units": "t/ha",
        "how": "Comparing a field of grass with a field of hay, and working "
               "out how much feed a field really gives. The green weight is "
               "mostly water.",
        "example": "A field giving 25 t/ha fresh at 20% DM = 5 t/ha of dry "
                   "matter, which is about 11 round bales.",
        "tags": "forage,dry matter,grass,silage,hay",
    },
    {
        "slug": "hay-bales-per-hectare",
        "name": "Bales per hectare",
        "topic": "agronomy",
        "expression": "bales/ha = (DM yield in t/ha x 1,000) / (DM per bale in "
                      "kg) x (1 - losses)",
        "symbols": "a small round bale at 85% DM holds about 220 kg of dry "
                   "matter; losses in the field are 5-15%",
        "units": "bales/ha",
        "how": "For checking whether there is enough hay for the winter, and "
               "for working out how many bales to book in.",
        "example": "5 t/ha of dry matter at 220 kg a bale with 10% loss = "
                   "20.5 bales a hectare.",
        "tags": "bales,hay,yield,stocking,winter",
    },
    {
        "slug": "germination-and-emergence",
        "name": "Germination and field emergence",
        "topic": "agronomy",
        "expression": "germination % = (seeds germinated / seeds sown) x 100 ; "
                      "field emergence % = (plants per m2 / target plants per "
                      "m2) x 100",
        "symbols": "count 100 seeds on a damp cloth for the germination test; "
                   "count plants in four 1 m2 quadrats for emergence",
        "units": "%",
        "how": "The two numbers that tell you whether the drill or the seed is "
               "at fault. A poor emergence with a good germination test "
               "means a drilling problem, not a seed problem.",
        "example": "Target 350 plants/m2 and you count 245: 70% emergence.",
        "tags": "germination,emergence,drilling,seed test,establishment",
    },

    # ------------------------------------------------------------- livestock
    {
        "slug": "average-daily-gain",
        "name": "Average daily gain",
        "topic": "livestock",
        "expression": "ADG (kg/day) = (final weight - starting weight) / days "
                      "on feed",
        "symbols": "use actual liveweight gains, not estimated ones",
        "units": "kg/day",
        "how": "The single number that tells you if a ration or a system is "
               "working. Weigh the animals, do it again in 30 days, and "
               "divide.",
        "example": "A lamb goes from 30 kg to 42 kg in 60 days = 0.2 kg/day.",
        "tags": "gain,adg,growth,weigh,performance",
    },
    {
        "slug": "feed-conversion-ratio",
        "name": "Feed conversion ratio",
        "topic": "livestock",
        "expression": "FCR = feed eaten (kg dry matter) / liveweight gain (kg)",
        "symbols": "a calf might convert at 4:1, a pig at 2.5:1, a lamb at 4:1",
        "units": "kg feed per kg gain",
        "how": "How much feed you get back for every kilo you put in. A "
               "higher number means more feed per kilo of meat, and a bigger "
               "feed bill.",
        "example": "A calf eats 8 kg of feed to gain 2 kg: FCR 4:1.",
        "tags": "fcr,feed,efficiency,ration,gain",
    },
    {
        "slug": "dry-matter-intake",
        "name": "Dry matter intake as a percentage of liveweight",
        "topic": "livestock",
        "expression": "intake (kg DM/day) = body weight (kg) x intake % / 100",
        "symbols": "2% for a mature dry cow, 2.5-3% for a growing animal, 3.5% "
                   "for a lactating cow, 2.5% for a ewe in late pregnancy",
        "units": "kg DM/day",
        "how": "To size a ration. Get this wrong in either direction and the "
               "animal is either hungry or overfed, and you will not see which "
               "from the ration sheet.",
        "example": "A 500 kg cow at 3.5% needs 17.5 kg of dry matter a day.",
        "tags": "intake,dry matter,cow,sheep,ration",
    },
    {
        "slug": "stocking-rate",
        "name": "Stocking rate in livestock units",
        "topic": "livestock",
        "expression": "stocking rate (LU/ha) = (number of animals x LU factor) "
                      "/ hectares",
        "symbols": "1 LU = one 450 kg cow, or about 10 ewe lambs, or 4 sows, "
                   "or 100 poultry, or 2.5 horses",
        "units": "livestock units per hectare",
        "how": "The fair way to compare a flock, a herd and a paddock. It also "
               "tells you whether you are about to overgraze.",
        "example": "100 ewe lambs at 0.1 LU each on 5 ha = 2 LU/ha.",
        "tags": "stocking rate,LU,grazing,paddock,ewe",
    },
    {
        "slug": "grazing-days-per-hectare",
        "name": "Grazing days per hectare",
        "topic": "livestock",
        "expression": "grazing days = (forage DM kg/ha x grazeable %) / "
                      "(stock units x intake per unit per day)",
        "symbols": "for a dairy cow at 3.5% of 600 kg, that is 21 kg of dry "
                   "matter a day",
        "units": "days per hectare",
        "how": "The practical version of the stocking rate. It tells you when "
               "to move the herd on, and how long a paddock lasts.",
        "example": "6,000 kg DM/ha at 60% grazeable with 40 cows at 18 kg DM: "
                   "3,600 / 720 = 5 days.",
        "tags": "grazing,paddock,dry matter,cow,move on",
    },
    {
        "slug": "milk-yield-per-hectare",
        "name": "Milk yield per hectare of forage",
        "topic": "livestock",
        "expression": "milk (kg/ha) = (forage DM kg/ha x energy content MJ/kg "
                      "DM) / (milk energy MJ/kg)",
        "symbols": "milk is about 3.14 MJ of net energy a kg; grass at "
                   "sillage is about 9-10 MJ of ME a kg of DM",
        "units": "kg of milk per hectare",
        "how": "The number that shows whether the land or the cow is the "
               "limiting factor, and the reason a good dairy farmer looks at "
               "the forage first.",
        "example": "12,000 kg DM/ha at 9.5 MJ/kg gives 114,000 MJ, which is "
                   "36,000 kg of milk a hectare.",
        "tags": "milk,yield,forage,hectare,dairy",
    },
    {
        "slug": "lambing-rate",
        "name": "Lambing and calving rate",
        "topic": "livestock",
        "expression": "lambing rate % = (lambs born / ewes tupped) x 100",
        "symbols": "a rate of 130 means 130 lambs per 100 ewes, which means "
                   "twins are doing the work",
        "units": "%",
        "how": "The measure of the whole system - rams, condition, feed, "
               "scanning and lambing. It is the number to write down every "
               "year.",
        "example": "120 lambs from 100 ewes = 120% lambing.",
        "tags": "lambing,calving,rate,flock,herd",
    },
    {
        "slug": "calving-interval",
        "name": "Calving interval",
        "topic": "livestock",
        "expression": "calving interval (days) = date of this calving - date of "
                      "the last calving",
        "symbols": "the target is 365 days; every extra day is a lost day of "
                   "milk and a heavier cow at the next calving",
        "units": "days",
        "how": "Measure it, and aim to get it under 380. A long interval "
               "usually means the cow is losing condition before the bull "
               "goes in.",
        "example": "Calved 15 March and 20 March the next year = 370 days.",
        "tags": "calving,interval,reproduction,fertility,cow",
    },
    {
        "slug": "conception-rate",
        "name": "Conception rate and calving rate",
        "topic": "livestock",
        "expression": "conception rate % = (cows confirmed in calf / cows "
                      "served) x 100 ; calving rate % = (calves born alive / "
                      "cows served) x 100",
        "symbols": "calving rate is always lower than conception rate, and "
                   "the gap is the loss at calving",
        "units": "%",
        "how": "Two different questions. Conception tells you about the bull "
               "and the condition score; calving rate tells you about the "
               "calving shed and the hard cases.",
        "example": "90 cows served, 80 in calf, 78 calves born: 89% "
                   "conception, 87% calving rate.",
        "tags": "conception,fertility,calving,bull,losses",
    },
    {
        "slug": "mortality-rate",
        "name": "Mortality and culling rate",
        "topic": "livestock",
        "expression": "mortality % = (animals that died / animals born) x 100 ; "
                      "culling % = (animals sold or culled / animals born) x "
                      "100",
        "symbols": "a smallholder should be able to keep lamb and calf "
                   "mortality under 5-8%",
        "units": "%",
        "how": "The honest measure of the system. Write it down every year; "
               "it tells you whether the problem is the housing, the feed or "
               "the lambing.",
        "example": "10 lambs dead from 100 born = 10% mortality.",
        "tags": "mortality,culling,lamb,calf,losses",
    },
    {
        "slug": "body-condition-score",
        "name": "Body condition score and liveweight",
        "topic": "livestock",
        "expression": "condition score is a 1 to 5 scale; the liveweight a "
                      "cow can carry is about (condition x 50) + 400 kg",
        "symbols": "score 1 = emaciated, 3 = good, 5 = obese; target 3.0 to "
                   "3.5 at calving and 2.5 to 3.0 at mating",
        "units": "score and kg",
        "how": "A condition score tells you more than a weight, and it takes "
               "ten seconds. Handle the animal and look at the hooks, the "
               "hips, the tailhead and the ribs.",
        "example": "A cow scoring 3.0 can carry about 550 kg, and loses "
                   "condition on the way to calving.",
        "tags": "condition score,weight,cow,ewe,fertility",
    },
    {
        "slug": "carcass-yield",
        "name": "Carcass yield and dressing percentage",
        "topic": "livestock",
        "expression": "dressing % = (carcase weight / liveweight) x 100",
        "symbols": "a lamb is 45-55%, a pig 75-80%, a beef animal 55-65%",
        "units": "%",
        "how": "The price of your stock depends on it. A heavy animal with a "
               "poor dressing percentage is not worth much more than a lighter "
               "one, and the killing sheet tells you which you have.",
        "example": "A 60 kg lamb with a 26 kg carcase = 43% dressing.",
        "tags": "carcase,dressing,meat,price,lamb",
    },
    {
        "slug": "water-intake-animals",
        "name": "Water intake",
        "topic": "livestock",
        "expression": "water (L/day) = body weight (kg) x 0.05 to 0.10, more "
                      "in hot weather or on dry feed",
        "symbols": "a lactating cow drinks 60-100 L a day; a 40 kg calf needs "
                   "about 5 L; a sow 20-30 L",
        "units": "litres per day",
        "how": "Size the troughs. A trough that is too small for a hot day is "
               "the reason a cow stops eating. See "
               "[[water-troughs-and-algae]].",
        "example": "A 600 kg lactating cow in summer may drink 100 L a day, "
                   "so a 200 L trough empties twice.",
        "tags": "water,intake,trough,cow,summer",
    },
    {
        "slug": "hen-egg-production",
        "name": "Egg production and feed per egg",
        "topic": "livestock",
        "expression": "lay rate % = (eggs / hens) x 100 ; "
                      "feed per dozen eggs (kg) = feed eaten / (eggs / 12)",
        "symbols": "a good free-range hen lays 250-300 eggs a year",
        "units": "% and kg per dozen",
        "how": "For working out whether a flock of hens is worth keeping. The "
               "feed per dozen is the number to watch, and it gets worse in "
               "winter when the birds are burning energy to stay warm.",
        "example": "20 hens, 5 eggs a day, 1.1 kg of feed a day: 240 eggs a "
                   "month, 1.65 kg of feed per dozen.",
        "tags": "hens,eggs,lay rate,feed,flock",
    },
    {
        "slug": "honey-yield-per-hive",
        "name": "Honey yield per hive",
        "topic": "livestock",
        "expression": "honey (kg) = colonies x kg per colony",
        "symbols": "a good flow gives 20-40 kg a colony; a poor year gives 5-10",
        "units": "kg",
        "how": "For planning how many hives you can keep, how much equipment "
               "you need and what the honey is worth. See [[keeping-bees]].",
        "example": "6 colonies at 25 kg each = 150 kg of honey.",
        "tags": "bees,honey,colonies,yield,flow",
    },
    {
        "slug": "drug-withdrawal-period",
        "name": "Withdrawal period and milk and meat",
        "topic": "livestock",
        "expression": "withdrawal time (days) = date of last treatment + "
                      "withdrawal period",
        "symbols": "the withdrawal period is on the label and on the vet's "
                   "card; it can be 3 to 60 days, and it applies to milk and "
                   "meat separately",
        "units": "days",
        "how": "Write the treatment date and the withdrawal date on the animal "
               "or in the book, and check the milk before it goes in the "
               "tank. See [[vaccinating-and-cold-chain]].",
        "example": "Treated on 1 June with a 14-day withdrawal: nothing in "
                   "the tank before 15 June.",
        "tags": "withdrawal,medicine,milk,meat,veterinary",
    },
    {
        "slug": "moulting-and-wool",
        "name": "Wool yield and fleece weight",
        "topic": "livestock",
        "expression": "wool (kg/head) = (body weight x fleece weight factor)",
        "symbols": "a ewe usually carries 3-6 kg of fleece, more in a good year "
                   "and on a fine fleece; a hogget carries less than a ewe",
        "units": "kg",
        "how": "For working out the wool income from a flock, and for judging "
               "whether the condition of the sheep at shearing was right.",
        "example": "A 70 kg ewe with a 4.5 kg fleece yields 6.4% of her "
                   "liveweight in wool.",
        "tags": "wool,fleece,she,shearing,weight",
    },

    # --------------------------------------------------------------- growing
    {
        "slug": "row-and-plant-spacing",
        "name": "Row and plant spacing for a vegetable bed",
        "topic": "growing",
        "expression": "spacing (m) = square root of (area per plant in m2)",
        "symbols": "area per plant = 1 / (plants per m2)",
        "units": "m",
        "how": "Bed planning. Work out how many plants you want, divide the "
               "bed area by the number, and that is the space each one gets.",
        "example": "Brassicas at 60 cm: 1 / 0.6 x 0.6 = 2.8 plants a square "
                   "metre, so about 0.4 m2 each.",
        "tags": "spacing,bed,brassicas,planning,planting",
    },
    {
        "slug": "plants-per-square-metre",
        "name": "Plants per square metre",
        "topic": "growing",
        "expression": "plants per m2 = 1 / (row spacing in m x plant spacing "
                      "in m)",
        "symbols": "use the same spacing figures the seed packet gives",
        "units": "plants/m2",
        "how": "The quickest way to plan a bed or a border. Onions at 10 cm "
               "square give 100 a square metre; potatoes at 30 cm give 11.",
        "example": "Carrots at 5 cm in 15 cm rows: 1 / (0.15 x 0.05) = 133 a "
                   "square metre.",
        "tags": "plants,spacing,bed,onions,carrots",
    },
    {
        "slug": "seed-spacing-on-row",
        "name": "Seed sown in a row at a spacing",
        "topic": "growing",
        "expression": "seeds per metre = 1 / spacing in metres ; "
                      "seed needed (g/m) = seeds per metre x seed weight in g",
        "symbols": "thinning is easier if you sow a little thicker and pull "
                   "the weak ones out",
        "units": "seeds/m, g/m",
        "how": "For beans, beetroot, carrots and onions sown in a drill in a "
               "bed. Sowing three seeds in a station and taking the best one "
               "is often more reliable.",
        "example": "Onions at 3 cm: 33 seeds a metre, and at 0.05 g a seed "
                   "that is 1.7 g a metre of row.",
        "tags": "sowing,drill,bed,seeds,thinning",
    },
    {
        "slug": "bed-area-and-planting-count",
        "name": "How many plants fit in a bed",
        "topic": "growing",
        "expression": "plants = (bed length x rows) / plant spacing in metres",
        "symbols": "count the rows, do not multiply up the bed area, because "
                   "the edges waste space",
        "units": "plants",
        "how": "Every bed plan starts with this. A 10 m bed with rows 30 cm "
               "apart has 33 rows, and at 25 cm in the row that is about 1,300 "
               "plants.",
        "example": "A 10 m bed, 30 cm rows, 25 cm plants: 10 / 0.25 = 40 "
                   "plants a row.",
        "tags": "bed,planning,rows,count,allotment",
    },
    {
        "slug": "compost-for-a-bed",
        "name": "Compost for a bed",
        "topic": "growing",
        "expression": "compost (litres) = bed area (m2) x depth (m) x 1,000",
        "symbols": "5-10 litres a square metre is a good working dose; 2 cm "
                   "is a light dressing, 5 cm is a proper one",
        "units": "litres",
        "how": "How much compost to barrow across the plot. One wheelbarrow "
               "is about 60 litres, so a 10 m2 bed at 5 cm needs about 5 "
               "barrows.",
        "example": "A 2 m x 1.5 m bed at 5 cm: 3 m2 x 0.05 x 1,000 = 150 L, "
                   "or about 2.5 barrows.",
        "tags": "compost,bed,soil,barrow,manure",
    },
    {
        "slug": "watering-a-bed",
        "name": "Water for a bed or a polytunnel",
        "topic": "growing",
        "expression": "litres per day = area (m2) x daily need (L/m2)",
        "symbols": "a growing vegetable bed needs about 4-6 L/m2 a day in "
                   "summer, less in spring, more in a polytunnel",
        "units": "litres",
        "how": "For a watering can shift or a hose timer. A 10 L can covers "
               "about 2 m2 a day, and a hose sprinkler covers about 20 m2.",
        "example": "A 6 m x 2 m polytunnel bed at 5 L/m2 = 60 L a day, or "
                   "six watering cans.",
        "tags": "watering,polytunnel,bed,summer,irrigation",
    },
    {
        "slug": "isolation-distance-for-seed-saving",
        "name": "Isolation distance for saving seed",
        "topic": "growing",
        "expression": "isolation = the distance needed to stop pollen from "
                      "another variety reaching the flower",
        "symbols": "maize 300 m, brassicas 800 m-1 km, onions 400 m, peas "
                   "10 m, squash 400 m, lettuce 300 m",
        "units": "m",
        "how": "Only worth it if you grow one variety at a time, or if the "
               "neighbours are not growing the same crop. Otherwise you will "
               "save a hybrid.",
        "example": "Saving brassica seed on a smallholding usually needs an "
                   "agreement with the neighbours.",
        "tags": "seed saving,isolation,pollen,variety,allotment",
    },
    {
        "slug": "seed-viability",
        "name": "Seed viability and storage",
        "topic": "growing",
        "expression": "years of life = about (log of seed number) / (log of 2) "
                      "halvings per year",
        "symbols": "the halving rule: onion and leek seed 1-2 years, brassica "
                   "3-4 years, lettuce 3-5, tomato 4-6, bean 3, onion 2, "
                   "parsley 2-3",
        "units": "years",
        "how": "The halving rule: seed loses half its life each year, so "
               "freshness doubles the years it lasts. Buy fresh seed for the "
               "crops that go over quickly.",
        "example": "Two-year-old onion seed is about half as good as new.",
        "tags": "seed,viability,storage,halving rule,germination",
    },
    {
        "slug": "germination-test",
        "name": "Home germination test",
        "topic": "growing",
        "expression": "germination % = (seeds that sprout / seeds sown) x "
                      "100",
        "symbols": "count 20 to 100 seeds on a damp cloth or in a sandwich of "
                   "paper and kitchen towel, keep them warm, count in 7-14 days",
        "units": "%",
        "how": "Ten minutes and it tells you whether a packet is worth "
               "sowing. Old or badly stored seed is the most common reason a "
               "row does not come up.",
        "example": "18 of 20 seeds sprout = 90% germination, so sow 10% more "
                   "than the packet says.",
        "tags": "germination,test,seed,cloth,viability",
    },
    {
        "slug": "succession-planting",
        "name": "Succession planting",
        "topic": "growing",
        "expression": "total plants = bed area / (spacing x spacing) x number "
                      "of sowings",
        "symbols": "three sowings of quick crops, one sowing of a slow crop",
        "units": "plants",
        "how": "How to keep a small bed productive all season. Sow little and "
               "often, and swap a fast crop for a slow one when the space "
               "frees up.",
        "example": "A 3 m2 bed of radishes at 5 cm squares gives 120 plants, "
                   "or 40 a sowing for three sowings.",
        "tags": "succession,bed,radish,planning,season",
    },
    {
        "slug": "green-manure-cover-crop-rate",
        "name": "Sowing rate for a green manure crop",
        "topic": "growing",
        "expression": "seed rate (kg/ha) is set by the target canopy, not by "
                      "the seed size",
        "symbols": "rye 60-80 kg/ha, oats 80-100, vetch 30-40 with 40 kg of "
                   "cereal, mustard 15-20, phacelia 15-20, lucerne 20-25, "
                   "clover 15-20",
        "units": "kg/ha",
        "how": "A cover crop is worth nothing if it is too thin to shade the "
               "soil and hold the rain. See [[cover-crops]].",
        "example": "A vetch and rye mix at 40 + 50 kg/ha gives a canopy in "
                   "eight weeks.",
        "tags": "cover crop,green manure,sowing rate,rye,vetch",
    },
    {
        "slug": "planting-out-date",
        "name": "Planting out after the last frost",
        "topic": "growing",
        "expression": "planting date = average last frost date - 2 to 3 weeks "
                      "of hardening off",
        "symbols": "hardening off means a week at 2 hours outside, then 4, "
                   "then 8, then all day",
        "units": "days",
        "how": "A plant that goes out too early loses a fortnight. Harden it "
               "off properly and it will lose a week of growth instead of a "
               "month of plants.",
        "example": "Last frost 15 May: plant out the tomatoes from 27 May.",
        "tags": "frost,planting out,hardening,tomatoes,date",
    },
]
