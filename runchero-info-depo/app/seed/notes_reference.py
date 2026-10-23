"""Extra notes for the reference desk: tables, calculators and safety.

These are the pages people come back to. Short answers, real numbers, and
nothing that needs a network connection.
"""

from __future__ import annotations

NOTES: list[dict] = [
    {
        "slug": "conversion-tables",
        "title": "Conversion tables for the farm",
        "category": "workshop",
        "summary": "Length, area, volume, mass, temperature, fuel and pressure, all on one page. The numbers you look up with muddy hands.",
        "author": "Dave, top field",
        "difficulty": "easy",
        "read_minutes": 7,
        "tags": "conversion,tables,units,imperial,metric",
        "body": """Half the old books are in pounds, acres and gallons, and half the new equipment is in metric. These tables are for the gap.

## Length

| From | To | Multiply by |
| --- | --- | --- |
| Inches | mm | 25.4 |
| Feet | metres | 0.3048 |
| Yards | metres | 0.9144 |
| Miles | kilometres | 1.609 |
| Furlongs | metres | 201.2 |
| Chains | metres | 20.12 |
| Rods | metres | 5.03 |

- **A chain** is 20.12 m, the old unit for measuring a field, and an acre is 10 chains by 66 feet.
- **A rope** is 20 feet, and **a perch** is 16.5 feet, 5.03 m.

## Area

| From | To | Multiply by |
| --- | --- | --- |
| Square feet | square metres | 0.0929 |
| Square yards | square metres | 0.8361 |
| Acres | hectares | 0.4047 |
| Acres | square metres | 4,047 |
| Hectares | acres | 2.471 |

- **One acre** is 4,047 m2, which is about 140 paces by 140 paces.
- **One hectare** is 10,000 m2, roughly 100 m by 100 m.

## Volume

| From | To | Multiply by |
| --- | --- | --- |
| Pints | litres | 0.568 |
| Quarts | litres | 1.136 |
| Gallons (UK) | litres | 4.546 |
| Gallons (US) | litres | 3.785 |
| Bushels | hectolitres | 36.37 (grain) |
| Cubic feet | cubic metres | 0.0283 |
| Cubic yards | cubic metres | 0.7646 |
| Acre inches | cubic metres | 253.7 |

- **A UK gallon is 4.546 litres** and a US gallon is 3.785. Old recipes and old machinery are usually UK.
- **An acre inch** is 2,537 m3 over an acre, the old unit of rain. An inch of rain on an acre is 22,000 gallons.

## Mass

| From | To | Multiply by |
| --- | --- | --- |
| Ounces | grams | 28.35 |
| Pounds | kilograms | 0.4536 |
| Stones | kilograms | 6.35 |
| Hundredweight (112 lb) | kilograms | 50.8 |
| Ton (imperial) | kilograms | 1,016 |
| Ton (US short) | kilograms | 907 |
| Kilogram | pounds | 2.205 |
| Stone | pounds | 14 |

## Temperature

| Fahrenheit | Celsius | Description |
| --- | --- | --- |
| -40 | -40 | Same number |
| 32 | 0 | Freezing |
| 39 | 4 | Chilling, meat fridge |
| 46 | 8 | Cold day |
| 50 | 10 | Cold, jackets on |
| 57 | 14 | Cool |
| 64 | 18 | Room temperature |
| 77 | 25 | Warm |
| 86 | 30 | Hot |
| 98 | 36 | Fever |
| 212 | 100 | Boiling |

- **Celsius to Fahrenheit**: multiply by 1.8 and add 32.
- **Fahrenheit to Celsius**: subtract 32 and multiply by 0.5556.

## Fuel and power

| From | To | Multiply by |
| --- | --- | --- |
| Litres | Imperial gallons | 0.219 |
| Imperial gallons | Litres | 4.546 |
| US gallons | Litres | 3.785 |
| Horsepower | kW | 0.746 |
| kW | Horsepower | 1.341 |
| Joules | BTU | 0.000947 |
| kWh | BTU | 3,412 |

- **A British thermal unit** is the heat to raise 1 lb of water 1 degree F. A small room heater pulls about 2,000 W, and a kettle is about 3,000 W.

## Pressure and flow

| From | To | Multiply by |
| --- | --- | --- |
| Bar | psi | 14.5 |
| psi | bar | 0.069 |
| Bar | kPa | 100 |
| Litres per minute | gallons per minute (UK) | 0.22 |
| US gallons per minute | litres per minute | 3.785 |

- **Tractor tyre pressures** are quoted in bar, and the old books use psi. See [[tyre-pressures-and-loads]].
- **A fire hose** running at 3 bar delivers about 25 litres a minute. A pressure washer at 100 bar delivers about 8.

## Quick rules of thumb

- **A mile is 10 furlongs, 8 furlongs a mile, 1760 yards a mile.**
- **A hectare is 2.47 acres; an acre is 0.4 hectares.**
- **A yard is 3 feet; a foot is 12 inches; an inch is 25.4 mm.**
- **A pound is 16 ounces; a stone is 14 pounds; a hundredweight is 112 pounds.**
- **A kilometre is 1000 m, a mile is 1609 m, so a mile is 1.6 km, and 5 miles is 8 km.**

> **Print this page and stick it on the workshop wall.** Every conversion mistake costs a trip to the merchant.
""",
    },
    {
        "slug": "inches-to-millimetres",
        "title": "Inches, millimetres and the sizes that matter",
        "category": "workshop",
        "summary": "Screens, spanners, pipe, timber, tyres and the sizes that catch people out when an old manual and a new part disagree.",
        "author": "Wes, workshop",
        "difficulty": "easy",
        "read_minutes": 6,
        "tags": "inches,millimetres,sizes,spanner,pipe,timber",
        "body": """Old manuals are in inches, new parts are in millimetres, and a farm yard has both. These are the sizes that actually turn up.

## Common conversions

| Inches | mm | Typical use |
| --- | --- | --- |
| 1/4 | 6.35 | Nyloc nuts, washers |
| 5/16 | 7.94 | Spanners, common on older machines |
| 3/8 | 9.53 | Spanners |
| 7/16 | 11.11 | Spanners |
| 1/2 | 12.7 | Spanners, conduit, BSP pipe |
| 9/16 | 14.29 | Spanners |
| 5/8 | 15.88 | Spanners |
| 3/4 | 19.05 | Spanners, BSP pipe |
| 7/8 | 22.23 | Spanners |
| 1 | 25.4 | BSP pipe, sockets |
| 1 1/4 | 31.75 | BSP pipe |
| 1 1/2 | 38.1 | BSP pipe, bar clamps |
| 2 | 50.8 | BSP pipe, clamps |
| 2 1/2 | 63.5 | Pipe |
| 3 | 76.2 | Pipe, fence posts |

## British Standard Pipe (BSP)

The old British thread, still on every hose, tap and old engine part.

- **1/2 inch BSP** has about 14 threads per inch, and the thread is 1/2 inch across the crest, not the hole.
- **15 mm is not 1/2 inch.** 1/2 inch BSP is 14.29 mm at the crest, which is why 15 mm fittings do not fit a 1/2 inch BSP tap.
- **Use the tape or a washer, not a sealant on BSP.** A dab of silicone on a wash face is better than PTFE tape on a tapered thread, which can split the fitting.
- **BSP sizes go up in eighths**: 1/8, 1/4, 3/8, 1/2, 5/8, 3/4, 7/8, 1 inch.

## Metric pipe and hose

- **20 mm** hose is common on a 15 mm BSP tap with a 20 mm washer, and it is the usual washers size on a modern tap.
- **Farm water pipe** is often 50, 63, 75 or 90 mm in metric, which is 2, 2.5, 3 or 3.5 inch. Measure the outside and take the nearest metric size.
- **Pumping 3 inch pipe** moves roughly 10 litres a second at a reasonable pressure.

## Timber sizes

| Metric (mm) | Imperial (inches) | Use |
| --- | --- | --- |
| 38 x 38 | 1.5 x 1.5 | Batten |
| 47 x 47 | 2 x 2 | Light post, studwork |
| 63 x 63 | 2.5 x 2.5 | Post, joist |
| 75 x 75 | 3 x 3 | Post, gate frame |
| 100 x 100 | 4 x 4 | Heavy post, frame |
| 150 x 150 | 6 x 6 | Big frame |
| 225 x 225 | 9 x 9 | Barn post |

- **Sawn softwood is sold in metric, and the sizes are nominal.** A 47 x 47 is really about 45 x 45 because of the planing allowance.
- **A 4 x 2 is the same as a 2 x 4**, just a different way round. Half the confusion on site comes from this.

## Spanners

- **Metric spanners** are 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 24.
- **Imperial spanners** are 1/4, 5/16, 3/8, 7/16, 1/2, 9/16, 5/8, 11/16, 3/4, 13/16, 7/8, 15/16, 1 inch.
- **A 19 mm spanner fits a 3/4 inch BSF nut.** That is worth remembering, because 19 mm is the most common metric spanner on a farm and it is the same nut.
- **Never guess.** A 13 mm spanner on a 9/16 inch nut will round the corners.

## Tyres and wheels

- **Tyre sizes are in inches and are the section width, not the rim.** 6.00-16 means a 6 inch wide tyre on a 16 inch rim.
- **Wheel studs** on a car and trailer are usually 5/16, 3/8, 1/2 or M12, M14, M16.
- **Bolt circle patterns** are stated in inches for old wheels and millimetres for new ones, and the number of studs is the more useful clue.

## Screens and filters

- **A 100 micron fuel filter** catches what a 10 micron one does not, and a 10 micron filter is what a modern common rail diesel wants.
- **A 5 micron filter** is for a common rail system, and 30 micron for an old injection system.

> **Measure twice, order once.** A 14 mm washer and a 15 mm washer look identical in the hand and cost a wasted trip to the merchant every time.
""",
    },
    {
        "slug": "yield-and-storage-calculator",
        "title": "How much to grow and where to put it",
        "category": "farming-crops",
        "summary": "From a household of four to a field of potatoes: work out the yield you need, the ground it takes, and the space it needs to live in.",
        "author": "Nadia, plot",
        "difficulty": "easy",
        "read_minutes": 6,
        "tags": "yield,storage,planning,harvest,space",
        "body": """Most growing plans fail because nobody wrote down how much they actually need. Work through the four numbers in order and the plan writes itself.

## 1. How much do we eat?

Start with the people and the animals.

| Person | Vegetables a week | Potatoes a week | Eggs a week |
| --- | --- | --- | --- |
| Adult | 1.5 kg | 1 kg | 3-4 |
| Child | 0.8 kg | 0.5 kg | 3-4 |
| 500 kg pig | 2 kg | 1 kg | - |
| 450 kg cow | 4 kg | - | - |
| 70 kg ewe | 1 kg | - | - |
| Hen | 0.1 kg | - | 1 egg a day |

- **A working man eats roughly 400 kg of vegetables a year**, and a family of four needs around 600-800 kg of fresh vegetables a year from the garden.
- **Add 20% for waste.** Bolts, slugs, bad weather and the rows that never got picked.

## 2. How much does that take in ground?

Typical yields per hectare (or per square metre for a plot):

| Crop | Per m2 | Per hectare | Notes |
| --- | --- | --- | --- |
| Potatoes | 3 kg | 30 t | Maincrop |
| Onions | 2 kg | 20 t | Sets, not seed |
| Carrots | 1.5 kg | 15 t | Maincrop |
| Cabbage | 2.5 kg | 25 t | White cabbage |
| Beetroot | 1.5 kg | 15 t | |
| Beans | 0.8 kg | 8 t | Broad beans, picked |
| Courgettes | 2 kg | 20 t | |
| Onions, shallots | 1.5 kg | 15 t | |
| Sweetcorn | 1.2 kg | 12 t | Fresh |
| Winter wheat | 0.8 kg | 8 t | Grain, not flour |
| Hay | 0.5 kg | 5 t | At 85% dry matter |

- **Work out the area from the yield you need, not the other way round.** A family of four needs about 400 m2 of vegetables, and a 200 m2 plot with good soil and a rotation can carry a good part of that.
- **Double it for failures.** A bad year, a wet June, a failed crop of one thing.

## 3. Where does it go?

Storage space for the crops you will actually keep:

| Crop | Space per tonne | Notes |
| --- | --- | --- |
| Potatoes, clamped | 1.2 m3 | Needs frost free, dark, airy |
| Onions, in store | 1.5 m3 | Cool, dry, well ventilated |
| Carrots, in sand | 1.2 m3 | 60-80% sand, no frost |
| Beetroot | 1.2 m3 | |
| Apples in crates | 2.2 m3 | |
| Cabbage, headed | 1.5 m3 | |
| Grain in a bin | 1.35 m3 | Wheat at 0.75 t/m3 |
| Hay, small bales | 2.5 m3 | 220 kg of dry matter a bale |
| Silage in a clamp | 1.3 m3 | |

- **A 4 x 4 m root store with 2.3 m walls** holds about 35 m3, which is 28 tonnes of potatoes. See [[root-cellar-storage]].
- **A 6 m diameter, 4 m deep grain bin** holds about 113 m3, which is 85 tonnes of wheat. See [[storing-grain]].

## 4. What does it cost to keep?

| Store | Build cost | Running cost a year |
| --- | --- | --- |
| Potato clamp, earth and straw | Almost nothing | Straw and labour |
| Ventilated root store | 2,000-5,000 | Rodent bait, electricity |
| Grain bin | 3,000-10,000 | Power, bird control |
| Cold store | 8,000-20,000 | Electricity, maintenance |
| Freezer | 400-1,500 | Electricity |

- **Work out the loss.** A clamp that loses 8% of the potatoes is cheaper than a cold store that loses 2% but costs 400 euro a year in electricity, until you are storing more than 30 tonnes.
- **Add the labour.** An hour a week of checking a store is worth more than any thermometer.

## A worked example

A household of four, two pigs and ten hens:

- Vegetables: 4 x 400 kg = 1,600 kg, plus the pigs' 2 x 1.5 kg a week = 156 kg. Say 1,800 kg a year.
- Add 20% for waste: 2,160 kg.
- Potatoes: 4 x 52 kg = 208 kg, plus the pigs' 104 kg. Say 320 kg.
- Eggs: 14 hens x 300 a year = 4,200 eggs, and the house uses about 1,500 of them.

- 2,160 kg of vegetables at 1.5 kg a square metre = 1,440 m2. Add half for rotation and failures: about 2,200 m2 of ground, which is 0.22 hectare.
- 320 kg of potatoes at 3 kg a square metre = 107 m2, so 12 m2 of clamp.

> **Write the numbers down.** A plan on the back of an envelope beats a good intention every time.
""",
    },
    {
        "slug": "spraying-safely",
        "title": "Spraying safely: the rules that keep you well",
        "category": "farming-crops",
        "summary": "Protective gear, mixing, drift, buffers, records and the disposal of the washings. The boring rules are the ones that save you.",
        "author": "Priya, agronomy",
        "difficulty": "medium",
        "read_minutes": 8,
        "tags": "spraying,safety,pesticide,drift,protective,ppe",
        "body": """Every year people are poisoned by chemicals they handled carelessly for thirty years. The products have improved; the habits have not.

## Before you start

- **Read the label. All of it.** It carries the legal requirements: the dose, the harvest interval, the buffer zone, the protective gear, the water volume, the maximum dose per year.
- **Keep the label.** Take a photo of it and put it in the cab, and keep the paperwork for at least three years. See [[spraying-and-weed-control]].
- **Check the sprayer.** No leaks, a sound hose, a clean filter, a working cut-off, a pressure gauge that reads zero with the trigger off.
- **Know the weather.** Do not spray in wind above 5 km/h, in rain, or when a forecast says rain within a few hours. See [[working-alone-and-emergency]].

## Protective gear

| Job | Minimum |
| --- | --- |
| Handling concentrate | Nitrile or butyl gloves, coverall, eye protection, face shield for pouring, respirator for dusts |
| Knapsack spraying | Coverall, gloves, eye protection, boots, wide brimmed hat |
| Tractor spraying | Coverall, gloves, eye protection, and a cab with a filter if you can |
| Working near a treated area | Closed shoes and long sleeves, no skin exposed |

- **A coverall is not a rain jacket.** A cotton coverall absorbs the chemical and holds it against your skin. Non-woven coveralls are the ones to buy.
- **Change gloves** every time you handle concentrate, and wash them inside out before you take them off. Never wash them in the kitchen sink.
- **Keep the PPE in a sealed bag**, and wash it separately from the family laundry. See [[venting-the-workshop]].

## Mixing

1. **Half fill the tank with clean water.** Always the water first, never the concentrate into an empty tank.
2. **Measure the product with a proper jug**, and use the jug for nothing else. Keep it with the sprayer, not in the kitchen.
3. **Add the product to the water** with the agitation running.
4. **Top up with water** to the required volume, keeping the agitation on.
5. **Do not leave a part-full tank** overnight. See [[water-in-the-fuel]] for what a stale mix does.
6. **Rinse the container three times** and put the washings in the tank. Do not tip the container in the yard.

- **Never mix products unless the label says it is allowed.** Some tank mixes are genuinely dangerous, and a few are illegal.
- **The agitation is not there to help you mix.** It stops the product settling on the bottom.

## Applying

- **Wear the gear from the label, not what feels reasonable.**
- **Never spray in the wind**, and never near a boundary if there is any doubt. A fine drift travels further than you think, especially on a warm day with a slight inversion.
- **Keep children, food, animals and water troughs out of the area.** Cover or move them before you start.
- **Watch the weather during the job.** Conditions change faster than a spray round.

## The buffer zone

- **A buffer zone is a no-spray strip** measured from the watercourse, the boundary or the well, and its width is on the label.
- **Spray along the buffer, not across it.** Fit a marker flag on the sprayer boom so you know where the edge is.
- **No buffer zone is a licence to spray the ditch.** If it is a watercourse, treat it as a watercourse.

## Records

Keep a record of every application: date, field, product, dose, water volume, operator, weather, and the harvest date you worked out from the label interval.

- **The interval is a legal minimum.** Washing a crop early is illegal, and it is the single most common thing people get wrong.
- **Keep records for at least three years.** Buyers, auditors and the inspector all ask.

## Disposal

- **Washings go on the ground you sprayed, at the label rate, and not near a drain.** See [[draining-water-pipes]].
- **Empty containers go to a licensed waste contractor.** Never burn them and never bury them.
- **Do not wash the sprayer over a drain or in a ditch.** See [[underground-pipe-and-trenches]].

## If you get it on you

- **Skin:** take off the contaminated clothing, wash with soap and plenty of water for 15 minutes.
- **Eyes:** rinse with water for 15 minutes and get medical advice.
- **Breathing:** move into fresh air and seek help.
- **Swallowed or a serious exposure:** call the emergency number and take the label with you. See [[working-alone-and-emergency]].

> **The label is the law, and the law is written by the people who tested the product on people.** Follow it exactly and the risk is small. Guess and it is not.
""",
    },
    {
        "slug": "hot-work-and-fire-safety",
        "title": "Hot work: welding, grinding and fire",
        "category": "workshop-welding",
        "summary": "Permits, screens, gas checks, extinguisher drill and the clean-up that stops a weld fire three hours later.",
        "author": "Wes, workshop",
        "difficulty": "medium",
        "read_minutes": 8,
        "tags": "welding,grinding,fire,hot work,safety,extinguisher",
        "body": """Most farm fires start from hot work: a grinder in straw, a welder in a barn with a hay bale next to the wall, a blowtorch near a haystack. The rules below are simple and they are not optional.

## Before you start

- **Check the fire point.** Is there a working extinguisher, a bucket of sand or water, and a clear way to call for help?
- **Move anything that can burn.** Straw, hay, feed sacks, cardboard, paint, petrol, weedkiller, plastic. Move it at least 10 m, and put it somewhere it cannot roll back.
- **Do not hot work on a fuel tank, a cylinder or a drum** unless it has been emptied, degassed and certified. A petrol tank with vapour in it is a bomb.
- **Check the weather and the space.** A hot works area needs ventilation, or the fumes will kill you before the fire kills the barn. See [[venting-the-workshop]].
- **Tell somebody.** Even if you are only grinding for five minutes. See [[working-alone-and-emergency]].

## A hot work permit

For anything beyond a cold job, a simple written permit keeps everyone straight.

| Field | Example |
| --- | --- |
| Where | Workshop bay 2, outside the door |
| What | MIG welding a bracket |
| When | 10 March, 09:00 to 11:00 |
| Fire watch | Sam, until 12:00 |
| Extinguisher | 6 kg powder at the door, water at the far end |
| Gas check | Oxygen and acetylene checked 08:45 |
| Checks | 11:00 fire watch extended to 13:00 |

- **A fire watch is a person with nothing else to do.** They stay for an hour after the last spark and they carry an extinguisher.
- **The permit is closed when the fire watch signs it off.** Not when the welding is finished.

## Gas and cylinders

- **Oxygen and fuel gas cylinders upright, secured, and apart.** A chain or a strap, not a leaning wall.
- **Check for leaks** with soapy water, never a naked flame. The flame test is for the far end, at the torch.
- **Acetylene and oxygen must be used in the right order.** Start the oxygen, then the fuel gas to light. Shut the fuel gas off first, then the oxygen. Getting it wrong puts a flame in the cylinder.
- **Check the regulators and hoses** before every job. A green oxygen hose and a red or black fuel hose is the usual colour code, and the hose is replaced if it is perished, cracked or gets near a hot job.
- **Acetylene dissolves in acetone** and the cylinder gets lighter over time. Keep it upright.
- **Take the cylinders to the job on a trolley**, not carried, and never with the regulator fitted and the valve open.

## Grinding and cutting

- **Check the wheel** for cracks before every job, and do not use a wheel that has been dropped.
- **A grinder needs a guard**, and the guard must be in the right position. A wheel that runs out past the guard is a wheel that will come off.
- **Let the wheel run up to speed** before you touch the work.
- **No gloves near a grinder**, and no loose sleeves.
- **Grinding sparks travel a long way.** They will go through a shed wall and start a fire in the next bay. Use a spark guard screen.

## The fire plan

| Situation | What to do |
| --- | --- |
| Small fire in a solid object | Water or foam from the extinguisher at the base |
| Fire in an electrical item | Isolate the power first, then water or CO2 |
| Fire in oil, diesel or paint | Foam, or the lid of a metal bin. Never water |
| Fire in a hay or straw bale | Water, and lots of it, and call the fire brigade early |
| Fire spreading or you are not sure | Get out, close the door behind you, and call the brigade |
| Clothing on fire | Stop, drop and roll. Do not run |

- **Know your extinguisher.** Check the gauge is in the green, the pin is in, the seal is unbroken, and the hose is not cracked. Mark the date you checked it.
- **A 6 kg powder extinguisher** is the minimum for a workshop. A 2 kg CO2 for electrical work and a water one for the office is a sensible set.

## After the job

- **Wait an hour** before you leave. Sparks fall a long way and hide in straw.
- **Feel the area** for heat. Back of the hand, not the palm.
- **Check the floor, the roof space and the walls** near the work, and the grass outside.
- **Put the fire blanket back** and the gas cylinders away.

> **A weld is finished when the fire watch says it is.** Not when the arc stops.
""",
    },
    {
        "slug": "working-alone-and-emergency",
        "title": "Working alone and what to do in an emergency",
        "category": "survival",
        "summary": "Check-ins, phones, first aid, fire, cattle and the plan that decides whether a helper is 10 minutes away or an hour.",
        "author": "Dave, top field",
        "difficulty": "medium",
        "read_minutes": 8,
        "tags": "lone working,emergency,first aid,phone,safety",
        "body": """A lot of farm work is done alone, and a lot of it is dangerous alone: the roof, the grain bin, the beasts, the dark, the chemicals.

## The check-in plan

1. **Decide who checks on you.** A partner, a neighbour, a family member who is not on the farm.
2. **Agree a time.** One fixed time each day for a call, and one time you expect to be finished.
3. **Say what you are doing.** "On the barn roof, back by four" and "in the grain bin" are not the same.
4. **If you miss the call, they escalate.** A missed call starts a phone round, and after 30 minutes they call the emergency services with your last known job and location.
5. **Write the plan down** and leave it where the helper can find it, with the gate code, the site address and the nearest hospital.

- **Text, do not phone,** if the signal is poor. A text gets through on one bar and a call does not.
- **Charging.** A phone with 4% battery in a cold shed is a phone that will die exactly when you need it.
- **Location sharing** on the phone, if the helper has it switched on, is worth more than a description.

## Lone working jobs

| Job | Do not do it alone |
| --- | --- |
| Grain bin entry | Never, not even with a rope and a partner |
| Roof work over 2 storeys | Not without a harness and someone on the ground |
| Working in a confined space | Not without a permit and an attendant |
| Chainsaw work | Not without a first aid kit within reach |
| Working with cattle | Not without an escape route and a partner |
| Electrical work | Isolate and prove dead, then still be careful |
| Spraying | Not without a phone on you and the label |
| Working at height on a silo | Not without a harness and a trained partner |

- **The grain bin is the one that kills people.** Grain flows like water, and a 1.3 m3 silo can bury a person in seconds. Never enter, never even partially. See [[silo-and-grain-safety]].

## The first aid kit

| Item | Why |
| --- | --- |
| Dressings and bandages | Cuts and grazes from wire and tools |
| Adhesive plasters and tape | Everything |
| Antiseptic or saline wipes | Cleaning a wound before it is closed |
| Scissors and forceps | Removing debris, dressings |
| Gloves, disposable | To protect you and the wound |
| Tourniquet | A bleeding farm injury can kill in minutes |
| Painkillers | Paracetamol and ibuprofen |
| Saline and an eye wash | Dust, chemicals, splash |
| Burn gel and a cold pack | Scalds and burns |
| Thermometer | Fever in a calf or a child |
| Sticky notes and a pen | Writing down what happened |
| Yellow waste bag | Clinical waste |

- **Check the kit every six months.** Replace anything open, and check the expiry on the medicines.
- **Put a kit in the tractor, the workshop and the house.** See [[tractor-wont-start]] for keeping the tractor kit stocked.

## The emergency plan

- **Know the address you give.** "The farm at the end of the lane" is not enough. Put the postcode and the grid reference on the gate.
- **Nearest hospital with an A&E**, and the two nearest doctors, written down.
- **Emergency number, ambulance, fire, police, vet.** On the fridge and in the phone.
- **What to say:** what happened, how many people, what is wrong, where you are, and the gate code.

## Specific emergencies

### A bleeding animal or a bleeding person
- **Press hard with a clean pad** and do not lift it to look.
- **A limb wound that will not stop bleeding** needs a tourniquet above the wound, tight, and written down with the time it went on. See [[working-with-chocolate]] for nothing, and ask the vet for the technique.

### A animal down
- **A cow in a slurry pit or a ditch** will drown in a few minutes. Get a rope on it and pull it out at the head, or roll it a bale as a roller. See [[cattle-handling-race]].

### Fire in a building
- **Get everyone out.** Close the door behind you. Call the brigade from outside. Never go back in.

### Poisoning or chemicals
- **Take the container with you.** The label tells the hospital what to do. See [[spraying-safely]].

### Machinery injury
- **Do not pull a limb out of a machine.** Switch it off, isolate the battery, and wait for help. A crush injury is far worse if you make it worse.

> **Someone should always know where you are.** It is the cheapest safety device on the farm and it costs nothing.
""",
    },
    {
        "slug": "silo-and-grain-safety",
        "title": "Grain bin and silo safety",
        "category": "farming-crops",
        "summary": "Grain entrapment, bin entry, dust explosions, augers and the rules that stop the deadliest accident in grain farming.",
        "author": "Marta, arable",
        "difficulty": "medium",
        "read_minutes": 8,
        "tags": "silo,grain,entrapment,dust,auger,confined space",
        "body": """Grain bin accidents are rare and almost always fatal, because the grain holds you up and something heavy falls on top of you.

## How people die in grain

- **Entrapment.** A person sinks into grain and cannot get out. A bushel of grain weighs about 27 kg, and body weight equals the weight of the grain displaced. Once you are in to chest height, you cannot lift yourself out, and the grain around your legs moves to fill the space you made.
- **Burial.** A grain bridge forms over a bin that looks empty. It looks safe and it is not. It collapses without warning.
- **Equipment.** An auger running in grain will draw a person in and hold them. People have been augered out of a bin and out of a loader bucket.
- **Dust explosions.** Grain dust is explosive when it is suspended in air at the right concentration, and a 1 kg/m3 layer of dust in a machine house is enough.

## The rules

1. **Never enter a bin with grain in it.** No exceptions, not even to level it out.
2. **Never enter a bin that is empty but has had grain in it.** The bridges and the floor of hard-packed grain are the danger.
3. **Never work on a grain surface without a permit, an attendant and a harness.** If a bin has to be emptied by hand, it is emptied by a machine with the power locked off.
4. **Lock out the power** before anyone puts a hand, a foot or a body near an auger, a conveyor, a elevator or a door.
5. **Assume the grain is flowing** whenever a gate is open. A bridge can fail without warning.

## Before any bin work

- **Empty the bin down to the level where the work is needed**, with a machine, not by hand.
- **Isolate and lock off** the power at the isolator, and put a padlock and a tag on it.
- **Block the auger intake** so nothing can be started by accident.
- **Test for air** with a gas meter if the bin has been fumigated. See [[venting-the-workshop]] for the same rules in a workshop.
- **Have a trained person with a harness and a rope at the mouth**, ready to pull, and never in the bin unless the plan is written down and rehearsed.

## The grain auger

- **Never stand under a raised auger**, and never reach into a swinging auger intake.
- **Keep hands and feet clear of the intake** and the drive chain. The drive shaft on an old auger is unguarded.
- **A bridging auger must be cleared with a rod from the side, never by reaching over the top.**
- **Clamp the flighting** before working on it. It is heavier than it looks and it will fall.
- **Never run an auger with the intake in grain and the discharge empty**, that is the run-away.

## Dust and fire

- **Grain dust collects in every corner**, on top of motors, inside electrical boxes, on lights.
- **Do not use a naked flame or a hot bulb** in a grain store. Use a sealed light or a head torch.
- **Sweep with a vacuum**, never with compressed air, which puts the dust into the air where it is most dangerous.
- **Run the fans before you work** in a dusty building. See [[grain-silo-airflow]] for moving the air through the grain.

## Clothing and entry

- **A harness with a rope and a winch is the only way to work in a bin**, and only with a trained attendant at the mouth.
- **The attendant must be able to pull you out** and must not be alone.
- **Never work alone in a bin.** Ever.

## After the work

- **Take the locks off and put the power back on** properly, so the next person is not caught out by a machine that will not start.
- **Clear the dust** before you leave the building.
- **Have the fire point checked** and the extinguishers in place.

## If someone is trapped in grain

1. **Call the emergency services immediately** and say "person trapped in grain".
2. **Do not jump in after them.** You will be trapped too, and now there are two.
3. **Get a ladder and a rescue board, or a big flat panel**, and put it in the grain next to the person. It spreads the load and gives them something to push against.
4. **Cut the grain away with a shovel or a loader bucket**, slowly, from the side of the bin, not through the person.
5. **Keep the grain flowing** if the machine is safe to run, since flowing grain is what lets them sink out. Stop it if the bridge is over them.

> **If you cannot get a person out within a few minutes, wait for the brigade and keep talking to them.** They have the gear and the training. You have the rope.
""",
    },
    {
        "slug": "mixing-concrete",
        "title": "Mixing concrete by hand and by machine",
        "category": "workshop",
        "summary": "Mix ratios, quantities, the water to cement rule, and how to get a strong footing without adding water.",
        "author": "Wes, workshop",
        "difficulty": "medium",
        "read_minutes": 7,
        "tags": "concrete,mix,cement,footing,slab,curing",
        "body": """Concrete is simple and unforgiving. Get the mix right and a footing will outlast the building on it. Add water to make it easier to work and you have made weak concrete that will fail in the frost.

## Mixes

| Mix | Cement : sand : stone | Use |
| --- | --- | --- |
| 1:2:4 | 1 : 2 : 4 | Footings, paths, general work |
| 1:2:5 | 1 : 2 : 5 | Mass bases, ground floors |
| 1:1.5:3 | 1 : 1.5 : 3 | Stronger work, drives, steps |
| 1:1:2 | 1 : 1 : 2 | Strongest, expensive, rarely needed |
| 1:4 | 1 : 4 | Mortar for brickwork |
| 1:5 | 1 : 5 | Mortar for foundations and render |
| 1:3 | 1 : 3 | Pointing and thin work |

- **These are volume ratios, not weights.** Use the same bucket for every material.
- **The strength comes from the cement and the water, not the stone.** The stone and sand fill the space and stop it cracking.

## Quantities for one cubic metre

| Mix | Cement | Sand | Stone | Water |
| --- | --- | --- | --- | --- |
| 1:2:4 | 7 bags of 25 kg | 0.5 m3 | 0.75 m3 | 140 litres |
| 1:2:5 | 6 bags | 0.45 m3 | 0.8 m3 | 135 litres |
| 1:1.5:3 | 8 bags | 0.4 m3 | 0.65 m3 | 135 litres |

- **A 25 kg bag gives about 12.5 litres of mixed concrete.** So one bag makes about 50 litres.
- **A wheelbarrow holds about 0.07 m3**, so 60 litres. A "bucket" of sand is about 14 litres.
- **A 1 x 1 m x 100 mm slab needs 0.1 m3**, which is 8 bags of cement, 0.05 m3 of sand, 0.075 m3 of stone and 20 litres of water.

## The water rule

| Water : cement | Strength | Notes |
| --- | --- | --- |
| 0.40 | About 30 MPa | Very strong, hard to work |
| 0.45-0.50 | About 25 MPa | Good structural work |
| 0.55-0.60 | About 20 MPa | Normal for a footing |
| 0.70 | About 15 MPa | Weak |
| 0.80 and above | About 10 MPa | No good in a frost |

- **Every extra litre of water cuts the strength and adds roughly 7 kg of cement per cubic metre to put it right.** A bucket of extra water is a bucket of weak concrete.
- **Use a plasticiser** if the mix is stiff and hard to work. It makes the concrete flow without more water.
- **Never add water to a mix that is setting.** Mix a fresh batch.

## Mixing by hand

1. **Mix the dry materials** on a hard surface until the colour is even, with a shovel.
2. **Add the water in two goes**, mixing thoroughly between each. Keep a bucket for the water and a shovel for the mix.
3. **Mix for 3 minutes after the last water goes in.** This is what gets the cement to spread evenly.
4. **Beat the surface flat** and check the level before it starts to set.
5. **Have a second pair of hands if you can.** Slabs and footings are much easier with two.

## Mixing by machine

- **A mixer of 90 litres** will do a footing and a path in two or three batches.
- **Never put a shovel or a hand into a running mixer.** Shut it off and unplug it.
- **Mix for 2-3 minutes** after the water is in, which is longer than you think.

## Placing and curing

- **Level the ground** and compact it. Concrete on soft ground cracks in the middle.
- **Damp the ground** before you pour, so it does not drink the water out of the mix.
- **Vibrate or tamp the concrete** to push out the air bubbles. Tamping with a stick or a bar is enough for a footing.
- **Cover it** with polythene or a hessian sheet and keep it damp for three days. See [[compost-heap]] for why moisture and cover matter.
- **Walk on it after 24-48 hours**, put a load on at 7 days, and expect full strength at 28 days.
- **Do not build in freezing weather** unless you are using a cold-weather mix.

## Common mistakes

- **Too much water.** The number one mistake, and the reason footings crack across the middle.
- **Sand that is too fine.** Sharp sand or a washed concrete sand. Builder's sand is for mortar.
- **Stone that is too small.** 20 mm gravel is right for a footing; pea gravel is for a slab.
- **No membrane under a slab.** Lay 100 mm of compacted hardcore and a polythene sheet, or the ground moisture will lift the slab.
- **Pouring straight onto soil.** Always put a layer of hardcore first.

> **A footing is the one thing in the yard that is very hard to fix later.** Dig it deep, mix it strong and let it cure.
""",
    },
    {
        "slug": "three-phase-and-single-phase",
        "title": "Three phase, single phase and farm power",
        "category": "workshop",
        "summary": "What each supply gives you, the loads a farm actually runs, and how to work out whether a circuit will carry the machine.",
        "author": "Wes, workshop",
        "difficulty": "medium",
        "read_minutes": 7,
        "tags": "electric,three phase,single phase,motor,supply,amperage",
        "body": """Farm power comes in three sizes, and knowing which one you have saves a lot of guessing.

## The supplies

| Supply | Voltage | Typical uses |
| --- | --- | --- |
| Single phase 230 V | 230 V | Lights, sockets, small motors, tools |
| Three phase 400 V | 400 V | Motors, workshop machines, welders, heating |
| Single phase 230 V with a neutral | 230 V | Same, but you have an earth and a neutral for the plug |

- **In the UK and Ireland, single phase is 230 V and three phase is 400 V line to line, which is 230 V line to neutral.**
- **Three phase comes in two kinds.** 400 V with a neutral (TN-S and TN-C-S) and 230 V with a neutral and earth (TT, which is most rural supplies). The difference matters for the electrician, not for you.
- **Phase rotation** matters on three phase motors: swap any two of the three phases to reverse the motor. On a single phase motor, swap the live and neutral.

## What each load draws

| Load | Single phase 230 V | Three phase 400 V |
| --- | --- | --- |
| 1 hp motor (0.75 kW) | 5 A | 1.5 A |
| 3 hp motor (2.2 kW) | 13 A | 4 A |
| 5 hp motor (3.7 kW) | 21 A | 6.5 A |
| 7.5 hp motor (5.5 kW) | 30 A | 9 A |
| 10 hp motor (7.5 kW) | 39 A | 13 A |
| Electric welder, 200 A | 25-30 A | 16-20 A |
| Workshop compressor 3 kW | 15 A | 5 A |
| Small electric heater 2 kW | 9 A | 3 A |
| Electric boiler 12 kW | 52 A | 18 A |
| Fence charger | 0.5 A | - |

- **Three phase is much easier on the supply.** A 7.5 kW motor draws 13 A on three phase and 39 A on single phase. That is the whole argument for a three phase supply on a farm.
- **A 16 A socket is a 3.7 kW limit on single phase**, less for a motor, because motors draw a high starting current.

## Size of the supply

A single phase farm supply is usually 60 A or 100 A, and three phase is 60 A, 100 A or 200 A per phase.

- **60 A three phase gives about 41 kW**, and it is enough for a welder, a compressor and the house.
- **A 100 A single phase supply gives 23 kW**, which sounds like plenty until you put a 12 kW boiler and a welder on it at once.

## Cables

| Cable | Single phase 230 V | Three phase 400 V |
| --- | --- | --- |
| 1.5 mm2 | 16 A, lighting | - |
| 2.5 mm2 | 20 A, sockets | - |
| 4 mm2 | 28 A | - |
| 6 mm2 | 36 A | 26 A |
| 10 mm2 | 50 A | 42 A |
| 16 mm2 | 68 A | 58 A |
| 25 mm2 | 89 A | 77 A |
| 35 mm2 | 110 A | 96 A |

- **These are the current-carrying capacities in free air or in insulated cable in a wall.** Buried or in a conduit, take the next size up.
- **The length of the run matters.** More than 30 m and you need the next size up, or you will get a voltage drop. See [[electrical-fault-finding]].

## Motors

- **Three phase motors are cheaper, quieter and more efficient** than single phase of the same power, and they start better.
- **A star-delta starter** is used on larger three phase motors to limit the starting current. An 8-13 kW motor on a 32 A supply usually needs one.
- **A phase failure monitor** is worth fitting on a remote machine. A motor running on one phase gets hot and burns out.
- **Sizing a motor:** the belt, the load and the duty decide it, and the starting current decides the starter. See [[pallets-and-scraps]] for building the drive.

## Earthing and protection

- **Every circuit needs RCD protection** at 30 mA for sockets, and 100 mA for a garage or a workshop. See [[electrical-fault-finding]].
- **A three phase supply still needs an RCD.** Get a 30 mA three phase RCD, or four pole for a neutral.
- **TT supplies** need the earth electrode and the resistance checked. Get it done by a proper electrician and keep the certificate.

> **Never work on a supply that is live.** Isolate, lock off, prove dead with a tester, and prove the tester on a known live source. Every time.
""",
    },
    {
        "slug": "electrical-fault-finding",
        "title": "Electrical fault finding on the farm",
        "category": "workshop",
        "summary": "Tripped breakers, dead sockets, flickering lights and the tests that find the fault without guessing.",
        "author": "Wes, workshop",
        "difficulty": "medium",
        "read_minutes": 8,
        "tags": "electric,fault,breaker,rcd,tester,mcb",
        "body": """Most farm electrical problems are simple, and most farm electrical injuries start with somebody guessing instead of testing.

## The rules before anything else

1. **Isolate.** At the consumer unit, switch off the breaker and lock it off if it is a fault you cannot leave.
2. **Prove dead.** Test with a two-pole tester on a known live source first, then on the circuit.
3. **Prove the tester.** Always, every time, before and after. A tester that reads nothing because it is flat is the most dangerous thing in the workshop.
4. **Never work live** unless the job is testing live, and then with the right instrument, insulated tools and a second person.
5. **Any work on the board, the meter or the supply** is for a competent electrician with a certificate.

## The consumer unit

| Device | What it does |
| --- | --- |
| MCB | Overcurrent protection, one per circuit, 6 A to 32 A |
| RCD | Detects current imbalance, 30 mA for sockets, 100 mA for a workshop |
| RCBO | An MCB and an RCD in one, one per circuit |
| Main switch | Isolates everything |
| SPD | Surge protection, worth having with a farm supply |

- **A main switch, an MCB per circuit and an RCD covering the sockets** is the minimum on a modern installation.
- **A 30 mA RCD is for humans.** 100 mA is for a garage or a workshop where the equipment is rough. 300 mA is for a sub-board, not for sockets.
- **Label every circuit** with a proper label and a printed chart. The electrician should leave you one, and you should keep it in the box.

## A circuit that will not stay on

Work through it in this order:

1. **Unplug everything on that circuit.** A kettle or a freezer with a leaking element will trip the RCD every time.
2. **Reset once.** If it holds with everything unplugged, the fault is in the appliance.
3. **If it trips again with nothing plugged in**, the fault is in the wiring, a light fitting or a socket. This is where you need a proper circuit tester.
4. **Look for the classic causes:**
   - A garden light or a shed socket with water in it
   - A junction box in the roof space with a poorly made joint
   - A cable pinched by a nail or a door
   - An outside socket with a missing rubber gasket
   - A heater element in a freezer or a chest freezer
   - A rodent chewed cable in the roof void
   - Water in an outside light fitting
5. **Split the circuit.** Turn off the MCB and test each part of the circuit in turn to find the section. See [[underground-pipe-and-trenches]] for the same idea applied to water.

## Finding a dead socket

- **A socket with no power but the breaker is on** is usually a single break in the ring, or a spur with a joint that has failed.
- **Test at each socket in turn** with a socket tester or a multimeter.
- **A break in the neutral** shows up as a socket that tests live but will not power a lamp, and a reversed polarity. Test with a lamp on a known good supply.

## Flickering lights

| Cause | Test |
| --- | --- |
| Loose lamp holder | Switch off and check, look for heat and discolouration |
| Loose terminal in a ceiling rose | Check for heat marks and buzzing |
| LED lamp with the wrong dimmer | Change the dimmer or the lamp |
| Overloaded ring with a heater | Move the heater to its own circuit |
| Failing LED driver | Replace the lamp |
| Loose neutral in the board | Torque check by an electrician |

- **A light that flickers when a large appliance starts** means a loose connection somewhere on that circuit. It is not the appliance.
- **Never leave a flickering light.** It is a sign of a hot joint, and hot joints cause fires.

## Outside and workshop circuits

- **Every outside socket needs an RCD**, and a weatherproof cover with a lid that closes.
- **Sockets in a workshop need a metal enclosure and a tough flex**, and a socket at 1.5 m for the machine and one at 0.5 m for the vacuum.
- **Any socket within 1.5 m of a sink needs an RCD**, and a 30 mA one.
- **A cable run across a yard** should be in a pipe or on a cable ramp. See [[setting-fence-posts]] for how to set posts without hitting a buried service.
- **Check where the services are** before you dig. See [[underground-pipe-and-trenches]].

## Insulation resistance testing

- **The test is called an insulation resistance test, and it needs an insulation tester, not a multimeter.**
- **Test between the conductors and earth, with the circuit isolated**, and read the insulation resistance. Anything under 1 megohm on a lighting circuit is a fault.
- **A good electrician does this every few years and leaves you the readings.** Keep them.

> **Test, do not guess.** A meter with a battery in it and a pair of probes is the best money you will spend on the farm.
""",
    },
    {
        "slug": "solar-and-battery-storage",
        "title": "Solar panels and battery storage off the grid",
        "category": "survival",
        "summary": "Sizing a panel and a battery for the shed, the fence or the whole yard, and the losses nobody mentions until winter.",
        "author": "Nadia, plot",
        "difficulty": "medium",
        "read_minutes": 7,
        "tags": "solar,panel,battery,off grid,charge,inverter",
        "body": """Solar on a farm is not hard, but the arithmetic matters more than the hardware. Get the sizing wrong and you have an expensive battery that is empty in January.

## The numbers

| Fact | Figure |
| --- | --- |
| Peak sun hours, UK summer | 4-5 a day |
| Peak sun hours, UK winter | 1-2 a day |
| Yearly average, UK | 2.5-3.5 a day |
| A 200 W panel | 800 Wh a day in summer, 300 Wh in December |
| Panel efficiency | 15-22% for the good ones |
| Charge controller losses | 5-15% |
| Battery round trip | 85-90% |
| Inverter losses | 3-5% |
| Self-discharge of a lead acid battery | 3-5% a month |

- **Rule of thumb: a 200 W panel gives about 1 kWh a day in a British summer and 0.4 kWh in midwinter.** Size for the winter if the load is critical.
- **The 5 peak sun hours a day figure is a summer sales number.** The winter figure is 1, and that is the one that matters for a fence charger or a water pump.

## Sizing the load

| Appliance | Watts | Hours a day | Wh a day |
| --- | --- | --- | --- |
| LED lamp | 8 | 4 | 32 |
| Fence charger | 20 | 24 | 480 |
| Small water pump | 250 | 1 | 250 |
| Freezer (old) | 150 | 12 | 1,800 |
| Freezer (modern) | 60 | 12 | 720 |
| Wi-Fi router | 8 | 24 | 192 |
| CCTV camera | 10 | 24 | 240 |
| Workshop light | 40 | 2 | 80 |

- **A fridge or freezer is the killer.** A chest freezer is a big battery with a plug. See [[water-in-the-fuel]] for the same idea with a tractor.
- **A modern freezer on a solar system is a 3-4 day battery.** An old one is a 10 day battery.

## Sizing the array

    Panel watts = (daily Wh x 100) / (peak sun hours x 1000)

- **Add 30% for the losses** in the controller, the battery and the inverter, and round up to the next panel size.
- For a 1,800 Wh a day freezer in winter at 1.5 peak sun hours: (1,800 x 1.3) / (1.5 x 1000) = 1,560 W of panel, so four 400 W panels. See [[battery-capacity-and-charging]] for the arithmetic.

## Sizing the battery

    Battery Ah = (daily Wh x days of autonomy) / (battery volts x depth of discharge x inverter efficiency)

- **Depth of discharge** is 0.5 for a lead acid battery and 0.8 for lithium. A lead acid battery kept above 50% lasts far longer.
- **Days of autonomy** is 3 for something that can wait, 5 to 7 for a freezer or a medical device, and 10 for a house.
- For a 1,800 Wh a day load, 5 days, a 12 V battery at 50% depth and 90% efficiency: (1,800 x 5) / (12 x 0.5 x 0.9) = 1,667 Ah. That is a big bank of flooded batteries.

## Choosing the batteries

| Type | Life | Notes |
| --- | --- | --- |
| Flooded lead acid | 3-5 years | Cheap, needs a ventilated shed, must be kept full |
| Sealed lead acid (AGM) | 3-5 years | No watering, needs a decent charge, hates heat |
| Gel | 4-6 years | Good in a cold shed, charges slowly |
| Lithium | 10-15 years | Light, no maintenance, expensive, needs a lithium charge controller |
| LiFePO4 | 10-15 years | The safest lithium, keeps a charge in the cold |

- **Cold kills lead acid.** A battery at 0 degrees C will not take a charge properly. Keep the battery room above 5 degrees C, or use lithium.
- **Heat kills them faster.** Keep them out of a hot tin shed in July if you can. See [[venting-the-workshop]].

## Controllers and inverters

- **The charge controller is not optional.** A panel without one will boil the battery dry.
- **MPPT controllers** give 10-30% more energy than the cheap PWM ones, and they are worth it if the panel is in a shaded yard.
- **The inverter must match the battery.** A 12 V inverter on a 24 V battery will not work properly, and a pure sine wave inverter is needed for sensitive equipment like a laptop, a fridge or a welder.
- **Never run a welder off an inverter.** A welder needs a big peak current. Run it off the tractor or a generator.

## Practical notes

- **Put the panels where they see the sun from 9 am to 3 pm** with no shade from the barn or the trees. A tree that grows into the panels halves the output.
- **Angle them for the latitude**, roughly 52 degrees in the UK, facing south, and adjust seasonally.
- **Keep the cable run short.** Every metre of cable costs you current. Use 4 mm2 or 6 mm2 for the panel to battery run.
- **A battery box on the north wall of the shed, in shade, is the right place.** See [[building-a-shed]] for the shed itself.
- **A small wind turbine** with a big battery can beat solar in a windy site, and costs more.

> **Buy the panels and the controller, and borrow the battery.** The panels are the cheap, reliable part. The battery is the expensive part that dies, and you can defer that bill.
""",
    },
    {
        "slug": "building-a-step",
        "title": "Building steps that do not wobble",
        "category": "workshop-timber",
        "summary": "Rise, going, the two times rise plus going rule, foundations, and making a set of steps that lasts fifty years.",
        "author": "Wes, workshop",
        "difficulty": "medium",
        "read_minutes": 6,
        "tags": "steps,stair,concrete,footing,building",
        "body": """Steps are the easiest thing on a farm to build badly and the first thing that hurts somebody. Two numbers decide everything: the rise and the going.

## The numbers

- **Rise** is the height of one step, going up.
- **Going** is the depth of one step, measured from the front of one to the front of the next.
- **2 x rise + going = 630 mm** is the comfortable rule for a farm building.
- **Rise 170-200 mm** and **going 250-280 mm** is the usual range.
- **A going of less than 250 mm** is a trip hazard, especially with a barrow, a bucket or a full feed sack.

| Rise | Going (2R + G = 630) | Use |
| --- | --- | --- |
| 150 mm | 330 mm | Easy, public buildings |
| 175 mm | 280 mm | Farm buildings, good |
| 200 mm | 230 mm | Steep, only for a loading yard |
| 225 mm | 180 mm | Too steep, avoid |

## How many steps

    Number of steps = total rise / rise per step

- **A 900 mm rise with 180 mm steps** is 5 risers, and you need 4 treads if the top and the bottom are both floors.
- **A door step has one tread.** A flight of steps has one fewer tread than it has risers, because the top floor is the last tread.
- **Always measure the total rise before you design anything**, from the finished floor to the finished floor, and add the thickness of the finish.

## Building them

### Concrete steps
1. **Dig the footing.** A step needs concrete down to 600 mm below the lowest level, or below the frost line, whichever is deeper. See [[mixing-concrete]].
2. **Form the shape** with shuttering board and stakes. Get the top level right before you pour.
3. **Pour the base slab** 100 mm thick, compacted, with a polythene sheet over the hardcore.
4. **Build the risers** on top, one at a time, checking the height of each with a level and a tape.
5. **Order of work:** always work from the bottom up, and each step needs the one below to be cured first.
6. **Float the top** with a float and a trowel, and brush it rough so it is not slippery.
7. **Cure it** under a sheet for three days. See [[compost-heap]] for the logic of keeping it damp.

### Block or brick steps
- **A concrete block 440 x 215 laid on edge** gives a rise of 215 mm with a 100 mm mortar joint, or 150 mm with a 65 mm joint. Two courses make 300 mm.
- **Bricks on edge** give a rise of 100 mm with a 10 mm joint, so a 200 mm rise is two bricks.
- **Build the cheeks** (the sides) first, in the right shape, and fill the middle with concrete or hardcore.

## Details that matter

- **A nosing on each step.** The front edge should overhang by 25-30 mm and be rounded or bullnosed. It stops people catching their toe and it stops the concrete breaking off the front.
- **A handrail** if the drop is more than 600 mm. A single rail at 900 mm, or a rail and a second one for a public building.
- **Non-slip.** Rough finish, or a slip-resistant coating, or grating on industrial steps. Wet concrete is dangerous.
- **Drainage.** A fall of 1 in 60 across the step, and a channel or a gravel bed at the bottom.
- **Keep the edges clear.** A step in the middle of a doorway is a trip. Put it where the door swings to one side.
- **A gate step** must be load bearing, because a gate post puts a lot of weight through the corner.

## Loads

- **A person** is 100 kg.
- **A full feed sack** is 50 kg, a barrow of potatoes 200 kg, a small trailer wheel 300 kg.
- **A farm step should be rated for a barrow and a sack**, so a 150 mm slab on a proper footing, not a slab on the ground.

> **Get the rise right and people will use the steps without thinking. Get it wrong and somebody will fall.** Measure twice, and write the numbers down.
""",
    },
    {
        "slug": "chemical-storage-on-the-farm",
        "title": "Chemical storage on the farm: poisons, fuels and the shed corner",
        "category": "survival",
        "summary": "Where to keep herbicides, pesticides, fertiliser, fuels and veterinary medicines, what has to be separated, and why a locked cupboard beats a locked shed.",
        "author": "Priya",
        "difficulty": "easy",
        "read_minutes": 8,
        "tags": "safety,chemicals,pesticide,storage,fuel,fertiliser,locked",
        "body": """A farm chemical store is the one place on the farm where a mistake kills somebody without an obvious culprit. The rules are mostly about separation, labels and temperature, and they are simple to follow.

## The rules that matter

- **Keep chemicals locked away**, in a purpose-built or adapted store, with the door locked. See [[spraying-safely]].
- **Keep the label.** An unlabelled container is a poison with no instructions and no owner.
- **Keep the original container.** Never decant a chemical into a milk bottle or an old tea urn.
- **Never mix two chemicals** unless the label says to. See [[spraying-and-weed-control]].
- **Wash out the empty container three times** and use the rinse water on the target crop, exactly as the label says.
- **Take the empty containers to a licensed disposal point.** Do not bury them or burn them.

## What has to be kept apart

| Store | What goes in | Why |
| --- | --- | --- |
| Chemical store | Herbicides, pesticides, fungicides | Locked, bunded, ventilated, no heat |
| Fertiliser store | Nitrogen, potash, urea | Away from moisture, off a damp floor |
| Fuel and oil store | Diesel, petrol, oil, old fuel | Bunded, ventilated, no ignition sources |
| Veterinary store | Medicines, vaccines, wormers | Cool, dark, locked, separate from feed |
| Feed and food store | Meal, hay, seed, additives | Separate from every chemical |
| Milk and food store | Milk, meat, eggs, vegetables | Nothing chemical within reach of it |

- **Never store fertiliser and fuel in the same building.** A fertiliser fire is violent and a fuel fire in a chemical store takes the whole shed.
- **Keep the animal feed store and the chemical store apart**, always. A spilled feed additive that looks like a feed is how animals get dosed by accident. See [[calf-rearing]].
- **Medicines away from feed and away from the milk.** See [[vaccinating-and-cold-chain]] for the cold chain.

## The chemical store itself

- **A building with a door that locks, a window that opens, and a roof that does not leak.**
- **Bunded** - a floor and kerb that will hold the whole contents. See [[water-tank-size]] for the arithmetic on how big a bund should be.
- **Ventilated**, so the vapour does not build. A fan is better than a propped door, because a propped door defeats the lock.
- **No heat, no naked flame, no sparky switchgear.** A light on a pull cord is the safe way to light a chemical store.
- **A sink or a bucket of sand** for dealing with a spill. Sand, not sawdust - sawdust can be made worse by some chemicals.
- **A phone and a list of what is inside**, for the fire brigade. A list on the door, not in a drawer.
- **A warning sign on the door.**

## Fertiliser

- **Keep it dry.** Nitrate fertiliser cakes in the bag and then goes hard, and it is much easier to handle in a good condition.
- **Store it off the ground**, on pallets, so it does not pick up moisture from the slab.
- **Keep it away from anything acidic or alkaline.** Urea and ammonium nitrate are the two to be careful with.
- **Do not smoke in a fertiliser store**, and keep the heap well away from the building.
- **Wash your hands and face** after handling it. See [[manure-and-slurry]] for the wider nitrogen picture.

## Fuel, oil and paints

- **Bund the diesel tank.** 110% of the biggest container inside, or a third of the total if there is more than one. See [[water-tank-size]].
- **A fire extinguisher** rated for fuel, and a shovel of sand. See [[hot-work-and-fire-safety]].
- **No smoking, no welding, no grinder** anywhere near an open fuel container. See [[welding-safety-on-the-farm]].
- **Keep oil drums away from the door** so a leaking drum does not put a slick in the exit.
- **Collect old oil and fuel** for a proper recycler. It is illegal to put it down the drain.

## Veterinary medicines

- **Follow the cold chain.** Most vaccines need 2-8 degrees C, and a shed that is 30 degrees C in August is a shed full of worthless vaccine. See [[vaccinating-and-cold-chain]].
- **Use a fridge with a thermometer** and a data logger if the medicine is valuable.
- **Keep a written record of every treatment**: animal, date, dose, withdrawal period. See [[mastitis]] and [[drug-withdrawal-period]].
- **Withdraw the milk and the meat** for the full withdrawal period, every time, and write the date down. See [[cooking-temperatures]].

## A quick check of the store

- [ ] The door locks and the key is not in the door.
- [ ] Every container is labelled and in its original container.
- [ ] The chemicals, the fuel, the fertiliser and the feed are in separate places.
- [ ] The bund is intact and the floor is clean.
- [ ] The ventilation opening is clear.
- [ ] The list of contents is on the door.
- [ ] The fire extinguisher is in date and the sand is clean.

> **If you can read a label, you can use a chemical safely. If you cannot, it does not belong in your shed.**
""",
    },
    {
        "slug": "portable-power-and-generators",
        "title": "Portable power: generators, inverters and safe use",
        "category": "survival",
        "summary": "Choosing between a generator, an inverter and a battery, sizing them for the job, earthing them, and running one without it killing somebody.",
        "author": "Wes, workshop",
        "difficulty": "medium",
        "read_minutes": 8,
        "tags": "generator,inverter,battery,power,earthing,solar,workshop",
        "body": """A generator is the easiest way to have power in a field, and the easiest way to be electrocuted. The rules below are not fussy - they are the difference between a tool and a fatality.

## Choosing the source

| Source | Best for | Limit |
| --- | --- | --- |
| Petrol generator | Welding, power tools, anything high power | Noise, fumes, fuel |
| Diesel generator | Running for days, low running cost | Heavy, noisy, needs a fuel store |
| Inverter generator | Sensitive electronics, camping, a workshop | Lower peak power, more expensive |
| Battery with inverter | Low and medium power, silent, indoors | Needs charging, limited output |
| Solar and battery | Slow, steady power, off grid | No power at night unless you have a big battery |
| Tractor PTO generator | Farm power, already have the engine | Needs a PTO, see [[hitching-and-towing]] |

- **Size it for the starting current, not the running current.** A motor that draws 2 amps running can draw 15 amps for a second when it starts. See [[electrical-power]].
- **A small generator cannot start a big motor.** If you are running a welder, a compressor or a saw, buy twice the size you think you need.
- **An inverter generator** gives a steady sine wave, which is what a laptop, a radio or a fuel injection pump wants. See [[single-phase-power]].

## Running a petrol generator

- **Outdoors, always.** A generator in a shed or a garage will kill you, and so will one in the back of a van with the doors open. See [[working-alone-and-emergency]].
- **At least 2 metres from any opening** - windows, doors, vents - and never in a porch or a lean-to.
- **Point the exhaust away** from the door you are working through and away from the animals.
- **Let it cool before you refuel or move it.** A hot exhaust and petrol vapour is the classic fire. See [[hot-work-and-fire-safety]].
- **Do not run it in the rain.** If you must, put it under a proper canopy, not a tarpaulin that traps the exhaust.
- **Check the oil before you start it.** Most small engines die of no oil, not of bad fuel.
- **Let it run to cool before you shut it off**, unless the manual says otherwise.

## Earthing, and the earth rod

- **The earth rod goes in the ground, not in the shed.** See [[earthing]].
- **A 1.5 metre rod, driven into the ground**, with a clamp and a proper earth cable. See [[earth-clamp-tyres-and-leads]].
- **A generator on rubber feet is not earthed.** That is what the earth rod is for.
- **Test the earth rod** with an earth resistance tester, or at the very least with a continuity check, before you trust it.
- **Never back-feed a generator into the mains** without a proper changeover switch and a qualified electrician. See [[three-phase-and-single-phase]].

## Connecting up

- **Use the sockets on the generator first**, and only run an extension lead out of one of them.
- **Extension leads are rated by their full length and their load.** A 2.5 mm lead is fine for a light tool; a heater or a welder needs 6 mm. See [[cable-voltage-drop]].
- **Coil the lead up if you do not need the length.** A long lead coiled up does not get hot, and a hot lead is a fire waiting. See [[heat-loss-through-a-wall]] for why heat is the enemy of everything electrical.
- **Keep the leads off the ground and out of the water.** A trip in the mud with a live lead is a hospital trip.
- **RCD on everything.** A plug-in residual current device on the lead is the cheapest insurance in the shed. See [[electrical-fault-finding]].

## Batteries and solar

- **A battery is not a generator.** It gives you what you put in, and when it is empty you have nothing. See [[battery-capacity-and-charging]].
- **Size the battery for the load, not for the label.** A 100 Ah battery gives about 500 Wh, which is an hour of a 500 W tool. See [[solar-array-output]].
- **Keep batteries above freezing** and out of direct sun. See [[battery-capacity-and-charging]] for the arithmetic.
- **Equalise and keep them charged.** A battery left at half charge for a year will be scrap.
- **Lead acid and lithium are not the same.** Lithium is lighter, holds more charge and lasts longer, but it needs a matched charger with the right chemistry setting. See [[three-phase-and-single-phase]] for the electrical side.

> **A generator is a machine that makes electricity and carbon monoxide, close to you.** Keep it outside, keep it earthed, and keep the leads dry.
""",
    },
    {
        "slug": "scales-and-weighing",
        "title": "Scales and weighing: pigs, feed, trailers and the yard",
        "category": "workshop",
        "summary": "Which scale for which job, how to keep a platform scale honest, how to estimate weights in the yard, and how to write down a weight so it means something.",
        "author": "Ruth",
        "difficulty": "easy",
        "read_minutes": 7,
        "tags": "scales,weighing,pigs,feed,trailer,yard,records",
        "body": """Every animal and every feed ration comes down to a weight, and a farm that does not weigh is guessing. Weighing does not have to be expensive, but it has to be honest.

## Which scale for which job

| Scale | Use | Range |
| --- | --- | --- |
| Platform scale | Weighing pigs, sheep, small calves, feed sacks | 300-500 kg |
| Crush scale | Weighing cattle in the race | 500-1500 kg |
| Weighbridge | Trailers, loads, the whole farm | 5000 kg and up |
| Hanging scale | Hanging a lamb, a chicken, a bundle | 20-50 kg |
| Bucket and feed scale | Flour, seed, feed, fertiliser | 1-30 kg |
| Livestock scale with a head gate | Daily weight gain on pigs and lambs | 300 kg |
| Spring balance | Hanging a gate, a bale, a bird | 100-500 kg |

- **For daily weight gain** you need a scale you can move, and a pen that does not move the animal. See [[average-daily-gain]].
- **For feed conversion** you need the same scale for the feed and the animal. See [[feed-conversion-ratio]].

## Keeping a scale honest

- **Check it against a known weight** at the start of the season. A 25 kg bag of fertiliser is a good standard, and so is a bag of feed.
- **Weigh the standard twice a year** and write the result down. A scale that has drifted is worse than no scale.
- **Level it.** A platform scale on a slope reads wrong. See [[levelling-a-yard]].
- **Keep it clean and dry.** Mud and dung and straw under the platform change the reading.
- **Zero it** before each use if it is a hanging scale, and never weigh an animal that is standing on someone else's results.
- **Do not weigh a full sow on a scale she is trying to escape from.** You will get a number and a vet's fee.

## Weighing in the yard

- **Weigh the empty trailer, then the loaded trailer.** Difference is the load. Use the same trailer, the same tyres and the same level ground. See [[trailer-brakes-and-lights]] for the roadworthiness side.
- **Do not move the vehicle between the two weighings** if you can avoid it. A different load on the springs changes the reading.
- **Weigh at the same point on the run-in** for both. A few metres of difference matters on a slope.
- **For a rough estimate**, a full 25 kg sack of feed is 25 kg, a barrow of potatoes is about 200 kg, and a full bale of straw is about 350 kg. See [[conversion-tables]].

## Records that mean something

- **Write the weight, the date, and the animal ID** in the same line. A weight without an animal is a number in a book.
- **Keep the records where the animal is.** A clipboard in the shed beats a memory in January. See [[body-condition-scoring]].
- **Weigh at the same point in the cycle** - the same age, the same time of day, the same feed. A pig weighed at 8 am on Tuesday and 4 pm on Wednesday is not a comparison.
- **Do not round to the nearest 5 kg** on a scale that reads to 1 kg. The precision is the point.

| Job | Weighing interval | Why |
| --- | --- | --- |
| Piglets after weaning | Weekly for 6 weeks | Catch the ones that fall behind early |
| Growing pigs | Every 2 weeks | Plan the feed and the sale date |
| Ewes | At tupping and 4 weeks before lambing | Body condition, and then lambing weight |
| Calves | At birth, then monthly | Growth rate and the check for illness |
| Layers | Every 4 weeks | See [[hen-egg-production]] |
| Grain in the store | At filling, and monthly | See [[grain-storage-mass]] |
| Hay and silage | As it comes off the field | To work out how much you have |

## The small stuff

- **A spring balance for the poultry house** tells you the weight of a bird in seconds, and it is the difference between selling a bird at 2 kg and at 2.4 kg.
- **Weigh the feed bag when it is opened** and write it on the sack. It is the easiest habit on the list.
- **Mark the tare on the hopper.** A feed bin that is 200 kg empty and 900 kg full is a useful thing to know.

> **Weigh it, write it down, and do it the same way each time.** A number that was measured properly beats a number that was estimated, every time.
""",
    },
]
