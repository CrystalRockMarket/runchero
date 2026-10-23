"""Community notes: the articles written on the farm.

Each entry is a practical note - symptom, cause, fix, and the safety bit that
somebody forgot the first time. Markdown bodies; ``[[wiki-slug]]`` links are
resolved against other notes at render time.
"""

from __future__ import annotations

ARTICLES: list[dict] = [
    # ------------------------------------------------------------ vehicles
    {
        "slug": "tractor-wont-start",
        "title": "Tractor will not start: a ten-minute diagnosis",
        "category": "vehicle-diagnosis",
        "summary": "Before you order a starter motor, work through fuel, air, compression and spark in that order. Most no-starts are one of the first two.",
        "author": "Dave, top field",
        "difficulty": "easy",
        "read_minutes": 8,
        "featured": 1,
        "tags": "starter,fuel,ignition,diesel,diagnosis",
        "body": """Machine turns the key and either does nothing at all, cranks slowly, or cranks fast but never fires. Those are three different faults. Sort out which one you have before you start buying parts.

## Does it crank at all?

**No click, no noise.** Check the battery terminals first. Push the positive post hard back into place and try again. Then check the earth strap between the engine and the battery - a corroded strap will make a good battery look dead. If the lights dim heavily when you crank, the battery is flat and needs charging, not replacing.

**Cranks but slowly, like it is dragging.** This is a battery, a starter, or a seized engine. Put a meter on the battery while cranking. Below 9.6 volts under load and the battery is finished. Above that and the starter is the problem.

**Cranks fast but does not fire.** Air, fuel or compression. Go to the next section.

## Fuel

Diesel: is there fuel at the injector? Lift the shut-off lever and check the supply. On an old lever-pump engine, prime it until the glass bowl is full. If the bowl refills in seconds, the supply valve is passing and the injection pump is starving.

Petrol: check the float chamber. Unscrew the float bowl and see what is in there. Sludge and water collect in the bottom of the bowl and will not pass the needle valve. Clean it, and while you are in there check that the needle valve seats - pour a little petrol in and see if it holds.

## Air

A tractor that has been standing in the wet will have a blocked air filter. Pull the element, knock out the dust, and wash it if it is a paper filter. A blocked filter shows up as smoke from the exhaust under load.

## Compression

For a diesel, the glow plug is the cheap test. If the plug is dark and corroded, the plug has failed and the engine will not fire on a cold morning. Clean it, or fit a new one.

If it is still dead, take a compression reading. A healthy 3-cylinder diesel should be well over 20 bar. If one cylinder is way down, suspect a valve or a head gasket. See [[overheating-tractor]] for what a blown head gasket does to the coolant system.

## Spark (petrol engines)

Remove a plug and lay it on the engine block so it earths. Crank and watch for a fat blue spark. A weak orange spark means the coil or the plug. No spark at all with a wet plug means the ignition switch, the points or the condenser.

## The last thing to try

On many old tractors the ignition switch only energises the fuel solenoid through a wire that breaks near the steering column. Wiggle the key and watch the solenoid - if it clicks intermittently, you have found it.

> **Safety note.** Do not spray starter fluid into a hot exhaust manifold. On a tractor that has been sat in long grass you can set the whole field alight.
""",
    },
    {
        "slug": "overheating-tractor",
        "title": "Overheating: thermostat, radiator cap or scaling?",
        "category": "vehicle-engine",
        "summary": "Three causes cover nine out of ten overheating complaints. Test in that order and you will usually not need to pull the engine apart.",
        "author": "Marta, arable",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "cooling,thermostat,radiator,diesel",
        "body": """If the temperature gauge climbs and stays there, the coolant is not going round the block. Work through these three before blaming anything expensive.

## 1. The radiator cap

The cheapest test on the farm and the one most often skipped. A cap that does not hold pressure lets the coolant boil away before the gauge reads anything. Warm the engine until hot, then take the cap off. If it is at or near boiling point, the cap is not holding - or there is no coolant left in the system at all.

Replace suspect caps with the correct pressure rating. The rating is stamped on the cap. A 1 bar cap on a 1.5 bar system will cause boiling; a 2 bar cap on a low-pressure system will crack the radiator.

## 2. The thermostat

Take the thermostat out and put it in a pan of water with a thermometer. Heat it slowly. It should start to open somewhere around 82-88 degrees C. If it stays shut, it is stuck. If it opens immediately, it is stuck open and you will get a slow warm-up and poor cabin heat instead of overheating.

While the thermostat is out, check the water pump as well. Turn it by hand - it should turn smoothly. If it is gritty, the bearing has gone.

## 3. Scaling and blockage

Pull the radiator out and pour the coolant out of the bottom. Thick brown sludge in the top tank means sludge. If the fins are packed with straw and field debris, that is what is blocking the flow.

A garden hose backwards through the core will clear most of it. A chemical radiator flush handles the rest, but do not use it on an old brass radiator - it dissolves the alloy.

## Other things worth a look

- **The fan belt.** A glazed belt slips and the fan turns too slowly. Squeeze the belt; it should deflect about 10 mm.
- **Fan shroud.** Missing shrouds on a tractor running in tall grass will cook the radiator from the inside.
- **Coolant level.** Some engines have the header tank on the opposite side from the filler, which catches people out.
- **Head gasket.** If you have cooling loss, white exhaust smoke and a bubble in the radiator when the engine is running, stop and call someone. See [[tractor-wont-start]] for the compression side of the same failure.

> **Never open a cooling system while it is hot.** Scalding steam does more damage than the fault you were chasing.
""",
    },
    {
        "slug": "oil-pressure-warning",
        "title": "Oil pressure warning light: stop, or keep going?",
        "category": "vehicle-engine",
        "summary": "Stop the engine. A red oil pressure lamp with a ticking noise is a bearing running out of oil, and the repair bill is set by how long you keep running.",
        "author": "Old Bill",
        "difficulty": "easy",
        "read_minutes": 5,
        "tags": "oil,pressure,lubrication,bearings",
        "body": """The red oil pressure light comes on and the warning bell starts ticking. That bell is not a fault indicator. It is a knock.

## What is actually happening

Your oil pump has lost pressure. Below a certain pressure the bearings are no longer held in a film of oil and they start to touch. That touching is the ticking. It gets louder as the damage spreads, and then the engine seizes.

## The first thirty seconds

1. **Pull over and stop the engine.** Do not coast it down. Shut it off where you are.
2. **Check the oil level on the dipstick.** On a lot of older tractors the dipstick is under the bonnet, and a low level is the whole story. Top it up and restart it.
3. **Look at the oil.** If it smells of petrol, or it has a milky texture, the oil is not what it should be.

## If the level is fine

Then the pump, the filter or the relief valve is at fault. Before you start stripping:

- Check the oil filter is the right one and was fitted with a clean gasket. A filter fitted the wrong way round blocks the supply completely.
- Check the sump plug. An over-torqued plug or a missing washer will leak the oil out faster than the pump can replace it. Look underneath the tractor - a puddle tells the story.
- Check the suction pipe to the pump is not full of air. A leak on the suction side gives exactly the same symptoms as a worn pump.

## Do not

Do not run the engine "just to get it back to the yard". A tractor that seizes on a road is a recovery job and a recovery operator charges more than the repair.

Do not use a thicker oil to "fix" low pressure. If the pump is worn, thicker oil makes it worse by making the pump harder to turn.

> **The one exception.** A momentary flicker of the light during a hard turn is often just the oil sloshing away from the pickup. A light that stays on, even briefly, is not.
""",
    },
    {
        "slug": "tractor-hydraulics-slow",
        "title": "Hydraulics lifting slowly: finding the blockage",
        "category": "vehicle-engine",
        "summary": "Lift arms that crawl upwards are usually a restricted filter or a sticking spool. Split the system into pump, filter, valve and ram before you condemn the pump.",
        "author": "Tomasz",
        "difficulty": "hard",
        "read_minutes": 7,
        "tags": "hydraulics,three-point,pump,filter",
        "body": """The three-point linkage goes up at a walking pace, or only with the engine at full revs. Sometimes the arms will not hold a load and drift down. Different symptoms point at different parts.

## Symptom guide

| Symptom | Most likely cause |
| --- | --- |
| Slow lift, engine must be revved | Pump worn or suction restriction |
| Arms rise then drop when you stop | Spool valve sticking or worn |
| Arms will not hold load | Seal failure in the spool or the lift cylinder |
| Jerky movement, shudder | Air in the system |
| Noise from the pump area | Cavitation - air or restriction on the suction side |

## Start with the easy checks

**Oil level.** Check it with the arms on the ground. Many hydraulics use a separate gearbox oil and a separate hydraulic tank, and they get confused constantly.

**Filter.** If the tractor has a suction strainer in the hydraulic tank, pull it and look at it. A blocked strainer will starve the pump and make the lift slow while the engine labours. Clean it and refit it with a new seal.

**Air.** Raise the arms slowly to full height, then lower them fully. Repeat. If the movement is smooth and quiet, the air is out. If it is jerky, the pump is sucking air - check the pipe from tank to pump for a cracked union.

## The spool valve

If the lift is slow but the oil is clean and plentiful, the spool valve is the next suspect. It sits under the gearbox cover on most older tractors.

With the engine off, work the lift lever through its full travel and watch the spool. It should move smoothly from end to end. If it stays put when you move the lever, it is seized. Pull it carefully and check the edges for a score mark - a single score is enough to make a valve leak.

> **Safety.** Support the arms on a block before you get underneath with the lift raised. Hydraulic oil under pressure will go through skin. Never use a piece of card to find a leak - that is how people get a hole in their hand. Use paper, then a rag, then your hand last.
""",
    },
    {
        "slug": "dtl-500-tension-adjustment",
        "title": "Adjusting drawbar tension on a three-point hitch",
        "category": "vehicle-implements",
        "summary": "Bottom link sway is not the same problem as a bouncing implement. Work through stabilising bars, lift rods and top link length in that order.",
        "author": "Dave, top field",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "three-point,drawbar,stability,implements",
        "body": """The linkage bounces, the implement side to sides, or the tractor lifts the front wheels off the ground when you drop the plough in. All three are "drawbar tension", but they are not the same fault.

## The bounce

The lift rods have more play in them than the bottom links. The top link is doing the job it is meant to do - it stops the implement rising when the ground goes over a ridge.

Check the length of the top link. If the implement is bolted straight to the bottom links with no top link fitted, the linkage has no pitch control at all. Fit the top link and set it so the implement is level or slightly nose down.

Adjusting the top link is a length job. Lengthen it and the implement tilts nose down; shorten it and the nose lifts.

## The side to side sway

That is the stabilising bars. They run from the lower link to the frame on either side.

1. With the implement on the ground and the linkage at its lowest, tighten both stabilising bar lock nuts fully.
2. Then back them off about a quarter turn each side.
3. Raise the implement until it is just off the ground. It should stand level with no side movement.

If the sway comes back quickly, the bars are bent. Straighten them or replace them - a bent bar puts a constant side load on the bottom link pins and wears them out.

## The front wheels lifting

This one is about weight transfer, not linkage geometry.

- Lower the implement depth. A plough set too deep will lift the front no matter how the linkage is set.
- Ballast the front. A bracket with a front weight block is cheaper than a new gearbox.
- Check the tyres are inflated to the right pressure. Under-inflated tyres push the tractor backwards under load.

## When the arms will not hold

If the implement sinks, the lift cylinder or the spool is the problem, not the geometry. See [[tractor-hydraulics-slow]].

> **Rule of thumb.** Every time you change the top link length, re-check the stabilising bars. They interact.
""",
    },
    {
        "slug": "battery-dies-overnight",
        "title": "Battery dies overnight: hunting a parasitic drain",
        "category": "vehicle-diagnosis",
        "summary": "A battery that is fine in the morning and flat by evening is being drained by something. Pull fuses one at a time instead of guessing.",
        "author": "Sam K.",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "battery,electrics,parasitic-drain,fuses",
        "body": """The tractor starts first thing, then the lights are dim by the end of the afternoon and it will not turn over the next morning. Something is drawing current with the ignition off.

## First, rule out the simple things

- **The battery is old.** A battery that will not hold a charge over a weekend in winter is finished regardless of what else you find. Buy a new one, clean the terminals, and check the charge.
- **The alternator is not charging.** With the engine running, a meter across the battery should read 13.8-14.4 volts. If it reads the same as the battery voltage, the alternator is not doing its job and everything else on this page is a distraction.

## Then hunt the drain

Do this in the evening with the tractor switched off and settled for an hour.

1. Put a meter in series between the battery negative terminal and the earth strap. Set it to milliamps.
2. Wait for the reading to settle. Most machines draw something - lights off, alarm off, clock on. That is usually under 50 mA.
3. If the draw is high, pull fuses one at a time and watch the meter. The fuse whose removal makes the number collapse is your culprit.

Work in the order that makes sense: horn and lights first, then the instrument cluster, then the trailer socket, then the fuel solenoid and the starter.

## The usual suspects

**The trailer socket.** A trailer with a bad earth or a lamp wired directly to the battery will drain flat over a week. Fit a proper isolating switch.

**The fuel solenoid.** Some tractors energise the solenoid directly from the battery through the ignition switch. If the switch is leaky, the solenoid is held open all night and the fuel pump hums away.

**The clock and the radio.** Small, but on a machine with a flat battery these are the last thing standing.

## A useful trick

If you cannot find it by fuse, disconnect the battery and leave it overnight with a meter across it. If the battery stays flat with nothing connected to it, the battery is scrap. If it holds its charge, the drain is on the machine and you go back to the fuse box.

> **Do not fit a heavy-duty isolator switch until you have found the drain.** You will just hide the fault and drain the battery slower.
""",
    },
    {
        "slug": "mower-vibration-after-blade-change",
        "title": "Mower vibration after a blade change",
        "category": "vehicle-implements",
        "summary": "If it only vibrates at full throttle, it is the engine. If it vibrates at a set engine speed, it is the blades or the deck.",
        "author": "Old Bill",
        "difficulty": "moderate",
        "read_minutes": 5,
        "tags": "mower,vibration,blades,deck",
        "body": """The moment you fitted new blades the mower started shaking. Nearly always one of three things.

## Check the balance first

Take the blade off and hold it on a finger at the centre boss. A balanced blade sits level. If it tips, the two cutting edges are at different heights.

Blades come from the packet in matched sets. Fitting a fresh blade against a worn one means the deck is out of balance, and it will show as a slow shake that comes and goes with the blade position.

## The bolt hole and the boss

Look at the centre boss of the blade. It should be flat and square. If the blade has been dropped, or levered on, the boss is dished and the blade will never sit true.

The blade bolt should be torqued properly and the locking nut fitted. A blade that works loose lets the blade rotate out of balance within minutes of running.

## The deck

If the blades are good, look at the deck.

- **Deck height.** A bent deck plate will make one blade cut higher than the other. Straighten it, or drop the whole deck until the blade runs clear of the plate.
- **Grass build-up.** A thick mat of dried grass under the deck is enough to cause a heavy shake. Clean it out and check that the new blade clearance is right for a clean deck.
- **Spindle bearings.** A spindle bearing with play shows up as a heavy shake that changes when you hold the machine down. Replace the bearing and the seal as a pair.

## Engine or not

Use the throttle as the test. A vibration that only appears at full throttle and disappears below it is an engine or exhaust issue. A vibration that peaks at one particular engine speed and then goes away above it is the blades.

Check the exhaust pipe and the muffler for a loose bracket. A rattling exhaust on a single cylinder engine can sound and feel exactly like a bad blade.

> **Never run a mower with a blade that is loose.** A thrown blade will not stop when it hits the ground.
""",
    },
    {
        "slug": "chainsaw-chain-care",
        "title": "Chainsaw chain tension, sharpening and safe refuelling",
        "category": "vehicle-implements",
        "summary": "A chain that will not cut is usually dull rather than tight. Learn to read the chain while it is in the guide bar.",
        "author": "Old Bill",
        "difficulty": "easy",
        "read_minutes": 5,
        "tags": "chainsaw,chain,sharpening,safety",
        "body": """Cutting poorly is dullness, not tension. A tight chain on a dull edge just makes the engine work harder and throws more sawdust.

## Reading the chain

Hold the saw up and look at the chain in the guide bar. The cutter should stick out past the guide bar by roughly the thickness of the chain itself.

- **Cutter sticking out well past the bar:** the chain is too loose.
- **Cutter barely showing:** the chain is too tight.
- **Cutter flush, and it cuts poorly:** the chain is dull.

Check with the saw off and the brake released. Slacken the tension screw by about a quarter turn, then tighten it with the engine off until the chain sits against the guide bar but still moves by hand.

## Sharpening

A chain is sharpened with a round file. Match the file to the chain - 4.0 mm for most light saws, 5.5 mm for heavy timber. The file should travel with the top of the cutter and just touch the depth gauge on the side.

The depth gauge is the piece in front of the cutter. It needs to be filed down as the cutter gets shorter, or the chain will not cut. A good test: the depth gauge should be about half the height of the cutter.

## Oil

Check the chain oil reservoir. A chain running dry gets hot, gets dull fast, and wears the guide bar out in no time.

Use bar oil. Never engine oil - it will carbonise and gum the chain.

## Safe refuelling

- Refuel on the ground, with the engine off and cold.
- Do not smoke.
- Start the saw away from the fuel cap so fumes are not drawn into the airbox.
- Loosen the cap slowly so pressurised fuel does not spray out.

> **Chainsaw safety.** Wear a helmet with a face screen, ear protection, and chaps. Never cut with the saw in front of your legs, and never cut overhead without thinking about where the chain goes if the bar binds.
""",
    },
    {
        "slug": "tractor-smoke-colours",
        "title": "What that smoke colour means",
        "category": "vehicle-diagnosis",
        "summary": "White, blue and black smoke each point at a different part of the engine. A bit of smoke is normal; the colour tells you where to look.",
        "author": "Marta, arable",
        "difficulty": "easy",
        "read_minutes": 4,
        "tags": "smoke,exhaust,diagnosis,diesel",
        "body": """Engines smoke. What matters is the colour and when it happens.

## White smoke

**On a cold start, for a minute:** completely normal. It is condensation and unburned oil vapour clearing out of the crankcase. It stops when the engine warms up.

**All the time, thick and sweet-smelling:** burning oil. On a diesel, either the rings are worn or the injector is dribbling. On a petrol engine, worn rings or valve guides.

**A sudden burst of white:** coolant in the combustion chamber - a cracked head or a blown head gasket. Do not keep running it. See [[overheating-tractor]].

## Blue smoke

Thick blue smoke on a diesel that gets worse under load is usually an injector pumping too much fuel, or a turbo that is not supplying enough air. Check the turbo wastegate and the oil feed to the turbo.

On a petrol engine, blue smoke under acceleration is valve stem seals. It is worth doing, but it is not urgent.

## Black smoke

An engine under heavy load produces a lot of smoke. If it clears when you back off, it is usually a rich mixture - too much fuel, not enough air.

Common causes on a tractor:

- A blocked air filter. Check it first, every time.
- A sticking injection pump lever set for a harder pull than the machine can manage.
- Turbo wastegate sticking open.
- A blocked exhaust or a leaking turbo inlet pipe.

## The straw test

Park the machine next to a straw bale and run it at working load. Black smoke will leave a black smudge on the straw. Blue smoke leaves a blue oil film. That is a very cheap diagnostic and it works.

> **If the machine is emitting black smoke under load, do not keep working it.** The soot ends up in the oil and in the turbo, and you will be paying for it later.
""",
    },
    {
        "slug": "tyre-pressure-fuel-use",
        "title": "Tyre pressures and fuel use",
        "category": "vehicle-diagnosis",
        "summary": "Under-inflated tyres waste fuel, cause slip and get punctured more often. Over-inflated tyres bounce the crop and damage the machine.",
        "author": "Ruth",
        "difficulty": "easy",
        "read_minutes": 4,
        "tags": "tyres,pressure,fuel,soil",
        "body": """A tractor set up for the road is set up wrong for the field. The pressures that suit a 50 km/h run to the yard will destroy the seedbed and cost you fuel.

## Why it matters

- **Rolling resistance.** An under-inflated tyre deforms more with every revolution. The extra drag shows up directly at the fuel pump.
- **Slip.** Too much pressure and the drive wheels spin instead of pulling. You burn fuel and you still do not move.
- **Ground damage.** Too much pressure and the pressure points punch through a soft field, leaving ruts you cannot fill in.
- **Punctures.** A low tyre presses the sidewall into every stone and nail on the ground.

## Setting pressures

Start from the tyre sidewall. It is stamped with the load and pressure ratings - for example "18.4-34 12 bar". That is a maximum for the rated load, not a target.

The rule of thumb for a normal working load on a field is to use about two thirds of that figure and then adjust for conditions.

| Condition | Adjustment |
| --- | --- |
| Hard ground, transport | Use close to the sidewall figure |
| Normal field work | About 70% of the sidewall figure |
| Light soil, low load | 55-60% |
| Very soft or wet ground | Drop further, or use low-pressure option tyres |

Front tyres carry much less than the rears and are often over-inflated by people who never think about them. A front tyre at 3 bar when it should be at 1.5 bar makes the steering heavy and wears the shoulder.

## Ballasting as an alternative

More modern advice is to use fewer, larger tyres at lower pressure rather than ballast weights. A lighter ballasted tractor puts less pressure on the ground and burns less fuel because the engine is not lifting dead weight.

Whichever route you take, **check pressures cold**, once a day at the start of the season, and any time you change the load.

> **Use a proper gauge.** A pencil-type gauge on a warm tyre is roughly 20% out and always in the same direction.
""",
    },
    {
        "slug": "brake-pedal-sinks",
        "title": "Brake pedal sinks to the floor",
        "category": "vehicle-diagnosis",
        "summary": "A pedal that goes down and stays down is a hydraulic fault. A pedal that goes down and comes back up is usually a rod adjustment.",
        "author": "Sam K.",
        "difficulty": "moderate",
        "read_minutes": 5,
        "tags": "brakes,hydraulics,safety,roadworthiness",
        "body": """Two different faults present the same way and need different fixes.

## Sinks and stays down

The fluid is going somewhere. Work through it:

1. **Check the reservoir.** Low fluid or a loose cap that has let air in will do it. Top it up with the right grade of fluid and bleed the system.
2. **Look for a leak.** Rubbing a finger along the rigid pipe and looking for wet patches is more reliable than guessing. Check the wheel cylinders and the pipes where they pass over moving suspension.
3. **Master cylinder.** If the fluid is correct and there is no external leak, the master cylinder is letting fluid past its internal seals. On older machines the seal kit is a cheap part and a straightforward job with the master off the firewall.

## Sinks then comes back up

That is a mechanical problem with the linkage, not the hydraulics.

- **Pedal rod adjustment.** Most tractors have an adjuster on the push rod. Turn it to take up the free play.
- **Worn pedal bushings.** The pedal pivots and the bushings wear oval. The pedal travels further before it starts to move the rod.
- **Rods bent in a previous repair.** Check the rod is straight against a straight edge.

## Bleeding the system

You need a bucket, a clear tube and a helper. The helper presses the brake pedal while you open the bleeder. Watch the fluid coming out - when it runs clear with no bubbles, close the nipple and move to the next wheel. Work back to the master cylinder, and then top the reservoir up and check it again after a day.

## Do not

Do not drive a tractor on the road with a soft brake pedal and hope it improves. On a machine carrying a trailer that has a legal and a moral obligation to stop.

> **Test it loaded.** A brake that feels firm with an empty trailer can still be marginal with a full one on a downhill.
""",
    },
    {
        "slug": "quad-wont-shift",
        "title": "Quad will not shift out of high range",
        "category": "vehicle-diagnosis",
        "summary": "Stuck in one gear is usually the range switch or a cable off its lever. Wet weather also puts a surprising amount of rust into the chain.",
        "author": "Ruth",
        "difficulty": "moderate",
        "read_minutes": 5,
        "tags": "atv,quad,transmission,gears",
        "body": """A quad that only sits in one gear, or that will not go into low, is nearly always a switch or a cable. Wear in the gearbox is much rarer and much more expensive.

## Test it first

Put the quad on stands with the wheels clear, or on a flat bit of ground where you can crawl. Work the gear lever slowly through the positions and listen.

- **Lever moves but nothing happens:** the linkage has come off, or the detent ball is broken.
- **Lever will not move:** the shift mechanism is seized or a cable is binding.
- **Lever moves and the quad changes gear but will not select low:** the range switch.

## The range switch

Many quads have a separate range selector for low and high. These are usually a switch on the handlebar. Water gets into the switch, corrodes the contacts, and the quad stays in one range.

Open the switch, clean the contacts with contact cleaner, and check that the lever on the switch actually moves the plunger all the way. A worn switch lever that no longer pushes the plunger far enough is a common fault and a cheap fix.

## The cable

If the gear lever feels vague or springy, a cable has stretched or come off its stop. Re-tension it, and check the cable is not rubbing on anything as the steering moves.

## Water and mud

After a wet season, the chain case and the gear selector housing fill with mud. Clean it out, flush with water, and grease the selector shaft.

## Brake change

If the quad has been through wet ground and will not shift, remember the rear brakes are often drum on a small quad and they will not bite until they have bedded in again. Replace the shoes and expect a period of poor braking.

> **A quad that will not shift is not a safe machine to ride.** Sort it before it is used on a slope.
""",
    },
    {
        "slug": "stuck-in-the-mud",
        "title": "Getting a tractor out of the mud",
        "category": "vehicle-diagnosis",
        "summary": "Digging makes it worse. The way out is usually less weight on the wheels, more grip, and a plan before you try.",
        "author": "Old Bill",
        "difficulty": "easy",
        "read_minutes": 4,
        "tags": "mud,recovery,towing,4wd",
        "body": """The first thing everybody does is dig, and it is the worst thing you can do. Digging takes the traction away from the tyre and gives the wheel a clean face to spin against.

## Before you try anything

- **Stop and think.** What has the machine got available? A winch on the front of a bigger tractor, a recovery strap, a third tractor, a low-loader?
- **Assess the depth.** If the axles are in and the belly is dragging, you need recovery gear, not pushing.
- **Do not spin the wheels.** Every minute of spinning digs the hole deeper and buries the tyre.

## Getting out gently

1. **Lower the pressure.** Deflate the tyres to about half. More footprint, more grip. Reinflate them to normal afterwards - very low pressure is not safe on the road.
2. **Straighten the wheels.** If they are at an angle, that angle is digging a rut. Straighten and go forward only.
3. **Use the diff lock.** On a machine with a rear differential lock, engage it. It does not add grip, but it stops one wheel spinning while the other does nothing.
4. **Use the brakes to keep the machine straight.** A light application of the brakes prevents the wheelspin from wandering.
5. **Reverse out if you went in forward.** Sometimes the way back is the way out. Reverse in a straight line if the front is buried.

## Recovery

- **Recovery straps** rated for the machine, and know how to use them. Wet straps are stronger than dry ones, and the strap should be pulled by a vehicle that can pull, not by one in the same hole.
- **A winch** on the front of the tractor is the tool for the job. Every farm should have one and every farm should practise with it.
- **A third tractor** pulling from the low point of the drawbar, not the top link. Pull from the drawbar or a recovery point - never from the three-point linkage.

> **Recovery points.** Older tractors often have no proper recovery points. Fit one, rated for the machine, before you need it.
""",
    },

    # ------------------------------------------------------------- farming
    {
        "slug": "setting-plough-depth",
        "title": "Setting plough depth without guesswork",
        "category": "farming-crops",
        "summary": "Depth is measured from the ground to the top of the landslide, not to the bottom of the furrow. That one fact fixes most depth complaints.",
        "author": "Marta, arable",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "ploughing,depth,setup,machinery",
        "body": """Everybody argues about ploughing depth and everybody means something different by it. Get the definition right first.

## What depth actually means

Plough depth is measured from the surface of the ground to the top of the land - the unploughed slice of soil the plough turns over. It is not the bottom of the furrow.

A plough set to 20 cm depth turns over a slice that is about 15 cm thick, because the mouldboard also moves soil sideways. Remember this and half the arguments disappear.

## Setting it

1. **Start shallow.** Set the plough for about 12 cm and work in a short length of ground.
2. **Dig out a spadeful** of the finished furrow. Measure the slice thickness. That is the plough depth minus the thickness of the surface soil you are burying.
3. **Adjust the top link** to level the plough, and the depth wheel or hydraulic control to change the depth.
4. **Check the same point in the field.** Depth wheels sink into soft ground and ride up on the firm patches. If the plough is wandering, that is the fault - not the setting.

## Depth and the weather

- **Deep is not better.** Deep ploughing mixes the fertile topsoil with subsoil and dilutes the seedbed.
- **Never plough wet ground.** Wet soil ploughed smears and compacts, and the damage shows up in the crop three years later. See [[soil-compaction]].

## Breaking the ground

On heavy ground, working at 20 cm with a chisel plough and then following with a shallow pass at 10 cm gives a better seedbed and uses less fuel than one deep pass.

## Slipping the wheel

If the plough keeps pulling the tractor sideways, the depth is too deep for the power. Either work shallower or use a bigger tractor.

> **Practical tip.** Mark the depth wheel with a paint pen at the setting you want, and check it every time you head out. It takes ten seconds and saves an argument.
""",
    },
    {
        "slug": "soil-compaction",
        "title": "Diagnosing and fixing compaction",
        "category": "farming-soil",
        "summary": "A hardpan at the plough depth is the single most common cause of a disappointing crop. Find it with a spade, then break it in dry conditions.",
        "author": "Priya",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "soil,compaction,subsoiling,drainage",
        "body": """Compaction is squashed soil. It cuts off air and water, stops roots going down, and makes the field work badly in every other respect.

## Find the layer

Dig a hole about 30 cm deep in a bad part of the field. Look at the profile.

- **A dense horizontal band at a consistent depth** is a plough pan - the plough has been smearing the bottom of each furrow into a hard layer.
- **A dense layer across a slope** is from driving up and down the hill.
- **Ruts on the surface only** are just wet ground, and they will grow back.

The band should be visible as a change in colour and structure. A good spade will slice it out as a distinct slab.

## Why it matters

A plough pan sits right in the root zone of most crops. Roots cannot get through it, so the plant is shallow rooted and droughts early. Water cannot get through it either, so the field holds water in wet spells and is dry in dry ones.

## Fixing it

**Subsoiler or deep tine.** Run at 30-40 cm in dry conditions. The tines must run at the same spacing as the wheels - a mis-aligned subsoiler creates a new pan in between the tines.

**Timing.** Do it when the soil is dry enough to shatter and dry enough that the subsoiler does not just smear. Late summer after a dry spell is ideal.

**Do not subsoil a wet seedbed.** You will make the problem worse. Subsoiler, then cultivate, then drill.

**Permanent fix.** Fix the cause: reduce the axle load, use lower tyre pressures, or stop working the field when it is too wet.

## Prevention

- Do not cultivate wet soil.
- Use controlled traffic - keep the same wheel lines year after year.
- Cover crops with roots that open the soil.
- Watch the ground with a spade every season. Ten minutes a year saves a lot of money.

> **If a field is only yielding well on the headland, you have told yourself where the problem is.** The headland gets turned more often, so it is the least compacted.
""",
    },
    {
        "slug": "sowing-winter-wheat",
        "title": "Sowing dates for winter wheat",
        "category": "farming-crops",
        "summary": "The right date depends on your region and your soil, not on a calendar. Get the date right and the seed rate can follow from it.",
        "author": "Marta, arable",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "wheat,sowing,seed,drilling,rotation",
        "body": """Ask three farmers when to sow winter wheat and you will get three different dates. The honest answer is that it depends on where you are and what the soil is doing.

## The rule behind the rule

Sow winter wheat **after** the day-to-day average temperature drops below about 8 degrees C, and not before the ground is wet enough to give the seed a chance but not so wet that the drill smears.

In practice that puts the UK and similar maritime climates in the second half of October through to the end of November. Further north and east, earlier. Mild winter climates, later - and if you are too late, the seed sits in the ground all winter and rots.

## What you lose by sowing too early

- The seed goes in warm and grows too fast, then gets hit by aphids and virus.
- Too many leaves, too much growth, and the plant lies over in the winter rain.
- High disease pressure from volunteers and the previous crop.

## What you lose by sowing too late

- The seed sits cold and wet and rots - you lose the stand.
- The plant has too few roots before it hits spring.
- If the ground freezes, you cannot drill at all and you lose days you cannot get back.

## Seed rate

Sow on date, and the seed rate goes **down**. On heavy, cold soil at the right date you might use 250 kg/ha. Early into cold soil, 350-400 kg/ha to compensate for the losses.

A common rule of thumb: for every week you are early, add about 10% to the seed rate, up to a limit.

## Drilling

- Drill at 4-5 cm into the seedbed. Deeper and the seed uses more energy to emerge.
- Leave the seedbed with some tilth, but not so much that the seed drops too deep in a soft drill slot.
- Check the drill calibration with a tray and a sheet of paper. Every time you change seed.

> **Record your dates.** Keep a note of sowing date, seed rate and variety for each field each year. After three seasons you will know your own farm better than any book does.
""",
    },
    {
        "slug": "soil-ph-and-lime",
        "title": "Reading soil pH and knowing when to lime",
        "category": "farming-soil",
        "summary": "Lime is not a fertility treatment. It is a pH treatment, and it is the one thing that will unlock fertiliser you have already paid for.",
        "author": "Priya",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "soil,ph,lime,fertiliser,testing",
        "body": """Most nutrient problems on arable land are not nutrient problems. They are pH problems.

## What pH does

Soil nutrients are only available to plants within a range. Lime the soil and you unlock phosphorus, nitrogen and potassium. Leave the soil too acid and the nutrients stay locked up, no matter how much you spread.

- **Below pH 5.0:** aluminium becomes available and it poisons the roots. This is acute damage, not a subtlety.
- **pH 5.0-6.0:** the range where most crops start to struggle.
- **pH 6.0-7.5:** the sweet spot for most arable crops and grassland.
- **Above 7.5:** phosphorus and some trace elements start to lock out again.

## Testing

Test every three to four years on arable land, and every field separately if the land varies. A spade test in the corner of the field tells you nothing.

Take samples at the plough depth, 15-20 cm, in a zig-zag across the field, avoiding headlands and odd spots. Mix thoroughly in a clean bucket, and take about a kilo of the mix to the lab.

A home test kit is fine for spotting a field that is grossly wrong. For lime decisions, use the lab - lime is expensive to get wrong.

## Applying lime

**Which lime.** Agricultural lime (ground limestone) is the standard. Dolomite lime adds magnesium, which helps on light, acid soils where magnesium is low. Avoid hydrated lime - it is quick acting, burns the organic matter and is not a long-term answer.

**Rate.** Typically 2-5 tonnes per hectare to raise the pH by about 0.5, depending on the soil type and the pH you are starting from. The lab tells you the rate for your soil.

**Timing.** Apply in autumn, ahead of the autumn cultivations, and spread it evenly. Lime moves down the soil profile over years - one big application every three or four years is better than small amounts every year.

## A caution on heavy land

Lime plus dung plus a lot of rain can push a heavy soil into a structureless mess. Do not lime and apply slurry to the same field in the same autumn without thinking about it.

> **Do not guess.** Lime is one of the few inputs where the wrong rate genuinely costs money and cannot be undone for a season.
""",
    },
    {
        "slug": "storing-grain",
        "title": "Storing grain without losing money",
        "category": "farming-crops",
        "summary": "Moisture, temperature and time. Get those three right and grain can be stored for months without loss.",
        "author": "Tomasz",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "grain,storage,moisture,silo",
        "body": """Grain is alive. It respires, it uses up its own reserves, and if it is warm and damp it will lose quality and grow mould before you notice.

## The numbers

- **Below 14% moisture:** safe to store for months.
- **14-15%:** safe for a few months in good conditions.
- **15-17.5%:** only store for a short time, and you must dry it and check it.
- **Over 17.5%:** cool it quickly and dry it. Do not put it in the store.

These figures are for wheat and barley. Oats and other small grains run wetter, and oilseed rape is much more sensitive - 8-9% for long storage.

## Drying

- Dry as slowly as the temperature allows. Over-hot drying kills the germination and gives you a batch that is good for feeding and useless for seed.
- Cool the grain after drying. Warm grain in a cold store makes condensation on the roof and in the middle of the heap.
- Get the grain off the ground and off the damp floor. A concrete floor with a damp-proof membrane, or a raised floor over a drainage channel.

## The heap

- Do not make one enormous heap if you can avoid it. Smaller heaps cool faster and are easier to manage.
- Do not mix loads with different moisture contents. They will separate, and the wet pocket in the middle will go mouldy.
- Fill the store in layers if you are using a flat floor.

## Watch it

Put a probe thermometer into the heap. Check every two weeks for the first month, then monthly. Warm spots show as a rise of several degrees above the ambient.

Turn the heap if you find a hot spot and you can do it without wetting the grain.

## Insects

- Keep the store clean and the ground free of spillings before you fill it.
- Treat empty stores before filling.
- Watch for the webbing and dust trails of grain weevil, and for the actual smell - grain that is infested has a slightly musty, nutty smell.

> **The cheapest monitoring tool is a probe thermometer and a notebook.** Write the reading and the date every time. Trends tell you things a single reading does not.
""",
    },
    {
        "slug": "combine-settings",
        "title": "Setting a combine for wheat",
        "category": "farming-crops",
        "summary": "Four settings decide most of the loss: reel speed, cylinder speed, concave clearance and fan speed. Set them for the crop in front of you.",
        "author": "Tomasz",
        "difficulty": "hard",
        "read_minutes": 7,
        "tags": "harvest,combine,wheat,settings",
        "body": """A combine that is set badly loses money in the tank, in the field and on the straw. Most of the loss comes from four adjustments.

## 1. Reel speed

The reel should tip the crop onto the cutterbar. Too slow and the crop is pushed over rather than brought in, and you lose the heads. Too fast and the reel smashes the stems and throws the crop over the front.

The rule: reel tip speed should be about 10-25% faster than the forward speed of the machine.

**Watch it working.** Drive alongside with the reel and check whether the heads are being pushed under the cutterbar or knocked off. If the crop is bobbing, the reel is too fast.

## 2. Cylinder and rotor speed

For wheat at a normal moisture, the cylinder runs roughly at a quarter of the drum diameter in revolutions per minute. Too slow and the threshing is incomplete - you find grain in the straw. Too fast and you crack the grain, which shows up as broken grain in the sample and in the price you get paid.

**Use the sample.** Tip the grain from the tank every few minutes and look at it. Whole kernels with a bit of unthreshed head means the cylinder is too slow.

## 3. Concave clearance

This controls how much straw goes through with the grain.

- Too tight: you get a clean sample but you overload the separator and lose grain in the straw.
- Too open: you save power but you put a lot of straw through and the sample is dirty.

Start with the book, then adjust in small steps while watching the loss from the back of the machine.

## 4. Fan speed

The fan cleans the grain by blowing chaff out through the sieves. Too fast and you blow good grain out with the chaff. Too slow and the sample is dirty.

## Field speed

Most combines should run at 3-6 km/h in good, dry wheat. Going faster to get the job done loses more than it saves.

## Straw

Check the straw is coming out in neat, even bunches with the grain properly separated. Ragged straw with grain still in the heads means the cylinder is too slow. Stripped, dusty straw means the concave is too open.

> **Record your settings.** Write down the four numbers for each crop variety. You will find yourself adjusting them back and forth for a whole harvest otherwise.
""",
    },
    {
        "slug": "irrigation-scheduling",
        "title": "Irrigation scheduling by soil feel",
        "category": "farming-water",
        "summary": "Water at the right moment and you use less of it. The spade and a bucket will tell you more than a calendar.",
        "author": "Priya",
        "difficulty": "easy",
        "read_minutes": 5,
        "tags": "irrigation,water,soil,scheduling",
        "body": """Most irrigation is wasted because it is applied too early or too much at a time. Scheduling by calendar means watering whether the crop needs it or not.

## The feel test

Dig a hole 20-30 cm deep in the root zone. Take a handful of soil from the bottom of the hole and squeeze it.

- **Squirts water between your fingers:** far too wet. Do not irrigate.
- **Holds together and forms a ball, but breaks up with a tap:** about right for most crops.
- **Crumbles and will not hold together:** time to irrigate.

Do the test in three or four places across the field. Do it at the same time of day. Do it at the same depth every time, and mark the depth.

## How much

One millimetre of water is 10 cubic metres per hectare. That is a useful number to keep in your head:

| Application | Equivalent |
| --- | --- |
| 10 mm | 100 m3/ha |
| 25 mm | 250 m3/ha |
| 50 mm | 500 m3/ha |

Most crops want a deep, infrequent watering rather than a little and often. A small daily application wets the surface, encourages the roots to stay near the surface, and loses a lot to evaporation.

## When to irrigate

- **Morning or evening.** Midday irrigation loses a lot to evaporation.
- **Never in the wind**, unless you have a sprinkler that can cope with it.
- **Avoid irrigating in the last few weeks before harvest** on many crops - it can delay maturity.

## A cheap alternative

If you have no moisture meter, dig a hole and put a sheet of plastic on the bottom of it overnight. If there is condensation on the plastic in the morning, the soil is wet enough. It is crude and it works.

> **Check the pump before you need it.** Flow rate drops with a blocked filter and a tired impeller, and the day you find out is the day you need the water.
""",
    },
    {
        "slug": "field-drainage",
        "title": "Field drainage and ditch maintenance",
        "category": "farming-water",
        "summary": "Water sitting on a field is a symptom. The question is whether it has anywhere to go.",
        "author": "Ruth",
        "difficulty": "moderate",
        "read_minutes": 5,
        "tags": "drainage,ditches,water,flooding",
        "body": """After heavy rain, look at the field and ask where the water is going. If it stands in the same place every year, the field has no way to drain.

## Surface water versus groundwater

**Surface water** sits on top because the ground is sealed or the slope is too flat. It goes away slowly, if at all.

**Groundwater** comes up from below. It is often worse, because it brings iron bacteria and smells of rotten eggs when it hits the air.

## The order of work

Fix things in this order, cheapest first.

1. **Ditches.** Every ditch on the farm should be clear, deep enough and with a fall. A blocked ditch makes the whole catchment above it wet.
2. **Field ditches.** Cut and clean these every year in the autumn, before the winter fills them.
3. **Cultivation.** Do not plough a wet field. A field that has been ploughed wet has a smeared, sealed surface that will not let water in or out. See [[soil-compaction]].
4. **Subsoiler.** For a plough pan.
5. **Underdrainage.** The expensive option, and the right one for a field that stays wet whatever you do to the surface.

## Ditch maintenance

- Cut ditches in the autumn, not in the spring.
- Keep a consistent width and depth. A ditch that varies collects silt in the narrow places.
- Do not push the spoil into the field - it makes the field smaller and the ditch shallower.
- Keep the outlet clear. A ditch that ends in a blocked culvert is a ditch that is full of water.
- Mend the banks before they collapse. A collapsed bank is a good deal of work to rebuild.

## When to call in an engineer

If a field is wet in the same place every year and the ditches are clean, you have a soil or a groundwater problem. That is the point to get a drainage contractor to look, and it is also the point where grants and schemes may be available.

> **Record it.** Take a photograph of the wet corner of the field from the same spot each year. After three years you have evidence for a drainage scheme application.
""",
    },
    {
        "slug": "cover-crops",
        "title": "Cover crops between cash crops",
        "category": "farming-crops",
        "summary": "A cover crop is a crop you do not sell, grown to protect the soil. It costs seed and time, and it usually pays for itself.",
        "author": "Priya",
        "difficulty": "moderate",
        "read_minutes": 5,
        "tags": "cover crop,rotation,soil,organic matter",
        "body": """Bare soil between crops is soil at its worst. It is being rained on, baked by the sun, and walked on by machinery. A cover crop protects it.

## What a cover crop does

- **Holds the soil together.** Roots and the mycorrhizal network that follows them bind soil particles.
- **Feeds the soil life.** Root exudates feed the bacteria and fungi that make the soil aggregate.
- **Adds organic matter.** A good cover crop adds more carbon per hectare than a good crop of compost.
- **Stops nutrient leaching.** Nitrate left in the soil after a crop is easily lost. A cover crop takes it up and releases it later.
- **Eats the weeds.** Some species suppress weeds better than a herbicide.

## Which one

| Purpose | Species |
| --- | --- |
| Best at fixing structure | Phacelia, oats, vetch |
| Cheapest ground cover | Rye, oats, barley |
| Nitrogen fixing | Vetch, clover, lucerne |
| Deep roots, breaks a pan | Lucerne, radish, chicory |
| Pollinator and soil insect habitat | Mustard, phacelia, buckwheat |
| Suppresses weeds | Rye, vetch, tagasaste |

Mixes are usually better than single species - they spread the risk of a wet autumn or a cold spring.

## Sowing and destroying

Sow as soon as you have harvested. Every week of delay costs you.

- **Terminate with a roller** if you can. It looks convincing, but it does not actually kill anything unless you follow with a herbicide or a frost.
- **Crimper or flail** works, especially if you roll afterwards.
- **Herbicide** is the most reliable, and it costs money.
- **Frost** works in continental climates. Not much use in a mild winter.

## The trade-off

A cover crop uses water. In a dry region you may be stealing water from the next crop. It uses nitrogen if it is a legume, which is not always a good thing if you are trying to reduce nitrogen. And it needs management - a cover crop that survives the winter and then seeds in the spring is a disaster.

> **Try it on one field first.** Pick a field with a clear problem - a wet corner, a thin patch - and see what happens for two seasons.
""",
    },
    {
        "slug": "fencing-that-works",
        "title": "Fencing that keeps sheep in and predators out",
        "category": "animal-sheep",
        "summary": "Most fence failures are a height problem, a ground problem or a tension problem. Fix those three and most fences last.",
        "author": "Ruth",
        "difficulty": "easy",
        "read_minutes": 5,
        "tags": "fencing,sheep,predators,wolves",
        "body": """Fencing is not about the wire. It is about tension, height and a gap at the bottom.

## Height

- **Ground-level fence:** good for cattle and horses.
- **Sheep netting:** about 1.1 m for sheep, 1.4 m if there are lambs or you are trying to keep out dogs.
- **Mixed fence:** sheep netting with two or three strands above it, or with a barbed top. Barbed wire at the top is what stops a fox.

Sheep push against a fence with their nose and go under it. They do not jump it.

## Tension

A fence with no tension waves in the wind and every animal pushes it further over. Tension every 50-100 m along the line, with a proper strainer and a wire gripper.

Check tension by pushing the fence at its middle height. It should give about 5 cm and spring back. If it moves more, the strainer has slipped or the wire has stretched.

## The bottom

- Sheep push under. If the ground is soft, the fence lifts. Use a wider post spacing and a staple that holds the bottom wire down.
- Badger gates are a legal requirement in some places and a good idea in most. They are not expensive.
- A rabbit-proof bottom 20 cm works, but be prepared for maintenance.

## Posts

Set posts properly. A post that is only driven 30 cm into the ground will pull out in the first wet winter, and the whole line will go with it. In stony ground, use a post hole and a post rammer rather than a driver.

## The stock side

- **Deer** need a fence about 2 m high or a fence with a deer topper.
- **Dogs** will go under or through anything that is not taut.
- **Rabbits** will find any gap. Chicken wire keeps them out but does not hold sheep.

> **Walk the line.** Every month, walk the whole fence. Most failures are visible from the fence line, long before they are visible from the house.
""",
    },

    # ------------------------------------------------------------- animals
    {
        "slug": "difficult-calving",
        "title": "Difficult calvings and when to call the vet",
        "category": "animal-cattle",
        "summary": "The line between pulling a calf and causing harm is a matter of a few minutes. Know where the line is before you need it.",
        "author": "Old Bill",
        "difficulty": "hard",
        "read_minutes": 7,
        "tags": "calving,cattle,dystocia,vet",
        "body": """Most calvings go on their own. The ones that go wrong go wrong slowly, and the damage is usually done by a person who waited too long - or who pulled too hard too early.

## Before the birth

- Move the cow into a clean, quiet, well-bedded shed with plenty of room.
- Have a head rope, clean towels, a bucket of warm water, and long clean gloves ready.
- Check the calf is in the right position: two front legs and a nose, or two front legs and a tail.

## When to call the vet

Call early if any of these apply:

- The cow has been straining hard for 30 minutes with no progress.
- The legs or head are in the wrong position.
- The membranes are at the vulva but nothing follows for two hours - a twisted uterus.
- The calf is presented with its back towards the cow.
- The cow is down and cannot get up, or seems in shock.
- Anything at all feels wrong.

Your vet would far rather arrive for a cow that turns out to be fine than arrive to a dead calf and a dead cow.

## Positions

**Normal:** two forelegs extended, nose resting on them. The cow should make progress without help.

**Head back:** the legs are forward but the head is turned back. This needs to be corrected - a rope on the head plus two on the legs, pulled alternately.

**Breech:** tail and hocks presented. Difficult and often needs a vet.

**One leg back:** usually a rope on the one forward leg and a hand pushing the other back.

## If you must pull

- **Never pull.** Pulling without counter-pressure can invert the cow.
- **Push back first.** Push the calf back into the birth canal to make room to reposition it.
- **Use a calving jack properly.** The jack is for leverage, not for force. If both handles meet, you have enough.
- **Alternate.** Pull one leg and then the other, so the shoulders come through square.
- **Work with the contractions.** Pull when she pushes, rest when she rests.

## Afterwards

- Disinfect the navel with iodine within an hour, or dip the stump.
- Make sure the calf takes colostrum within two hours. That is the single most important thing you do in the first day.
- Watch the cow for milk fever - she may be weak, off her legs or unable to eat in the first 48 hours.
- Check for a retained placenta and keep the cow comfortable.

> **Antibiotics.** Only use them under a vet's direction. Using them routinely at calving is how you get antibiotic resistance on your own farm.
""",
    },
    {
        "slug": "mastitis",
        "title": "Mastitis: find it early, treat it properly",
        "category": "animal-health",
        "summary": "Most mastitis is found in the parlour before it is found in the bucket. A monthly check saves the cow and saves the milk.",
        "author": "Priya",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "mastitis,milk,cattle,treatment,prevention",
        "body": """Mastitis is an infection of the udder. Untreated it costs milk, it costs the cow, and in bad cases it ends her milking life.

## Spotting it

**In the parlour.** Look at every cow's udder every day. Swollen quarters, heat, hardness, a cow that kicks at a normal milking, or milk that comes out stringy or bloody. Those are all early signs and all of them are easy to miss if you are in a hurry.

**In the milk.** A cow whose milk separates into two layers - cream on top, watery below - or whose milk is pink or yellow, has a problem. Test it.

**By the California mastitis test.** A cheap, fast way to spot cows with an elevated cell count. It is worth the ten minutes a month.

## Treating

- **Identify the cow.** Write the number on a card on her leg and write it on the treatment record. Mistreating the wrong cow wastes money and does nothing.
- **Treat the right cow for the right thing.** A vet can take a milk sample and run a culture. Blind treatment is mostly wasted.
- **Complete the course.** Stopping when the milk looks normal is how you get a relapse that is harder to treat.
- **Withhold milk.** Follow the withdrawal period on the product, and observe it.

## Prevention, which is most of the job

- **Teat dipping** is the single most effective measure there is. Dip every cow at every milking, and change the dip every 500 cows.
- **Keep the parlour clean.** Bedding, floor, and the cow's own hind legs.
- **Cows are the biggest source of infection.** Cull chronic infections - a cow with a quarter that is blind and produces thin milk is a reservoir for the rest of the herd.
- **Teat ends matter.** Any teat injury is an entry point. Keep the yards and passages free of stones and ice.

> **A cow with a blind quarter is a decision, not an illness.** If she is not going to recover, decide now whether she is worth keeping.
""",
    },
    {
        "slug": "cattle-winter-feeding",
        "title": "Feeding cattle through winter",
        "category": "animal-feed",
        "summary": "Biggest wins come from good silage, enough feed, clean water and dry bedding. Ration detail is the fine tuning on top of that.",
        "author": "Old Bill",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "cattle,feed,silage,winter,ration",
        "body": """Winter feeding problems are usually not ration problems. They are hay quality, water access and bedding problems wearing a ration costume.

## The four things that matter most

**1. Good silage.** A properly made silage should smell like cut grass and vinegar, be sour but not foul, and squeeze like a wet sponge, not like wet paper. If it smells of vinegar and ammonia and you would not want to eat it yourself, the cows will not either.

- Cut at the right stage - for most silage, before the seed heads fill.
- Wilt the grass so it is not going in like soup.
- Compact it properly. Air is the enemy.
- Cover it and seal it. If you can drive a pen in it, it will keep.

**2. Ad libitum feeding.** Cattle should never be waiting for their food. If they have to wait, the dominant animals eat and the shy ones do not. Push the feed closer than you think you need to.

**3. Clean water.** A cow drinks 40-60 litres a day in winter. Check the frost on the troughs twice a day in a hard spell. A frozen trough is a production loss that looks like a feeding problem.

**4. Dry bedding.** Wet bedding pulls heat from the animal and grows bacteria. Keep the bedded area dry and deep.

## Body condition

Assess body condition at the start of winter and again in February. A half a condition score lost over winter is a lot of condition to recover in spring.

If the cows are already thin, adding feed now is less efficient than adding feed in October. See [[body-condition-scoring]].

## Rations

For most wintering beef cattle, the answer is:

- **50-60% of the diet as silage or hay**, and the rest as a bought-in protein or energy feed if the forage is poor.
- **Always include a mineral supplement**, particularly copper, selenium and, in some areas, cobalt. Deficiencies show up as poor growth, dull coats and poor fertility.
- **Salt** should be available at all times - a plain salt lick or a mineral block.

## Watch for

- Dropped dung can mean too much protein or too much starch.
- Scour on lush grass in autumn is a different problem entirely - a high fibre supplement like straw or hay helps.
- Coughing in the shed is a sign of a dusty feed or a wet, mouldy silage. Sort the feed.

> **Test your silage.** Put a core through it and look at it. A handful that is dry and fibrous throughout the core, with no dark wet centre, has been packed well.
""",
    },
    {
        "slug": "sheep-lambing-pasture",
        "title": "Lambing on pasture",
        "category": "animal-sheep",
        "summary": "Lambing outdoors works, but it needs planning: the right ewes, the right ground, and lambing in small groups rather than all at once.",
        "author": "Ruth",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "sheep,lambing,pasture,colostrum",
        "body": """Outdoor lambing is cheaper, healthier and less labour-intensive than a shed - if you set it up properly.

## Before the lambing

**Group the ewes.** Lamb small groups, 20-40 ewes at a time, rather than the whole flock at once. You can find a lambing problem when it is 30 ewes, not when it is 300.

**Choose the ground.** Sheltered, not exposed. Dry, not wet. Shelter from wind and rain matters enormously - a lamb that is wet and cold has no chance.

**Move them early.** Bring the group onto the lambing area a week or two before you expect them to start. Moving ewes close to lambing causes stress and delays things.

**Prepare the feed.** Have the right amount of concentrates available before the lambs come. A ewe with two lambs needs a lot more feed than a ewe with one.

**Have the essentials ready.** Booster (colostrum supplement), lamb feed, a bottle and teat, identification tags, and a lambing record book.

## At lambing

- **Check within a couple of hours of birth.** A lamb that is cold and has not fed is in trouble.
- **Colostrum in the first two hours is the target.** A lamb that has had a good feed in the first two hours has a much better chance than one that fed late.
- **Watch the bonding.** If the ewe does not take to the lamb, get the smell right. Put the lamb's birth fluids on the ewe's nose and let her clean him.
- **Twin lambs** are the risk. A lamb that is small and cold is at real risk of starvation.

## After

- Check the navels. Dip in iodine.
- Mark and record everything - the date, the number of the ewe, the number of lambs, any problems.
- Look for a lamb that is standing but not suckling. That is the one that dies.
- Creep feed the lambs from about 10 days old if the pasture is short.

## Weather

Lambs that are born in cold rain die quickly. Watch the weather forecast and be ready to bring a group into a shed if it turns.

> **Record the numbers.** Licking rate, lamb deaths, ewe losses. Two seasons of records and you will know where your flock's losses are - which is usually the answer to the question people ask every year.
""",
    },
    {
        "slug": "poultry-mites-and-flies",
        "title": "Poultry mites, flies and the smell in the shed",
        "category": "animal-poultry",
        "summary": "Red mite is the reason your hens are pecking at their feathers and your house is smelly. It lives in the cracks, not on the bird.",
        "author": "Sam K.",
        "difficulty": "moderate",
        "read_minutes": 5,
        "tags": "poultry,mites,flies,bedding,henhouse",
        "body": """A henhouse that smells and hens that peck constantly at their backs is the classic picture of red mite. The mite is not on the bird - it hides in the crevices of the house by day and feeds at night.

## Confirming it

Put a white sheet or a piece of white cardboard on the perch at night, under the roosting birds. In the morning, look for tiny moving red dots. If you find them, you have red mite.

A severe infestation is visible in the morning, when the birds come off the perch and there are little red smears on the white sheet.

## Getting rid of them

Red mite lives in the cracks of the house, the perch ends, the nest boxes and the featherboards.

- **Clean out thoroughly.** Take everything out, scrape the perches and the crevices, and wash down with a pressure hose. Do it in the warm weather when they are most active.
- **Treat the structure.** An approved acaricide applied to the cracks, perches and nest boxes, repeated at the interval on the label. Red mite stages hide away from the spray, so a single treatment rarely finishes the job.
- **Treat the birds.** Most licensed products are also licensed for use on the birds themselves. Follow the withdrawal period before eating the eggs.
- **Replace the bedding** completely rather than turning it over.
- **Wild birds** carry mite in and out. Try to keep them out of the run.

## Flies

- **Clean, dry bedding.** Flies breed in wet litter.
- **Disrupt their life cycle.** Move the birds out, clean the house out completely and leave it empty for a week or two.
- **Wild bird proofing** helps here too.

## Smell

A smelly shed is a wet bed and probably mites. Fix the litter management and a lot of the smell goes with it.

> **Be careful with dog and cat flea products.** Some are dangerous to chickens and to the eggs. Use only products licensed for poultry and follow the egg withdrawal period.
""",
    },
    {
        "slug": "weaning-piglets",
        "title": "Weaning piglets without losing them",
        "category": "animal-pigs",
        "summary": "Weaning is a stress event, not a feed event. Preparation in the week before matters more than anything you do on the day.",
        "author": "Tomasz",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "pigs,weaning,piglets,feed,stress",
        "body": """Weaning at 6-8 weeks is the biggest stress in a pig's life apart from being born. Get it wrong and you lose a week of growth and start a run of scours.

## Prepare before you wean

**Creep feed from 10 days old.** Piglets need to learn to eat solid feed while they still have milk in front of them. Creep feed should be a highly digestible starter, placed where the piglets are, in a separate feeder the sows cannot reach.

**Feed the sow the same diet she will get after weaning.** Her gut has to adjust. Sudden changes of diet cause a drop in milk yield and a gut upset in the piglets.

**Wean by pen, not by age.** Wean the biggest piglets a few days before the smallest. It removes the runts from the stress.

**Check the drinkers.** Flow rate in the weaners must be higher than in the farrows - about 1 litre per minute for weaners. A pig that cannot drink in the first hour will not eat.

## The move

- Move the piglets at the same time of day each week so the routine is predictable.
- Keep the temperature at 28-30 degrees C for the first three days. Heat lamps in the farrows are often not enough for freshly weaned pigs.
- Feed a very digestible diet for at least a week - no sudden changes.
- Leave the farrows empty for a few days after weaning, cleaned and disinfected, before you put the next group in.

## Watch for

- **Scour in the first week** is usually diet-related. Go back to the previous feed.
- **Piglets that do not eat.** Pick them up, check the temperature, and get them eating individually.
- **Coughing.** Dusty feed or a draught. Wet feed keeps dust down.
- **A swollen belly with no scour** may be a twist - get the vet.

> **Do not wean on a day you are busy.** It is tempting to wean because the piglets are big enough. Wean because the week afterwards is quiet.
""",
    },
    {
        "slug": "making-hay-in-a-wet-week",
        "title": "Making hay in a wet week",
        "category": "animal-feed",
        "summary": "Wet weather hay-making is a game of managing the moisture you cannot dry away. Spread wide, turn early, and do not stack it green.",
        "author": "Ruth",
        "difficulty": "moderate",
        "read_minutes": 5,
        "tags": "hay,baling,wet weather,forage",
        "body": """A wet week means you will not be making hay. You will be managing a wet crop. Here is how to lose as little as possible.

## While it stands

- **Spread the swath as wide as your mower allows.** Wide swaths dry faster. Do not windrow until the last possible moment.
- **Do not bunch.** Every metre of width is extra surface area to the air.
- **Ted as soon as it is cut.** Turning wet grass onto wet ground picks up dirt and slows drying.
- **If rain is coming, do not mow.** A cut crop with the rain off it will be no drier than the standing crop, and you have lost a lot of leaf.

## The afternoon decision

If the grass has been lying since morning and the weather is turning:

- **Spread it out** as much as you can and let the wind at it.
- **Do not stack it.** Wet grass stacked deep will heat, go mouldy and sometimes catch fire.
- **If it must be baled,** bale it as a separate batch, keep it well away from the main stack, label it clearly and use it first.

## Baling

- **Bale at 18-20% moisture** for good hay. Bales that squeak when you squeeze them are too dry; bales that leave a cold wet mark on your hand are too wet.
- **Wet hay heats.** Stack it with gaps between the bales so air can move, and check the stack centre for a warm spot for the first few days.
- **Never stack wet hay in a barn with livestock in it.** Fire risk.

## When to give up on hay

Sometimes the honest answer is that it is silage year or dry year, not hay year. If the grass is consistently over 25% moisture, closing the clamp and waiting for it to turn into silage is better than bailing a heap of rot.

> **Label everything.** Date every bale and every stack. In six months, when you are feeding it out, you will want to know what you have.
""",
    },
    {
        "slug": "body-condition-scoring",
        "title": "Body condition scoring for cattle and sheep",
        "category": "animal-cattle",
        "summary": "You cannot feed what you have not measured. A condition score takes about a minute and tells you when to change the ration.",
        "author": "Old Bill",
        "difficulty": "easy",
        "read_minutes": 4,
        "tags": "condition scoring,cattle,sheep,feed,monitoring",
        "body": """Look at a cow and you see a cow. Score her and you see a number you can act on. That is the whole point.

## The scale

**Cattle: 1 to 5.**

| Score | Description | Ribs | Hip bones | Tail head |
| --- | --- | --- | --- | --- |
| 1 | Very thin | Sharp to the point of being painful | Prominent, sharp | Very thin |
| 2 | Thin | Visible | Visible | Thin |
| 3 | Moderate | Full, rounded | Rounded | Filled |
| 4 | Good | Not visible | Not visible | Filled |
| 5 | Very fat | - | - | Flush, deep fat |

**Sheep: 1 to 5 as well**, with the spine and the hips as the main reference points.

## How to do it

- **Look at the animal from behind.** The tail head and the hips are the clearest part.
- **Feel the backbone and the short ribs.** Run your hand over the last rib and along the spine.
- **Look at the tailhead from above.** That is the most reliable single view.
- **Score the whole flock, not the best-looking ones.** Handling and feeding decisions are about the animals that need help.

## When to score

- At the start of winter, to plan the ration.
- In the middle of winter, to check the ration is working.
- At weaning, to decide which ewes to re-breed.
- Six weeks before lambing. A ewe that is too thin at lambing has a hard time and a lamb that is too small.

## Targets

- **Beef cows at weaning:** around 3.
- **Pregnant ewes at lambing:** 3 to 3.5. Thin ewes produce small lambs and poor milk.
- **Lactating ewes:** they should drop no more than half a point and no more than one point through lactation.

> **Write the scores down.** The number in the yard changes slowly and you will not remember. A date and a number in the book is worth more than a good memory.
""",
    },
    {
        "slug": "water-troughs-and-algae",
        "title": "Water troughs, algae and the importance of clean water",
        "category": "animal-health",
        "summary": "Cattle drink more when the water is clean. Algae in a trough is a health risk, not just a green stain.",
        "author": "Sam K.",
        "difficulty": "easy",
        "read_minutes": 4,
        "tags": "water,trough,algae,stock,health",
        "body": """Water is the cheapest feed on the farm and the one most often taken for granted.

## How much

- **Cattle:** 40-60 litres a day in summer, half that in winter.
- **Sheep:** 2-5 litres.
- **Lactating cows:** up to 100 litres in hot weather.

If you are short of water, intake drops and milk yield follows. Check the troughs before you check the ration.

## Keeping them clean

- **Empty and scrub at least weekly.** Scrub, rinse, and leave to dry in the sun if you can.
- **Move the trough around.** Moving it every week stops the ground underneath from becoming a mud hole and a reservoir of bacteria.
- **Use a sloped, smooth surface** so debris slides out rather than settling.
- **Prevent the fouling** by keeping the water access area gravel-covered and well drained. Mud around a trough is mud into the trough.

## Algae

Green scum in a trough is not just untidy.

- It harbours bacteria, including ones that make the water smell.
- It can produce toxins in warm, stagnant, sunlit water.
- It gives the water an off taste and animals drink less of it.

To control it: clean it out, keep the water moving, keep it shaded where you can, and use an approved treatment if the fouling is persistent.

## Frozen troughs

In winter, a frozen trough is an emergency. Check twice a day in a hard spell, fit a heater or a frost-resistant float valve, and keep a spare. Ice on the surface of the trough also reduces the amount of water the animals can drink.

## Testing

If the water is from a borehole, check it for sulphate and iron. High sulphate causes diarrhoea and looks exactly like a feed problem. Take a sample to the lab once a year - it is cheap.

> **A cow drinks more when it is cool and clean.** Moving a trough into the shade in July can be worth more than a change of feed.
""",
    },

    # ----------------------------------------------------------- reference
    {
        "slug": "seed-rate-calculator",
        "title": "Seed rate calculator",
        "category": "farming-crops",
        "summary": "Seed rate in kg/ha from target plants, thousand seed weight, germination percentage and expected establishment loss.",
        "author": "Marta, arable",
        "difficulty": "easy",
        "read_minutes": 4,
        "tags": "seed,calculation,drilling,reference",
        "body": """The seed rate you need depends on four things: how many plants you want per square metre, the thousand seed weight of the variety, its germination percentage, and the proportion you expect to lose in the field.

## The formula

```
seed rate (kg/ha) = target plants/m2 x thousand seed weight (g)
                    x 10 -------------------------------
                        germination % x expected establishment %
```

## Working it

**Example: wheat at 250 plants/m2, TSW 45 g, germination 98%, establishment 92%.**

```
250 x 45 x 10
----------------- = 1246 kg/ha
   98 x 92
```

That is 124 kg/ha of seed - about 1.24 bags per hectare.

## The four numbers

**Target plants per square metre.** For winter wheat, 220-280 in a normal year. Higher in a cold, wet autumn, lower in a mild one. For spring barley, 280-350. For beans, 40-70.

**Thousand seed weight.** On the seed label, or count 1,000 seeds. Give or take 5% matters more than you would think.

**Germination percentage.** On the seed label. Do not use the number from last year.

**Expected establishment.** This is the honest one. In a normal autumn, 90-95%. In a terrible one, 80%. In a perfect seedbed drilled at the right time, 98%.

## The rule of thumb version

If you do not want to do the sum: a decent winter wheat seed rate is 250-300 kg/ha, barley 180-220 kg/ha, oats 200-250 kg/ha. Adjust for sowing date and conditions.

> **Always weigh.** Take a drill fill, run it over a measured area, weigh the seed and calculate the rate you are actually using. It is ten minutes and it is the only way to know.
""",
    },
    {
        "slug": "safe-lifting-tractors",
        "title": "Safe lifting: loads, three-point linkage and getting off the ground",
        "category": "vehicles",
        "summary": "Most injuries on farms happen while getting on and off machines. A stable machine with a low centre of gravity is the fix for both lifting and crushing.",
        "author": "Old Bill",
        "difficulty": "easy",
        "read_minutes": 4,
        "tags": "safety,lifting,three-point,crushing",
        "body": """Lifting and mounting are the two things that kill and maim farm workers every year, and both are about the same thing: getting your body into a machine that moves.

## Mounting

- **Three points of contact, every time.** Two feet and one hand, or two hands and one foot. Always facing the machine.
- **Do not jump up.** The step and the handhold are there so that you do not have to.
- **Keep the steps clean.** Mud, ice and slurry on a step is the single most common cause of a fall at the yard gate.
- **Park on level ground** with the engine off before you dismount.
- **Wear your boots.** Steel toe, slip resistant. Not wellies.

## Getting off

The same three points of contact, in reverse. And do not jump down - a twisted ankle in a yard is how people end up with a long-term problem.

## Lifting on the three-point linkage

The three-point linkage is not a crane. It is designed to control the position of an implement, not to lift a load into a trailer.

- **Get the load close to the tractor before you raise it.** The further out the load is, the more the moment arm multiplies the tipping force.
- **Lower the load before you stop the tractor.** Never stop with a load held high.
- **Do not stand under a raised implement.** Not even briefly, not even to fetch a spanner.
- **Do not ride on the implement.**
- **Watch the height.** A raised loader blocks your view and can hit a low branch, a shed door or a power line.

## Tipping

The tractor tips forward or backwards when the centre of gravity moves outside the wheelbase.

- Adding a load at the front is safer than removing one at the rear.
- A load on a raised rear loader arm is much worse than the same load low down.
- Slow down before you turn. Sudden steering at speed is the classic rollover cause.
- Keep the side of the hill downhill, and if the ground is soft, take the steeper line not the safer-looking one.

## The rule that covers everything

**If you cannot get out of the machine quickly, you are in the wrong place.** Get a seatbelt fitted if the machine has one. If it does not, fit one.

> **Nobody works alone with a raised loader.** Not for a minute. Not for a quick adjustment.
""",
    },
    {
        "slug": "fuel-log",
        "title": "Keeping a fuel log that is actually useful",
        "category": "workshop",
        "summary": "A fuel log is only worth keeping if it is simple enough to fill in. Four numbers per job is enough.",
        "author": "Ruth",
        "difficulty": "easy",
        "read_minutes": 3,
        "tags": "fuel,log,bookkeeping,costs,reference",
        "body": """Fuel is the biggest variable cost on most farms after labour, and it is the easiest to lose control of because nobody is measuring it.

## The four numbers

For each job, write down:

1. **Date**
2. **Machine and job** (e.g. "Ford 5000 - ploughing block 3")
3. **Hours on the clock** (or litres used)
4. **Litres bought**

That is it. Anything more and it will not get filled in.

## What it tells you

After a season you can answer the questions that matter:

- Which machine is burning the fuel? Compare litres per hour across machines of different ages.
- Which job is expensive? Ploughing at 9 litres per hectare versus harvesting at 22 tells you where the attention should go.
- What is the fuel use per hectare across the whole year? That is the number you compare with the seed and fertiliser bill.
- Is the trend rising? A machine that used 6 litres an hour last year and 8 this year is telling you something.

## Tips that make the difference

- **Fill up at the same time each week** - a Sunday morning is fine - and record it in one go.
- **Record litres from the pump ticket**, not from memory.
- **Watch the machine, not just the log.** A meter showing more hours than the book is a clue.
- **Log the fuel you put in cans for the quad and the chainsaw.** Small engines are thirsty and it adds up.

## Watch for the usual losses

- A partly blocked air filter on a tractor can cost 5% and it is a twenty-minute job.
- Under-inflated tyres cost more than most people expect.
- A machine left idling while the loader is down is burning your money and warming the world.
- Running the air conditioning with the windows open on a summer's day is a diesel heater pointed at the sky.

> **Measure it for one season.** That is all it takes to find the leak that has been costing you money for years.
""",
    },
]
