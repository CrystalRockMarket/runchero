"""Extra notes for the farming shelves: soil, crops, water and small tools."""

from __future__ import annotations

NOTES: list[dict] = [
    {
        "slug": "compost-heap",
        "title": "Building a compost heap that actually heats",
        "category": "farming-soil",
        "summary": "A hot compost heap needs the right size, the right mix and the right turning. Get those right and it will cook in a fortnight.",
        "author": "Priya",
        "difficulty": "easy",
        "read_minutes": 6,
        "tags": "compost,manure,soil,waste,organic matter",
        "body": """Compost is the one thing a farm makes that is worth more than it costs. A good heap turns garden waste and dung into something that changes the ground in a year.

## Size matters more than anything else

- **Make it at least a metre cube, and two metres by two metres by one metre is better.** A small heap loses more heat through the sides than it makes in the middle. A tiny heap will never get hot.
- **It needs to be big enough to hold its heat and small enough to turn.** Above about 5 cubic metres you need a front loader to turn it.
- **Site it on soil, not on concrete.** It needs to drain, and the worms like to get in from the bottom.

## What goes in

The rule is balance: half the volume brown and dry, half green and wet.

| Brown, dry | Green, wet |
| --- | --- |
| Cardboard, torn | Grass clippings, fresh |
| Straw, hay, stalks | Vegetable peelings and tops |
| Small branches, shredded | Manure, fresh from the yard |
| Coffee grounds | Weeds that have not gone to seed |
| Egg shells, crushed | Spoilt milk |

- **Cut everything small.** The smaller the pieces, the bigger the surface area the bacteria can get at, and the faster it works.
- **A compost heap is not a bonfire.** If it is properly mixed it never burns. If it is all dry straw it will just sit there and go grey.
- **Nothing cooked, no meat and no dairy** unless you have a very good system for it. Cooked food and dog mess attract rats.

## Water and air

- **Squeeze test.** A handful of the mix should feel like a wrung-out sponge: damp, but no water coming out of it.
- **If it is dry, water it.** If it is dripping, mix in dry material.
- **Air comes from turning.** Turn the heap when the middle is hot and the outside is cold. That is usually every two to three weeks in summer.
- **A heap that smells of nothing** is too dry or too wet. **A heap that smells of sour ammonia** has too much green material and not enough carbon.

## Reading the heap

- **A hand in the middle should be comfortably warm.** If you can keep your hand in it, it is over 50 degrees C and the weeds in it are dead.
- **A heap that never heats** is almost always the wrong size, too dry, or too woody.
- **Straw that has been eaten and left as a fine brown material** is what success looks like. It should be dark, crumbly and smell like a forest floor.

## Using it

- **Let it finish before you use it.** Six to eight weeks in summer. If you cannot get your hand into it and it will not heat any more, it is ready.
- **Screen it** if you want a fine compost for seedbeds. A screen is a frame of chicken wire on four posts.
- **Use it as a mulch around the plants** you want to protect from frost, or work it into the top few centimetres of soil.
- **Keep a working heap and a maturing heap.** The one you are building and the one that is finishing. Otherwise you are always putting fresh material on top of stuff that was not ready.

> **Do not put fresh manure straight onto a growing crop.** It will burn the roots and it will bring in every weed seed in the yard. Compost it first.
""",
    },
    {
        "slug": "manure-and-slurry",
        "title": "Manure, slurry and how to get the value out of it",
        "category": "farming-soil",
        "summary": "Farm manure is the cheapest fertiliser there is. The value depends entirely on how it is stored, spread and timed.",
        "author": "Marta, arable",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "manure,slurry,dung,nitrogen,fertiliser",
        "body": """A yard full of manure is either an asset or a liability, and the difference is entirely in the management.

## What is actually in it

| Type | Dry matter | Typical N content | Best use |
| --- | --- | --- | --- |
| Cattle, fresh | 20-25% | 4-5 kg per tonne | Too fresh. Compost it first. |
| Cattle, well made | 30-35% | 6-8 kg per tonne | Autumn on grassland |
| Pig, fresh | 15-20% | 7-9 kg per tonne | Very strong. Use with care. |
| Poultry, fresh | 25-30% | 10-14 kg per tonne | As a top dressing, in small amounts |
| Slurry | 5-10% | 3-6 kg per cubic metre | Grass, autumn, with a injector |

The numbers vary wildly with the feed and the bedding. **Always test if you are making a big change** - a heap of poultry manure applied as if it were cattle manure will scorch a field.

## Storage is where the value leaks

- **Cover the heap.** Rain falling on manure washes out the nitrogen and leaches the fine material. A roofed yard or a covered heap keeps most of it.
- **Keep it out of the runoff.** Manure in a gutter that runs into a ditch is money in the water.
- **Compact it.** A loose heap loses air and goes anaerobic, which means it rots and smears instead of composting.
- **Add straw.** Straw is the carbon that makes the heap work. Without it the manure goes slimy.

## Spreading

- **Spread evenly.** Cakey patches of manure grow crop unevenly and the grass over them will scorch.
- **Do not spread on frozen or very wet ground.** It will run off, and the nutrients go with it.
- **Use an injector for slurry** on grassland if you can. It puts the nitrogen into the soil instead of letting it evaporate into the air.
- **Do not spread slurry before heavy rain.** The field will be bare and the soil will be saturated, which is exactly the wrong combination.
- **Respect the buffer zones.** At least 10 metres from a watercourse, and more on a slope.

## Timing

- **Autumn on grassland** is the classic answer. The nitrogen is there for the grass in spring and the ground is soft enough to take the weight.
- **Before ploughing** on arable land, if the manure is well made and the soil is not too wet.
- **Never on growing crops with fresh manure** in the spring. See [[compost-heap]].
- **Do not lime and spread slurry on the same field at the same time** without thinking about it. See [[soil-ph-and-lime]].

## Testing

- **Test the nutrient value once a year** if you spread a lot. A laboratory analysis of a composite sample is cheap against the value of the spread.
- **Keep a field map.** Record what went where and how much. After three seasons you will know which fields do not need it.

> **Never spread manure or slurry in the rain.** Run-off from a field is a pollution incident and it will land on you whether you were ready for it or not.
""",
    },
    {
        "slug": "soil-tilth-and-earthworms",
        "title": "Tilth, earthworms and the structure of a healthy field",
        "category": "farming-soil",
        "summary": "A handful of soil will tell you more about a field than any bag of fertiliser. Learn to read it.",
        "author": "Priya",
        "difficulty": "easy",
        "read_minutes": 5,
        "tags": "soil,tilth,structure,earthworms,organic matter",
        "body": """Fertiliser feeds the plant. Soil structure feeds the roots. A field with good tilth holds water, air and nutrients at the same time, which is the whole job.

## What tilth actually is

Tilth is the crumb structure of the topsoil - small aggregates held together by fungal threads and root exudates, so the soil behaves like a sponge rather than like a block.

- **Good tilth:** a handful squeezes into a ball and breaks apart with a tap. It crumbles in the hand. It is dark, smells of earth, and has visible organic matter in it.
- **Poor tilth:** a handful either will not hold together at all, or holds together like a lump of plasticine and smears. It is pale, blocky and has no life in it.
- **Compacted soil:** see [[soil-compaction]] for finding the hardpan underneath.

## Read it with a spade

Dig a hole 30 cm deep in a representative place - not the headland, not the gate.

1. **Look at the colour.** Dark at the top fading down means organic matter is where it should be.
2. **Look at the roots.** Roots should branch freely through the profile. If they run sideways at a fixed depth, there is a pan. See [[soil-compaction]].
3. **Count the earthworms.** In a healthy field you will find a dozen or more in a spadeful of the top 15 cm. In a poor one, none.
4. **Squeeze it.** Sand feels gritty, clay feels sticky, loam feels like a squeezed sponge.
5. **Drop it.** A clod that falls apart when you drop it from waist height has structure. One that lands as a lump does not.

## Earthworms do the work for you

- **Worms channel the soil.** Their burrows are drainage and aeration, and they are bigger than anything a tillage machine makes.
- **Worms pull organic matter down.** They eat crop residue and drop it as castings at depth.
- **No worms means no structure.** You cannot cultivate your way into tilth. If there are no worms in the top 15 cm, the field has a problem that is not about nitrogen.

## Building tilth

- **Organic matter.** Every year, in some form: manure, compost, roots, cover crop. See [[cover-crops]] and [[manure-and-slurry]].
- **Green manures.** A grass-clover ley left for two years rebuilds a soil that has been ploughed for thirty.
- **Roots.** A cover crop with deep roots opens the soil and leaves channels behind.
- **Do not cultivate when it is wet.** This is the single biggest cause of lost tilth. See [[setting-plough-depth]].
- **Varied rotations.** A monoculture builds the same structure every year and wears it out.

## The test that matters

Dig the same hole in the same place every spring and take a photograph of it. Put a ruler in the frame. After three years the difference between the top and the bottom of the frame is worth more than most of the advice in this book.

> **Do not judge a field by its crop alone.** A field that looks thin in a dry year may have the best structure on the farm. Dig it.
""",
    },
    {
        "slug": "crop-rotation-planning",
        "title": "Planning a rotation that breaks the cycle",
        "category": "farming-crops",
        "summary": "The same crop on the same ground year after year builds up disease and weeds. A rotation breaks the cycle and it costs nothing.",
        "author": "Marta, arable",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "rotation,crops,planning,disease,weeds",
        "body": """A rotation is simply the plan for which crop follows which on each field. Done well it is the cheapest soil and disease control you will ever buy.

## What a rotation actually breaks

| Problem | Broken by |
| --- | --- |
| Cereal root diseases (take-all, eyespot) | A non-cereal break: beans, brassicas, grass |
| Grass weeds (blackgrass, wild oat) | A ploughed or cultivated break crop |
| Onion fly and carrot fly | A three to four year break from the same family |
| Potato blight and eelworm | Four years out of potatoes |
| Clubroot in brassicas | Seven years between brassicas |
| Pea and bean weevil | Two to three years between peas and beans |

## A simple four-course rotation

1. **Winter wheat**
2. **Spring beans or a ley**
3. **Spring barley**
4. **A ley or a break crop, or potatoes**

Then repeat. The order matters more than the crops: put the most demanding crop after the fertility-building one, and keep the cereals apart.

## Break crops worth considering

- **Legumes.** peas, beans, lucerne, clover. They fix nitrogen and leave the ground in better condition than a cereal.
- **Grass leys.** Two or three years of grass is the strongest soil builder available on an arable farm, and it will grow a lot of hay on poor ground.
- **Brassicas.** Good break crops, but they bring their own problems, and clubroot is permanent in the soil. See [[spraying-and-weed-control]].
- **Maize.** A great crop for silage but it is a cereal in every way that matters for disease. See [[maize-for-silage]].
- **Potatoes.** A good break but they take the ground out of the rotation for four years. See [[potatoes-field-to-store]].
- **Fodder crops.** Swedes, kale, lucerne and forage rape are all good breaks and all feed the animals.

## Planning it

1. **List every field**, with its size, soil type, drainage and any history you know of.
2. **List the crops you actually need** - what feeds the animals, what you sell, what the rotation needs.
3. **Draw the rotation out on paper.** One row per field, one column per year. It is easier to see the clash on paper than in your head.
4. **Check the family groups** so nothing comes round too soon.
5. **Put a break in before a bad year.** If a field had take-all this year, it should not carry wheat next year.

## Keep it flexible

- **Plan two years ahead, revise one year ahead.** Long plans break; keep the near years firm and the far ones loose.
- **Keep a field map.** Every crop, every year, with the date and the rate. Three seasons of records and you will know what your ground actually does.
- **Write the plan down** and put it somewhere you will find it in January.

> **A rotation only works if you break it.** The most common reason a rotation fails is that a field that should have been a ley got ploughed because there was a bad price one year.
""",
    },
    {
        "slug": "spring-barley",
        "title": "Spring barley: sowing, spraying and harvest",
        "category": "farming-crops",
        "summary": "Barley is the forgiving cereal that turns into a bad crop for about six different reasons. Here they are in the order they happen.",
        "author": "Marta, arable",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "barley,sowing,spraying,harvest,grain",
        "body": """Barley is more forgiving than wheat about depth and date, and much less forgiving about drainage and blackgrass. Work through it in order.

## Sowing

- **Barley wants a fine, firm seedbed.** Less tilth than wheat - a too-loose seedbed dries out and the seed sits in a pocket with no moisture. See [[setting-plough-depth]].
- **Sow shallow.** 3-4 cm, even shallower on a heavy soil. Barley is a small seed and it uses up its energy getting out of the ground.
- **Do not sow into a cold wet soil.** March sowing into a cold field gives a slow, uneven start. Wait for the soil to warm and for the tractor to be able to leave a rolled print.
- **The seed rate** is between wheat and oats. See [[seed-rate-calculator]]. A typical figure is 250-350 plants per square metre, which on a good seedbed is around 180-220 kg/ha.
- **Roll it.** Barley on a firm seedbed is worth 2-3% of yield.

## Weeds

Barley is sprayed, usually, but it is also the crop where the spraying window is tight.

- **Blackgrass is the one that matters.** By the time you can see blackgrass in a barley crop it is too late to do anything about it. It has to be killed before it comes up, or the crop has to be cut for hay instead. See [[spraying-and-weed-control]].
- **Wild oats** come from the seed, so they come back in patches. There is no herbicide that solves it - only a rotation and a clean seed sample.
- **Volunteer barley** comes from the previous crop. The only answer is to bury the volunteers with a plough and wait.

## Disease and the season

- **The important spray is the early one.** A single well-timed fungicide at growth stage 30-32 is worth more than three late ones.
- **Watch for net blotch** in second barley - it survives on the stubble, so a break from barley in the rotation is the real fix.
- **Ramularia** comes late in a dense, high nitrogen crop with a lot of dead leaf at the bottom. Less nitrogen and a less dense canopy reduce it.

## Harvest

- **Barley ripens unevenly.** The head can be ready while the straw is still green, and in a wet year a lot of the crop will be laid over.
- **Watch the moisture.** Barley for malting is bought on a specification, including the moisture, the germination and the protein. Deliver wet grain and you will be docked. See [[storing-grain]].
- **The straw is worth more than the grain in a bad year.** Do not rush it and do not cut too high.

## When it goes wrong

- **Too thin:** sowing date, seedbed, or a failed establishment from a cold wet start.
- **Lodged:** too much nitrogen, or a wet season on a heavy soil.
- **Full of weeds:** a failed autumn or spring weed control.
- **Poor germination:** stored badly or hit by a hot spell in the drill.

> **Do not spray a crop that is stressed and dying.** It will not recover, you will spend the money, and you may have to deal with the residues.
""",
    },
    {
        "slug": "potatoes-field-to-store",
        "title": "Potatoes from the field to the clamp",
        "category": "farming-crops",
        "summary": "The crop is only made when it is in the store. Harvesting, curing, grading and clamping decide what you actually get.",
        "author": "Ruth",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "potatoes,harvest,clamp,store,haulm",
        "body": """Potatoes are worth more in the clamp than in the field. A good harvest that is handled badly loses a quarter of it in a month.

## Before you lift

- **Stop the growth.** Two weeks before lifting, kill the haulm and let the skins set. The skin set is what stops the potatoes bruising and losing water in the store.
- **Do not lift a wet field.** Wet soil sticks to the crop, carries disease and makes the harvester work harder. Wait for a dry spell.
- **Check the store before you harvest, not after.** Clamp, ventilation, rodents, drainage, and somewhere for the rejected potatoes to go.

## Lifting

- **Set the web height to the size of your crop.** Too low and you take soil in; too high and you leave potatoes in the ground. Start at about 5 cm and adjust.
- **Do not lift potatoes that are too wet.** The skin bruises easily above about 14% soil moisture.
- **Limit the drop height.** Every metre of drop is a bruise. Keep the elevator gentle.
- **Pick the field well.** The potatoes left behind are volunteers for next year, and every one you miss is a weed you have to deal with next year.

## Curing

- **Let them dry before you store them.** Two weeks in the field or in a shed with good airflow, in the dark, so the skins set and any damage heals.
- **Curing is a warm, dry, ventilated spell** of about ten days at 15-20 degrees C. Do not let the temperature get above 25 degrees or the potatoes will go soft and grow sprouts.

## Grading and clamping

- **Grade out the damaged, green and small potatoes.** Green ones are solanine and must not go in the household supply. Small ones will not keep and they will rot the neighbours.
- **Clamp in layers.** Two or three metres deep, so the middle of the clamp does not go anaerobic.
- **Ventilation is everything.** Straw bales on the sides and the ends, a ridge along the top, and ventilation ducts running down the middle of a big clamp.
- **Store in the dark.** Light turns potatoes green and sweet.

## The store

- **Temperature between 7 and 10 degrees C.** Warm stores make the potatoes sprout; cold stores turn the starch into sugar and the chips come out orange and oily.
- **Humidity high, air moving.** 90-95% relative humidity with good air movement keeps the skins from drying out.
- **Check it every week for the first month** and then monthly. Look for a hot spot, for condensation on the roof, or for a smell of rot.
- **Keep the potatoes off the floor** and off the walls, on pallets or a slatted floor with a drainage channel under it.

> **Keep the rejected potatoes away from the store.** A few tonnes of rotting potatoes in the corner will start the whole clamp going.
""",
    },
    {
        "slug": "spraying-and-weed-control",
        "title": "Spraying and weed control without the drift",
        "category": "farming-crops",
        "summary": "Timing beats chemistry. Most poor results from a spray are a timing problem, not a product problem.",
        "author": "Marta, arable",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "spraying,weed control,herbicide,drift,sprayer",
        "body": """A spray is decided long before the nozzle goes on. Variety, timing, weather and drift decide the result.

## The four things that matter

1. **What is actually there.** Identify the weeds before you treat them. A broadleaf spray on a grass crop will hurt the grass as well. Grass weeds in a broadleaf crop need a different product entirely.
2. **Timing.** Most failures are spraying too early or too late.
3. **Conditions.** Wind, temperature and rain.
4. **Application.** Dose, water volume, nozzle and pressure.

## Timing, by weed

| Weed | Best time to treat |
| --- | --- |
| Blackgrass | Before it emerges, or crop the field for hay instead |
| Annual meadow grass | Early, while it is small and actively growing |
| Cleavers | Late, once it has climbed and beaded with water |
| Chickweed | Autumn or early spring, on a leaf |
| Broadleaf weeds in cereals | When they have 4-6 true leaves and are growing |
| Bracken | When the fronds are fully open and before the spores form |
| docks and thistles | As rosettes in the autumn, or in the spring before the flower bud |

## Conditions

- **Wind.** Spraying in a breeze is drift. Most labels say do not spray above 8 km/h. Check the direction and note where you are spraying.
- **Rain.** Most products need 2-6 hours without rain to work. Check the label and the forecast, not the weather at the moment you start.
- **Temperature.** Between about 8 and 22 degrees C. Too cold and the plant is not moving; too hot and the product evaporates before it works.
- **Time of day.** Mid-morning is usually best - the leaves are dry, the wind is light and the plants are photosynthesising.

## The sprayer

- **Calibrate it.** Put a measured amount of water in the tank, spray a measured area, and work out the litres per hectare. A sprayer that is out by 30% is out by 30%.
- **Check the nozzles.** Nozzles wear at the edges of the pattern and you get a striped application. Replace them, do not try to correct it with the pressure.
- **Strain the fill.** A nozzle blocked by a bit of hedge in the tank gives you a stripe down the field.
- **Wash it out properly** after every product. Three buckets of water and the label's instruction, and never let the washings go near a drain or a watercourse. See [[spraying-safely]].

## The sprayer and the operator

- **Keep a spray record.** Date, product, rate, field, weather, operator. Without it you cannot repeat what worked and you cannot prove what you did.
- **Never fill a sprayer from a hose without a backflow preventer on the hose.** See [[spraying-safely]].
- **Wash off before you leave the field** if you can, or at least before you go home.
- **Keep the phone number of the poison centre** in the cab and in the workshop.

> **Never spray in a strong wind to save time.** Drift onto a neighbour's crop or a watercourse is a legal problem and a very expensive letter.
""",
    },
    {
        "slug": "borehole-pump-and-filters",
        "title": "The borehole pump: filters, pressure and winterising",
        "category": "farming-water",
        "summary": "Every water problem on a farm ends up at the pump. Learn the pump, learn the filter, and you will not be guessing at 6am.",
        "author": "Tomasz",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "pump,borehole,water,filtration,pressure",
        "body": """The borehole pump is the single most important machine on the farm that nobody looks after. Everything the animals, the garden and the washing machine need comes through it.

## Know your pump

- **Write down what it is.** Submersible with a pressure control, or a surface pump with a pressure switch. The model number and the serial number, so you can get parts.
- **Know the flow rate.** It should be on the pump or in the paperwork. A typical farm borehole gives 5-20 litres a second.
- **Know the static level and the drawdown level.** Static is the water level when the pump is off. Drawdown is how far the level drops when it runs. A big difference means a low-yielding well or a badly set pump.

## Filters

- **A filter is a consumable.** Change it when it blocks, not when the pump stops. A blocked filter makes the pump run hot and it will burn out.
- **Every filter has a direction arrow.** Flow the wrong way and the element is ruined.
- **Check the filter housing for a bypass valve.** Many filters have one that opens when the filter is too blocked, so the pump still gets water - but dirty water. If you have never changed a filter for years, that valve has almost certainly been open.
- **Keep a spare element on the shelf.** Not "spares for the filter", the actual element for your filter.

## Pressure

- **A low-pressure problem is usually a filter, a partially closed valve, or a leak.**
- **A pressure that goes high and then stops is a blocked filter or a failing pressure switch.**
- **Check the accumulator.** If the pump short-cycles - on, off, on, off - the accumulator has lost its air and the switch is not holding it off. You can often recharge it with a bicycle pump and a Schrader valve.
- **Fit a pressure gauge where you can see it from the yard.** A gauge you have to go and look at is a gauge you will not look at.

## Winterising

This is the part that catches people out in a cold spring.

- **Drain the pipework that is not underground.** Every exposed pipe, every yard hydrant and every animal trough needs draining or a lagging.
- **Insulate the trace pipe** on a lagged pipe, and keep the lagging on. A lag that has been left off since August is the whole problem.
- **The pump house itself** should be above freezing. A pump that has frozen will crack the casing, and a replacement pump is not a cheap morning.
- **Keep the pump house dry and ventilated.** A damp pump house rusts the pipework and the electrics.

## Filtration and the animals

- **Stock water needs to be clean.** See [[water-troughs-and-algae]].
- **A filter on the yard line** is worth every penny, and a cheap in-line filter on the trough line is worth more.
- **Check the water for iron and sulphate once a year.** High sulphate causes diarrhoea that looks exactly like a feed problem. See [[water-troughs-and-algae]].

> **Test the pump before the hot spell, not during it.** Flow drops with a blocked filter and a tired impeller, and the day you find out is the day you need the water.
""",
    },
    {
        "slug": "rainwater-harvesting",
        "title": "Catching rainwater for the yard and the garden",
        "category": "farming-water",
        "summary": "Roofs deliver more water than most farm boreholes, for free. Gutters, a tank and a little plumbing will do it.",
        "author": "Nadia, plot",
        "difficulty": "easy",
        "read_minutes": 5,
        "tags": "rainwater,water,butts,tanks,harvesting",
        "body": """Every roof on the farm is a free water supply, and most of them are being wasted. A 100 square metre roof gives about 200 litres for every millimetre of rain.

## How much you get

| Rainfall | Litres per 100 m2 of roof |
| --- | --- |
| 1 mm | 100 litres |
| 5 mm | 500 litres |
| 10 mm | 1 000 litres |
| 25 mm | 2 500 litres |

A year of rain in the UK is around 700-1 200 mm, so a good roof gives 70 000-120 000 litres a year. That is enough for a garden, a yard of washing, and a lot of animal troughs.

## Where to put it

- **The house roof** is the biggest and cleanest. It gives you water for drinking, for the garden and for washing.
- **The barn roof** gives you water for the yard, for washing down and for the animals.
- **The shed roof** is usually on a tank already, feeding the troughs.

## The setup

- **Gutters:** the right size for the roof, with a proper downpipe and a leaf guard. Most failures are a blocked downpipe, not a hole.
- **The tank:** a purpose-made water tank, a covered IBC container, or a buried tank. Buried is better - it keeps the water cool in summer and stops it freezing in winter.
- **The overflow** must go somewhere sensible. An unblocked overflow will undermine your foundations or wash out your yard.
- **The tap** should be at the bottom, with a ball valve, and something to stop a hose being left running.
- **Screening:** a mosquito screen on the top of the tank and a leaf guard on the gutter. An open tank in summer is a mosquito breeding site.

## Using it

- **Watering the garden:** a hose and a sprinkler. Water in the morning, at the soil, not over the leaves.
- **The animals:** troughs fed from a tank need a float valve. See [[water-troughs-and-algae]].
- **Washing down the yard:** this is where most of the tank water should go.
- **A hosepipe ban** is a good discipline for everyone.

## Keeping it clean

- **Clean the gutters twice a year**, in spring and in the autumn.
- **Scrub the tank** once a year and check the screen.
- **Do not put anything in the tank** - no dead birds, no leaves, no old scaffolding.
- **If the water smells, check for a dead animal in the tank** and clean it out completely.

> **Check the law before you connect it to the house.** In some places using harvested rainwater for drinking is restricted, and in others the rules are surprisingly specific about the pipework.
""",
    },
    {
        "slug": "two-stroke-fuel-mix",
        "title": "Mixing two-stroke fuel: ratios, storage and safety",
        "category": "farming-tools",
        "summary": "Wrong mix is the number one cause of a two-stroke engine dying. The ratio, the shaking and the storage are all simple.",
        "author": "Old Bill",
        "difficulty": "easy",
        "read_minutes": 5,
        "tags": "two stroke,fuel mix,chainsaw,quad,petrol",
        "body": """A two-stroke engine mixes its own oil, but it can only do that with the right fuel already in the tank. Get the mix wrong and the engine smokes, fouls the plug and eventually seizes.

## The ratios

Modern two-stroke engines usually run on a 50:1 mix, or 25:1 for a machine with a separate oil pump. The manual or the side of the engine is the authority - check it.

| Ratio | 1 litre of petrol | 5 litres | 20 litres |
| --- | --- | --- | --- |
| 25:1 | 40 ml | 200 ml | 800 ml |
| 32:1 | 31 ml | 156 ml | 625 ml |
| 40:1 | 25 ml | 125 ml | 500 ml |
| 50:1 | 20 ml | 100 ml | 400 ml |

**The honest advice:** buy the two-stroke oil with the measuring bottle in it and you cannot get this wrong. The small cost of the bottle saves the cost of a cylinder.

## Mixing it properly

1. **Mix in the right order.** Pour the oil into the empty fuel can first, then the petrol on top. If you pour petrol in first, the oil sits in the bottom and does not mix.
2. **Use a proper can with a spout.** Never a jerry can that has had petrol in it and a plug of old fuel in the bottom.
3. **Shake it.** Two minutes of shaking mixes it properly. The oil does not want to mix.
4. **Do not rely on the machine's own bottle.** It is a rough measure and it gets out of step with reality.

## Storage

- **Use fresh fuel.** Two-stroke fuel goes off in about four to six weeks, faster in warm weather. Old petrol separates and the water in it will rust the engine.
- **Keep cans in the shade** and off the ground. Do not store them in the hot metal toolbox on a tractor.
- **Do not store a partly used can of mixed fuel** and top it up later. Start a fresh one.
- **Label the can.** "2-stroke" in marker pen, and the date it was made.
- **Do not keep fuel in the shed.** It is a fire waiting for a spark. A metal cabinet outside the buildings is the right answer.

## What the engine tells you

| Symptom | Likely cause |
| --- | --- |
| Blue smoke | Too much oil, or oil in the petrol |
| White smoke | Fuel getting into the crankcase, or a bad seal |
| Plug oily and black | Too much oil |
| Plug dry and white | Too little oil |
| Engine smokes and will not run | Wrong mix |
| Poor running, loud rattle | Cheap fuel, or a plug that is fouled |
| Engine stops and will not restart | No fuel, or a flooded carburettor |

## The carburettor

- **The float chamber holds the fuel.** If the engine will not run with a full tank and will run with the fuel line disconnected and the inlet open, the float valve is stuck shut.
- **Clean the jets** with a needle and a dab of penetrating oil, and blow them out with compressed air. Never with a wire.
- **Check the float valve** by pouring a little clean petrol in and seeing whether it holds it.

> **Petrol vapour is heavier than air.** Do not run a small engine in a shed with the door shut, and never store fuel next to a hot engine.
""",
    },
    {
        "slug": "sharpening-hand-tools",
        "title": "Sharpening scythes, axes, hoes and knives",
        "category": "farming-tools",
        "summary": "A blunt tool is more dangerous than a sharp one and it does less work. Sharpening is ten minutes and a flat stone.",
        "author": "Nadia, plot",
        "difficulty": "easy",
        "read_minutes": 5,
        "tags": "sharpening,tools,axe,scythe,hoe,knife",
        "body": """Sharpening is the most satisfying job on a small farm and the one most often skipped. A sharp scythe cuts in a third of the passes, tires you out less, and does not throw stones at your legs.

## The tools

**The scythe.** A long, curved blade with a thin, flexible edge.

- Use a **whetstone** for the bevel and a **strop** (a piece of leather with compound on it) for the back.
- Lay the stone flat on the ground, heel of the blade on the stone, and work the edge along the stone in a long sweeping curve. Keep the angle about 20 degrees from flat.
- **Work both sides.** Then use the strop on both sides to remove the burr.
- The edge should be sharp enough to shave hair from your arm.

**The axe.** A short, thick edge.

- Use a **flat file or a coarse whetstone** to get the edge back to shape.
- **Do not sharpen a splitting axe into a felling axe.** A splitting axe needs a thick, wedge-like edge; a felling axe needs a curve.
- A little oil on the blade stops it rusting.

**The hoe and the cultivator.**

- A **file** for a bent or broken edge, then a **whetstone** to sharpen it.
- The blade should be polished bright where it rubs the soil. That is the easy test of a good edge.

**The knife.** A kitchen knife, a harvesting knife, a pocket knife.

- A **honing steel** for a kitchen knife, used at an angle of about 20 degrees, one side then the other.
- A **stone** for a knife that has gone dull.

## Keeping the edge

- **Do not use a tool with a dull edge.** It damages the tool and it is more likely to slip.
- **Wipe the blade clean after use** and put a film of oil on it. Soil left on a blade with a wet edge rusts overnight.
- **Use a wooden handle.** Steel handles slip when they are wet and they blister your hands.
- **Keep a stone in the tool bag.** A small flat stone in your pocket is the difference between a sharp tool and a blunt one.

## Sharpening wheels and files

- **Use a wheel with a fine grade** for a final edge and a coarse one for a lot of metal.
- **Never use a grinding wheel on a scythe or a knife.** The heat kills the temper and the edge rolls.
- **A file only cuts on the pull stroke.** Push it and you are polishing the edge.

> **Do not sharpen a tool with a chip in it that you have not looked at.** A nick can turn into a crack and a cracked axe head is a projectile.
""",
    },
    {
        "slug": "splitting-firewood",
        "title": "Splitting, stacking and drying firewood",
        "category": "farming-tools",
        "summary": "Wood that is green will not burn, will not dry and will not keep the stove in. Three years of drying is the usual answer.",
        "author": "Wes, workshop",
        "difficulty": "easy",
        "read_minutes": 6,
        "tags": "firewood,splitting,stacking,drying,log splitter",
        "body": """Firewood is the one thing on the farm that is free, and the one that is most often wasted. Splitting and stacking are not glamorous, but they decide whether the stove works.

## Choosing and cutting

- **Seasoned wood is best.** Look for grey, cracked bark, and a sound when you knock it with a spade.
- **Hardwood burns longer and hotter.** Oak, ash, beech and birch are all good. Softwood burns fast with a good flame and a lot of smoke.
- **Never burn treated timber, painted timber, or plywood.** The smoke will be poisonous and it will wreck the stove and the flue.
- **Cut the rounds to fit your stove.** A log that will not fit burns on the outside and leaves a carbon core in the middle.

## Splitting

- **Split with the grain.** A maul and a wedge, or a proper splitting axe.
- **Split rounds into quarters rather than splitting them into sticks.** Smaller pieces dry faster and burn better.
- **Get the axe sharp.** A blunt axe bounces off. See [[sharpening-hand-tools]].
- **Split on a block, not on the ground.** You will wreck your back and the axe head.
- **Use a log splitter if you have one.** A hydraulic splitter will split a tonne in an afternoon; an axe will take a week and a bad back.
- **Wear a visor, gloves and steel toe boots.** Splitting wood is one of the few jobs where a piece of steel can genuinely be launched at you.

## Stacking

- **Stack it in the open, with the cut ends facing out** and the top row covered.
- **Never stack firewood inside the house or in a building with a stove or a boiler nearby.** It carries moisture and it brings insects.
- **Stack on pallets or a timber base**, not on the bare ground. Concrete underneath draws the damp out of the bottom of the stack.
- **Leave an air gap at each end** so air can move through the middle.
- **Small pieces in the middle, big pieces on the outside** makes a stable stack that lets the middle dry.

## Drying

- **Seasoning takes time.** Oak and ash want two to three years. Softwood is a year. Pine is a year if it is split small.
- **The split is the whole trick.** A log that is split into quarters dries several times faster than a round of the same size.
- **Cover the top, leave the sides open.** Rain washes the colour out of the wood and it slows the drying.
- **Store it in the sun and the wind**, not in a shed.

## Smoke and chimneys

- **Seasoned wood burns clean.** Green wood makes smoke, soot, creosote and a fire risk in the flue.
- **Have the chimney swept** at least once a year, and more if you burn a lot of wood.
- **Keep the stove pipe and the flue clean.** A metal flue pipe collects creosote and it burns.

> **Never burn anything that is not wood in a wood stove.** Plastic, treated timber, old furniture with melamine and MDF in it all make fumes that will make you ill.
""",
    },
]
