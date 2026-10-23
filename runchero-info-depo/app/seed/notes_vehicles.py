"""Extra notes for the machinery shelves: engines, diagnosis and implements.

These sit alongside the original 35 notes in ``articles.py`` and follow the
same house style: symptom, cause, fix, and the safety bit somebody forgot the
first time.
"""

from __future__ import annotations

NOTES: list[dict] = [
    {
        "slug": "winterising-a-tractor",
        "title": "Winterising a tractor: coolant, antifreeze and drains",
        "category": "vehicle-engine",
        "summary": "Six jobs in an afternoon that stop a frozen block in January. Do them before the first frost, not after.",
        "author": "Old Bill",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "winter,antifreeze,cooling,freeze,preparation",
        "body": """A tractor that stands out in the yard through January is a tractor you will not have in March. Winterising is not complicated, but it has to be done before the cold, not after.

## The antifreeze

- **Drain the cooling system** and flush it with clean water. Old coolant full of sludge and rust is what freezes first.
- **Fill with the right antifreeze** for the lowest temperature you expect, not the one you had last year. The label gives the protection in minus degrees.
- **Check the specific gravity** with a hydrometer or a refractometer once the engine is cold. Old antifreeze loses strength as it absorbs water.
- **Never mix glycol and ethylene glycol types.** They do not mix cleanly and the result can be a gel that blocks the pump.

## The drain taps

A lot of old tractors have a drain plug on the cylinder head and one on the block. These are the ones that freeze.

1. Put the tractor on firm level ground with the nose up, so the plugs are at the low point.
2. Open every drain tap and the radiator outlet.
3. Run the engine for two minutes with the heater on full. That pushes the warm water out of the block.
4. Close the taps, refill, and check the level after a minute.

## Everything else that holds water

- **The washers and the air filter housing.** Clean them out, and leave the intake off the dust cap or the cover off so nothing traps water.
- **The exhaust.** A pipe pointing down collects water and will split. A pipe pointing up keeps rain out. Either is fine; down and full of water is not.
- **The fuel tank and the lines.** Water sits at the bottom. Drain it, or add a fuel filter with a water separator.
- **The battery.** Clean the terminals, top up the electrolyte, and put the machine on a trickle charger if it will stand for months.
- **Any hydraulic ram.** Raise it fully and put a prop under it before you leave it. A ram that slowly lowers onto its own seal is a ram that needs a seal.
- **The water pump and the cab heater hoses.** These are the ones people forget.

## The last thing

Turn the engine over by hand once before you leave it. If it does not move freely, something is seized or frozen and you want to know that in the yard, not in March.

> **Do not drain the cooling system on a hot engine.** Let it cool first, and open the filler cap slowly - hot coolant will come out as a spray.
""",
    },
    {
        "slug": "belts-and-hoses",
        "title": "Belts, hoses and the rubber parts that fail on the road",
        "category": "vehicle-engine",
        "summary": "A fan belt or a hose rarely fails at a convenient moment. Five minutes of looking saves the walk home.",
        "author": "Marta, arable",
        "difficulty": "easy",
        "read_minutes": 5,
        "tags": "belts,hoses,rubber,cooling,maintenance",
        "body": """Belts and hoses are cheap, they are easy to change, and they are the parts that leave you walking. A check takes five minutes and needs nothing but your hands.

## Belts

**Look for:** glazing (a shiny glassy surface), cracking across the belt, fraying at the edges, missing ribs, and any oil or diesel on the belt. Oil on a belt will destroy it quickly.

**Check the tension.** On a fan belt, push the middle of the span and it should deflect about 10 mm. Too tight wears the bearings; too loose slips and you lose the fan speed.

**Check the alignment.** Look along the belt run. If the pulleys are not in line the belt runs off the edge and wears unevenly.

**Fan belts should not be dressed or polished.** A bit of slip is normal in the cold; a glazed belt needs replacing, not adjusting.

## Hoses

**Look for:** a bulge when the engine is running, a soft or spongy feel, a crack along the hose, chafing where the hose touches a bracket, and the ends where the hose is clamped.

- A hose that has gone soft and squeezable is finished. It will burst at the first hot pressure.
- **Rubber hoses perish from the inside out.** The outside can look perfect while the inside has gone to a brittle lining.
- **Chafing kills more hoses than heat does.** Check where the hose passes a bracket, a rocker panel or a sharp edge, and fit a spiral wrap or a piece of split hose over it.

## Which hose is which

| Hose | Job | Symptom when it goes |
| --- | --- | --- |
| Radiator top | Hot water out of the engine | Coolant level drops, engine overheats |
| Radiator bottom | Cool water back into the engine | Overheating, air locks in the system |
| Heater | Hot water to the cab | No heat, or a sweet smell |
| Fuel | Tank to pump | Engine dies, or runs on the reserve |
| Air filter | Air into the engine | Smoke, power loss |
| Hydraulic | Pump to the rams | Slow lift, or arms that will not hold |

## The cheap habit

Keep a spare fan belt, a length of the top radiator hose and a handful of hose clips in the toolbox. Not the ones for the tractor in front of you - the ones for the tractor behind you.

> **Never use clamps or tape as a repair on a fuel line.** A hose that lets fuel onto a hot engine is a fire.
""",
    },
    {
        "slug": "gear-oil-and-clutch",
        "title": "Gear oil, clutch judder and the gearbox",
        "category": "vehicle-engine",
        "summary": "Judder when you pull away is nearly always the clutch, the oil, or both. Learn to tell them apart.",
        "author": "Tomasz",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "clutch,gearbox,oil,judder,gears",
        "body": """A gearbox that jumps or judders when you pull away is telling you something specific. Work out what before you strip anything.

## Judder that changes with the gear

| What you hear | What it means |
| --- | --- |
| Judder in first gear only, stops in second | Clutch friction plate or pressure plate |
| Judder in every gear, worse when loaded | Engine mounts or gearbox mount |
| Judder when you brake and the tractor slows | Driveshaft or propshaft |
| Click going into a gear | Dog clutch or gear lever linkage |

## The clutch

**The symptoms of a worn clutch:**

- Slipping under load. The engine revs and the tractor does not speed up.
- A heavy gear change, or a change that makes the tractor jump.
- Judder on pulling away, worse when the clutch is cold or the oil is warm.

**Checks before you condemn it:**

1. **Look at the pedal free play.** It should be a couple of centimetres. If it is slack and the gearbox is in gear with the clutch down, the clutch is not fully released - that is a throwout bearing or a badly adjusted linkage.
2. **Check the linkage and the fork.** A linkage that has lost a bit of grease can make a good clutch feel bad.
3. **Check for oil on the friction plate.** That comes from the rear seal and it puts a slipper oil on the plate that will not burn off.
4. **Look at the adjustment on the pedal rod.** The adjuster on the push rod sets the free play and it is the first thing to check.

## The oil

Gear oil is not engine oil and the difference matters.

- **Use the grade the manual or the gearbox plate asks for.** A modern tractor may want a multi-viscosity oil; an old one wants a straight 90 weight.
- **Check the level with the oil cold and the tractor on level ground.** Let it settle for ten minutes first.
- **Look at the oil when you check it.** Metal particles mean gears are wearing. Milky oil means water - a bad seal or a cracked casing.
- **Do not overfill.** Half the "gearbox trouble" people report is oil on the dipstick because it was filled with the oil still draining from the filter.

## Changing the oil

- Drain it hot, if you can, so the metal comes out with it.
- Fit a new washer on the plug and tighten it properly. A stripped plug will let the oil out under the road and you will never find it.
- Refill with the right grade, run the engine for a minute to circulate it, then check the level again.

> **If the gearbox is grinding, stop using it.** Metal in the oil means the damage has started, and the repair grows with every hour you keep going.
""",
    },
    {
        "slug": "warning-lights-explained",
        "title": "What each warning light is telling you",
        "category": "vehicle-diagnosis",
        "summary": "Oil, temperature, charging and brakes: what the panel says, and what to do about it before it becomes an expensive noise.",
        "author": "Sam K.",
        "difficulty": "easy",
        "read_minutes": 5,
        "tags": "warning lights,dash,gauges,oil,charging",
        "body": """Most dashboards are a handful of lights and two gauges. Learn what each one is for and you will never need a manual.

## The lights

**Oil pressure (red).** The most serious light on the panel. Stop the engine. See [[oil-pressure-warning]] - the ticking that comes with it is a bearing running out of oil.

**Water temperature (red or amber).** The engine is too hot. Switch off, let it idle for a minute to let the coolant circulate, then stop. Do not open the filler cap. See [[overheating-tractor]].

**Charging (red).** The alternator is not charging. The machine will run on the battery until it does not. Check the belt first - a glazed or broken fan belt is the common cause.

**Amber / bulb on the dash at start-up.** Some machines run a bulb test. If it goes out when the engine starts, that is normal. If it stays on, there is a fault in that circuit.

**Brake or park brake (red).** On a lot of tractors this is the handbrake warning, and it stays on until the handbrake is properly released with the lever all the way down or back.

**Direction indicators (green).** Self cancelling or not, depending on the machine. A relay that ticks without the bulbs lighting means a burnt bulb somewhere.

**Headlight dip (blue).** Working. If it stays on with the lights off, the dip relay is stuck.

## The gauges

**Oil pressure gauge.** The needle should sit in the middle once the engine is warm. Do not let it sit at the bottom - on some older machines the gauge is fed directly from the pump and the needle at the bottom means the pump is not moving oil at all.

**Temperature gauge.** A steady needle in the middle. A needle that swings wildly is a thermostat that is stuck, and a needle that climbs steadily is a blocked radiator or a missing fan shroud.

**Ammeter.** On older machines this shows charge and discharge. It should sit a little above zero with the engine running. Sitting hard on discharge means the alternator is not charging; sitting hard on charge means the regulator is overcharging and cooking the battery.

**Hours meter.** Write the hours down. It is the cheapest maintenance tool on the farm and it tells you when the oil actually needs changing rather than guessing by season.

## Test the warning lights

Once a month, with the ignition on and the engine off, check that every warning light comes on. A bulb that has been out for years tells you nothing when it matters.

> **If the oil light and the temperature light both come on, stop.** Two warnings at once usually means the oil has gone and the engine is about to overheat as a result.
""",
    },
    {
        "slug": "tractor-stalls-when-hot",
        "title": "Starts cold, dies hot: the hot restart problem",
        "category": "vehicle-diagnosis",
        "summary": "An engine that runs for twenty minutes and then stops usually has one of four faults. None of them are the coil.",
        "author": "Dave, top field",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "hot start,dies hot,stalls,fuel,cooling",
        "body": """It starts first thing, runs all morning, then coughs once and stops. It will not restart until it has cooled for half an hour. That pattern narrows the fault down sharply.

## 1. Air in the fuel system

The most common cause by a distance, and the easiest to confirm.

- **Check for air under the tank.** Look at the glass bowl on the filter or the transparent pipe. Air bubbles in the bowl mean air is coming in faster than it is being used.
- **Check the supply valve.** If the bowl refills within seconds of being drained, the shut-off valve is passing and the pump is drawing air.
- **Check the unions on the suction side.** Every union between the tank and the pump is a candidate. Fuel systems get cracked by vibration and by rodents.
- **Check the filter.** A blocked filter starves the pump and pulls air in.

**Fix:** bleed the system, tighten every union, and look for a hairline crack at the fuel filter head.

## 2. The injection pump

On a hot engine the pump gets hot, and some of them do not like it.

- **The fuel is too hot.** Old diesel has a lower flash point than new. If the tank is open to the sun and full of old fuel, it can be a genuine problem in summer.
- **The pump needs cooling.** Some engines have a fuel-to-water heat exchanger or a separate cooler for the injection pump. A blocked one shows up exactly like this.
- **The governor is misbehaving.** On a hot engine with the governor running out of fuel, the pump can shut off and not restart.

**Fix:** check the pump cooling lines are clear, drain and clean the fuel lines, and if the tank is in the sun, put a shade over it.

## 3. The cooling system

An engine that is overheating will run, then die. The gauge climbing is the clue, and it may only be visible in the last five minutes before it stops.

- Check the level cold, not hot. A hot system hides a low level.
- Check the radiator cap, the thermostat and the fan belt. See [[overheating-tractor]].
- Look for a weep from the water pump or the radiator pipe.

**Fix:** find the leak. See [[winterising-a-tractor]] for the drain taps that often leak.

## 4. The electrics

- **The ignition switch.** Heat expands the contacts and they open. Wiggle the key while the engine is hot and see if it catches.
- **The stop solenoid.** Some engines energise the fuel shut-off solenoid to run and de-energise to stop. A hot solenoid that drops out will stop the engine cleanly.
- **The charging.** If the alternator is failing, the battery voltage sags as the engine heats and the fuel pump slows.

## The way to find it

Put a clamp meter on the battery and watch the voltage while it dies. If the voltage stays above 13 volts and the engine stops, it is fuel or cooling. If the voltage collapses, it is the charging circuit or a heavy draw from the fuel pump.

> **Do not keep restarting a hot engine.** If it will not start within three or four tries, stop and think. You will not fix it by trying harder, and you will flatten the battery.
""",
    },
    {
        "slug": "water-in-the-fuel",
        "title": "Water, rust and sludge in the fuel tank",
        "category": "vehicle-diagnosis",
        "summary": "Water in diesel comes from condensation, from a badly fitted cap, or from the tank being drawn down to the last of it. All three are fixable.",
        "author": "Sam K.",
        "difficulty": "moderate",
        "read_minutes": 5,
        "tags": "fuel,water,diesel,tank,sludge",
        "body": """Diesel and water do not mix. Even a few pints of water at the bottom of the tank will rust the whole system and wreck the injection pump.

## Where the water comes from

- **Condensation.** A tank that is half full on a cool morning has condensation on the walls. In a sealed tank with a breather, it eventually drips down and collects.
- **A bad cap or a missing cap.** Rain gets in, or dust and rain get in through a broken cap seal.
- **Drawing the tank dry.** When the tank is run empty, air is drawn in through the supply, and that air carries any rust and moisture with it.
- **Old fuel that has been standing.** Diesel that has sat for a year separates, and the water ends up in the bottom.

## How to spot it

- **The filter.** A glass bowl filter will show water at the bottom and a rust ring at the top of the diesel. That ring is the giveaway.
- **A fuel sample.** Draw it from the bottom of the tank into a clear jar and let it stand. Water settles out in a layer at the bottom.
- **The symptoms.** A misfire that is worse when the tank is low, a smoky exhaust, a strange noise from the injection pump, or the engine that cuts out for a second and picks up again.
- **Rust on the injector tips.** Pull an injector and look at it. Any rust at all means the water has been in there.

## Draining and cleaning

1. **Siphon the tank out.** Use a proper pump, not a hose on the inlet, and put the fuel into a labelled drum.
2. **Let it stand.** The diesel will separate. Pour off the clean diesel from the top and keep the water and sludge at the bottom for disposal.
3. **Clean the tank.** Take the filler neck off, drop a light in and look. If there is rust at the bottom, flush it with a little diesel and a chain.
4. **Fit a water separator.** A spin-on filter with a clear bowl and a drain at the bottom catches everything. It is the single best thing you can fit to a machine that lives outside.
5. **Change the filter and the injection lines.** If the water has been in the system, the lines are rusted inside and the injector will not be clean.

## Preventing it

- **Keep the tank full.** A full tank has no air space to make condensation in.
- **Fit a proper cap with a seal.** A cap that rattles is a cap that lets rain in.
- **Never run the tank dry.** Keep a reserve.
- **Drain water from the glass bowl filter every week** in the wet season.

> **Do not put a strainer on the bottom of the tank and forget it.** It will hold water against the pickup and make the problem worse.
""",
    },
    {
        "slug": "trailer-brakes-and-lights",
        "title": "Trailer brakes, lights and the road test",
        "category": "vehicle-implements",
        "summary": "A trailer that will stop is a legal trailer and a safe one. Here is how to set the brakes up and how to check they work.",
        "author": "Old Bill",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "trailer,brakes,lights,roadworthiness,towing",
        "body": """More trailer accidents come from a brake that was never adjusted than from a bad driver. Setting a trailer up properly takes twenty minutes and it is done once, not every time.

## Set the brakes before you load

1. **Jack the trailer so the wheel can be turned by hand.** The wheel must turn freely and must not have any slack in the hub.
2. **Check the slack adjusters.** Most trailer brakes have an adjusting mechanism on the back of the drum. The gap should be about a quarter inch, tight enough that the drum cannot be turned by hand, loose enough that the shoes always release.
3. **Back the adjuster off until the shoes just touch, then take it up a quarter turn.** Tighten the locknut after every adjustment.
4. **Do the wheels one at a time** and check each one is exactly the same. A trailer that pulls to one side is usually a brake on the other side that is not releasing.

## The test

- **Push the trailer forward with the brake on.** It should push easily. If it is hard to push, the shoes are dragging.
- **The pull test.** Hitch it up, jack the front of the trailer a foot, and pull forward on the drawbar. The trailer should push back hard against the hitch, and the jack should not move. If it pushes back hard but still rolls, the brakes are working.
- **The loaded test.** Load it properly and drive up a gentle slope. The trailer should hold the tractor back. If the trailer pushes the tractor, the brakes are not holding and the load is too heavy for them.

## The lights

- **Check the plug, not just the bulbs.** A seven-pin plug with a bent pin will light some of the trailer and not the rest.
- **Test every function with the tractor running.** Brake lights, indicators, hazard, position lights, reverse, and the reflectors.
- **Check the trailer's own earth.** A trailer with a poor earth shows up as the brake lights glowing dimly, or the indicators flashing when you put the hazards on. It is a dirty earth pin in the plug.
- **Trailer reflectors are not optional.** Triangle at the back, the right size for the width of the trailer.

## The hitch

- **The coupling must be locked.** A hitch that lifts off the ball when the trailer bounces is a trailer that comes off on a hill.
- **The safety chain or cable must be attached.** It must be crossed under the drawbar so it catches the coupler if the hitch fails, and it must have enough slack for the trailer to steer.
- **The jockey wheel must be up.** Every year. Every time.
- **Check the load rating.** A trailer's rating is a braking rating as well as a weight rating.

## On the road

- **Check the tyre pressures cold, and higher than you would think.** Trailer tyres at low pressure overheat and fail.
- **Lift the tyre brands and the pressures on a marker on the trailer.** Everyone who uses the trailer should be able to read it.
- **Do the first check at five miles and the next at fifteen.** That is when a loose coupling or a wheel nut shows up.

> **Never tow a trailer with no working brakes on the road.** If the brakes are not right, it does not go on the road, whatever the distance.
""",
    },
    {
        "slug": "flail-mower-maintenance",
        "title": "Flail mowers: blades, belts and bearings",
        "category": "vehicle-implements",
        "summary": "A flail mower that has been left all winter will jam the first time you use it. Two hours of maintenance saves the gearbox.",
        "author": "Ruth",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "flail,mower,blades,belts,bearings",
        "body": """A flail mower cuts hedgerows, scrub and rushes that a rotary mower would choke on. It is also the most brutal machine on the farm for the bearings.

## Before the season

- **Grease every bearing on the mower.** The main rotor bearings are the ones that kill you. Grease them at the start of the season, every month, and at the end.
- **Turn the rotor by hand.** With the engine off, the rotor should turn smoothly with a little play. If it is stiff or rough, one of the bearings is on its way out and it will take the rest with it.
- **Check the belt tension.** A worn belt slips and the blades stop cutting before they break.
- **Replace the blades in sets.** A single new blade on an old set puts the mower out of balance. See [[mower-vibration-after-blade-change]].

## The belts

- Check for glazing, fraying and cracks.
- Check the tension by eye. A belt on a flail mower should be tight, but not stretched over-tight - you should be able to twist it slightly with your fingers.
- **Keep the belt tension adjuster at the midpoint of its travel** if it has one, so you can go both ways when it stretches.
- **Keep a spare belt of the right length** in the shed. Not the same length - the right one.

## The blades

- **Check the pivot pins.** These are the first thing to fail, and a failed pivot sends a blade through the housing.
- **Flip the blades over** if they are reversible, so they wear evenly.
- **Balance the rotor.** If you can hang a set of blades on a bar and it balances at the middle, the set is good. If it will not balance, take that blade out.

## Working with the mower

- **Never work with the blades down in long wet grass.** It stalls the engine and the heat can warp the gearbox housing.
- **Cut high in the first pass** and come down over a few passes.
- **Watch for stones.** Flail mower blades are designed to break rather than to shatter. They will still send a stone through the housing.
- **Do not cut wire, cable or fence posts.** A length of fencing wire wrapped round the rotor will wreck the machine and is nearly impossible to remove.

## After the work

- **Blow the grass out** of the housing and off the bearings every time. Wet grass packed against a bearing is what kills it.
- **Wash the machine down.** Grass and mud hold moisture against the bearings and the paint.
- **Check the guards are straight.** A bent guard is a guard that will catch.

> **Disconnect the spark plug before any work on the cutter.** A mower that starts with you underneath it is the oldest accident in this book.
""",
    },
    {
        "slug": "hitching-and-towing",
        "title": "Hitching up: drawbar, PTO and towing weights",
        "category": "vehicle-implements",
        "summary": "The moment the drawbar pin goes in, the tractor and the implement become one machine. Getting the hitch right is safety, not fussy.",
        "author": "Tomasz",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "drawbar,pto,hitch,towing,safety,weights",
        "body": """Most towing accidents come from a hitch that was not properly made up, or from a load that was too high or too far back.

## The drawbar

- **Use the right hole.** A drawbar with several holes is adjustable so the implement can be balanced. The right hole is the one that puts the weight where the tongue weight should be.
- **The pin must be the right size and it must be secured.** A split pin or a R-clip, every time. A drawbar pin with a bent clip comes out at the first bounce.
- **The hitch should sit level.** If the drawbar is nose-down, the load is pulling the tractor down and up. If it is nose-up, the implement can lift the rear of the tractor.
- **Do not grease the pin if it is a splined pin.** Grease collects dirt and grit and then the pin will not pull out on a wet day.

## Ballast and the load on the back

- **The rear of a tractor is lighter than the front.** Hanging a heavy implement on the back unloads the front wheels and makes the steering dangerous.
- **Add front ballast** whenever you put a weight on the back. See [[dtl-500-tension-adjustment]] and [[safe-lifting-tractors]].
- **The rule of thumb:** for every kilo of weight on the back, allow a kilo of ballast on the front.
- **A loader bucket full of earth is worse than a box of weights** because the weight moves with the load.

## The PTO shaft

- **Match the spline.** A 1-3/8 inch shaft will not go into a 1-3/4 spline, and a splined shaft that is forced in will be destroyed.
- **The shaft must be the right length.** The telescoping part should be half engaged at the closest point and must never bottom out when you turn.
- **Guard the shaft.** Every PTO shaft has a plastic or steel guard and a chain. If the guard is missing or the chain is broken, stop and fix it before you turn the engine over.
- **Grease the universal joints** and the telescoping tube. The tube is the one that lets the shaft change length and it is the one that seizes.
- **Before you start the engine,** make sure the implement is in its working position and nobody is standing behind it.

## Towing on the road

- **Check the lights.** Every time.
- **Slow down on the bends.** A trailer that starts to push will push harder.
- **Take corners slowly and leave room.** A trailer cuts the corner.
- **Do not tow with the parking brake on the tractor.** Some tractors have the handbrake locked when you release the clutch, and it will overheat.

## The load

- **Do not exceed the trailer's rating.** It is a braking rating as much as a weight rating.
- **Put the weight over the axle, not behind it.** A load hanging off the back of the trailer is what makes it sway.
- **Strap the load.** A load that can move will move, usually in a braking emergency.

> **Never tow on the three-point linkage.** The linkage is for controlling implements, not for pulling. It can let go without warning.
""",
    },
    {
        "slug": "grain-drill-servicing",
        "title": "Looking after the grain drill",
        "category": "vehicle-implements",
        "summary": "A drill that is calibrated before it goes into the ground sows on time. A drill that is not, sows two rates at once.",
        "author": "Marta, arable",
        "difficulty": "moderate",
        "read_minutes": 6,
        "tags": "drill,seeding,calibration,coulter,fertiliser",
        "body": """The drill is the one machine on the farm that puts the whole year's money into the ground in a day. Ten minutes of checking before you sow is the best return on the farm.

## Before it goes in the ground

- **Check the coulters.** They should all run at the same depth and the same angle. A bent coulter drags a furrow.
- **The discs on the sides of the coulters** scatter the seed sideways into the furrow. If the disc is missing or bent, the seed is dropped on the surface and dries out.
- **Check the seed tubes** are not cracked or blocked. A cracked tube loses seed down the inside of the drill and it shows up as a thin patch in the field.
- **Check the metering rollers** for wear and for a build-up of seed. A worn roller changes the rate without changing the setting.
- **Grease the bearings and the ground wheel spindles.**

## The calibration test

This is the one that matters. Do it with the seed you are actually going to sow.

1. **Put a sheet of paper or a tray under the drill** and roll it forward a measured distance - five turns of the ground wheel is the usual measure.
2. **Collect the seed** that comes out and weigh it.
3. **Compare it with the setting.** The book tells you what a given wheel turn should deliver.
4. **Adjust the rate** and test again until it matches.
5. **Write the setting down** and mark the adjusting handle so the next person gets it right.

Do it again if you change seed, because a small seed and a big seed do not flow the same way. See [[seed-rate-calculator]] for the figures the book quotes.

## Fertilisers

- **Fertiliser is corrosive.** Wash the drill out thoroughly after every use, especially the hopper and the metering rollers. Water plus fertiliser plus steel equals a seized drill.
- **Check the row spacing** against the drill width and the tramlines so the rows line up with the sprayer.
- **Granular fertiliser and seed together** is a combination worth testing on a small strip first. Too much nitrogen down the seed line gives you thin, leggy plants.

## In the field

- **Check the depth on every field.** The first furrow of the day tells you if the drill is set right.
- **Stop and check the coulters** if the field has stones in it.
- **Watch the tramlines.** They are what makes controlled traffic work - see [[soil-compaction]].
- **Do not fill the drill on the headland** with the drill folded. Fill it with the drill down and the hitch attached, where it cannot tip.

## At the end of the season

- **Wash it out and dry it.** Do not leave it with fertiliser in the hopper over the winter.
- **Store it under cover** if you can, on a hard standing, with the coulters off the ground.
- **Grease the wheels** and pull the clutch in.
- **Write down the settings** that worked. That note is worth more than the drill.

> **Never clean the drill out with the seed hopper over your head.** A drill that has been left with damp seed in it will not empty the way you think it will.
""",
    },

    {
        "slug": "ford-tractors-a-century",
        "title": "Ford tractors: a century of farm work in America",
        "category": "vehicles",
        "summary": "From the 9N of 1939 to the last Ford-badged tractors of the 2000s: the models, the changes and what to look for when you buy one.",
        "author": "Dave, top field",
        "difficulty": "easy",
        "read_minutes": 8,
        "tags": "ford,tractor,history,machinery",
        "body": """# Ford tractors: a century of farm work

Ford put the small farm on wheels. The 9N of 1939 brought the three-point hitch and
the PTO to every smallholding in America, and every model since has been a variation
on that idea: simple, strong, and fixable with a spanner.

## The early years
- [[ford-9n]] (1939-1942) - the tractor that started it all
- [[ford-2n]] (1942-1947) - wartime, steel wheels, magneto
- [[ford-8n]] (1947-1952) - the most common small tractor in the country
- [[ford-naa]] (1953-1954) - Golden Jubilee, overhead valve

## The hundred series
- [[ford-600]] and [[ford-800]] (1955-1962) - five-speed gearbox, choice of engines

## The 000 series
- [[ford-2000]], [[ford-4000]] (1962-1965) - early squared styling
- [[ford-6000]] (1961-1968) - Ford's first big diesel

## The 1965-1975 range
- [[ford-3000-65]] - the workhorse of the smallholding
- [[ford-5000-65]] - the classic medium Ford
- [[ford-7000]] - big Ford for big work

## The heavy tractors
- [[ford-8000-row]], [[ford-8600]], [[ford-9600]], [[ford-9700]]

## The TW series
- [[ford-tw10]], [[ford-tw20]], [[ford-tw30]] (1979-1983) - turbo, wet clutch, better cab

## The 10 series
- [[ford-3910]], [[ford-4610]], [[ford-5610]], [[ford-6610]], [[ford-7610]], [[ford-8210]]

## The late models
- [[ford-7840]], [[ford-5110]], [[ford-6610s]], [[ford-7740]], [[ford-8340]]

## Buying a used Ford
Check the hydraulics first: lift a heavy implement and watch for drift. Then the
clutch, the PTO and the brakes. Parts are still available for most models, and the
community notes on each model page list the known weak points.

> **Safety:** never work under a raised implement without the transport lock engaged.
""",
    },
]
