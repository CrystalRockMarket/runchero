"""Deep-dive notes for the chainsaw shelf.

These cover the small farm chainsaw from bar and chain to safe felling,
written for someone who fixes their own gear and works alone most days.
"""

from __future__ import annotations

NOTES: list[dict] = [
    {
        "slug": "chainsaw-wont-start",
        "title": "Chainsaw will not start: the five-minute check",
        "category": "vehicle-implements",
        "summary": "Fuel, air, spark, and the choke. Most no-start saws fail on one of the first three, not the coil.",
        "author": "Top field crew",
        "difficulty": "easy",
        "read_minutes": 7,
        "tags": "chainsaw,starting,fuel,carburettor,spark,2-stroke",
        "body": """A saw that will not start usually means one of four things: old fuel, a blocked filter, a flooded engine, or no spark. Work through them in this order.

## 1. Fuel

Old petrol goes stale in as little as thirty days, and stale fuel will not fire. If the saw has stood over winter, drain the tank and fill with fresh 2-stroke mix at the ratio the bar tells you - usually 40:1 or 50:1. Never run straight petrol; it will seize the piston.

## 2. Air

Pull the air filter. If it is soaked in oil or packed with sawdust, wash it in warm soapy water, dry it, and put a few drops of filter oil back on it. A blocked filter makes the saw hard to start and sluggish under load.

## 3. Spark

Remove the plug and earth it against the cylinder. Crank and watch for a fat blue spark. A weak orange spark means the plug or the coil. No spark at all with a dry plug means the switch, the lead, or the points on older saws.

## 4. Flooding

If you have been pulling the cord with the choke on, the cylinder is flooded with petrol. Pull the plug, set the choke to off, hold the throttle wide open, and pull the cord six to ten times to blow the excess fuel out. Fit a clean plug and try again with the choke off until it pops, then one choke click.

> **Safety.** Never start a saw inside a shed or garage. The exhaust is invisible and deadly. Start it outside, on the ground, with the chain brake on.
""",
    },
    {
        "slug": "chainsaw-chain-sharpening",
        "title": "Sharpening a chainsaw chain by hand",
        "category": "vehicle-implements",
        "summary": "A dull chain burns wood and wears you out. File every cutter to the same length and depth, or the saw will pull to one side.",
        "author": "Top field crew",
        "difficulty": "moderate",
        "read_minutes": 8,
        "tags": "chainsaw,chain,file,sharpen,depth gauge,bar",
        "body": """A sharp chain cuts with almost no pressure. If you are forcing the saw into the wood, the chain is dull.

## What you need

A round file that matches the chain pitch, a flat file for the depth gauges, and a file guide that holds the angle. The pitch is stamped on the drive link or the bar - common sizes are 3/8, 0.325, and 0.404.

## File the cutters

1. Clamp the bar in a vice so the chain does not move.
2. Start with the shortest cutter and file every cutter to that same length. File from the inside out, at the angle stamped on the cutter or the guide - usually 25 to 35 degrees.
3. Count the strokes. Give every cutter the same number so they stay even.
4. File only on the push stroke; lifting the file back dulls it.

## Set the depth gauges

The depth gauges (the little hooks in front of each cutter) control how deep the bite is. Use the flat file and the depth-gauge tool so every gauge sits the same height - usually 0.025 inch. If they are too high, the saw grabs and kicks. Too low, and it will not cut.

> **Safety.** Disconnect the spark plug lead before you file, and wear gloves - a freshly filed chain is razor sharp.
""",
    },
    {
        "slug": "chainsaw-bar-and-chain",
        "title": "Bar, chain and oiler: keeping the cut straight",
        "category": "vehicle-implements",
        "summary": "A bent bar, a stretched chain, or a dry oiler will ruin a good saw in an afternoon. Check them before every tank of fuel.",
        "author": "Top field crew",
        "difficulty": "easy",
        "read_minutes": 6,
        "tags": "chainsaw,bar,chain,oiler,tension,lube",
        "body": """The bar and chain do the work, and the oiler keeps them alive. Three things kill a bar: running dry, cutting into the ground, and letting the chain stretch.

## Chain tension

A chain that is too loose will jump off the bar. Too tight, and it will burn the bar and the clutch. Pull the chain away from the bar at the middle - it should snap back and the drive links should just barely stay in the bar groove. Adjust it cold; a hot chain is loose when it cools.

## Bar wear

Run your finger along the bar rails. If they are burred or the bar is worn thin on one side, the cut will wander. Dress the rails with a flat file, and flip the bar over from time to time so both sides wear evenly.

## Oiler

Start the saw and hold the tip over a piece of white cardboard. You should see a thin line of oil appear within a few seconds. If nothing comes out, the oiler port is blocked or the oil line is cracked. Clean the port with a fine wire and refill with bar oil - never use old engine oil, it is too thin and flings off.

> **Safety.** A chain that has hit dirt or a nail is trash. Sharpening will not fix a cracked or bent cutter; replace the chain.
""",
    },
    {
        "slug": "chainsaw-safe-felling",
        "title": "Safe felling: notch, back cut and escape",
        "category": "vehicle-implements",
        "summary": "Felling a tree is the most dangerous job on the farm. Plan the fall, cut the notch, make the back cut, and walk away on the escape route.",
        "author": "Top field crew",
        "difficulty": "moderate",
        "read_minutes": 9,
        "tags": "chainsaw,felling,notch,back cut,escape route,safety",
        "body": """Never fell a tree alone if you can help it, and never stand behind the trunk when it starts to move. A falling tree does not always fall where you want it.

## Plan the fall

Look at the lean, the wind, and the weight of the crown. Pick a clear fall direction with nothing in the way - no fences, power lines, or sheds. Clear your escape route at a forty-five degree angle from the fall line, ten feet back from the stump.

## The notch

Cut the notch on the fall side. It should be about one-quarter of the trunk diameter and open at forty-five to sixty degrees. The notch tells the tree which way to go.

## The back cut

Make the back cut on the opposite side, slightly above the bottom of the notch. Leave a hinge of uncut wood - about one-tenth of the diameter - so the tree falls controlled instead of splitting or barber-chairing.

As soon as the tree starts to move, shut the saw off, set the chain brake, and walk away down your escape route. Watch the top, not the base - branches can snap off and fly.

> **Safety.** Wear a helmet, eye protection, hearing protection, gloves, and chainsaw chaps. A chipped tooth or a kicked-back bar will end your day fast. Do not cut above shoulder height, and never cut with the tip of the bar - that is where kickback comes from.
""",
    },
]



