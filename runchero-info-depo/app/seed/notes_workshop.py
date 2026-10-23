"""Extra notes for the workshop: welding, fabrication and timber."""

from __future__ import annotations

NOTES: list[dict] = [
    {
        "slug": "mig-welding-basics",
        "title": "MIG welding: the basics that make good welds",
        "category": "workshop-welding",
        "summary": "Wire, gas, stickout, torch angle and speed. Set these five up and most MIG welds come out right first time.",
        "author": "Wes, workshop",
        "difficulty": "moderate",
        "read_minutes": 7,
        "tags": "mig,welding,arc,steel,fabrication",
        "featured": 1,
        "body": """MIG welding - gas metal arc welding - is the first process most people learn and the one they use the most. It is forgiving, it is fast, and it will hide bad technique if you are not careful.

## The setup

- **The machine.** Set the voltage and the wire speed for the material and the wire. The manual gives a table; start there and adjust.
- **Shielding gas.** For outdoor work on mild steel, use a mix of argon and CO2 - 80/20 is the common one. Pure CO2 makes a hotter, spatterier arc and needs more wire. Nitrogen in the mix will ruin the weld.
- **Gas flow.** 10-15 litres a minute for MIG, up to 20 for a big gun. Set the flowmeter before you light the machine.
- **The torch.** Check the liner, the nozzle and the contact tip before every job. A worn liner is the most common cause of a poor MIG weld.

| Wire | Material | Typical use |
| --- | --- | --- |
| 0.6 mm solid | Mild steel, 1-2 mm | Thin sheet, general repair |
| 0.8 mm solid | Mild steel, 2-4 mm | Farm repair work |
| 0.9 mm solid | Mild steel, 3-6 mm | Structural work |
| 0.8 mm flux core | Mild steel, 3-8 mm | Outdoor work, no gas needed |
| 1.0 mm flux core | Mild steel, 6-12 mm | Heavier structural work |
| 0.9 mm MIG aluminium | Aluminium | Gate frames, alloy parts |
| 1.0 mm MIG stainless | Stainless | Wash-down areas, tanks |

## The five things that matter

**Wire stickout.** The distance from the contact tip to the work. 10-15 mm for short-arc work, 20-25 mm for spray and penetration on thicker plate. Too short and you get a stubby, cold weld. Too long and the arc is unstable.

**Torch angle.** 10 to 15 degrees of drag - pulling the torch slightly in the direction of travel. Pushing the torch makes a bead that sits on top and a bad root.

**Travel speed.** Steady and even. If you are slow the heat builds up and the bead becomes a wide, flat, burnt lump. If you are fast the bead is narrow, high and cold.

**Arc length.** Keep the contact tip about one wire diameter off the work. A gap the size of the wire diameter is the standard short arc.

**Work angle and position.** Flat and horizontal is the easy part. Vertical needs slower travel and more heat, and overhead needs practice.

## The sequence of a fillet weld

1. **Fit up and tack.** Two or three tacks, not five. Check the alignment with a square before you tack.
2. **Grind the tacks flat.** A weld starts at a defect.
3. **Weld the first leg** - the one you stand behind, so the slag falls away from you.
4. **Clean it.** Chip the slag and grind or wire brush the bead. Filler metal will not stick to a dirty bead.
5. **Weld the second leg**, and make sure the wire lands on the centre of the first bead.
6. **Clean, inspect, and dress** the profile. A smooth bead with no undercut and no spatter is a good weld.

## Filler and joint preparation

- **Clean the steel back to bright metal** within 20 mm of the joint. Paint, rust, oil and galvanising all stop a weld.
- **Grind out the old weld** completely if you are re-welding. Do not weld over it. See [[repairing-a-cracked-frame]].
- **Bevel the thicker edge** if you are welding over 5 mm. A V or a U prep will let you fill the joint properly.
- **Fit-up is more important than the welding.** Use clamps, clamps and more clamps.

## Safety

- **Eye protection with the correct shade lens** on the helmet, plus goggles or a visor for grinding. See [[welding-safety-on-the-farm]].
- **A helmet with a proper auto-darkening filter** is worth the money.
- **Extraction.** MIG on galvanised or painted steel makes fume that will make you ill the same evening. See [[venting-the-workshop]].
- **Fire watch.** A fire blanket and a bucket of sand within reach. See [[hot-work-and-fire-safety]].

> **Practise on offcuts.** Ten minutes of bead on a piece of scrap does more for your welds than any amount of reading.
""",
    },
    {
        "slug": "stick-and-tig-welding",
        "title": "Stick and TIG welding",
        "category": "workshop-welding",
        "summary": "The other two arc processes, when to reach for them, and what makes them different from MIG.",
        "author": "Wes, workshop",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "stick,arc,tig,aluminium,stainless,welding",
        "body": """MIG covers most farm repair work. But there are jobs where stick or TIG is simply better.

## Stick (SMAW) welding

The electrode melts to make the joint. Slower than MIG, but it is robust, it works outside in the wind and rain, and it is forgiving on dirty steel.

**The electrodes you will use:**

| Electrode | Material | Notes |
| --- | --- | --- |
| 6013 | Mild steel | The general-purpose one. Easy, forgiving, all-position |
| 7018 | Mild steel | Stronger, low hydrogen, good for structural and 7018 for outdoor joints |
| 308L | Stainless | Stainless steel and stainless to mild steel |
| 4043 | Aluminium | Aluminium and most alloys except the 5000 series |
| 7018 is the one to buy | | Good all-round choice for farm work |

**The technique.**

- **Hold the electrode at about 70 degrees to the work, in the drag position.**
- **Maintain a short arc.** 2-3 mm gap. A long arc gives a wandering, weak weld.
- **Keep the arc on the leading third of the puddle**, not at the front edge and not behind. A long puddle is a cold, wide, weak weld.
- **Angle the electrodes 20-30 degrees to the work** for an uphill or overhead weld, so the slag peels off behind the arc.
- **Let each pass cool and clean it** before you weld the next one. See [[mig-welding-basics]].
- **Watch for the stub** - if the arc keeps going out, the electrode is too far away or the amperage is too low.

**Where stick wins:** outdoor repairs, dirty or rusty steel, in a wind, on a trailer frame, on a gate post, and anywhere you need to weld in a awkward position with one hand.

## TIG (GTAW) welding

An arc between a tungsten electrode and the work, shielded by argon, with the filler rod added by hand. Slow, precise, and the best looking weld you can make.

**When it is worth it.**

- **Aluminium.** MIG is poor on aluminium and TIG is the answer. See [[gates-and-brackets]].
- **Stainless.** TIG gives a clean, unpickled weld with full corrosion resistance. See [[pipe-and-plumbing]].
- **Thin sheet.** 1 mm and down.
- **Repair work where heat has to be controlled**, or where the joint must be invisible.

**The technique.**

- **Tungsten is not an electrode.** It is not meant to touch the work. The gap between the tungsten and the work sets the voltage.
- **Use the right tungsten for the material.** Pure green for aluminium, lanthanated red or blue for steel, thoriated red for general work.
- **The tungsten angle is 15-20 degrees for a DCEN start.** Grind it on a dedicated wheel, with a grinding wheel that is not for steel.
- **Set the argon flow to 6-10 litres a minute.** Too little and you get oxidation, too much and you blow the arc around.
- **The puddle is the key.** Push the puddle around with the torch. A puddle that sits still is a puddle that is freezing.
- **Add the filler from the side, into the leading edge of the puddle.** Do not stab at the puddle.
- **Do not let the tungsten touch the filler or the work.** It will contaminate the weld and you will throw the tungsten away.

**TIG is a filler-in-the-hand skill.** It takes a day of practice to be competent and a year to be fast.

## Choosing

| Situation | Process |
| --- | --- |
| Farm gate, frame, trailer repair | MIG or stick |
| Outdoor job in the wet | Stick with flux core |
| Aluminium gate or trough | MIG with spool gun, or TIG |
| Stainless tank or rail | TIG |
| 1 mm sheet | TIG or MIG |
| Structural steel over 10 mm | Stick or flux core MIG |
| Repair in a confined space | Stick - MIG spatter is a problem in there |

## Common mistakes

- **MIG: wire feed speed too high** - the gun gets hot and the spatter increases.
- **Stick: arc too long** - a weak, wide, spattery weld.
- **TIG: too much gas, too little gas, or tungsten contamination** - all three make the same spitting noise.
- **All three: welding over dirty steel.** Clean it back to bright metal. No exceptions.

> **Do not mix processes on the same job without telling whoever inspects it.** Different processes need different testing.
""",
    },
    {
        "slug": "welding-safety-on-the-farm",
        "title": "Welding safety on the farm",
        "category": "workshop-welding",
        "summary": "Fumes, fire, electricity, noise and the neighbouring shed. Most welding injuries happen twenty minutes before the weld.",
        "author": "Wes, workshop",
        "difficulty": "easy",
        "read_minutes": 6,
        "tags": "safety,welding,ppe,fume,fire",
        "body": """Welding is not the most dangerous job on the farm, but it has a peculiar set of hazards, and most of them are not the arc.

## Before the arc

- **Clear the area.** Remove anything that can burn within 11 metres of the work. That includes paper, straw, paint, solvents, fuel and gas cylinders. See [[hot-work-and-fire-safety]].
- **Have a fire watch.** Somebody whose only job is the fire. With a bucket of water, a fire blanket and a torch.
- **Have a fire extinguisher** within reach and know which type it is. A CO2 extinguisher for a gas fire, a water extinguisher for wood, dry powder as the general-purpose one.
- **Check the earth clamp.** It must be on the job itself, not on a scaffold or a machine that might be moved. See [[earth-clamp-tyres-and-leads]].
- **Check the leads** for damage and check the insulation on the electrode holder.
- **Know where the gas cylinder is and where the isolator is.** Both should be reachable without walking past the arc.

## During the weld

- **Helmet on before you strike the arc.** The flash burns the retina and you will not see it coming. A welder's flash is a permanent eye injury.
- **Correct shade lens.** Shade 10-13 for MIG and stick on mild steel. A glass shade 5 is for gas welding. The shade is on the front of your helmet for a reason.
- **Goggles or a face shield for grinding.** A welder's helmet is not eye protection for grinding.
- **No gloves near the electrode holder** in stick welding - the heat is at the holder. Gloves are for handling hot metal and for the grinder. See [[cutting-and-grinding-metal]].
- **A leather apron and sleeves** for any overhead or hot work.
- **Ventilation.** This is the one most people get wrong. See below.
- **Keep the gas cylinder upright and secured** with a chain or a strap, with a regulator and a hose that is not stretched over a sharp edge.

## The fumes

Welding fume is metal oxide, and it can make you ill the same evening - headache, sore throat, chest tightness, and a cough that lasts for days. Worse, the fume from galvanised steel contains zinc oxide, which causes metal fume fever, and from painted or dirty steel contains lead and chromium compounds.

- **Extract the fume.** A portable extraction unit with a hood near the work, or a workshop with a proper extraction system. See [[venting-the-workshop]].
- **Never weld galvanised steel without extraction.** Zinc fume is the nastiest of them.
- **Never weld on a container that held fuel, chemicals or anything unknown.** The vapour inside will burn or explode. Gas it out first.
- **Never weld stainless or aluminium without a clean, dedicated extraction** and without contaminating your steel extraction. See [[stick-and-tig-welding]].
- **Know where your fume is going.** An open door into a cowshed puts the fume into the cows.

## Electricity

- **Check the earth clamp** every time. A clamp on a greasy, painted or rusty surface is not a ground.
- **Keep the machine off the ground** and off damp floors. A workshop floor that is wet and a 230V machine is a shock risk.
- **Do not weld in the rain** unless you are using a machine and leads rated for it. See [[stick-and-tig-welding]] for the wet-weather process.
- **Extension leads** on a lead that is longer than the machine's own lead will cause voltage problems. See [[earth-clamp-tyres-and-leads]].

## Noise and the rest of the body

- **Ear protection** for grinding, chipping and hammer work.
- **Welding in a confined space** - a trailer, a silo, a tank - needs gas monitoring, a spotter outside, and a proper permit. This kills people. See [[storing-grain]] for keeping grain without losing money.
- **Take the position that lets you breathe** - a welding position that puts your head in the fume is a bad one.

## After

- **Turn the gas off at the cylinder**, not just at the torch. Then bleed the hose.
- **Turn the machine off and unplug it.**
- **Check for fire.** Half an hour later, and again before you leave.
- **Leave the helmet off your head** only when the area is clear of moving parts. A loose helmet on a bench is a way to break your neck.

> **If the job needs a permit, needs a gas monitor, or needs a spotter, you do not have the equipment to do it safely.** Book someone in who does.
""",
    },
    {
        "slug": "cutting-and-grinding-metal",
        "title": "Cutting and grinding metal",
        "category": "workshop-welding",
        "summary": "Angle grinder, plasma, cold chisel and the rules that keep the sparks out of the straw.",
        "author": "Wes, workshop",
        "difficulty": "easy",
        "read_minutes": 5,
        "tags": "grinder,cutting,plasma,chisel,sparks",
        "body": """Grinding and cutting is the most common metalwork on a farm, and the easiest way to set a shed on fire.

## The angle grinder

- **Check the disc before you mount it.** The speed rating on the disc must be at least the speed of the grinder. Look for cracks, and check the date stamp on the cut-off wheel - resin discs have a shelf life.
- **The guard goes on.** Every time. It is there for the sparks and the fragments.
- **Hold it with two hands.** The side handle is not optional.
- **Let the wheel do the work.** Pressing harder grinds slower and throws more sparks.
- **Keep the wheel at about 15 degrees to the surface**, not flat, so sparks go down and away from you.
- **Never cut on a round pipe held in your hand.** Put it in a vice.
- **Angle grinder in a vice with the wheel spinning** is a bad combination. Support the work properly.

| Guard | Wheel | Use |
| --- | --- | --- |
| No guard | Cutting off | Never |
| 90% guard | Cutting off | Cutting and grinding |
| Full guard | Grinding wheel | Grinding only |
| Full guard | Wire brush cup | Cleaning |

## Cutting metal

**Angle grinder with a cut-off wheel** - fast, cheap, and it makes a bevel. It is the right tool for most farm jobs, and it is noisy and it throws sparks everywhere.

**Plasma cutter** - the tool for thick plate. A plasma cut is a clean, straight, square edge that a grinding wheel cannot make. It needs air and a working supply. See [[welding-safety-on-the-farm]] for the hazards.

**Oxy-fuel** - for heavy thick plate and for cutting dirty, painted or rusted steel. It is slower, it is hot, and it leaves a scale that must be cleaned before welding.

**Cold chisel and hammer** - for cutting out rivets, shearing off a bolt head, and cutting a flat in a tight spot where nothing else fits.

**Band saw** - for accurate cuts in sections. Worth having for repeating the same cut.

## Sparks and fire

- **Sparks travel ten feet.** A grinder throws burning metal a long way, and it goes down into the straw.
- **Work on a non-combustible surface.** A metal bench or a concrete floor, not a wooden one.
- **Clear the area of anything that burns.** See [[hot-work-and-fire-safety]].
- **Have a fire blanket and a bucket of water within reach.**
- **Do not grind on the tailgate of a trailer with straw in it.** Move the vehicle or move the job.
- **Stop work if you are tired.** Most grinder injuries happen at the end of a long day.

## Grinding properly

- **Keep the wheel at 15-20 degrees to the work.**
- **Use a light touch** and let the wheel cut.
- **Do not side-load a cut-off wheel.** A side load will crack it and it can come apart at 12,000 rpm.
- **Let the wheel stop before you put the grinder down.** Never stop it on the work.
- **Check the wheel has stopped before you lift the guard.**

## Hot work

- **Hot metal is worth respecting.** A piece of steel at cutting temperature will burn through a glove, and it will keep burning after it looks cold.
- **Have a designated quenching can** - a bucket of water or sand for offcuts. Not on the floor, not in the straw.
- **Let the offcut cool before you pick it up.**

## PPE

- **Eye protection** - goggles, and a face shield for the sparks that come off the sides.
- **Ear protection.**
- **Respirator** for grinding galvanised or painted steel. See [[venting-the-workshop]].
- **Leather gloves** for handling hot metal and for the grinder body.

> **A grinder is the most dangerous tool in the workshop and the least expensive to use carefully.** Guards on, two hands, and nothing flammable within ten feet.
""",
    },
    {
        "slug": "trailer-repair-and-welding",
        "title": "Trailer repair and welding",
        "category": "workshop-fabrication",
        "summary": "Frames crack at the same six places. Chassis, axle, springs, drawbar - and the checks that keep a trailer legal.",
        "author": "Wes, workshop",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "trailer,repair,welding,chassis,axle,brakes",
        "body": """A trailer is a stressed box on springs, and it fails in predictable ways. If you know where it cracks, you can find it before it lets go on a hill with a load on.

## Where trailers fail

- **The spring hangers and spring seats.** Cracks start at the ends of the springs where the load goes up into the body.
- **The axle-to-suspension welds.** The classic crack, and it is a fatigue crack so it grows slowly.
- **The drawbar and its gusset plates.** The gussets crack at the toe, near the ring.
- **The body-to-chassis joints**, especially at the rear crossmember.
- **The rims**, at the weld between the disc and the rim.
- **The chassis rails**, at the over axle area, especially where a load hanger is welded on.

## A crack in a chassis is a stop

- **A crack in a structural member is not a repair job for a Saturday.** Chassis cracks need a design: doubler plates, boxed sections, and a competent welder.
- **A doubler plate must be a different size and thickness to the parent metal**, and the pack must be ground back to a taper.
- **Never weld a crack straight. Weld in the metal that is missing.**
- **Do not weld over a crack and walk away.** Grind it out to sound metal and inspect the joint before you fill it.

## The repair sequence

1. **Jack it up safely.** Use axle stands, rated for the load, on firm ground. Never work under a trailer on the jack alone. See [[jack-points-and-stands]].
2. **Strip the part.** Take the wheel off, take the bed off if you have to, get to the metal.
3. **Grind back to clean metal.** Bright steel, no rust, no paint, no old weld. See [[mig-welding-basics]].
4. **Check the whole area for the cause.** A cracked spring hanger is usually a cracked spring hanger because the shock absorber is dead or the load is too heavy. Find the cause.
5. **Fit the new part, bolt it or tack it, check the alignment, then weld it.**
6. **Weld the doubler plates, the gussets and the load hangers back on.**
7. **Re-check everything with the trailer loaded**, not empty.

## Brakes and lights

- **A trailer must have working brakes if it is over a certain weight.** Check the local rule. See [[trailer-brakes-and-lights]].
- **Test the brakes with the load on.** A trailer that will not stop at 20 mph empty will not stop at 20 mph loaded.
- **Check the coupling over the pin, the safety chain, the breakaway cable, and the lights.** Every trip. See [[trailer-brakes-and-lights]].
- **The breakaway cable** should be attached separately from the safety chain, so that if the coupling comes off, the brakes apply.

## Wheels and tyres

- **Check the wheel nuts on a bearing hub after the first 50 miles** and then regularly. A wheel nut off on a loaded trailer is a road accident.
- **Tyre pressures** on a trailer are set for load, not for the side of the road. See [[tyre-pressures-and-loads]].
- **Repairs to a tyre sidewall are not proper repairs.** A trailer tyre that has had a sidewall cut is a scrap tyre.

## Welding on a trailer

- **Weld from the outside where you can.** The distortion of a trailer frame is the enemy.
- **Tack, check, then weld.** Use clamps to hold the alignment.
- **Do not weld on a galvanised chassis without grinding it back and extracting.** See [[welding-safety-on-the-farm]].
- **Weld with the tractor attached, if you can.** A trailer on its drawbar is lighter to drag, and it keeps the frame straight.

> **Check the spring hangers and the axle welds on every trailer every year**, with the trailer jacked and the wheels off. It takes twenty minutes and it is the difference between a repair and a write-off.
""",
    },
    {
        "slug": "gates-and-brackets",
        "title": "Gates and brackets",
        "category": "workshop-fabrication",
        "summary": "Hinges, latches, gussets and the standard sizes. A gate that closes properly is worth more than a gate that looks good.",
        "author": "Wes, workshop",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "gates,hinges,brackets,fencing,aluminium",
        "body": """A farm gate is a hundred kilos of steel on a hinge that sees the whole force of the animal when it is kicked. The bracket is the part that fails.

## Standard gate sizes

| Opening | Gate leaf | Post |
| --- | --- | --- |
| 3.0 m (10 ft) | 3.0 m | 100 x 100 mm |
| 3.6 m (12 ft) | 3.6 m | 100 x 100 mm or 150 mm |
| 4.3 m (14 ft) | 4.3 m | 150 x 150 mm |
| 5.0 m (16 ft) | 5.0 m | 150 x 150 mm square or 200 mm round |

- **A gate needs a post that is set deep.** A 150 mm post goes in 900 mm, in concrete in a hole, not pushed in. See [[setting-fence-posts]].
- **The post must be plumb and in line with the fence**, or the gate will not swing properly and the latch will not line up.
- **The opening measurement is the gap between the posts**, and the gate leaf is made to that.

## The hinge

- **A gate hinge is bolted or welded to the post and the gate.** The welded-on lug on a square post is the strong option; a post-mounted hinge is easier but the screws pull out of a hollow post.
- **A heavy gate needs a top hinge with a drop bolt, and a bottom hinge.** One hinge in the middle lets the gate drop and rack.
- **The gate must swing against the post and the stop**, so the animal pushes it shut.
- **Never weld a hinge onto a hollow section without reinforcing it.** Weld a backing plate inside first.
- **Stiffen the hinge side of the gate leaf** with a flat bar or an angle. It is the side that carries the load.

## The latch and the keeper

- **The latch must be operable from the tractor seat.** If the driver has to get out to open the gate, it will be left open.
- **A gravity latch with a drop bar** is the standard for a stock gate. A spring-loaded self-closing latch is better still.
- **The keeper must be on the post, not on the gate**, and it must be a solid weld.
- **The latch and the keeper must not foul the post** when the gate swings.
- **A chain and a shackle is not a gate latch.** It is a temporary fix that becomes permanent.

## Gussets and reinforcement

- **Gusset the drawbar.** The toe of the gusset is where it cracks.
- **Gusset the corners of the gate frame** where the rails meet the stiles.
- **Do not put a gusset on both sides and think the job is done.** The real fix is to move the load away from the joint.

## Aluminium gates

- **Aluminium is the right material for a gate you open by hand.** It is a third of the weight of steel.
- **You cannot TIG weld aluminium near a steel workbench** without contaminating it. See [[stick-and-tig-welding]].
- **Aluminium and steel galvaniically corrode where they touch.** Use a barrier - a nylon washer, a bit of tape, or a coating.
- **Aluminium is not as stiff as steel.** Use a bigger section or more tubes for a wide gate.

## The build sequence

1. **Measure the opening** between posts, not the space you think you have.
2. **Cut all the tube to length** first, then fit.
3. **Tack the frame up on the bench**, check it is square, then weld it.
4. **Fit the mesh or the infill.**
5. **Hang the gate on the post** with the hinge in place and check the swing.
6. **Fit the latch last**, in the open position.
7. **Adjust the drop bolt so the gate closes tight and latches with a lift of the latch only.**

> **Test the gate with a stock gate on the back of a tractor before you hang it.** Push it hard with the tractor and see what moves.
""",
    },
    {
        "slug": "pipe-and-plumbing",
        "title": "Pipe and plumbing repairs",
        "category": "workshop-fabrication",
        "summary": "Galvanised, copper and plastic pipe, the fittings that leak, and how to find the leak before you make a bigger one.",
        "author": "Wes, workshop",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "pipe,plumbing,galvanised,copper,plastic,leak",
        "body": """Pipe work goes wrong in two ways: it leaks, or it freezes. Most of the work on a farm is a repair, and most of the repairs fail because the pipe was not cleaned and dried before it was joined.

## Galvanised steel pipe

- **Galvanised pipe is the standard for water and for small compressed air lines on a farm.** It is tough and it will not rot.
- **Cut with a hacksaw and ream the bore.** The burr inside the pipe is what blocks the flow and what catches debris.
- **Thread it with a pipe die**, and wrap the thread with PTFE tape or use a compound. Both, for a threaded joint that has to hold pressure.
- **Do not use a tap on galvanised pipe if you can avoid it.** A loose thread on a galvanised pipe is a leak that appears in the frost.
- **Seal the ends of a run with a plug or a cap**, not with a rag or a bolt. A rag in a pipe will be a blockage in the wrong place.

## Copper

- **Copper is for hot water and for heating.** It is easy to work with a pipe cutter and a brazing torch.
- **Cut square, ream, clean, and dry.** Flux only, no oxygen in the flame, and pull the joint tight as it cools.
- **Do not use a compression fitting on a system that gets hot.** They are for cold water, and they are not for gas.
- **Insulate the hot runs.** Copper moves, and a pipe that moves puts a joint under stress.

## Plastic (PE and PVC)

- **Polyethylene (PE) is for cold water and for pipe buried in the ground.** It is laid in a trench, joined with compression fittings or with a butt welder.
- **PVC is for cold water and drainage.** Never for hot water. It goes soft and fails.
- **Compression fittings** need the pipe cut square and reamed, and the compression ring must go on before the fitting.
- **Do not bury fittings.** A joint that is under the ground and under a tractor wheel is a joint you will dig up.
- **Do not lay PE pipe over stones or over a vehicle track.** It gets punctured. See [[underground-pipe-and-trenches]].
- **Support the pipe every metre or so** on a wall or a post, so it does not sag.

## Finding a leak

1. **Listen.** A leak in a pressurised line will hiss, and a leak in a water line you can hear with a screwdriver and a joint.
2. **Look for damp and staining** on the underside of the pipe and on the floor below.
3. **Check the fittings first.** Nine leaks in ten are at a joint.
4. **If it is underground**, the leak may be a pressure loss rather than a visible one. See [[underground-pipe-and-trenches]].
5. **Do not just put a jubilee clip on it.** A clip on a leaking joint is a temporary measure, and it will not survive the winter.

## Frost and lagging

- **Anything that carries water has to be drained or lagged**, or it has to be in a heated building.
- **Lag the vertical risers and the parts in the cold shed**, and lag the outdoor tap. See [[lagging-water-pipes]].
- **Drain the system before the first frost** if it is going to be unused. See [[draining-water-pipes]].
- **Insulate the outside of the lagging with foil or a plastic cover.** Otherwise the condensation goes into the lagging and it stops working.

## Making a joint properly

- **Clean and dry both ends.**
- **Test fit before you tighten.**
- **Tighten with a spanner on the fitting, not on the pipe.** Bending a pipe is how you create a leak in the next joint.
- **Check for leaks with a tissue** along the joint after it is made, rather than waiting for the drip.

> **A joint that has been assembled over mud will fail in the mud.** Clean it, dry it, and keep it clean until it is together.
""",
    },
    {
        "slug": "bolts-and-fasteners",
        "title": "Bolts, nuts and fasteners",
        "category": "workshop-fabrication",
        "summary": "Grades, washers, locking methods and the difference between a bolt that holds and a bolt that pretends.",
        "author": "Wes, workshop",
        "difficulty": "easy",
        "read_minutes": 5,
        "tags": "bolts,nuts,fasteners,grade,washer,nyloc",
        "body": """Most failed structures on a farm fail at a bolt, and almost always for one of three reasons: the wrong grade, no washer, or nothing to stop it turning loose.

## The grades

Bolts are marked on the head. The number is the grade.

| Marking | Property | Use |
| --- | --- | --- |
| 4.6 | Low strength, soft | Sheds and light work only |
| 8.8 | Medium | General purpose, most farm work |
| 8.8 with yellow zinc | General, corrosion resistant | Outdoor farm work |
| 10.9 | High strength | Heavier structural work |
| 12.9 | Very high strength | Not for general farm work |

- **8.8 is the workhorse.** Use it unless you have a reason not to.
- **Never use a 4.6 grade bolt on a trailer, a gate, a post or anything that carries load.** It is soft and it will stretch.
- **Zinc-plated or galvanised for outdoors.** See [[metal-corrosion-on-the-farm]].
- **Stainless for water and for food areas.** A galvanised bolt in a trough will eventually rust through.

## Washers

- **A plain washer under the bolt head spreads the load** and stops the head digging into soft wood or rusty steel.
- **A washer under the nut**, and a flat one under the head, is the correct arrangement. See [[hanging-a-gate-on-a-post]].
- **A penny washer** is a thin wide washer for spreading load on sheet metal. See [[sheet-metal-fixing]].
- **Never use a washer under the nut only**, with nothing under the head. The head will pull through.

## Stopping it turning loose

- **Nyloc nut** - for most bolted joints. It works as long as the joint does not vibrate hard and the nut is not over-tightened.
- **Spring washer** - the old flat spring type. Better than nothing, and it is a poor substitute for a nyloc.
- **Plain nut plus a lock nut** - the lock nut is tightened up against the plain nut.
- **Threadlocker** - for bolts going into aluminium, and for anything that vibrates.
- **Tab washer** - on a shaft or a pin, not a threaded bolt.
- **Split pin and castle nut** - for a wheel nut on a vehicle.

## Torque

- **Tightening to the right torque matters on anything that matters.** A torque wrench is not a luxury on a farm.
- **The rule of thumb:** snug, then a further turn, or use the manufacturer's figure. But use the figure.
- **Do not guess with a spanner and a length of pipe.** A 1.5 m bar on a 20 mm nut is a lot of torque.
- **Tighten in a star pattern** on anything with more than two bolts. See [[trailer-repair-and-welding]].

## Corrosion

- **Galvanised and stainless in the same joint will corrode the galvanised one.** See [[gates-and-brackets]].
- **Stainless bolts in a galvanised or painted structure** will leave a rust stain around the head.
- **Paint the bolt head and nut** after assembly, on a gate or a trailer.
- **Coat the threads** with a corrosion inhibitor or with cold galvanising paint before assembly.

## The one rule

- **A nut needs a washer under it and a bolt needs a washer under its head.** If you take nothing else from this note, take that.

> **Check the grade marking on a bolt before you put it in.** A 4.6 grade bolt on a gate bracket will look fine for a year and then let go when a bull finds it.
""",
    },
    {
        "slug": "timber-and-posts",
        "title": "Timber, posts and treating wood",
        "category": "workshop-timber",
        "summary": "Sizes, species, treatment and how long a post lasts in the ground. Get the timber right and the job lasts.",
        "author": "Sam K.",
        "difficulty": "easy",
        "read_minutes": 5,
        "tags": "timber,posts,wood,preservative,treated",
        "body": """Wood fails in three ways: it rots, the insects get it, and it moves. The species and the treatment decide how long you get.

## Species

| Timber | Good for | Lasts in the ground |
| --- | --- | --- |
| Oak | Posts, gates, hard use | 25-40 years untreated |
| Sweet chestnut | Fencing, posts, hurdles | 15-25 years untreated |
| Larch | Posts, cladding, sheds | 15-25 years untreated |
| Scots pine | General building, treated posts | Only when treated |
| Spruce | Roofing, studwork, internal | Not in the ground |
| Douglas fir | Posts, beams, cladding | 15-20 years treated |
| Hardwood (oak, ash) | Repairs, handles, tool handles | Depends on the job |

- **Oak and sweet chestnut are the traditional farm posts** and they need no treatment at all if they are the heart of the tree and not the sapwood.
- **Softwood is cheaper and it must be treated** if it goes near the ground.
- **Never use spruce or fir for a post in the ground.** It will rot in a few years.

## Posts and setting them

- **Set the post in the ground** - 600 mm for a light fence, 900 mm for a stock fence, 1200 mm for a gate post. See [[setting-fence-posts]].
- **Concrete the gate posts and the corner posts.** A gate post that moves will rack the gate.
- **A post end that is buried in concrete rots faster** because the concrete traps moisture against the timber. The post cap has a metal cap or a slope on it.
- **Set the post plumb.** A leaning fence line looks bad for the life of the fence.
- **Use a post rammer** or a drop weight. See [[setting-fence-posts]].

## Treatment

- **Pressure treated wood** is injected under pressure and the preservative goes right through. It is the standard for posts, rails and fencing.
- **The colour tells you the process.** Green is copper-based, brown is creosote or a water-borne treatment. Both work; creosote will not be painted, and it is not for anything that touches soil or food.
- **End grain drinks the most.** A post that has been cut needs its end re-sealed with a preservative or a cap.
- **Drilled holes need sealing** after the fixings are in.
- **Do not cut treated wood and then leave the cut end exposed.** Use the capping above, or brush on an end-grain preservative.

| Treatment | Where it can go |
| --- | --- |
| Creosote | Fence posts, rails, sleepers. Not near food, not for indoor use |
| Copper-based (green) | Posts, decking, borders. Avoid where livestock will chew it |
| Borate | Internal use, sheds, bird boxes |
| Linseed oil | Tool handles, small wooden items |

## Sheet material and fixings

- **Plywood and OSB** for sheds and for the floor of a trailer. See [[building-a-shed]].
- **Fix sheet material to a frame with screws, not nails.** A screw holds; a nail works loose. See [[sheet-metal-fixing]].
- **Use exterior-grade board and galvanised screws** on anything outdoors.

## Timber sizes for the job

| Job | Size |
| --- | --- |
| Post for a stock fence | 100 x 100 mm treated or 75 x 75 mm chestnut |
| Gate post | 150 x 150 mm treated, or 150 mm round |
| Shed wall studs | 75 x 50 mm |
| Shed roof beam | 100 x 50 mm or 150 x 100 mm depending on the span |
| Trailer board | 19 mm plywood or 25 mm hardwood |
| Fence rail | 75 x 50 mm treated |

## Storage

- **Stack timber off the ground** on bearers, in a stack that is squared up and banded.
- **Cover the top.** The end grain and the top of the stack is what gets wet.
- **Keep it off the ground at both ends** so you can get a bar under it.
- **Treat the ends of a bundle** and the cut ends of every piece.

> **Buy posts with the end grain sealed.** A post that is already starting to go soft at the bottom will not last another five years in the ground.
""",
    },
    {
        "slug": "building-a-shed",
        "title": "Building a shed",
        "category": "workshop-timber",
        "summary": "Site, base, frame, roof and cladding. A simple shed done properly is a week of work and twenty years of no worries.",
        "author": "Sam K.",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "shed,building,roof,cladding,base",
        "body": """A farm shed needs to do one job well. Decide what it is for before you draw anything.

## Plan the size

| Use | Size per item | Useful size |
| --- | --- | --- |
| Tractor and mower | 4.5 x 2.5 m each | 6 x 9 m for two |
| Small trailers | 3.5 x 2.2 m | 6 x 7 m for two |
| Bales | 2.4 x 1.4 m on edge | 4 x 6 m for six |
| Post and rail, lengths | Needs headroom | 4.5 m to the eaves |
| Workshop bench and machines | 1.5 m per person | 6 x 5 m |

- **Allow 1 m more width than the biggest thing you will put in.** You will put something else in it.
- **Height matters more than floor area.** A shed you cannot get the loader into is a shed you will not use in the wet.

## The site

- **Level, well drained, and out of the way.** See [[field-drainage]].
- **Do not build in a hollow.** Water will find it and you will have a pond.
- **Access for a large trailer, at least 4 m wide and with a turning circle.**
- **Consider the sun.** North side for the workshop, south for the hay store, and a hedge to take the worst of the wind.

## The base

- **Concrete slab** for machinery and for a workshop. 100 mm of concrete on a compacted hardcore base, with a 150 mm edge.
- **Hardcore and gravel** for a hay or implement store. Cheaper, drains well, and a crushed stone floor is easier to resurface.
- **Sleepers on the ground** for a light store.
- **Fall of 1 in 100 away from the doors** so the water goes somewhere else. See [[field-drainage]].

## The frame

- **75 x 50 mm studs at 400 or 600 mm centres.** See [[timber-and-posts]].
- **Double studs at every corner** and at the door openings.
- **A head beam over every wide opening.** A door opening with a 4 m span needs a beam, and the lintel needs a post.
- **Brace the corners.** A shed that is braced diagonally will not rack in a gale.

## The roof

- **A pitch of 15-25 degrees** is enough for a shed. Steeper is more work, less of it.
- **Fibre cement sheeting** on purlins for a low-cost, long-lasting roof. Good for a farm shed.
- **Corrugated steel** needs a purlin at every sheet end and a sealant on the laps. It will last longer than you expect if the laps are right.
- **Pitched and braced** for a shed that people work in.
- **Gutters and a downpipe**, and take the water away from the base. See [[rainwater-harvesting]].
- **Fix the sheeting with the right screws** - single roof sheeting screws for corrugated, and a proper washer under every fixing so it does not leak.

## Cladding

- **Horizontal boarding, vertical boarding, or profiled sheet.**
- **Galvanised or stainless screws.** See [[sheet-metal-fixing]].
- **Stagger the joints on sheet cladding** so the seams do not line up.
- **Put a DPC or a gravel board** between the cladding and the ground.

## The door

- **Double doors on a barn door** for a machinery shed, hung on the shed so they swing wide.
- **A single door of 900 mm** for a pedestrian store.
- **Hang it on the shed frame, not on a door frame that is only fixed to the cladding.** See [[hanging-a-gate-on-a-post]] for the principle.

## Ventilation and light

- **A workshop needs a window that opens**, and cross ventilation. See [[venting-the-workshop]].
- **A hay store needs air movement** to keep the hay from going mouldy. See [[making-hay-in-a-wet-week]].
- **A feed store needs to be dry and dark** to keep the rats out.

## The jobs

1. Site and level.
2. Base.
3. Frame, braced and square.
4. Roof structure and sheeting.
5. Cladding, with the flashing and the DPC.
6. Doors and windows.
7. Gutters, and a path around the building.
8. And then do it again in ten years.

> **Build it 1 m wider and 0.5 m taller than you need.** You will not regret it, and you cannot add it later.
""",
    },
    {
        "slug": "pallets-and-scraps",
        "title": "Pallets, offcuts and making something out of nothing",
        "category": "workshop-timber",
        "summary": "Reusing pallets and scrap is the cheapest way to build anything. Here is what a pallet will and will not do.",
        "author": "Nadia, plot",
        "difficulty": "easy",
        "read_minutes": 5,
        "tags": "pallets,scrap,reuse,workshop,storage",
        "body": """A stack of pallets in the yard is a free building material, and half the time it is also a fire waiting for a dry summer. Here is how to use it well.

## Pallet types

| Type | Look for | Use |
| --- | --- | --- |
| Standard export | 1200 x 800 mm, no nails | General, and the only safe one to cut up |
| Euro | 1200 x 800 mm, stringers | General, and the only safe one to cut up |
| Block | Blocks instead of stringers | Heavy loads, floor pallets, not for building |
| UK standard | 1200 x 1000 mm | General |
| Display or half pallets | Odd sizes | Shelving and small projects |
| Repaired | Patched, nailed | Only for a non-structural job |

- **Only build from pallets that have not been chemically treated or heat-treated.** Treated pallet wood is a disposal problem.
- **Never use a pallet that has held chemicals, meat or anything toxic.**
- **Look for the ISPM 15 mark.** Check the stamp on the pallet itself before you use it.
- **A pallet that has been in the yard with a broken board is still a good pallet** - use it flat, or repair it.

## Cutting a pallet up

- **Every pallet is made to be handled, not to be cut up.** If you cut the stringers, the boards fall off.
- **The boards come off in one piece** if you knock out the nails. Use a pry bar and a hammer and take your time with the last nails.
- **Take the nails out completely.** A nail head in a plank is a cut waiting to happen. See [[sharpening-hand-tools]] for a good way to pull nails.
- **Keep the top and bottom deck boards and the stringers separate.** That is the structure and it is worth keeping intact.
- **The narrow gap between the boards is a handle.** A cut-up pallet makes a good carry board.

## What to build from them

| Project | Notes |
| --- | --- |
| Grow box or table | 4 pallets, on end, as the sides |
| Compost bay | 3 pallets tall, corner-braced |
| Pallet rack | Two pallets, boxes off the top |
| Sandpit for the yard | Pallets filled with sand, on edge |
| Seed tray bench | A pallet on two blocks, 40 cm off the ground |
| Spud storage | Pallet sides, 100 mm of mesh, in the ground |
| Trailer deck | 3-4 pallets, screwed to angle iron |
| Bee hive stand | Two pallets, 300 mm off the ground |
| Firewood rack | Pallets on edge, stacked in a corner |

- **A pallet on blocks is a good base for anything** - it keeps the material off the wet ground and off the vermin. See [[compost-heap]] for a bay on the same idea.

## Fixing pallets together

- **Screws, not nails.** A screw holds in end grain. See [[sheet-metal-fixing]] and [[timber-and-posts]].
- **Coach screws** are the right fastener for pallet to pallet.
- **Pocket the screws** so the heads do not catch anything.
- **Sand the rough edges.** Splinters and a shed full of dog food is not a good combination.

## The fire risk

- **A stack of pallets against a wall is 6-8 tonnes of kindling.** Keep it away from the shed, the fence line and the building.
- **Store them flat and covered**, or on edge in rows.
- **Do not burn pallet wood in an open fire pit.** Treated wood makes toxic smoke. See [[wood-burning-and-stove-dampers]].

## Finding them

- **Ask the local forklift company.** They have a pile they cannot use and they are often happy for you to take it.
- **Check the builder's merchant** - they have broken pallets in the skip.
- **Keep a good pair of gloves and a pair of safety boots** for handling them, because some of them have nails and some have been in a skip.

> **The best material on the farm is the material you already have. A pallet is free, and the only cost is the nails you leave in it.**
""",
    },
    {
        "slug": "painting-and-prep",
        "title": "Painting metal and timber: prep, primers and brushes",
        "category": "workshop-fabrication",
        "summary": "Why paint peels, how to prepare a surface properly, what primer to use, and how many coats a job really needs.",
        "author": "Wes, workshop",
        "difficulty": "easy",
        "read_minutes": 8,
        "tags": "painting,prep,primer,rust,bristle,coat,steel",
        "body": """Paint does not fail because it is bad. It fails because it was put on a dirty, wet or rusty surface with the wrong primer, and then the weather took it off in sheets. Preparation is 80% of the job.

## Why paint peels

- **Rust under the paint.** Steel rusts from the inside out, and the rust pushes the paint off in blisters. See [[metal-corrosion-on-the-farm]].
- **No primer on bare steel.** Without a primer, paint soaks into the metal and lets it rust underneath.
- **Damp timber.** Paint on damp wood traps the moisture, and the paint lifts.
- **No sanding between coats.** A new coat bonds to the loose dust of the old one and peels off with it.
- **Painting in the wet.** Most paints need the surface to be dry and the air to be moving.

## Preparing metal

1. **Strip the old paint** with a wire wheel on a grinder, a scraper, or a chemical stripper.
2. **Get back to clean metal** wherever you can. Bare, bright steel is the best surface to paint.
3. **Take the rust off with 80 grit**, and finish with 120 grit if the surface is smooth. See [[cutting-and-grinding-metal]].
4. **Wash it down** with a degreaser or a solvent, and dry it properly.
5. **Paint within a few hours** of the sanding, or the flash rust starts again. Rust converter products help here.
6. **Use a rust-inhibiting primer** on bare steel - a zinc phosphate or red oxide primer, or a modern two-part epoxy primer.

## Preparing timber

1. **Let the timber dry** properly. A painted surface that traps moisture will blister.
2. **Remove the loose dirt** and any algae. See [[timber-and-posts]] for treating wood.
3. **Sand or scrape** the surface so the paint has something to grip. A weathered grey surface is a good enough key for a primer.
4. **Fill the knots and nail holes** with a wood filler, and sand it back.
5. **Prime bare wood**, especially the end grain, which drinks paint.
6. **Stop the end grain** with a bit of varnish or a coat of primer, and it will not crack first.

## The primer

| Surface | Primer |
| --- | --- |
| Bare steel | Zinc phosphate or red oxide, or epoxy primer |
| Galvanised steel | Special galvanised primer, or a degreaser and a plasticiser primer |
| Rusty steel, not cleaned | Rust converter, then a primer over it |
| New timber | Wood primer, or a universal primer |
| Masonry and render | Masonry primer |
| Already painted, sound | Just clean it and a light sand |

- **Galvanised steel is the one that catches people out.** Paint on new galv peels off in sheets because the surface is oily and it does not etch. Degrease it, and use a primer made for it. See [[sheet-metal-fixing]].
- **One good primer beats three thin coats of finish.**

## Painting

- **Two thin coats are better than one thick one.** A thick coat skins over and stays soft underneath. See [[paint-area]] for how much you need.
- **Brush it on with the grain**, and work the paint into the surface.
- **Do not over-brush.** The brush marks and the drag of a loaded brush are what make a brush finish look like a bad brush finish.
- **Keep a wet edge** and work around the job, not in stripes, so the wet paint joins the dry.
- **Do not paint in the evening.** The temperature falls, the paint skins, and the next morning it peels. See [[drying-herbs-and-food]] for why temperature and time matter.
- **Do not paint in direct sun or in the rain.** Early morning or a dry, overcast afternoon is best.

| Finish | Where | How many |
| --- | --- | --- |
| Primer and 2 coats of gloss | Steel gates and frames | 3 |
| Zinc primer and 1 coat of bitumen | Posts and underground steel | 2 |
| Masonry primer and 2 coats of masonry paint | Block walls and render | 3 |
| Wood primer and 2 coats of exterior wood paint | Doors, windows, timber | 3 |
| Creosote or preservative | Fence posts, sleepers | 1 or 2 |

## Brushes and rollers

- **Use the right brush for the paint.** A natural bristle brush for solvent-based paint, a synthetic one for water-based paint.
- **A cheap brush ruins good paint.** The bristles shed, and the paint goes lumpy.
- **Wash the brush out in the paint** at the end of every session, not in solvent weeks later. Keep the cans off the bench and away from any heat. See [[chemical-storage-on-the-farm]].
- **Do not stand the brush on its bristles.** It bends them permanently.
- **A roller is for walls and flat panels**, not for frames and rails.

> **If you have time for one thing, do the prep.** A properly prepared surface with a cheap paint will outlive a expensive paint on a prepared-nothing one every single time.
""",
    },
    {
        "slug": "insulating-a-workshop",
        "title": "Insulating a workshop: floor, walls and keeping the heat in",
        "category": "workshop-timber",
        "summary": "Where the heat actually goes, what to insulate, what to leave alone, and how to keep a shed dry while you make it warmer.",
        "author": "Wes, workshop",
        "difficulty": "medium",
        "read_minutes": 9,
        "tags": "insulation,warm,damp,workshop,ventilation,energy,shed",
        "body": """A workshop is the warmest room on most farms, and the worst to work in. You can make it 10 degrees better in an afternoon with foil-backed insulation, and you can make it worse by doing the same job wrong.

## Where the heat goes

| Part | Typical heat loss | What to do |
| --- | --- | --- |
| Roof and ceiling | 25-35% | Insulate first, it is the cheapest square metre |
| Walls | 25-35% | Insulate the solid walls |
| Floor | 10-15% | Insulate over a void, not over a slab |
| Doors and windows | 15-25% | Replace the worst, add a draught strip |
| Gaps and vents | 5-10% | Stop them first, they are free |

- **Start with the draughts.** A gap the width of a coin around a door loses more heat than a whole wall of insulation. See [[building-a-shed]] if you have a shed to convert.
- **Measure the heat loss before you buy anything.** See [[heat-loss-through-a-wall]] and [[insulation-thickness]].

## The floor

- **A concrete slab is a heat sink.** It draws heat out of the room all day and it is damp. See [[frost-and-water-logging]].
- **Insulate over the void** with rigid board or a foil-backed blanket, and lay the floor finish over it. See [[floor-insulation-over-void]].
- **Do not lay insulation on a damp slab** without a damp-proof membrane underneath. You will trap the moisture and rot the board.
- **If the floor is a slab with no void**, a layer of 30-50 mm of expanding foam and a board on top still lifts the floor off the cold and makes the room feel much better, even if it does not save much heat.

## The walls

- **100 mm of mineral wool or rigid board** in the cavity is enough for most farm workshops. See [[insulation-thickness]].
- **A vapour barrier goes on the warm side** - the inside of the wall. Polythylene or foil-backed insulation. Getting this the wrong way round traps the damp in the wall.
- **Insulate between the studs**, not on top of them, or you have a cold bridge at every stud. See [[thermal-bridge]].
- **Insulate the top of the wall** up to the eaves.** An uninsulated strip at the top is a heat highway.
- **Leave the blockwork alone** if it is solid. A 200 mm wall is already a good insulator.

## The roof

- **Insulate between and below the rafters.** Between gives you a vented, cold roof, which is better.
- **Do not put insulation under a metal roof without a gap.** The metal gets hot in the sun, the air gap lets it cool, and the vapour can escape. See [[roof-pitch]].
- **Insulate the ceiling if the loft is not used**, or the floor if it is.
- **Seal the roof space** to stop the wind washing through the insulation. A badly fitted insulation with wind passing through it works about half as well as the label says.

## Ventilation, and the damp trap

- **A workshop needs air.** Welding fumes, sawdust, paint vapour and a wood fire all need somewhere to go. See [[venting-the-workshop]].
- **A fan with a flap, or a trickle vent, high up.** Warm, wet air rises; that is where the extract goes.
- **Do not insulate a building that leaks.** Seal the roof, the walls and the ground first. Insulation on a leaking shell makes the damp worse. See [[humidity-and-condensation]].
- **Ventilation and insulation work together.** A warm, dry workshop with a fan is more comfortable than a sealed, damp one.

## Doing it in order

1. **Measure the room** and work out the wall area and the floor area. See [[wall-area-for-insulation]].
2. **Stop the draughts** - door sweeps, letterbox covers, pipe insulation, a roller blind on the window.
3. **Sort out the roof** and the guttering, so the walls are dry. See [[draining-water-pipes]].
4. **Insulate the ceiling or roof** first. It is the biggest win and the easiest job.
5. **Insulate the walls**, and vapour barrier the inside.
6. **Insulate the floor** last, and only over a void.
7. **Finish the lining** - sheet, plywood or plasterboard - and keep it vapour-tight.

> **Insulate the top, seal the gaps, and keep it dry.** A warm workshop that sweats will be colder and damper than the shed you started with.
""",
    },
    {
        "slug": "fencing-wire-and-straining",
        "title": "Fencing wire, strainers and getting it tight",
        "category": "workshop-fabrication",
        "summary": "Which wire to use, how to space the posts, how to work a ratchet strainer, and how to stop the whole fence pulling crooked.",
        "author": "Wes, workshop",
        "difficulty": "medium",
        "read_minutes": 9,
        "tags": "fencing,wire,strainer,posts,rabbit,sheep,barb-wire",
        "body": """A fence fails at the posts, not in the middle of the wire. Get the posts right, set them plumb, and strain the wire properly, and a farm fence will last twenty years.

## Choosing the wire

| Wire | Use | Notes |
| --- | --- | --- |
| Plain barbed wire | Cattle, sheep, general stock | The barbs catch animals, not birds |
| Galvanised plain wire | Poultry, garden, temporary | Not for cattle |
| Stock netting | Sheep, poultry, general | Comes in 75 mm and 100 mm mesh |
| Welded mesh | Hard wearing, good for sheep and poultry | Rigid, needs square posts |
| Electric netting | Temporary and poultry | See [[fencing-that-works]] |
| High tensile wire | Long spans, sheep and deer | Needs a good strainer |
| Chicken wire | Poultry only | Too flimsy for anything that pushes |

- **Galvanised is worth the extra money** on anything that will stay up. See [[metal-corrosion-on-the-farm]].
- **Never use plain wire on a boundary that animals push against.** It stretches and cuts.
- **Do not use barbed wire where there is stock that gets tangled** - calves, goats, and anything with a collar. Use stock netting. See [[fencing-that-works]].

## The posts

- **Post spacing** depends on the wire. See [[fence-post-spacing]] for the arithmetic.
- **Set the posts in a straight line** with a string line and a line level. A fence that zigzags looks bad and twists the wire.
- **Set them plumb** and brace them before the wire goes on.
- **Corner and end posts** need to be braced. A braced corner post takes the pull of the whole fence.
- **Drive the posts** on a frost-free day, or the ground heaves and the post comes out of alignment. See [[frost-and-water-logging]].

## Straining wire

- **Fix the wire to one end first**, at the height you want, and make it tight enough that it does not move when you push it.
- **Work along the fence, keeping the wire running high.** If the wire dips, you cannot pull it up later.
- **Use a ratchet strainer** for high tensile and for any wire you want really tight. A block and tackle works too and is cheaper.
- **Attach the strainer to the post, not to the wire.** A strainer on the wire just pulls the wire through the strainer.
- **Turn the ratchet slowly** and check the tension as you go. Over-tightening will pull the posts out of line.
- **Do it on a warm, dry day.** Wire contracts in the cold and expands in the heat. See [[thermal-expansion]]. Tension it in the middle of the day in summer, and it will be slack in the winter.

| Post spacing | Wire | Tension |
| --- | --- | --- |
| 3 m | Stock netting | Firm, no movement when pushed |
| 4-5 m | Plain wire | Firm |
| 10-25 m | High tensile | Very firm, with a ratchet |
| 25 m and over | High tensile with stays | Firm, with a brace every 25 m |

## Braces and stays

- **A brace takes the strain off the end post.** It is the difference between a fence that lasts and one that leans over in two winters.
- **A stay wire** runs back from the middle of a long span to a post behind it, at an angle. It stops the wire pulling the post towards you.
- **Hanging gates** are the other end of the story. See [[gates-and-brackets]] and [[hanging-a-gate-on-a-post]].

## Wire and the ground

- **A wire fence is not a boundary for burrowing animals.** If you have rabbits, foxes or badgers, you need a buried skirt or an apron. See [[fencing-that-works]].
- **Leave a gap under the wire** for field mice and wildlife, but not for sheep.
- **Keep the grass back from the wire** so you can see it and find damage.
- **Check the fence after every storm**, and after the first hard frost.

> **The wire is the cheap part. The posts, the bracing and the line are the fence.** Get those right and you will not think about it for twenty years.
""",
    },
    {
        "slug": "frost-and-water-logging",
        "title": "Frost heave and water-logging: keeping bases and cellars dry",
        "category": "workshop-fabrication",
        "summary": "Why concrete lifts and cracks, how deep a foundation has to go, how to drain a site, and what to do about a cellar that fills with water.",
        "author": "Wes, workshop",
        "difficulty": "medium",
        "read_minutes": 9,
        "tags": "foundation,frost,drainage,concrete,cellar,water-logging,heave",
        "body": """A slab on soil that freezes will lift. A foundation that is too shallow will heave. A hole dug in a wet field will fill with water and stay that way. Most of the expensive mistakes in a building job happen below the ground, where you cannot see them afterwards.

## Frost heave

- **Water in the soil freezes and expands** by about 9% - about 1.2 metres of frost in the ground lifts a post by 13 mm. Repeated winter after winter, that ruins a post and cracks a slab.
- **The depth of frost depends on the winter, not on the map.** Ask the local building control, or look at where the frost has ever reached.
- **Foundations must go below the frost line.** See [[foundation-depth-frost]] for the figures.
- **Drainage matters more than depth.** Soil that drains does not freeze hard, because it does not fill with water.
- **A post that has lifted** shows a gap under it, or a post that rocks. Lift it, dig out the frozen pocket, and set it in concrete - see [[post-hole-concrete]] and [[mixing-concrete]].

| Ground | Frost depth to work to |
| --- | --- |
| Southern, mild winters | 300-450 mm |
| Most of the UK and the north | 600-750 mm |
| Northern, hard winters, high ground | 900-1200 mm |
| Anything that holds water | The deepest of the above, and drain it |

## Water-logging

- **A site that holds water will push a building up.** The pressure of the water in the soil lifts the slab and the walls.
- **A slab with no hardcore under it** is a sponge. See [[hard-core-and-topsoil]].
- **Put hardcore down, compact it in layers, and lay a damp-proof membrane over it.** See [[levelling-a-yard]].
- **Fall the ground away from the building.** A 1 in 80 fall over 3 metres takes you 37 mm away from the wall. See [[drainage-fall-and-pipe-size]].
- **A french drain** round the uphill side of a building, with gravel in a trench and a pipe in it, is cheap and it works. See [[field-drainage]].

## Cellars and below-ground rooms

- **The old answer** is a sump with a pump. See [[effluent-and-sump]].
- **The new answer** is a void with a pump and a battery-backed alarm, so you know the pump has failed while you are asleep.
- **Waterproof the outside, not the inside.** A tanking membrane on the outside of the wall stops the water coming in. From the inside you are fighting it.
- **Never dig a cellar into a slope without checking where the water comes from.** A spring under the floor will find you.
- **If the ground is very wet, do not have a cellar.** Put the store and the freezer above ground level and save yourself the fight.

## The symptoms of a problem

| What you see | What it means |
| --- | --- |
| A crack across a slab, straight and even | A slab that has been heaved or has shrunk |
| Cracks at the corners of a building | Foundation movement |
| A door that will not close in winter | The frame has twisted, or the post has lifted |
| Damp patches that appear in the wet season and never dry | Water is coming through the ground |
| White salt deposits on the wall | Water is moving through the wall and evaporating |
| A floor that is cold and damp underfoot | No insulation, and no membrane |

- **A crack in a slab is not always a crisis.** A straight crack that does not move is mostly a shrinkage crack. A crack that is getting wider, or that steps, is movement and it needs attention.
- **A level is the cheapest tool on the farm.** Check a floor with a spirit level before you build on it, not after.

> **Everything below ground is invisible and expensive.** Get the depth, the drainage and the hardcore right the first time, and you will never think about it again.
""",
    },
]
