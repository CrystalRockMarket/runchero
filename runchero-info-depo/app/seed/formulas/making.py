"""Formulas: workshop, construction and utilities."""

from __future__ import annotations

FORMULAS: list[dict] = [
    # --------------------------------------------------------------- workshop
    {
        "slug": "bolt-torque",
        "name": "Torque on a bolt",
        "topic": "workshop",
        "expression": "T (N.m) = K x F (N) x d (mm) / 1000",
        "symbols": "K = 0.20 for a dry steel bolt, 0.15 for a lubricated one, "
                   "0.14 for a stainless steel bolt; F = the clamp force in "
                   "newtons; d = the bolt diameter in mm",
        "units": "N.m",
        "how": "The clamp force is what you actually want, and it is torque "
               "that gives it. Use a torque wrench on head bolts and wheel "
               "nuts, and never a guess on anything that matters.",
        "example": "A 10 mm bolt needing 8 kN of clamp: (0.20 x 8,000 x 10) "
                   "/ 1000 = 16 N.m.",
        "tags": "torque,bolt,nut,clamp,wrench",
    },
    {
        "slug": "pilot-hole-size",
        "name": "Pilot hole for a screw",
        "topic": "workshop",
        "expression": "pilot hole (mm) = screw thread diameter (mm) x 0.75",
        "symbols": "for a screw into softwood use 0.7, into hardwood 0.6, "
                   "into metal 0.7, into masonry a masonry bit of the same "
                   "diameter as the anchor",
        "units": "mm",
        "how": "The right pilot hole lets the screw pull the two parts "
               "together instead of just splitting the timber.",
        "example": "A 6.5 mm screw wants a 5 mm pilot in softwood.",
        "tags": "screw,pilot,wood,drill,splitting",
    },
    {
        "slug": "sheet-metal-bend-allowance",
        "name": "Bend allowance for sheet metal",
        "topic": "workshop",
        "expression": "BA (mm) = 1.57 x R (mm) x angle (degrees) / 90 for "
                      "steel ; for aluminium use 1.52",
        "symbols": "BA = the length of metal needed for the bend; R = the "
                   "inside radius of the bend",
        "units": "mm",
        "how": "Measure from the edge of the hole to the edge of the flange, "
               "not to where you think the bend goes. Add the allowance to "
               "the flat length before cutting.",
        "example": "A 10 mm radius bend at 90 degrees in steel: 1.57 x 10 = "
                   "15.7 mm of extra metal.",
        "tags": "sheet metal,bend,allowance,flange,brake",
    },
    {
        "slug": "cutting-speed",
        "name": "Cutting speed for a lathe or drill",
        "topic": "workshop",
        "expression": "RPM = (1000 x cutting speed in m/min) / (pi x diameter "
                      "in mm)",
        "symbols": "cutting speed: 20 m/min for mild steel with a carbide "
                   "tip, 40 for aluminium, 60 for brass, 25 for stainless",
        "units": "rpm",
        "how": "Set the speed from the tool material and the work, then let "
               "the chips tell you if you are wrong. Blue chips mean too "
               "fast.",
        "example": "Cutting 20 mm steel at 25 m/min: (1000 x 25) / (pi x 20) "
                   "= 398 rpm.",
        "tags": "lathe,drill,cutting speed,rpm,mild steel",
    },
    {
        "slug": "pulley-speed-ratio",
        "name": "Pulley and belt speed ratio",
        "topic": "workshop",
        "expression": "driven rpm = driving rpm x (driving pulley diameter / "
                      "driven pulley diameter)",
        "symbols": "the belt takes up the difference; the belt speed is the "
                   "same at both pulleys",
        "units": "rpm",
        "how": "The belt and pulley rules for a lathe, a compressor or a "
               "sander. A small pulley on a shaft with a big one on the belt "
               "gives speed and torque.",
        "example": "A 100 rpm motor on a 100 mm pulley driving a 400 mm "
                   "pulley: 100 x (100/400) = 25 rpm.",
        "tags": "pulley,belt,speed ratio,lathe,motor",
    },
    {
        "slug": "chain-speed",
        "name": "Chain and sprocket speed",
        "topic": "workshop",
        "expression": "chain speed (m/s) = pitch (m) x teeth x rpm / 60",
        "symbols": "a 12.7 mm pitch chain has 15.875 mm from pin to pin",
        "units": "m/s",
        "how": "For chain wear, sprocket sizing and the speed of a "
               "bicycle. Multiply by 3.6 for km/h.",
        "example": "A 48 tooth sprocket at 100 rpm on 12.7 mm pitch: "
                   "0.0127 x 48 x 100 / 60 = 1.02 m/s.",
        "tags": "chain,sprocket,bicycle,speed",
    },
    {
        "slug": "open-belt-length",
        "name": "Belt length over two pulleys",
        "topic": "workshop",
        "expression": "L = 2C + (pi/2)(D + d) + (D - d)^2 / (4C)",
        "symbols": "C = centre distance in mm; D = big pulley diameter; "
                   "d = small pulley diameter",
        "units": "mm",
        "how": "For a V-belt or a flat belt on a machine you have built. Add "
               "about 5% for tension and stretch, then cut to the nearest "
               "standard size.",
        "example": "C = 400, D = 200, d = 80: 800 + 440 + 14 = 1,254 mm, so "
                   "buy a 1,300 mm belt.",
        "tags": "belt,pulley,length,machine,driving",
    },
    {
        "slug": "gearbox-ratio",
        "name": "Gear ratio and overall ratio",
        "topic": "workshop",
        "expression": "ratio = teeth on the driven gear / teeth on the driving "
                      "gear ; overall ratio = the product of each ratio",
        "symbols": "a ratio above 1 turns the output slower and stronger",
        "units": "ratio",
        "how": "Whether you are rebuilding a gearbox, a mixer or a seedling "
               "thinner. Work it out on paper before you order the gears.",
        "example": "A 16 tooth pinion driving a 48 tooth gear is a 3:1 "
                   "reduction.",
        "tags": "gear,ratio,gearbox,pinion,reduction",
    },
    {
        "slug": "power-from-torque",
        "name": "Power from torque and speed",
        "topic": "workshop",
        "expression": "P (W) = T (N.m) x 2 x pi x n (rpm) / 60",
        "symbols": "T = torque; n = revolutions per minute",
        "units": "watts, kilowatts, horsepower (1 hp = 746 W)",
        "how": "To check whether a motor, an engine or a hand tool has the "
               "power for the job, and to compare an electric motor with a "
               "petrol one.",
        "example": "200 N.m at 720 rpm: (200 x 2 x pi x 720) / 60 = 15,080 W, "
                   "or 15 kW.",
        "tags": "power,torque,motor,engine,watts",
    },
    {
        "slug": "work-power",
        "name": "Work and power from a force",
        "topic": "workshop",
        "expression": "work (J) = force (N) x distance (m) ; "
                      "P (W) = force (N) x speed (m/s)",
        "symbols": "1 J = 1 N moved 1 m; 1 kW = 1,000 W",
        "units": "joules, watts",
        "how": "The physics behind leverage. A bar is a machine: it does not "
               "change the work, only the force and the distance.",
        "example": "Lifting 500 N through 0.3 m is 150 J of work whatever "
                   "lever you use.",
        "tags": "work,power,force,lever,joules",
    },
    {
        "slug": "efficiency",
        "name": "Efficiency of a machine",
        "topic": "workshop",
        "expression": "efficiency % = (useful output / input) x 100",
        "symbols": "a gearbox is 95-98%, a chain drive 96-98%, a screw jack "
                   "20-40%, an electric motor 85-95%",
        "units": "%",
        "how": "Friction and heat are the losses. A lower efficiency means "
               "more fuel, more electricity and more heat to shift away.",
        "example": "A 1 kW motor driving a 400 W pump is 40% efficient, which "
                   "means something is rubbing.",
        "tags": "efficiency,losses,friction,machine",
    },
    {
        "slug": "diesel-fuel-consumption",
        "name": "Diesel fuel consumption",
        "topic": "workshop",
        "expression": "fuel (L/h) = (engine kW x BSFC in g/kWh) / (density in "
                      "g/L) / 1,000",
        "symbols": "BSFC is about 220-250 g/kWh for a diesel at full load, "
                   "slower at idle; diesel density 840 g/L; 1 L of diesel "
                   "is about 10 kWh of energy",
        "units": "L/h, L/100km",
        "how": "For working out the cost of a job and whether a machine is "
               "worth keeping. Idle burn is a surprising share of a small "
               "engine's fuel.",
        "example": "A 30 kW engine at 240 g/kWh uses (30 x 240) / 840 / "
                   "1,000 = 8.6 L/h.",
        "tags": "diesel,fuel,consumption,engine,cost",
    },
    {
        "slug": "litres-per-100km",
        "name": "Fuel use in litres per 100 km",
        "topic": "workshop",
        "expression": "L/100km = (litres used / km driven) x 100",
        "symbols": "the reverse, mpg = 235.2 / (L/100km), is the imperial "
                   "figure some people still quote",
        "units": "L/100km",
        "how": "The standard way to compare a van, a tractor and a car. Keep "
               "a running total between fills.",
        "example": "60 L over 400 km = 15 L/100km.",
        "tags": "fuel,consumption,van,tractor,miles per gallon",
    },
    {
        "slug": "machine-running-cost",
        "name": "Running cost per hour of a machine",
        "topic": "workshop",
        "expression": "cost per hour = (purchase price x depreciation + "
                      "interest + fuel + maintenance + insurance) / hours per "
                      "year",
        "symbols": "depreciation is usually taken as 10-20% a year off the "
                   "purchase price; interest at the rate you pay the bank",
        "units": "per hour",
        "how": "The number that decides whether a second machine, a bigger "
               "one, or hiring it in makes sense.",
        "example": "A 12,000 euro tractor working 500 hours a year at 9 L/h "
                   "and 1.60 a litre burns about 7,200 euro a year in fuel "
                   "alone.",
        "tags": "cost,per hour,machine,tractor,hiring",
    },
    {
        "slug": "saw-teeth-per-inch",
        "name": "Saw teeth per inch",
        "topic": "workshop",
        "expression": "TPI = 1 / (2 x gullet depth in inches)",
        "symbols": "for a rip cut in hardwood use 4-6 TPI, for a crosscut "
                   "8-12 TPI, for a hand saw 10-14 TPI",
        "units": "teeth per inch",
        "how": "The difference between a saw that cuts along the grain and "
               "one that cuts across it. A rip saw has few deep teeth; a "
               "crosscut saw has many fine ones.",
        "example": "A 3/32 in gullet gives 1 / (2 x 0.094) = 5.3 TPI, a rip "
                   "saw.",
        "tags": "saw,tpi,teeth,rip cut,crosscut",
    },
    {
        "slug": "board-feet",
        "name": "Board feet of timber",
        "topic": "workshop",
        "expression": "BF = (thickness in inches x width in inches x length "
                      "in feet) / 12",
        "symbols": "a board foot is a piece 1 in thick, 12 in wide and 12 in "
                   "long, or 144 cubic inches",
        "units": "board feet",
        "how": "How timber is sold in the trade, and how you check a "
               "delivery. A rough conversion is 1 board foot about 0.0024 "
               "m3.",
        "example": "A 25 x 150 x 4.8 m board is (1 x 6 x 15.7) / 12 = "
                   "7.8 board feet.",
        "tags": "timber,board feet,lumber,volume,m3",
    },
    {
        "slug": "wood-movement",
        "name": "Movement of timber with moisture",
        "topic": "workshop",
        "expression": "movement (mm) = length (mm) x moisture change (%) x "
                      "0.03",
        "symbols": "movement across the grain is far greater than along it: "
                   "about 3% across the grain, 0.1% along the grain",
        "units": "mm",
        "how": "Why a door jams in a wet winter, why a solid wooden worktop "
               "cups, and why a gate needs a gap. Plan for the movement.",
        "example": "A 1,000 mm fence rail moving 8% in moisture: "
                   "1,000 x 0.08 x 0.03 = 2.4 mm.",
        "tags": "timber,moisture,movement,door,gate",
    },
    {
        "slug": "concrete-bags",
        "name": "Bags of cement for a volume of concrete",
        "topic": "workshop",
        "expression": "bags = volume (m3) x 7 for a 1:2:4 mix ; volume (m3) = "
                      "0.67 x (sum of the material volumes)",
        "symbols": "a 25 kg bag gives about 12.5 litres of mixed concrete; "
                   "sand and stone are measured by volume, not by weight",
        "units": "bags, m3",
        "how": "For a footing, a step, a post hole or a slab. A 1:2:4 mix is "
               "for footings and paths, 1:2:5 for a mass base and 1:1.5:3 "
               "for a stronger mix. See [[mixing-concrete]].",
        "example": "A 1 m x 1 m x 0.15 m pad needs 0.15 m3, so about 1 bag of "
                   "cement, 0.1 m3 of sand and 0.15 m3 of stone.",
        "tags": "concrete,mix,bags,cement,footing",
    },
    {
        "slug": "water-cement-ratio",
        "name": "Water to cement ratio and strength",
        "topic": "workshop",
        "expression": "compressive strength (MPa) is roughly 100 / (w/c "
                      "ratio) for a well-graded mix",
        "symbols": "w/c = litres of water / kg of cement; 0.45 gives about 20 "
                   "MPa, 0.60 gives about 15 MPa, 0.80 gives about 10 MPa",
        "units": "MPa",
        "how": "Water is the enemy of concrete strength. Never add water to "
               "make it easier to work; add cement or use a plasticiser "
               "instead. See [[mixing-concrete]].",
        "example": "A footing with 40 litres of water and 50 kg of cement "
                   "has a 0.8 ratio, so about 10 MPa, which is fine for a "
                   "post.",
        "tags": "concrete,strength,water,cement,mpa",
    },
    {
        "slug": "concrete-drying-time",
        "name": "Waiting time before loading concrete",
        "topic": "workshop",
        "expression": "no loading for 24-48 hours ; full strength at 28 days",
        "symbols": "walk on it after 24-48 hours, put a weight on at 7 days, "
                   "full strength at 28",
        "units": "hours, days",
        "how": "Concrete gains most of its strength in the first week. Keep "
               "it damp for the first three days and cover it if it is hot "
               "or frosty.",
        "example": "A gate post in concrete should stand for 48 hours before "
                   "the gate goes on.",
        "tags": "concrete,curing,time,strength,footing",
    },
    {
        "slug": "post-hole-concrete",
        "name": "Concrete for a post hole",
        "topic": "workshop",
        "expression": "volume (m3) = pi x r2 x depth ; add 10% for the "
                      "bulge at the top",
        "symbols": "a 100 mm post in a 200 mm hole at 900 mm deep holds about "
                   "0.028 m3, so 1.5 bags of cement mixed as a stiff "
                   "post mix",
        "units": "m3, bags",
        "how": "Set posts in concrete for a gate, a fence or a sign. A "
               "quick-setting post mix works in cold weather. See "
               "[[setting-fence-posts]].",
        "example": "A 250 mm hole 1 m deep = 0.049 m3, which is about 2.5 "
                   "bags of post mix.",
        "tags": "post,concrete,hole,fence,gate",
    },
    {
        "slug": "blocks-per-square-metre",
        "name": "Blocks or bricks per square metre",
        "topic": "workshop",
        "expression": "number per m2 = 1 / ((length in m) x (height in m))",
        "symbols": "allow for a 10 mm mortar joint; a standard block is "
                   "440 x 215 mm, so 12.5 per m2 in a 215 mm wall; a brick is "
                   "215 x 65 mm, so about 60 per m2",
        "units": "blocks per m2",
        "how": "For ordering. Always order 5% more than the calculation for "
               "cuts and breakages.",
        "example": "440 x 215 blocks: 1 / (0.45 x 0.225) = 9.9, so 10 "
                   "blocks a square metre.",
        "tags": "blocks,bricks,mortar,wall,quantity",
    },
    {
        "slug": "sand-and-stone-for-concrete",
        "name": "Sand and stone for a concrete mix",
        "topic": "workshop",
        "expression": "sand (m3) = volume x 1 ; stone (m3) = volume x 2 for a "
                      "1:2:4 mix ; these are volume buckets, not weights",
        "symbols": "1 bucket of cement, 2 of sand, 4 of stone, and 1 bucket "
                   "of water for 5 buckets of sand",
        "units": "m3, buckets",
        "how": "Mixing by bucket. A wheelbarrow of sand is about 0.07 m3, so "
               "a bucket is roughly 0.014 m3. See [[mixing-concrete]].",
        "example": "A 0.5 m3 batch of 1:2:4 needs 0.1 m3 of cement, 0.2 m3 of "
                   "sand and 0.4 m3 of stone.",
        "tags": "concrete,sand,stone,mix,buckets",
    },
    {
        "slug": "plinth-and-foundation-volume",
        "name": "Foundation volume for a wall",
        "topic": "workshop",
        "expression": "volume (m3) = length (m) x width (m) x depth (m)",
        "symbols": "a 400 mm wide strip foundation 500 mm deep under 10 m of "
                   "wall is 2 m3",
        "units": "m3",
        "how": "Work out the whole foundation before ordering, and add 10% "
               "for the lumps. Dig in a straight line, and set the pegs "
               "before the mixer arrives.",
        "example": "10 m x 0.4 m x 0.5 m = 2.0 m3 of concrete.",
        "tags": "foundation,volume,wall,strip,concrete",
    },
    {
        "slug": "rebar-length",
        "name": "Rebar cutting and lapping",
        "topic": "workshop",
        "expression": "total length = number of bars x length per bar ; "
                      "lap = 40 x bar diameter, or 50 x for a tension lap",
        "symbols": "a 12 mm bar needs a 480 mm lap at 40 diameters; cover is "
                   "25-50 mm depending on the exposure",
        "units": "mm",
        "how": "Order the bar in lengths that avoid joints in the worst "
               "places, and bend a hook at the ends. See "
               "[[mixing-concrete]].",
        "example": "A 12 mm bar lapped 480 mm and a 25 mm cover at each end "
                   "needs 530 mm of bar per lap.",
        "tags": "rebar,lap,length,concrete,foundation",
    },
    {
        "slug": "paint-area",
        "name": "Paint area and quantity",
        "topic": "workshop",
        "expression": "area (m2) = (perimeter x height) - openings ; "
                      "litres = area / coverage",
        "symbols": "coverage is 10-12 m2 a litre on a porous masonry wall, "
                   "8-10 on wood, 12-14 on new plaster",
        "units": "m2, litres",
        "how": "Measure the wall, not the tin. Two coats on new plaster need "
               "a primer first. See [[painting-and-prep]].",
        "example": "A 4 m x 2.5 m wall with a 1 m2 window: 10 - 1 = 9 m2, "
                   "so 1 L of paint for two coats.",
        "tags": "paint,area,coverage,litres,wall",
    },
    {
        "slug": "roof-pitch",
        "name": "Roof pitch and angle",
        "topic": "workshop",
        "expression": "pitch = rise / run ; angle (degrees) = arctan(rise / run) "
                      "x 180 / pi",
        "symbols": "35 degrees is a pitch of 0.7, which is the minimum for "
                   "most tile roofs in the UK; 45 degrees for a slate roof",
        "units": "degrees, ratio",
        "how": "The pitch decides the tile angle, the felt laps and how much "
               "water the roof throws off the building. The run is half the "
               "span for a normal gable.",
        "example": "A 3 m rise over a 4 m run is 36.9 degrees.",
        "tags": "roof,pitch,angle,tiles,slate",
    },
    {
        "slug": "roof-area",
        "name": "Roof area for covering",
        "topic": "workshop",
        "expression": "area = footprint x sqrt(1 + pitch2) for each slope",
        "symbols": "the footprint is the length x width of the building; "
                   "add 10-15% for the waste at the edges and the ridge",
        "units": "m2",
        "how": "For ordering felt, tiles, battens and underlay. Always order "
               "the underlay and never skimp on it.",
        "example": "A 10 m x 6 m building at a pitch of 0.7: 60 x 1.22 = "
                   "73 m2 a slope, so 147 m2 for both.",
        "tags": "roof,area,felt,tiles,underlay",
    },
    {
        "slug": "steps-and-rise",
        "name": "Stair rise, going and number of steps",
        "topic": "workshop",
        "expression": "number of steps = total rise / rise per step ; "
                      "2 x rise + going = 630 mm for a comfortable stair",
        "symbols": "rise 170-200 mm and going 250-280 mm for a farm building; "
                   "a ramp is 1 in 12, a path for a barrow 1 in 20",
        "units": "mm",
        "how": "Set the height of the first step from the finished floor and "
               "the landing, then work down. See [[building-a-step]].",
        "example": "A 900 mm rise with 180 mm steps gives 5 steps, so the "
                   "going can be 270 mm.",
        "tags": "steps,stair,rise,going,ramp",
    },
    {
        "slug": "ground-fall-and-drainage",
        "name": "Ground fall and drainage falls",
        "topic": "workshop",
        "expression": "fall % = (rise / run) x 100 ; a 1 in 80 floor falls "
                      "12.5 mm a metre",
        "symbols": "1 in 60 to 1 in 100 for a yard or a path; 1 in 40 to 1 in "
                   "60 for a yard slope; floors are level, the water goes to "
                   "the drain",
        "units": "%",
        "how": "Water on a level yard is water that never leaves. Get the "
               "fall right with a laser level or a long spirit level and a "
               "pegged board. See [[underground-pipe-and-trenches]].",
        "example": "A 20 m yard falling 1 in 80 drops 250 mm from end to end.",
        "tags": "fall,slope,drainage,level,yard",
    },
    {
        "slug": "fence-post-spacing",
        "name": "Fence post spacing and post number",
        "topic": "workshop",
        "expression": "posts = (fence length / spacing) + 1 ; "
                      "spacing 2.5-3 m for stock, 1.5-2 m for a dog",
        "symbols": "wires: 5 or 6 strand for sheep, 3 or 4 for cattle, and "
                   "keep the bottom wire 100-150 mm off the ground",
        "units": "posts, m",
        "how": "The wire needs to be tight and the post needs to be firm. "
               "See [[setting-fence-posts]] and [[fencing-wire-and-straining]].",
        "example": "A 100 m fence with posts at 2.5 m needs 41 posts.",
        "tags": "fence,posts,spacing,wire,stock",
    },
    {
        "slug": "wire-tension",
        "name": "Wire tension and strainer travel",
        "topic": "workshop",
        "expression": "tension force (N) = tension in the wire (N/m) x span; a "
                      "hand strainer gives about 1,500-2,500 N on a 2.5 mm "
                      "wire",
        "symbols": "a strained wire hums; if it thuds it is loose, if it "
                   "sings it is about right",
        "units": "N",
        "how": "Strain each wire to the same tension, lowest wire first, and "
               "keep the strainer run at the same place on every wire. See "
               "[[fencing-wire-and-straining]].",
        "example": "A 100 m fence with a strainer run 200 mm gives "
                   "1/500 of stretch in the wire.",
        "tags": "wire,tension,strainer,fence,straining",
    },
    {
        "slug": "single-phase-power",
        "name": "Electrical power, single and three phase",
        "topic": "workshop",
        "expression": "single phase: P (W) = V x I x power factor ; "
                      "three phase: P (W) = 1.732 x V x I x power factor",
        "symbols": "power factor is 0.8-1.0 for a motor; a 1 hp motor on "
                   "single phase draws about 7 A at 230 V",
        "units": "watts, amps",
        "how": "For working out whether a supply will carry a heater, a welder "
               "or a three-phase motor. See "
               "[[three-phase-and-single-phase]].",
        "example": "A 3 kW heater at 230 V draws 13 A, so a 13 A circuit is "
                   "at its limit.",
        "tags": "electric,power,amps,three phase,heater",
    },
    {
        "slug": "cable-voltage-drop",
        "name": "Cable size for voltage drop",
        "topic": "workshop",
        "expression": "voltage drop (V) = 2 x L x I x R / 1000 for copper",
        "symbols": "R for copper is 17.5 m-ohm/m for 1.5 mm2, 11.7 for 2.5 "
                   "mm2, 7.4 for 4 mm2, 5.6 for 6 mm2, 3.1 for 10 mm2; keep the "
                   "drop under 3% for lighting and 5% for power",
        "units": "volts, %",
        "how": "Long runs need bigger cable, not bigger fuses. Measure the "
               "run, use the table, and check the breaker size next.",
        "example": "A 30 m run at 16 A on 2.5 mm2: (2 x 30 x 16 x 11.7) / "
                   "1000 = 11.2 V, which is 5% of 230 V.",
        "tags": "cable,voltage drop,electric,run,amps",
    },
    {
        "slug": "solar-panel-sizing",
        "name": "Solar panel and battery sizing",
        "topic": "workshop",
        "expression": "battery (Ah) = (daily Wh x days of autonomy) / (battery "
                      "volts x depth of discharge x inverter efficiency)",
        "symbols": "depth of discharge 0.5 for a lead acid battery, 0.8 for "
                   "lithium; 1 hour of sun gives about 4 peak sun hours a day "
                   "in the UK in summer",
        "units": "Wh, Ah",
        "how": "For a shed, a fence charger or a small system. Size for the "
               "dark weeks of winter, not the bright ones. See "
               "[[solar-and-battery-storage]].",
        "example": "A 200 W panel for 4 hours of sun gives 800 Wh a day; for "
                   "three dark days on a 12 V battery at 50% depth: "
                   "(800 x 3) / (12 x 0.5 x 0.9) = 444 Ah.",
        "tags": "solar,battery,panel,off grid,days autonomy",
    },
    {
        "slug": "rainwater-harvesting",
        "name": "Rainwater you can catch",
        "topic": "workshop",
        "expression": "litres = rain (mm) x roof area (m2) ; "
                      "a year of 800 mm on 100 m2 = 80,000 litres",
        "symbols": "1 mm of rain on 1 m2 is 1 litre; the collection efficiency "
                   "of a roof with gutters and a downpipe is 0.85-0.9",
        "units": "litres, m3",
        "how": "For sizing a water butt or a tank for the yard and the "
               "animals. See [[water-troughs-and-algae]].",
        "example": "A 10 m x 10 m roof in a 20 mm storm collects 2,000 litres, "
                   "which is a full water butt and a bit.",
        "tags": "rainwater,tank,butt,roof,harvesting",
    },
    {
        "slug": "sealant-and-bead-coverage",
        "name": "Sealant coverage by bead size",
        "topic": "workshop",
        "expression": "length (m) = (volume in ml) / (bead area in mm2)",
        "symbols": "a 6 mm round bead is 28 mm2, a 10 mm bead is 79 mm2",
        "units": "m per cartridge",
        "how": "A 300 ml cartridge of a 6 mm bead does about 10 m; a 10 mm "
               "bead does about 3.5 m. Get the bead size right or you will "
               "run out halfway along the shed roof.",
        "example": "300 ml at a 10 mm bead: 300 / 79 = 3.8 m.",
        "tags": "sealant,silicone,bead,coverage,cartridge",
    },
    {
        "slug": "grain-silo-airflow",
        "name": "Airflow for drying grain",
        "topic": "workshop",
        "expression": "air (m3/s) = 1.3 x fan speed (m/s) x fan area (m2) x "
                      "efficiency ; a rule of thumb is 20 m3/s per kW of heat",
        "symbols": "static pressure of the grain depth is what a fan has to "
                   "push through, and it grows as the grain deepens",
        "units": "m3/s",
        "how": "Drying grain needs moving air, not hot air. If the fan is "
               "sized for the empty bin it will not cope with a full one. See "
               "[[storing-grain]].",
        "example": "A 400 mm fan at 10 m/s: 1.3 x 10 x 0.126 = 1.6 m3/s, "
                   "about 80 W of heat capacity.",
        "tags": "grain,fan,airflow,drying,silo",
    },

    # ------------------------------------------------------------ construction
    {
        "slug": "heat-loss-through-a-wall",
        "name": "Heat loss through a wall or floor",
        "topic": "construction",
        "expression": "heat loss (W) = area (m2) x U-value (W/m2K) x "
                      "temperature difference (K)",
        "symbols": "U-values: insulated wall 0.2, uninsulated stone 1.7, "
                   "single glazed window 5.0, double glazed 1.6, insulated "
                   "floor 0.2, bare concrete 1.7",
        "units": "watts",
        "how": "For comparing a shed, a workshop and a house, and for "
               "working out what a stove has to make up. Bigger U-value means "
               "more heat going out.",
        "example": "A 10 m2 stone wall with a 12 K difference: 10 x 1.7 x 12 "
                   "= 204 W.",
        "tags": "heat loss,u value,insulation,wall,stove",
    },
    {
        "slug": "insulation-thickness",
        "name": "Insulation thickness for a roof or wall",
        "topic": "construction",
        "expression": "R-value = thickness (mm) / thermal conductivity (W/mK)",
        "symbols": "conductivity: mineral wool 0.04, expanded polystyrene "
                   "0.038, PIR board 0.023, cellulose 0.04, and air is 0.025",
        "units": "m2K/W",
        "how": "For working out how much insulation to buy. Rule of thumb: "
               "100 mm of mineral wool is about R2.5, and a well insulated "
               "roof wants R4 or better.",
        "example": "150 mm of PIR: 0.150 / 0.023 = 6.5, so R6.5.",
        "tags": "insulation,thickness,r value,mineral wool,pir",
    },
    {
        "slug": "ventilation-rate",
        "name": "Ventilation and air changes in a building",
        "topic": "construction",
        "expression": "air changes per hour = (vent area x air speed x 3,600) / "
                      "room volume ; for a workshop allow 6-10 air changes an "
                      "hour",
        "symbols": "a 300 mm extractor fan at 3 m/s moves about 0.64 m3/s",
        "units": "air changes per hour, m3/s",
        "how": "The number that decides whether a workshop, a stable or a "
               "grain store is workable. See "
               "[[venting-the-workshop]].",
        "example": "A 3 x 3 x 2.5 m workshop is 22.5 m3; a 300 mm fan at "
                   "0.64 m3/s gives 102 air changes an hour, far too much "
                   "cold air in winter.",
        "tags": "ventilation,air changes,fan,workshop,extractor",
    },
    {
        "slug": "humidity-and-condensation",
        "name": "Condensation and ventilation",
        "topic": "construction",
        "expression": "dew point (C) at 100% relative humidity; a surface "
                      "below the dew point will be wet",
        "symbols": "warm moist air holds more water than cold air; 1 kg of "
                   "air holds about 0.008 kg of water per K of temperature "
                   "rise",
        "units": "degrees C, g/kg",
        "how": "Condensation on the roof sheets means the warm moist air is "
               "meeting a cold surface and there is no way out. Vent the "
               "building at both ends. See "
               "[[venting-the-workshop]].",
        "example": "Air at 20 C holds about 17 g of water a kg; cooled to 5 C "
                   "it can only hold 7 g, so 10 g of water comes out of every "
                   "kg of air.",
        "tags": "condensation,humidity,dew point,roof,ventilation",
    },
    {
        "slug": "foundation-depth-frost",
        "name": "Foundation depth and the frost line",
        "topic": "construction",
        "expression": "foundation depth = at least 600 mm below the frost "
                      "line, or 1 m in most of the UK",
        "symbols": "the frost line is the depth the ground freezes in a cold "
                   "snap; check with the local building inspector",
        "units": "mm",
        "how": "A foundation that is too shallow gets lifted by a hard frost "
               "and pushes the building out of square. See "
               "[[building-a-step]].",
        "example": "A frost line at 450 mm means the footing must go to at "
                   "least 1,050 mm.",
        "tags": "foundation,frost,depth,footing,building",
    },
    {
        "slug": "mortar-mix-and-brickwork",
        "name": "Mortar mix for brickwork",
        "topic": "construction",
        "expression": "1 part cement : 4 parts sharp sand for general work, "
                      "1:6 for foundations, 1:3 for a thin pointing joint",
        "symbols": "use plasticiser rather than extra water; a 25 kg bag "
                   "makes about 0.05 m3 of mortar",
        "units": "m3, buckets",
        "how": "The strength comes from the sand being sharp and clean and "
               "the joints being filled. Lime in the mix makes it work "
               "better.",
        "example": "A 0.1 m3 batch of 1:4 mortar needs about 1 bag of "
                   "cement and 0.2 m3 of sand.",
        "tags": "mortar,brick,pointing,mix,cement",
    },
    {
        "slug": "gutter-and-downpipe-size",
        "name": "Gutter and downpipe sizing",
        "topic": "construction",
        "expression": "downpipe (mm) = sqrt(roof area in m2) x 12, rounded "
                      "up",
        "symbols": "a 100 mm gutter serves up to about 80 m2 of roof, a 125 "
                   "mm up to 130 m2",
        "units": "mm",
        "how": "An undersized gutter overflows in a storm and wets the "
               "foundation. See [[draining-water-pipes]].",
        "example": "A 120 m2 roof needs a 132 mm pipe, so 150 mm.",
        "tags": "gutter,downpipe,roof,rainwater,size",
    },
    {
        "slug": "water-tank-size",
        "name": "Water tank size for a yard or house",
        "topic": "construction",
        "expression": "daily need (L) = people x 150 + animals x their need ; "
                      "tank = daily need x days of storage",
        "symbols": "a dairy cow needs 60-100 L a day, a horse 20-30 L, a "
                   "sheep 5 L",
        "units": "litres, m3",
        "how": "For a header tank and a trough system, and for a yard where "
               "the mains cannot keep up. See "
               "[[water-troughs-and-algae]].",
        "example": "2 people and 10 cows need 1,300 L a day; a two day buffer "
                   "is a 2,600 L tank.",
        "tags": "tank,water,storage,trough,size",
    },
    {
        "slug": "fence-post-hole",
        "name": "Post hole for a fence or a gate",
        "topic": "construction",
        "expression": "hole (m3) = pi x r2 x depth ; depth 450-750 mm for a "
                      "fence, 900 mm for a gate post",
        "symbols": "ram the bottom 150 mm with a post hole rammer so the post "
                   "stands on firm ground",
        "units": "m3, mm",
        "how": "Digging a hole the right width makes the job ten times "
               "quicker, and the post is stronger. See "
               "[[setting-fence-posts]].",
        "example": "A 150 mm radius hole 600 mm deep = 0.042 m3.",
        "tags": "post hole,fence,gate,depth,rammer",
    },
    {
        "slug": "levelling-a-yard",
        "name": "Levelling and volumes for a yard",
        "topic": "construction",
        "expression": "cut or fill (m3) = area (m2) x average change in "
                      "level (m)",
        "symbols": "take levels on a 5 m grid, work out the average, then "
                   "multiply",
        "units": "m3",
        "how": "Before the trucks arrive, work out how much hard core or "
               "soil you need. The average of the high and low spots is the "
               "honest way to do it.",
        "example": "A 400 m2 yard that needs an average of 75 mm of stone = "
                   "30 m3.",
        "tags": "levelling,yard,levels,volume,hard core",
    },
    {
        "slug": "hard-core-and-topsoil",
        "name": "Hard core, sub-base and topsoil",
        "topic": "construction",
        "expression": "volume (m3) = area (m2) x depth (m) ; 100 mm of "
                      "sub-base over 200 mm of hard core is the usual "
                      "construction",
        "symbols": "a 25 tonne tipper holds about 14 m3 of loose stone",
        "units": "m3, tonnes",
        "how": "For a yard or a track. Compact in layers of 100-150 mm or "
               "the bottom will go soft. See [[building-a-step]].",
        "example": "A 500 m2 yard at 200 mm of hard core = 100 m3, which is "
                   "7 tipper loads.",
        "tags": "hard core,sub base,topsoil,track,volume",
    },
    {
        "slug": "plaster-and-render",
        "name": "Plaster and render quantities",
        "topic": "construction",
        "expression": "litres = area (m2) x thickness (mm) / 1,000 ; "
                              "a 1:4 mix covers about 10 m2 a 25 kg bag",
        "symbols": "interior plaster is 10-12 mm, external render 15-20 mm",
        "units": "litres, bags",
        "how": "Rushing a render is how it cracks. Two coats, and let the "
               "first one set before the second.",
        "example": "A 10 m2 wall at 15 mm needs 0.15 m3 of render, about 3 "
                   "bags of cement and 0.6 m3 of sand.",
        "tags": "render,plaster,cement,sand,wall",
    },
    {
        "slug": "wall-area-for-insulation",
        "name": "Wall area for insulating a room",
        "topic": "construction",
        "expression": "area = (perimeter x height) - (window and door area)",
        "symbols": "a 3 m x 4 m room with 2.2 m ceilings has 15.7 m2 of "
                   "wall before the windows",
        "units": "m2",
        "how": "The first number for any insulation job. Measure every wall "
               "and subtract the openings, and buy 10% extra for the "
               "cutting.",
        "example": "15.7 - 3 m2 of window and door = 12.7 m2 to insulate.",
        "tags": "insulation,area,wall,room,measure",
    },
    {
        "slug": "floor-insulation-over-void",
        "name": "Insulating a suspended floor",
        "topic": "construction",
        "expression": "insulation (m2) = floor area less 5% for the joists "
                      "and edges",
        "symbols": "lay the insulation between the joists, cut carefully "
                   "around pipes and wires, and fill the gaps with expanding "
                   "foam",
        "units": "m2",
        "how": "A suspended timber floor over a cold ventilated void loses a "
               "lot of heat. See [[insulating-a-workshop]].",
        "example": "A 12 m2 room with 0.6 m2 lost to the joists needs about "
                   "11.4 m2 of 100 mm board.",
        "tags": "floor,insulation,joists,void,board",
    },
    {
        "slug": "double-glazing-u-value",
        "name": "Window heat loss and glazing",
        "topic": "construction",
        "expression": "heat loss (W) = area (m2) x U-value (W/m2K) x "
                      "temperature difference (K)",
        "symbols": "single glazed 5.0, double glazed 1.6, triple glazed 0.8, "
                   "secondary glazing on a single pane roughly halves it",
        "units": "watts",
        "how": "Windows are the weak point of any old building. A "
               "secondary glazing frame on the inside of a single glazed "
               "window is cheap and effective.",
        "example": "A 2 m2 single glazed window at 12 K: 2 x 5.0 x 12 = 120 "
                   "W, which is a small heater running all winter.",
        "tags": "window,glazing,u value,heat loss,draught",
    },
    {
        "slug": "thermal-bridge",
        "name": "Thermal bridges and damp",
        "topic": "construction",
        "expression": "a cold bridge shows up as a line of mould or a damp "
                      "patch at the same place every winter",
        "symbols": "common bridges: the slab edge, the window reveal, the "
                   "lintel, a pipe going through a wall",
        "units": "diagnostic",
        "how": "Mould on the same corner every winter is not bad luck. Look "
               "for the cold spot with a thermal camera or the back of your "
               "hand.",
        "example": "Damp at the base of a cold wall is condensation, not a "
                   "leak, unless it moves when it rains.",
        "tags": "damp,condensation,mould,bridge,wall",
    },
    {
        "slug": "drainage-fall-and-pipe-size",
        "name": "Drainage pipe size and fall",
        "topic": "construction",
        "expression": "pipe size (mm) = sqrt(roof area in m2) x 12 for "
                      "rainwater ; drains need a fall of 1 in 60 for a "
                      "laid pipe",
        "symbols": "a 100 mm pipe serves up to 80 m2 of roof",
        "units": "mm, %",
        "how": "A drain that does not fall will block, and the smell will "
               "find its way into the shed. See "
               "[[underground-pipe-and-trenches]].",
        "example": "A 60 m2 roof needs a 93 mm pipe, so 100 mm with a 1 in "
                   "60 fall.",
        "tags": "drain,pipe,fall,sewer,roof",
    },
    {
        "slug": "effluent-and-sump",
        "name": "Sump and effluent pit",
        "topic": "construction",
        "expression": "volume (m3) = length x width x depth, with 20% free "
                      "space above the working level",
        "symbols": "a yard that drains to one corner needs a fall of 1 in "
                   "80 at least",
        "units": "m3",
        "how": "A blocked sump floods the yard and the smell reaches the "
               "house. Keep the grate clear and the outlet clear.",
        "example": "A 2 x 2 x 1.5 m pit with 20% free space holds 3.6 m3.",
        "tags": "sump,effluent,pit,drainage,yard",
    },
    {
        "slug": "sand-under-paving",
        "name": "Sand bed under paving",
        "topic": "construction",
        "expression": "sand (m3) = area (m2) x 50 mm ; for a 50 mm bedding "
                      "layer on a compacted base",
        "symbols": "use sharp sand or a bedding sand, not building sand; it "
                   "must be compacted",
        "units": "m3",
        "how": "The sand bed is what makes the blocks sit flat. A slabbed "
               "area that wobbles has not enough compacted sand under it.",
        "example": "A 20 m2 path needs 1 m3 of sand, which is about 14 "
                   "wheelbarrows.",
        "tags": "sand,paving,path,bedding,blocks",
    },
    {
        "slug": "brickwork-quantity",
        "name": "Bricks, blocks and mortar for a wall",
        "topic": "construction",
        "expression": "number = wall area (m2) x units per m2 ; "
                      "mortar = area x 0.02 m3 per m2 for a 215 mm wall",
        "symbols": "a 215 mm block takes 10-12 blocks a m2 with 10 mm joints, "
                   "and about 0.02 m3 of mortar a m2",
        "units": "blocks, m3",
        "how": "Order 5% extra. A half block per row is needed at every "
               "corner and opening, and people always run out.",
        "example": "A 10 m2 wall of 440 blocks needs about 100 blocks and "
                   "0.2 m3 of mortar.",
        "tags": "bricks,blocks,mortar,wall,quantity",
    },
    {
        "slug": "workout-and-savings",
        "name": "Workout and savings on a job",
        "topic": "construction",
        "expression": "saving = (old annual cost - new annual cost) / cost of "
                      "the new one, per year",
        "symbols": "for a stove, an insulation job or a second vehicle, work "
                   "out the running cost before and after",
        "units": "per year",
        "how": "The way to sell an idea to whoever holds the purse. Half the "
               "cost of an insulation job often comes back in fuel in the "
               "first winter.",
        "example": "Insulation saving 900 euro a year for 1,800 euro of work "
                   "pays back in two years.",
        "tags": "saving,workout,cost,insulation,stove",
    },
]
