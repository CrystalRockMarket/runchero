"""Extra notes for the yard and the workshop: structures, pipework, corrosion, safety gear."""

from __future__ import annotations

NOTES: list[dict] = [
    {
        "slug": "venting-the-workshop",
        "title": "Venting the workshop",
        "category": "workshop-welding",
        "summary": "Fume, dust and heat all need somewhere to go. A workshop that cannot be ventilated is a workshop you should not weld in.",
        "author": "Wes, workshop",
        "difficulty": "moderate",
        "read_minutes": 5,
        "tags": "ventilation,extraction,fume,dust,workshop",
        "body": """The workshop is usually the smallest room on the farm and it is where all the dusty work happens. Air has to go somewhere.

## Fume from welding

- **Extract at the source.** A hood or a nozzle within 300 mm of the arc, not a general extract in the corner of the room.
- **General ventilation** - a high extract fan and a low make-up air opening - handles the rest. High extract, low intake. The opposite does not work.
- **Never extract galvanised, painted or stainless fume into the same duct as mild steel.** It poisons the extract and the operator. See [[stick-and-tig-welding]].
- **A portable fume extractor** is a good half-measure for a farm shop. Move it, do not move the job around it to save the cable.

## Dust

- **A general dust extract for grinding, sanding and cutting concrete.**
- **A cyclone or a good filter**, not a spark arrester that clogs and becomes a fire risk.
- **Wood dust from a saw or a planer** wants a separate system with its own filter. Wood dust in a general extract will clog it in a year.

## The workshop itself

- **A workshop that is used in winter needs a heat source that is not a gas heater in a dusty, flammable space.** See [[wood-burning-and-stove-dampers]].
- **Keep the extract running for a while after you stop.** Fume does not leave the room the moment you switch off.
- **Check the filters on a schedule** and write it on the calendar. A clogged filter is an extract that does not extract.

## Paint and solvents

- **Do not spray paint in the same room as you weld.** Move the job, not the extract.
- **Store paints and solvents in a ventilated, locked store.** See [[chemical-storage-on-the-farm]].
- **Do not store fuel or solvent in the workshop if there is a welding set-up in it.**

## Fire and dust

- **A dust layer of 1 mm on a surface is enough to carry a flame.** A dust extract that has not been cleaned is a fire load.
- **Clean the extract ducts** and the fan. Have a plan and a contractor for the high level.

> **If you cannot smell the fume, you are not breathing it.** If you can smell it, you are breathing it.
""",
    },
    {
        "slug": "earth-clamp-tyres-and-leads",
        "title": "Earth clamps, leads and tyres",
        "category": "workshop-welding",
        "summary": "The earth clamp is the most important part of the welding set. Get it right and the weld is safe; get it wrong and it is not.",
        "author": "Wes, workshop",
        "difficulty": "easy",
        "read_minutes": 4,
        "tags": "welding,earth clamp,leads,cables,tyres",
        "body": """A welding machine is earthed through the work, via the clamp. A bad clamp is the most common cause of electric shock at the bench.

## The earth clamp

- **Clamp to the job itself.** Not to a scaffold, a trailer bar, a bench or a machine that might be moved.
- **Bare metal only.** Grind the paint, rust and galvanising back until it is bright and clean. A clamp on a painted frame is no clamp at all.
- **Clamp near the weld.** The closer the clamp is to the weld, the less stray current runs through the structure.
- **Two clamps are better than one** on a big job, and on a rusty structure you may need to clamp both ends of the piece.
- **Keep it in good condition.** Replace a clamp with a broken jaw or a rusted screw.
- **Do not use a clamp handle on a plate that is hot** - you will drop it and you will remember it.

## The leads

- **Buy the lead length the machine needs.** A lead that is too long causes voltage drop and a poor weld.
- **Thicker lead for longer runs.** A 2 m lead and a 20 m lead are not the same cable.
- **Inspect the leads** regularly for cuts, kinks and bare copper. A damaged lead is a shock risk.
- **Do not run a lead under a vehicle wheel.** It gets crushed, and a crushed lead with a broken insulation is how a fire starts.
- **Coil the leads properly** when you store them, on a hanger, not in a heap on the floor.
- **Replace the electrode holder** when the grip is worn through to the cable.

## Wheels and tyres

- **A welding machine on a site needs a site power supply** or a generator, not a domestic extension lead. See [[portable-power-and-generators]].
- **A generator and a welding machine do not get along** unless the generator is the right size and the machine has a hot start or a stabiliser. A gen-set welder is a different machine.
- **Never weld in the rain** with a 230V machine in a wet field. See [[welding-safety-on-the-farm]].

## The plug

- **Check the plug and the socket.** A cracked plug is how a lead gets a bad earth.
- **PAT test the machine** and the leads, on a schedule, and write the date on it.

> **The earth clamp is the cheapest safety device on the farm and the one most often left in the toolbox.** Grab it first, every time.
""",
    },
    {
        "slug": "sheet-metal-fixing",
        "title": "Fixing sheet metal: screws, rivets and sealants",
        "category": "workshop-fabrication",
        "summary": "The right fixing for roofing, cladding, gutters and trailer bodies, and why the wrong one always leaks.",
        "author": "Wes, workshop",
        "difficulty": "easy",
        "read_minutes": 5,
        "tags": "sheet metal,screws,rivets,sealant,cladding,roofing",
        "body": """A sheet roof that leaks is a sheet roof that was fixed with the wrong screw.

## Choosing the fixing

| Material | Fixing | Notes |
| --- | --- | --- |
| Corrugated steel roofing | Single roofing screw with a bonded washer | The only correct answer for profiled steel |
| Fibre cement sheeting | Asbestos-free roofing screw with a washer | Never use an ordinary screw |
| Plywood and OSB | Exterior-grade wood screw | Screws, not nails |
| Steel to steel, light | Self-drilling screw with a bonded washer | Check the thickness |
| Trailer body | Countersunk rivet or tek screw | Both work; do not mix |
| Gutter | Clip and bracket | Not a screw through the gutter |

- **The washer is the seal.** A roofing screw has a bonded EPDM washer under the head. Without it, every fixing is a leak point.
- **The drill bit is not optional.** Drill the pilot hole for a screw that is not self-drilling. A self-drilling screw into a heavy section still needs a pilot.
- **The right length.** The screw must go through the sheet and into the purlin, and not come out the other side.

## The rules that stop the leaks

- **Fix the sheet at every purlin, and at the sheet ends.**
- **Stagger the sheet laps** so the seams do not line up, and so a lap is not over the lap below.
- **Sealant on the laps, not on the bolt heads.** On a roof, a bead of sealant under the overlapping sheet and a bead on the bolt head.
- **Never screw into the trough of a corrugated sheet.** Into the crest, always.
- **Do not over-tighten.** A screw driven too hard crushes the bonded washer and it stops sealing.
- **Flash every penetration** - a pipe through a roof, a vent, a chimney.

## Rivets

- **Use the right rivet for the sheet thickness.** A snap rivet in thick steel will not hold.
- **Use a rivet gun with the correct nosepiece**, and set it to the right blow for the material. See [[bolts-and-fasteners]] for the choice between a rivet and a screw.
- **A rivet cannot be removed.** If you might need to take it off, use a tek screw.

## Sealants

- **Use a sealant that is rated for the material and the temperature.** Most standard sealants go soft at low temperatures.
- **Butyl tape under lapped sheet** is better than a bead of silicone for roofing.
- **Silicone on a metal roof** will pull away as the metal moves. Use a roofing sealant.
- **Do not seal a lap that drains water between the sheets.** The water has to go somewhere.

## Sheet material grades

- **Galvanised sheet** for general work. It scratches easily and the scratches rust.
- **Stainless** for anything that will be washed down or that touches food.
- **Painted sheet** for cladding.
- **Purlins and rails** out of mild steel, galvanised if they will be wet.

> **The leak is never where the screw went through. It is always at the lap or the penetration.** Seal the laps and flash the holes.
""",
    },
    {
        "slug": "hanging-a-gate-on-a-post",
        "title": "Hanging a gate on a post",
        "category": "workshop-fabrication",
        "summary": "Position, height, swing and clearance. Most gates that will not close are hung wrong, not built wrong.",
        "author": "Wes, workshop",
        "difficulty": "easy",
        "read_minutes": 4,
        "tags": "gate,hinge,post,latch,hanging",
        "body": """Hanging a gate is a twenty-minute job if the posts are in the right places, and a whole afternoon if they are not.

## Before you hang it

- **The posts must be set, plumb and immovable.** If the post moves, the gate will never close properly. See [[setting-fence-posts]].
- **The two posts must be at the right spacing.** Measure the actual gap between the posts, not the gap you planned.
- **The gate must fit the opening with the hinge side square to the post and the closing edge clear.**
- **Check the swing direction before you hang it.** A gate that opens the wrong way is a gate that will be reversed the hard way.

## Position and height

- **The hinge stile of the gate sits 20-30 mm from the post**, clear of the post face.
- **The bottom rail should clear the ground by 50-75 mm** so the gate can swing over uneven ground and so it can be dragged through grass.
- **The top of the gate should be level with the top of the fence**, or a little above, so it cannot be climbed over.
- **The gate should hang so that it closes against the stop and the latch catches without lifting the gate.**

## The hinge

- **Use a hinge that is rated for the gate's weight.** A 3.6 m gate weighs 120 kg or more. See [[bolts-and-fasteners]].
- **A gate needs two hinges** - one at the top and one at the bottom - or it will drop and rack as it is used.
- **Weld the hinge lugs to the gate frame** and bolt or weld the post side, with a backing plate inside a hollow post.
- **The gate must open at least 90 degrees** without the gate hitting the post.

## Latch and stop

- **The latch must line up with the keeper on the post** and engage without lifting the gate.
- **Fit a drop bolt** at the closing end for a wide gate, so it cannot be pushed open.
- **The stop** - a piece of angle or pipe on the post - stops the gate swinging too far and taking the strain off the latch.

## The test

- **Stand behind the gate and swing it.** It should swing its full width, close under its own weight, and latch.
- **Push it hard with the tractor.** The post should not move, the gate should not drop, and the latch should hold.
- **Check the drop bolt drops into its hole** every time, because that is what actually stops the gate being forced.

> **Set the gate up on blocks, hinge it, and swing it before you fill it with mesh.** Getting the frame right is easier than getting the frame right with mesh already on it.
""",
    },
    {
        "slug": "setting-fence-posts",
        "title": "Setting fence posts",
        "category": "workshop-timber",
        "summary": "Spacing, depth, ramming and concrete. A post that moves is the reason a fence is never quite right.",
        "author": "Sam K.",
        "difficulty": "easy",
        "read_minutes": 5,
        "tags": "fencing,posts,rammer,concrete,alignment",
        "body": """Setting posts is the least glamorous job on the farm and the one that decides how long the fence lasts.

## Spacing

| Fence | Post spacing | Notes |
| --- | --- | --- |
| Sheep netting | 3.0-3.5 m | With a strainer at each end |
| Stock fence | 3.0 m | Two or three droppers per bay |
| Poultry netting | 3.0 m | With a stake every 1.5-2 m for wire netting |
| Barbed wire | 3.0-3.5 m | Stays out of sheep's wool |
| Deer fence | 3.0 m | Heavy, and needs a brace |

- **Use a line wire or a string line** to set the posts in a straight line. A string line is cheap and it is the difference between a fence that looks right and one that does not.
- **Measure the bays rather than counting posts.** Mark out the whole run first, then divide.

## Depth

- **600 mm for a light fence, 900 mm for a stock fence, 1200 mm for a gate post or a corner post.**
- **In hard ground, a post can be knocked in to full depth with a rammer.** In soft ground it must be dug and backfilled.
- **The post depth should be in firm ground**, not in the topsoil. A post set in topsoil will push out of the ground in a wet winter. See [[field-drainage]].

## Ramming

- **A post rammer** - a tube with a handle and a base plate - is the right tool. It drives the post and compacts the ground around it.
- **A sledgehammer and a driving plate** is the old way. It works, and it is hard work.
- **Ramming in layers.** Do it in 150-200 mm lifts. Ramming the whole hole at once leaves a hollow underneath.
- **Taper the hole backfill** - more loose material at the top than at the bottom - so the ground settles away from the post, not against it.

## Concrete

- **Concrete the gate posts, the corner posts and the strainers.** Nothing else that matters.
- **The strainer post** takes the whole tension of the wire, so it has to be immovable. See [[bolts-and-fasteners]].
- **Use a post hole that is wider at the bottom**, so the concrete keys into the ground.
- **Leave the top of the concrete an inch below the soil and mound soil over it**, so the frost does not lift the concrete out of the hole. See [[frost-and-water-logging]].
- **Concrete set a day or two before you fit the wire**, so the post is not knocked out of plumb.

## Alignment and finish

- **Check the run with a straight edge** before the concrete sets.
- **String the wire high and tight** - 150 mm at the top is a good tension - and add a dropper every bay.
- **The wire goes on the animal side of the post**, so the animal leans on the post rather than pushing the wire.
- **Strain it with a come-along or a fence strainer.** A wire that is not tight will sag and will let animals through it.

## Repairs

- **A leaning post** is usually a post in a hollow with nothing behind it. Drive a prop post diagonally behind it and tie the two together.
- **A broken post** - take it out, put a new one in the same hole, and it will be in the same bad ground. Put the new one a foot to the side.

> **A fence is only as good as its weakest post, and the weakest post is always the one that was set in a hurry.**
""",
    },
    {
        "slug": "jack-points-and-stands",
        "title": "Jacking up safely: stands and points",
        "category": "workshop-fabrication",
        "summary": "Where to put the jack, where to put the stand, and why a trailer on a jack alone is a death trap.",
        "author": "Wes, workshop",
        "difficulty": "easy",
        "read_minutes": 4,
        "tags": "jack,stands,safety,workshop,vehicle",
        "body": """Most injuries under a raised vehicle are not crushing injuries at the moment of the lift. They are injuries from a stand that slips, or a jack that fails, or a wheel that was never chocked.

## The rules

- **Never work under a vehicle supported only by a jack.** Always use axle stands or a ramp.
- **Chock the wheels** - on both sides, on the wheel that is off the ground, and on the downhill side.
- **Park on firm, level ground.** A jack on soft ground tips.
- **Set the stand as close to the wheel as possible** - no more than 300 mm away. The further away it is, the more the load swings onto it.
- **Check the stand is the right rating for the load.** A 2 tonne stand under a 4 tonne trailer is no stand at all.
- **Lower the jack slowly** after the stand is on, and check the stand is carrying the weight.
- **Never get under a vehicle on a ramp alone.** Use a drive-on lift with locking.

## The jack points

- **Use the manufacturer jacking points.** They are reinforced for a reason.
- **If you have to use a sill, use a sill that is designed for it and spread the load with a plate.** See [[timber-and-posts]] for the packing.
- **Never jack on a sill that is a thin pressing or a suspension arm.**
- **On a trailer, jack on the main chassis beam**, not on the axle or the leaf spring.

## The stands

| Type | Use |
| --- | --- |
| Fixed height, ratcheted | The standard. Cheap and fine |
| Axle stand, screw type | Adjustable, good for axle work |
| Axle stand, triangular base | Best on a soft or uneven floor |
| Sand jack | For heavy plant, on soft ground |
| Pneumatic jack | Fast, but it must be lowered and secured |

- **A stand with a wide base** is more stable on gravel than one with a narrow base.
- **Check the pawl is engaged** on a ratcheting stand, every time.

## Working on trailers and implements

- **A trailer off the tractor is a lot lighter to jack** and it is also better balanced. Take the drawbar load off first.
- **Support the axle, not the body**, and put a stand under the drawbar on a heavy trailer.
- **Remove the wheels and lay the trailer on the ground** if the work allows. Nothing beats that.

## Before you go under anything

- **Look at what you are about to work on.** Is the vehicle supported by springs that could be stored? Is the load stored hydraulically? A raised loader bucket is a raised loader bucket, not a support.
- **Lower the loader arms and lock the hydraulics.**
- **Let people know the vehicle is up.** A sign on the windscreen, or a tap on the wing.

> **The stand carries the load, not the jack.** The jack only carries it while you get the stand there.
""",
    },
    {
        "slug": "repairing-a-cracked-frame",
        "title": "Repairing a cracked frame",
        "category": "workshop-fabrication",
        "summary": "Grinding out a crack, adding a doubler, and knowing when the frame is beyond saving.",
        "author": "Wes, workshop",
        "difficulty": "moderate",
        "read_minutes": 5,
        "tags": "crack,frame,repair,doubler,welding,trailer",
        "body": """A crack in a frame is a crack that is going to grow. Repairing it properly is a design job, not a welding job.

## Is the frame repairable?

- **The crack is in a highly stressed area** - over the axle, at a spring hanger, at a load hanger, at the gusset toe - then think about replacing the whole member rather than the crack.
- **The metal around the crack is stretched and hard.** If the crack is open and the edges are ragged and discoloured, the whole section is fatigued.
- **Two or more cracks in the same frame** means the frame has been overloaded for a long time. See [[trailer-repair-and-welding]].
- **If the frame has been repaired before and cracked again**, it is telling you the repair was wrong.

## The repair

1. **Find out why it cracked.** Overloaded, a shock absorber dead, a bend in the rail, a bad weld, a pothole. If you do not fix the cause, the new repair will crack too.
2. **Unload the structure.** Take the weight off it - jack it, or support it properly. See [[jack-points-and-stands]].
3. **Grind the crack out** completely, back to clean, bright metal, in a smooth sweep. Not a V cut that leaves the crack tip behind.
4. **Check the whole member** for other cracks and for distortion. Straighten it if it is bent.
5. **Fit the doubler plate.** A plate at least 6 mm thick and at least 100 mm wider than the crack, welded all round. A plate the same thickness as the parent metal just makes two weak sections in a row.
6. **Weld it.** MIG for the fillets, or stick for the job. See [[mig-welding-basics]] and [[stick-and-tig-welding]].
7. **Grind the welds smooth** and paint it, so you can see the next crack.
8. **Load it and check it.** A loaded check, and then a check again after a month of work.

## Weld quality that matters

- **Weld all round the doubler** - a plug weld with a long crack between the welds is worse than nothing.
- **Vary the weld to avoid a straight line of welds** in the same place. A weld in a crack is a fatigue crack waiting to start.
- **Grind the surface of the doubler** between the sections of weld if you are doing it in stages.
- **No undercut.** Undercut is a notch at the toe of the weld and it is a crack starter.

## The end of the road

- **A frame with cracks in three places is a write-off**, and a trailer written off is cheaper than a trailer that lets go on a hill.
- **Get a second opinion** before you spend a day of welding on a repair that is not going to hold.
- **Know the sign of a serious structural crack** - a crack that goes right through the section, a crack with a gap you can get a finger into, or a crack at a corner.

> **A crack that is welded over without being ground out will crack again, in exactly the same place, in exactly the same way.**
""",
    },
    {
        "slug": "metal-corrosion-on-the-farm",
        "title": "Metal corrosion on the farm",
        "category": "workshop-fabrication",
        "summary": "Why the gate latch rusts but the hinge does not, and how to pick a coating that will survive the winter.",
        "author": "Wes, workshop",
        "difficulty": "easy",
        "read_minutes": 5,
        "tags": "corrosion,rust,galvanising,coating,paint",
        "body": """On a farm, metal does not just rust. It rusts in the way the water goes, and understanding that tells you what to do about it.

## The four things that corrode metal

- **Water.** Nothing corrodes without it. Everything on a farm has it.
- **Oxygen.** Wet steel needs both.
- **Salt.** Road salt, manure, urine, fertiliser, and the damp air near the sea. Salt cuts the time to rust by a factor of several.
- **Different metals touching.** This is galvanic corrosion, and it is the one that eats parts nobody expected. See [[gates-and-brackets]].

## Galvanising

- **Hot dip galvanising** coats the steel with zinc and it is the best value corrosion protection there is for farm steel. It lasts 20-40 years in a normal yard.
- **The zinc protects the steel even where it is scratched**, as long as the scratch is small. It corrodes in preference to the steel and closes the gap.
- **Galvanising does not survive welding.** The coating burns off around the weld. Protect the weld with a zinc-rich paint or a cold galvanising aerosol. See [[sheet-metal-fixing]].
- **Galvanised and stainless must not touch.** The stainless will be fine and the galvanised will be destroyed. Use a barrier.
- **Galvanised sheet in a shed where you weld will flake** as the fumes attack it. Weld somewhere else, or protect the roof.

## Paint and coating

| System | Where | Life |
| --- | --- | --- |
| Zinc-rich primer plus topcoat | Welded steelwork, repairs | 3-5 years |
| Alkyd enamel | General farm steel | 2-3 years |
| Epoxy primer | Steel that is going to be welded or wet | Under a topcoat |
| Cold galvanising paint | Touch-ups on galvanised steel | Long |
| Bitumen or tar | Underframes, buried steel | Long |
| Stainless 316 | Washdown, food, coastal | Very long |

- **Prep is the whole job.** A wire brush and a degreaser, then rust back to bright metal, then the primer within hours.
- **Paint over rust and it will come off in sheets.**
- **Paint the bolt heads and nuts as well as the steel.** See [[bolts-and-fasteners]].

## Rust removal

- **Needle gun, wire brush, or abrasive blasting** for a proper job.
- **A wire wheel on an angle grinder** is fast and it will take the paint with it.
- **Rust converter** and a rust-inhibiting primer is fine for a small job and a tool shed.
- **Do not weld over rust that has not been removed.** It comes out under the weld and you are back where you started. See [[mig-welding-basics]].

## The places that always go first

- **The bottom of a gate post**, in the ground or in the mud.
- **The underside of a trailer chassis** and the sills.
- **The bolt heads on a hinge**, and the latch.
- **Anywhere two metals meet** - a galvanised bracket bolted to a stainless hinge, a copper pipe to a galvanised tank.
- **Around a weld in a galvanised part.** See [[welding-safety-on-the-farm]].

## A simple annual routine

1. **Wire brush and touch up every spring**, before the wet season.
2. **Check the galvanised items** for white rust and the stainless for tea staining.
3. **Replace the fasteners** that have seized rather than fighting them.
4. **Check the anodes on anything galvanised that is in water** - a water tank, a trough.

> **Rust always starts where two things rub, where water sits, or where two metals touch.** Look in those three places first.
""",
    },
    {
        "slug": "tyre-pressures-and-loads",
        "title": "Tyre pressures and loads",
        "category": "workshop-fabrication",
        "summary": "A tractor tyre at the wrong pressure is a wear problem, a fuel problem and a safety problem.",
        "author": "Marta, arable",
        "difficulty": "easy",
        "read_minutes": 4,
        "tags": "tyres,pressure,load,ballast,traction,trailer",
        "body": """Tyre pressure is the cheapest way to change how a machine works, and it is the setting most people never touch.

## Why it matters

- **Under-inflated** means the tyre squashes, the sidewalls flex, the shoulders scrub off, the fuel goes up and the tractor wanders.
- **Over-inflated** means the tractor bounces over the lumps, the lugs do not grip, the soil compacts and the centre of the tyre wears out.
- **The pressure in a tubeless tyre is set by the load.** A trailer carrying a heavy load needs lower pressure than an empty one.

| Situation | Pressure |
| --- | --- |
| Trailer, light load | High, close to the sidewall rating |
| Trailer, full load | Low, down to the load rating in the handbook |
| Tractor, light soil work | Low |
| Tractor, road transport | High |
| Tractor, front axle with a loader | Set for the load, and check it with the loader down |

- **Always use the sidewall rating as the maximum and never exceed it.** The sidewall also carries the load and speed rating, and the lower of the two rules.
- **The handbook value for a given load beats the sidewall maximum.**
- **Check the pressure cold**, in the morning, before the tyres have warmed up. A hot tyre reads 20-30% higher.

## Ballast and weights

- **Front weights balance a rear-mounted implement.** A heavy rear implement lifts the front wheels and you lose steering and traction. See [[hitching-and-towing]].
- **Ballast is cheaper than a bigger tyre.** A front weight bracket and 500 kg of cast iron will save a set of tyres.
- **Match the ballast to the work.** Ballast for the heaviest job and you are carrying dead weight all day.
- **Remove the weights for transport and for yard work.**

## Checking and maintaining

- **A tyre gauge with a good dial is a tool worth having.** A cheap pencil gauge is not accurate.
- **Check the pressures on the tractor, the trailer, the quad and the car.** See [[tyre-pressure-fuel-use]].
- **Look for cuts, bulges and embedded objects** in the sidewall and the tread.
- **Never stand behind a tyre that is being inflated** and never inflate a tyre with a bead that is not seated.
- **The load rating on the sidewall is per tyre**, and the axle rating is per axle. Do not exceed the axle.

> **A tyre at the wrong pressure will cost you a set of tyres before it costs you an hour.**
""",
    },
    {
        "slug": "underground-pipe-and-trenches",
        "title": "Underground pipe and trenches",
        "category": "workshop-fabrication",
        "summary": "Trenching, laying and testing a water line, and the rules that stop the tractor finding it in January.",
        "author": "Sam K.",
        "difficulty": "moderate",
        "read_minutes": 5,
        "tags": "pipe,trench,water,underground,service,ditch",
        "body": """Burying a water line from the borehole to the yard is a job that is easy to get wrong and expensive to get wrong twice.

## Plan it

- **Map it.** Draw the route and keep the drawing. The next person to dig will need it.
- **Call before you dig.** In some places you have to, and you should know where the electric and the phone are.
- **Plan the fall.** Water needs to go somewhere. Lay the pipe with a steady fall towards a drain or a soakaway, not level.
- **Avoid the roots, the drains and the cesspit.**
- **Keep the pipe well away from the water tank's overflow** and away from where the tankers park.

## The trench

- **Trench width:** enough to work in and to get the pipe in a bed of sand. 300 mm is the minimum for a small supply.
- **Trench depth:** a minimum of 750 mm for PE pipe, and deeper in ground that is driven over or cultivated. Follow the local rules and the pipe maker's instructions.
- **The bottom of the trench must be firm and smooth.** No stones, no roots, no sharp edges.
- **A bed of sand, 100 mm, under the pipe.** The pipe does not lie on stones.
- **Backfill with sand first**, up and around the pipe, and compact it. Then the rest of the backfill.

| Burial depth | Ground conditions |
| --- | --- |
| 750 mm minimum | Under grass, not trafficked |
| 1.0 m | Under a yard that is driven on |
| 1.2 m minimum | Under a cultivated field or a track |

- **Put a marker tape 300-450 mm above the pipe** and a marker post at each end and at every change of direction.
- **Fill in with the same soil you took out**, not with rubble.

## The pipe and the fittings

- **PE pipe with compression fittings**, laid in a straight run, with the fittings made up as the maker says and buried in sand. See [[pipe-and-plumbing]].
- **A mains or a tank connection with a proper isolation valve and a drain-down point.**
- **A frost pit** at the shallowest point if the line cannot be buried deep enough. A vertical pipe with a valve at the bottom, so the water can be pushed out when it freezes. It has to be below the frost line.
- **Put the stopcock where you can reach it in the dark and in the rain.** Put it in a chamber with a lid, at the house or the yard entrance.

## Testing before you backfill

- **Fill the line with water and leave it under pressure** for an hour or two, with the ends capped. Check every joint and every exposed length.
- **Do not backfill until it has held.**
- **Then backfill, and then do it again once the trench has settled** - the joints settle after a frost.

## Maintenance

- **Know where the stopcock is** and keep it accessible. Nothing is more frustrating than a leak you cannot shut off.
- **Keep the record of the route** with the water board and the insurance policy.
- **Mark the route on the farm map.**

> **Every job that digs a hole on a farm has turned up a water pipe, a electric cable or a gas line at some point. Know what is under the ground before you dig.**
""",
    },
    {
        "slug": "lagging-water-pipes",
        "title": "Lagging water pipes",
        "category": "workshop-fabrication",
        "summary": "Insulating pipework so it does not freeze, and the two mistakes that make lagging useless.",
        "author": "Sam K.",
        "difficulty": "easy",
        "read_minutes": 4,
        "tags": "lagging,insulation,pipe,frost,water",
        "body": """Lagging is cheap and it works, but only if it is done properly and only if the pipe is actually empty when it freezes.

## Why pipes freeze

- **Water expands about 9% when it freezes.** A pipe that is full of water and freezes will split.
- **A pipe that is empty and open at both ends can freeze without splitting**, because the ice has somewhere to go.
- **A hot water pipe has a bigger problem** - the heat in the water keeps the pipe warm but it also keeps the insulation working hard.

## What to use

| Material | Use |
| --- | --- |
| Foam pipe insulation | The standard. 25 mm for an outside pipe, 19 mm for a hot pipe |
| Mineral wool | Pipes in a hot place, and where it will not be knocked |
| Foam with foil facing | The best long-term option, it sheds water and it looks right |
| Foam tape on small runs | Cheap, but it tears |
| Lagging on a water tank | Works, but check it every year |

- **Lagging the pipe is not the same as lagging the fittings and the valves.** Insulate the whole run.
- **Seal the joints with tape or a self-adhesive band.** A gap is a heat leak.
- **Finish it with a vapour barrier or foil facing** so the insulation does not soak up water. Wet insulation does not insulate.

## The two mistakes

1. **Lagging a pipe that is full of water and has no way to drain.** See [[draining-water-pipes]].
2. **Lagging a pipe that is already frozen in.** Thaw it first, slowly, with warm water and a cloth. Never with a blowtorch on a cast iron or a plastic pipe.

## Where to lag

- **The outdoor tap and the riser.** This is the one that always goes.
- **The pipe in an unheated shed.**
- **The pipe between the house and the shed, at the wall penetration.**
- **The header tank feed and the pipework in a loft or an unheated garage.**
- **The pipe to a yard trough or a washing point.**

## Also do these

- **Put the isolated outdoor tap inside, or use a frost-proof tap.** A tap with a hose on it is a pipe full of water to the outside of a wall.
- **Drain the washing machine and the outside lines** in a building that is not heated. See [[draining-water-pipes]].
- **Keep the heat on in the pipe run for a couple of hours before a hard frost** if you have a timer.
- **Do not use a tumble dryer vent or an oven to heat the whole house to solve it.**

## Check it

- **Look at the lagging every autumn** and replace the chewed and split sections.
- **Check the outdoor tap** and the exposed pipework on the first really cold morning.
- **Know where the stopcock is.** See [[underground-pipe-and-trenches]].

> **Lagging a pipe that is full of water gives you a frozen pipe with insulation on it. Drain it first, or accept that it will split.**
""",
    },
    {
        "slug": "draining-water-pipes",
        "title": "Draining water pipes",
        "category": "workshop-fabrication",
        "summary": "Draining a system properly before the frost, and getting it back afterwards without a flood.",
        "author": "Sam K.",
        "difficulty": "easy",
        "read_minutes": 4,
        "tags": "draining,pipes,frost,shut off,water",
        "body": """If a system is going to stand empty through a hard winter, it has to be drained properly. "Turn the tap off" is not draining.

## The order

1. **Turn off the water at the main stopcock.** Know where it is and that it works before you need it.
2. **Turn off the boiler and any water heater**, and let them cool.
3. **Open every outlet** - every tap, the shower, the outside tap, the washing machine, the dishwasher, the cistern, the water troughs, the hose reels.
4. **Open the drain points** - the drain valve on the boiler, the drain valve on a water tank, the bleed screw on a radiator.
5. **Let it all run until it is dry.** Water that is left in the low points is the water that freezes.
6. **Leave the outlets open** until the system is back in use. A closed system with a trapped void is worse than an open one.

## The parts that hold water

- **The cistern and the toilet.** Isolate the feed and empty the cistern, or fit a non-freezing drain.
- **The boiler.** A boiler has a drain valve. Open it and leave it open, and open the cold feed pipe too.
- **The radiator and the heating pipes.** Open the bleed valve at the highest point and the drain at the lowest.
- **The water tank.** Drain it and leave the outlet open. See [[root-cellar-storage]] for storing things cold.
- **The washing machine.** Turn off the tap, unplug it, and open the filter and the door.
- **The outside tap and the hose.** Disconnect the hose. It holds a litre of water and it is right at the wall.
- **The trough and the yard taps.** See [[water-troughs-and-algae]].

## Coming back into service

1. **Close the drain points** and the bleeds.
2. **Open the mains slowly** and let the air out at the highest point until the water comes out solid, with no spitting.
3. **Open the outlets one at a time.**
4. **Refill the cistern and the boiler.** Follow the maker's sequence for your boiler - some lock out if they are refilled in the wrong order.
5. **Run every tap until the water is cold and clear** and check for leaks at every joint you opened.
6. **Check the boiler pressure** and the heating, and check the pressure again the next day.

## What not to do

- **Do not use a blowtorch on a frozen pipe** unless you are certain it is metal and you know what you are doing. A plastic pipe with a torch on it is a fire and a flood.
- **Do not use a hairdryer or a heat gun unattended**, and never inside a cupboard.
- **Do not leave the system partly drained** - it will freeze from the top down and the top is where the damage is.

> **Test your drain-down before you need it.** On a warm day in November, drain the system, then refill it. That is a whole lot easier than doing it in a flood on a January night.
""",
    },
    {
        "slug": "wood-burning-and-stove-dampers",
        "title": "Wood burning and stove dampers",
        "category": "workshop-timber",
        "summary": "Burnt wood is the cheapest heat on a farm. Getting the air right is the whole trick.",
        "author": "Wes, workshop",
        "difficulty": "easy",
        "read_minutes": 5,
        "tags": "wood,stove,dampers,fire,heat,ash",
        "body": """A wood stove is the best value heat on a farm, and it is also a fire waiting to happen if you get the chimney wrong.

## The damper controls

- **The air inlet control** is the primary control. Open it for a hot fire, close it down for a long slow burn.
- **The flue damper or bypass** controls how fast the smoke leaves. Open for a fast burn, closed for a slow one.
- **Never close the flue damper while the fire is burning.** That is how you get a smoke-filled room and a carbon monoxide alarm going off.
- **The ash door** controls the air under the fire. A partly open ash door gives a slower burn with less smoke.
- **Learn the stove on a mild day**, not in the first cold week of the year.

## Getting the burn right

- **Seasoned wood burns. Green wood does not.** Green wood puts out steam, smoulders, makes creosote and will eventually block the flue. See [[timber-and-posts]] for the drying time.
- **Split the wood.** It dries faster and it burns better. See [[splitting-firewood]].
- **Small splits burn hotter.** Big logs smoulder.
- **A hot burn with the damper open, then a slow burn with it nearly shut** is the pattern to aim for.
- **Take the ash out** every day or two, into a metal bin with a lid, on a non-combustible surface, away from the building. See [[hot-work-and-fire-safety]].
- **Leave a bed of ash in the firebox.** It insulates and it slows the burn.

## Chimneys and flues

- **The flue has to be swept.** Every year, before the season, and more often if you burn a lot. A tarred flue is a chimney fire waiting to happen.
- **The chimney pot or the cowl must be more than 1 m above the ridge** of the roof, and more than 2 m from anything nearby.
- **A stove needs a carbon monoxide alarm** if the stove is in a room, and it needs a smoke alarm. Test both.
- **A stove in a workshop with a welder is a bad combination** - the welding fume and the stove smoke will fight for the extract.
- **The hearth must be a fireproof surface** and big enough for the door swing.

## Safety

- **The back of the stove gets hot enough to set fire to a wall.** Keep 300 mm of clearance, or use a heat shield.
- **Do not burn treated timber, painted wood, or pallet wood.** The smoke is toxic. See [[pallets-and-scraps]].
- **Do not burn plastic, cardboard with tape on it, or building insulation.**
- **Keep a fire blanket and a bucket of sand** next to the stove, not in the cupboard.
- **The ash bin has a metal lid and sits on concrete.**

> **A stove that smokes is a stove that is missing air or has wet wood. Fix one of those two things before you do anything else.**
""",
    },
]
