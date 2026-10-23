"""Formulas: physics, chemistry and energy."""

from __future__ import annotations

FORMULAS: list[dict] = [
    # ---------------------------------------------------------------- physics
    {
        "slug": "newtons-second-law",
        "name": "Newton's second law",
        "topic": "physics",
        "expression": "F = m x a",
        "symbols": "F = force (N); m = mass (kg); a = acceleration (m/s2)",
        "units": "newtons (N)",
        "how": "The force needed to move a mass. The tractor pulling a trailer, "
               "the ramp lifting a load, a horse pulling a plough. Double the "
               "mass and you double the force, for the same acceleration.",
        "example": "A 1,500 kg trailer accelerating at 1 m/s2 needs 1,500 N.",
        "tags": "force,mass,acceleration,newton,tractor",
    },
    {
        "slug": "weight-vs-mass",
        "name": "Weight and mass",
        "topic": "physics",
        "expression": "W = m x g   (g = 9.81 m/s2 on earth)",
        "symbols": "W = weight (N); m = mass (kg); g = gravitational "
                   "acceleration",
        "units": "N",
        "how": "Mass is how much there is, weight is how hard it presses. A "
               "sack of fertiliser has the same mass everywhere and a "
               "different weight on the moon. Lifting power is usually quoted "
               "in kilograms, which is really a mass in disguise.",
        "example": "A 200 kg sack weighs about 1,962 N.",
        "tags": "weight,mass,gravity,lifting",
    },
    {
        "slug": "work-done",
        "name": "Work done",
        "topic": "physics",
        "expression": "W = F x d",
        "symbols": "W = work (J); F = force applied (N); d = distance moved "
                   "along the force (m)",
        "units": "joules (J)",
        "how": "Work only happens when the force is in the direction of the "
               "movement. Lifting a load 2 m and pushing a barrow 100 m are "
               "different amounts of work.",
        "example": "Pushing with 100 N over 50 m = 5,000 J.",
        "tags": "work,energy,force,distance",
    },
    {
        "slug": "power-mechanical",
        "name": "Power",
        "topic": "physics",
        "expression": "P = W / t   (or P = F x v)",
        "symbols": "P = power (W); W = work (J); t = time (s); v = speed (m/s)",
        "units": "watts (W), kilowatts (kW), horsepower (hp)",
        "how": "How fast work gets done. 1 hp = 746 W, so a 50 hp engine is "
               "37 kW. A machine doing the same work in half the time has "
               "twice the power.",
        "example": "37 kW (50 hp) = 74,000 W.",
        "tags": "power,watts,horsepower,engine,work",
    },
    {
        "slug": "kinetic-energy",
        "name": "Kinetic energy",
        "topic": "physics",
        "expression": "E = (1/2) x m x v2",
        "symbols": "E = kinetic energy (J); m = mass (kg); v = speed (m/s)",
        "units": "joules (J)",
        "how": "The energy of something that is moving. Double the speed and "
               "you have four times the energy, which is why a braking problem "
               "gets serious very quickly above a certain speed.",
        "example": "A 1,200 kg car at 10 m/s carries 60,000 J.",
        "tags": "energy,motion,braking,collision",
    },
    {
        "slug": "potential-energy",
        "name": "Gravitational potential energy",
        "topic": "physics",
        "expression": "E = m x g x h",
        "symbols": "E = energy (J); m = mass (kg); g = 9.81; h = height (m)",
        "units": "joules (J)",
        "how": "The energy stored by lifting something. It is why a raised "
               "bale or a full water tank is dangerous, and why a ramp gains "
               "you the power to lift a load higher.",
        "example": "A 100 kg load lifted 3 m stores 2,943 J.",
        "tags": "energy,height,lifting,potential",
    },
    {
        "slug": "momentum",
        "name": "Momentum and impulse",
        "topic": "physics",
        "expression": "p = m x v ; impulse J = F x t = change in momentum",
        "symbols": "p = momentum (kg m/s); F = force (N); t = time (s)",
        "units": "kg m/s; N s",
        "how": "Why a soft bag of sand and a hard block hit differently at the "
               "same speed, and why you roll with a fall. Doubling the speed "
               "doubles the momentum and quadruples the stopping force.",
        "example": "A 2 kg tool at 5 m/s has 10 kg m/s of momentum.",
        "tags": "momentum,impulse,collision,safety",
    },
    {
        "slug": "friction",
        "name": "Friction",
        "topic": "physics",
        "expression": "F(friction) = mu x N",
        "symbols": "mu = coefficient of friction (steel on steel about 0.6, "
                   "rubber on tarmac about 0.8, oil on steel about 0.1); "
                   "N = normal force pressing the surfaces together",
        "units": "N",
        "how": "Why a ramp needs enough grip, why oil makes a bolt easier to "
               "undo, and why a ladder needs its feet on level ground.",
        "example": "A 500 N ladder on a wet floor with mu = 0.3 slips at "
                   "150 N of sideways push.",
        "tags": "friction,mu,ramp,grip,bolt",
    },
    {
        "slug": "pressure",
        "name": "Pressure and pressure from depth",
        "topic": "physics",
        "expression": "P = F / A ; P = rho x g x h",
        "symbols": "P = pressure (Pa); F = force (N); A = area (m2); rho = "
                   "density (kg/m3); h = depth (m)",
        "units": "pascal (Pa), bar, psi",
        "how": "Why a spade is sharp and a boot is not, and why a dam holds "
               "back a growing force. A 1 m column of water pushes 9,810 Pa "
               "on every square metre at the bottom.",
        "example": "A 500 N boot on 0.02 m2 of sole = 25,000 Pa.",
        "tags": "pressure,depth,dam,spade,pascal",
    },
    {
        "slug": "hydraulic-pressure",
        "name": "Pascal's principle and hydraulic rams",
        "topic": "physics",
        "expression": "P is the same everywhere, so F1 / A1 = F2 / A2",
        "symbols": "A1 = small piston area; A2 = large piston area; F1, F2 = "
                   "the forces on them",
        "units": "N",
        "how": "The jack, the brake press, the loader bucket and the post "
               "hole rammers. A 10 cm piston moved with 100 N will lift 1,000 "
               "kg on a 1 m piston.",
        "example": "A 100 N push on a 10 cm2 piston lifts 1,000 kg on a 1,000 "
                   "cm2 piston.",
        "tags": "hydraulic,jack,brake press,ram,loader",
    },
    {
        "slug": "buoyancy",
        "name": "Buoyancy",
        "topic": "physics",
        "expression": "F(b) = rho(fluid) x V x g",
        "symbols": "rho = density of the fluid (1,000 kg/m3 for water); "
                   "V = submerged volume (m3)",
        "units": "N",
        "how": "Why a boat floats, why a tractor wheel floats in mud, and why "
               "you cannot lift a submerged post out of a hole by pulling on "
               "it.",
        "example": "A 1 m3 of wood in water gets 9,810 N of lift, which is "
                   "1,000 kg of weight.",
        "tags": "buoyancy,floating,water,displacement",
    },
    {
        "slug": "torque",
        "name": "Torque (moment of a force)",
        "topic": "physics",
        "expression": "T = F x r",
        "symbols": "T = torque (N m); F = force applied (N); r = lever arm, the "
                   "distance from the pivot to the line of the force (m)",
        "units": "N m",
        "how": "The whole of the spanner, the jack, the pump handle and the "
               "gate hinge. Torque depends on where you put your hand, not on "
               "how hard you pull. A 100 N push at 0.3 m gives 30 N m.",
        "example": "A 300 N pull on a 0.4 m spanner gives 120 N m.",
        "tags": "torque,moment,spanner,lever,pivot",
    },
    {
        "slug": "mechanical-advantage",
        "name": "Mechanical advantage and velocity ratio",
        "topic": "physics",
        "expression": "MA = load / effort ; VR = distance moved by effort / "
                      "distance moved by load ; efficiency % = (MA / VR) x 100",
        "symbols": "load = the force you are overcoming; effort = the force you "
                   "apply",
        "units": "dimensionless, %",
        "how": "A lever, a block and tackle, a ramp, a screw jack. You trade "
               "distance for force, and no machine beats 100% efficiency. A "
               "ramp 4 m long and 1 m high has a theoretical advantage of 4.",
        "example": "A block and tackle with 4 supporting parts needs a quarter "
                   "of the force.",
        "tags": "advantage,lever,pulley,ramp,efficiency",
    },
    {
        "slug": "inclined-plane",
        "name": "The inclined plane and the screw",
        "topic": "physics",
        "expression": "MA = length of slope / height ; "
                      "MA of a screw = (2 x pi x r) / pitch",
        "symbols": "r = radius of the handle; pitch = distance turned per "
                   "revolution",
        "units": "dimensionless",
        "how": "Ramps, loading ramps, the screw jack, the post hole auger and "
               "the cider press. Work in always equals work out, so a gentle "
               "ramp just means more walking.",
        "example": "A 2 m ramp at 500 mm high gives an advantage of 4.",
        "tags": "ramp,screw,jack,press,advantage",
    },
    {
        "slug": "centre-of-gravity",
        "name": "Centre of gravity",
        "topic": "physics",
        "expression": "the balance point is where the sum of (mass x distance) "
                      "either side is equal",
        "symbols": "sum of moments about any point = 0 at the balance point",
        "units": "N m",
        "how": "Loading a trailer, tipping a wheelbarrow, setting a ladder, and "
               "why a tall stack of bales topples. Keep the load low and "
               "forward.",
        "example": "Half the load over the axle and half behind it puts the "
                   "balance point over the axle.",
        "tags": "centre of gravity,balance,trailer,ladder,tipping",
    },
    {
        "slug": "stress-strain-modulus",
        "name": "Stress, strain and Young's modulus",
        "topic": "physics",
        "expression": "stress sigma = F / A ; strain epsilon = dL / L ; "
                      "E = sigma / epsilon",
        "symbols": "E = Young's modulus, a material constant (steel about "
                   "200 GPa, oak about 11 GPa, concrete about 30 GPa)",
        "units": "Pa",
        "how": "The stiffness of a material. Steel is nearly twenty times "
               "stiffer than oak, which is why a steel frame sags less and "
               "lasts longer than a timber one of the same size.",
        "example": "A 10 mm steel bar pulled by 5 kN across 78.5 mm2 = 64 MPa.",
        "tags": "stress,strain,youngs modulus,materials,steel",
    },
    {
        "slug": "factor-of-safety",
        "name": "Factor of safety",
        "topic": "physics",
        "expression": "FoS = strength of the material / working stress",
        "symbols": "a trailer hoop might be designed for 4 times the working "
                   "load; farm machinery often uses 2 to 3",
        "units": "dimensionless",
        "how": "How much more than the job the part can take. Check it when "
               "you weld something load bearing - a gate bracket or a trailer "
               "chassis - and never design a lifting point yourself.",
        "example": "A bracket with a 20 kN failure load used for 5 kN has a "
                   "factor of safety of 4.",
        "tags": "safety,factor,load,welding,design",
    },
    {
        "slug": "beam-deflection",
        "name": "Beam deflection",
        "topic": "physics",
        "expression": "delta = (5 x w x L4) / (384 x E x I)  for a simply "
                      "supported beam with a central load",
        "symbols": "w = load per unit length; L = span; E = Young's modulus; "
                   "I = second moment of area = (b x h3) / 12",
        "units": "metres",
        "how": "Why a fence rail sags, why a steel beam needs to be deep rather "
               "than wide, and why a long trailer bed needs cross members. "
               "Depth beats width every time.",
        "example": "Doubling the depth of a beam reduces its sag by 16 times.",
        "tags": "beam,deflection,sag,beam,joist,trailer bed",
    },
    {
        "slug": "gear-ratio",
        "name": "Gear ratio",
        "topic": "physics",
        "expression": "ratio = teeth on driven gear / teeth on driving gear ; "
                      "speed out = speed in / ratio ; torque out = torque in x "
                      "ratio",
        "symbols": "ratio = driven teeth / driving teeth; speed out = speed "
                   "in / ratio; torque out = torque in x ratio",
        "units": "dimensionless",
        "how": "For a gearbox, a quad final drive, a mower gearbox or a "
               "winch. A 3:1 reduction triples the torque and drops the speed "
               "to a third. The power stays the same, less the losses.",
        "example": "A 12-tooth pinion driving a 36-tooth gear is 3:1.",
        "tags": "gear,ratio,box,torque,speed",
    },
    {
        "slug": "pulley-mechanics",
        "name": "Pulleys and block and tackle",
        "topic": "physics",
        "expression": "MA = the number of rope parts supporting the load",
        "symbols": "each part of the rope that carries the load counts as one",
        "units": "dimensionless",
        "how": "Count the rope, not the pulleys. A block and tackle with the "
               "load on a four-part reeve has an advantage of about 4, less "
               "the friction in every sheave.",
        "example": "A four-part tackle lifts 400 kg with a 110 kg pull.",
        "tags": "pulley,tackle,winch,lifting,ropes",
    },
    {
        "slug": "belt-length",
        "name": "Belt length",
        "topic": "physics",
        "expression": "L = 2C + (pi / 2)(D + d) + ((D - d)2) / (4C)",
        "symbols": "C = centre distance; D = large pulley diameter; "
                   "d = small pulley diameter; L = belt length",
        "units": "mm",
        "how": "For a drive belt on a tractor, a mower, a compressor or a "
               "bandsaw. Measure the old belt and copy it, or use the formula "
               "for a different pulley set.",
        "example": "A 300 mm and a 100 mm pulley at 500 mm centres needs about "
                   "2,110 mm of belt.",
        "tags": "belt,pulley,drive,length,replacement",
    },
    {
        "slug": "belt-and-shaft-speed",
        "name": "Rotational speed and belt speed",
        "topic": "physics",
        "expression": "N = rpm ; angular speed omega = 2 x pi x N / 60 ; "
                      "belt speed v = pi x D x N / 60",
        "symbols": "N = revolutions per minute; D = pulley diameter (m)",
        "units": "rpm, rad/s, m/s",
        "how": "To work out a pulley size for a different speed, and to check "
               "whether a driven machine is running at the speed it was "
               "designed for.",
        "example": "A 200 mm pulley at 1,400 rpm gives a belt speed of 14.7 m/s.",
        "tags": "rpm,speed,belt,pulley,angular",
    },
    {
        "slug": "heat-capacity",
        "name": "Specific heat capacity and heating",
        "topic": "physics",
        "expression": "Q = m x c x dT",
        "symbols": "Q = heat (J); m = mass (kg); c = specific heat (J/kg K): "
                   "water 4,180, steel 450, air 1,000; dT = temperature "
                   "change (K)",
        "units": "joules (J), kilojoules (kJ)",
        "how": "How much fuel or electricity a heater needs. Water needs far "
               "more energy per kilo than steel, which is why a hot water "
               "cylinder takes so long.",
        "example": "Heating 200 L of water by 60 degrees takes 50,160 kJ, "
                   "which is about 3.8 kWh.",
        "tags": "heat,specific heat,water,heating,energy",
    },
    {
        "slug": "thermal-expansion",
        "name": "Thermal expansion",
        "topic": "physics",
        "expression": "dL = alpha x L x dT",
        "symbols": "alpha = expansion coefficient (steel 12 x 10(-6) per "
                   "degree C, concrete about 10 x 10(-6), oak 3 x 10(-6)); "
                   "L = original length; dT = temperature change",
        "units": "metres",
        "how": "Why a long fence rail buckles in a heatwave, why a steel "
               "tank needs a sliding bearing, and why a concrete slab needs "
               "expansion joints.",
        "example": "A 10 m steel rail expands 1.2 mm for every 10 degrees C.",
        "tags": "expansion,heat,steel,concrete,fence",
    },
    {
        "slug": "heat-loss-through-walls",
        "name": "Heat loss through a wall or roof",
        "topic": "physics",
        "expression": "Q = U x A x dT x t",
        "symbols": "U = heat transfer coefficient (W/m2K): insulated wall 0.25, "
                   "brick wall 1.8, single glazing 5.7, double 2.8; A = area "
                   "(m2); dT = inside minus outside (K); t = time (s)",
        "units": "joules (J)",
        "how": "For a shed, a polytunnel, a cold room or a house. Insulation "
               "works by lowering U, and a door left open works by raising "
               "it again every time.",
        "example": "A 30 m2 shed wall with U = 2.5 and 10 K of difference "
                   "loses 750 W.",
        "tags": "insulation,heat loss,shed,u value,polytunnel",
    },
    {
        "slug": "density-specific-gravity",
        "name": "Density and specific gravity",
        "topic": "physics",
        "expression": "rho = m / V ; specific gravity = density / density of "
                      "water",
        "symbols": "rho = mass / volume; specific gravity = density of the "
                   "material / density of water (1,000 kg/m3)",
        "units": "kg/m3, kg/litre",
        "how": "Converts a volume of something into a weight. Water is 1 kg "
               "per litre. Milk is about 1.03, oil 0.92, honey 1.42, "
               "fertiliser 1.1, wheat 0.75, chopped straw 0.25.",
        "example": "A 200 litre drum of fertiliser at 1.1 kg/litre holds "
                   "220 kg.",
        "tags": "density,specific gravity,volume,weight,liquid",
    },
    {
        "slug": "wave-speed",
        "name": "Wave speed, frequency and wavelength",
        "topic": "physics",
        "expression": "v = f x lambda",
        "symbols": "v = speed (m/s); f = frequency (Hz); lambda = wavelength (m)",
        "units": "m/s, Hz, m",
        "how": "Sound, water, light and radio. Also the drum length of a pipe "
               "organ and the spacing of ripples on a pond.",
        "example": "Sound at 340 m/s at 170 Hz has a wavelength of 2 m.",
        "tags": "wave,frequency,wavelength,sound,light",
    },
    {
        "slug": "snells-law",
        "name": "Snell's law (refraction)",
        "topic": "physics",
        "expression": "n1 x sin(theta1) = n2 x sin(theta2)",
        "symbols": "n = refractive index; theta = angle from the normal",
        "units": "dimensionless",
        "how": "Why a stick looks bent in a pond, why a greenhouse bends the "
               "light, and how a lens focuses.",
        "example": "Light going from air into water bends towards the normal "
                   "because water has the higher index.",
        "tags": "refraction,light,water,stick,lens",
    },

    # -------------------------------------------------------------- chemistry
    {
        "slug": "moles",
        "name": "Moles and molar mass",
        "topic": "chemistry",
        "expression": "n = m / M",
        "symbols": "n = moles; m = mass (g); M = molar mass (g/mol) from the "
                   "periodic table",
        "units": "mol",
        "how": "The bridge between grams and reactions. Every recipe that uses "
               "chemicals is really counting molecules.",
        "example": "36 g of water is 2 moles, because H2O is 18 g/mol.",
        "tags": "moles,molar,mass,chemistry",
    },
    {
        "slug": "molarity",
        "name": "Molarity",
        "topic": "chemistry",
        "expression": "c = n / V",
        "symbols": "c = concentration (mol/L); n = moles; V = volume in litres",
        "units": "mol/L",
        "how": "The standard way to say how strong a solution is. A 1 mol/L "
               "solution of sodium hydroxide is 40 g of it in a litre of water.",
        "example": "50 g of NaOH (40 g/mol) in 2 L = 0.625 mol/L.",
        "tags": "molarity,concentration,solution,moles",
    },
    {
        "slug": "dilution",
        "name": "Dilution",
        "topic": "chemistry",
        "expression": "c1 x V1 = c2 x V2",
        "symbols": "c1, V1 = the stock solution; c2, V2 = what you want to make",
        "units": "mol/L and litres",
        "how": "Every time you mix a concentrate with water, for a spray, a "
               "disinfectant or a test solution. Always add the concentrate to "
               "the water, never the other way round.",
        "example": "50 mL of 5 mol/L acid made up to 500 mL = 0.5 mol/L.",
        "tags": "dilution,concentration,mixturing,spray,acid",
    },
    {
        "slug": "ph",
        "name": "pH",
        "topic": "chemistry",
        "expression": "pH = -log10 of hydrogen ion concentration",
        "symbols": "each whole pH step is a tenfold change in acidity",
        "units": "pH units",
        "how": "Soil, water, antacids and preserves. A change of one unit is "
               "ten times more or less acid, which is why a small pH change "
               "matters so much. See [[soil-ph-and-lime]].",
        "example": "pH 6 is ten times more acid than pH 7.",
        "tags": "ph,acidity,soil,water,preserving",
    },
    {
        "slug": "ph-alkalinity",
        "name": "pH, pOH and the pH scale",
        "topic": "chemistry",
        "expression": "pH + pOH = 14 (at 25 C) ; pH = 14 - pOH",
        "symbols": "pOH = -log10 of hydroxide ion concentration",
        "units": "pH units",
        "how": "For checking that a caustic solution is strong enough, and for "
               "understanding why a wash and a rinse need different strengths.",
        "example": "A solution at pH 12 has pOH 2.",
        "tags": "ph,poh,alkali,caustic,cleaning",
    },
    {
        "slug": "percentage-concentration",
        "name": "Percentage concentration",
        "topic": "chemistry",
        "expression": "% (w/w) = (mass of solute / mass of solution) x 100 ; "
                      "% (v/v) = (volume of solute / volume of solution) x 100",
        "symbols": "solution = solute plus solvent",
        "units": "%",
        "how": "For a 2% milk replacer mix, a 1% iodine solution, a 5% "
               "bleach mix or a salt brine. Note that the denominator is the "
               "solution, not the water.",
        "example": "25 g of powder in 1 litre of water is about 2.4% w/v.",
        "tags": "concentration,percentage,brine,mix,replacer",
    },
    {
        "slug": "ppm",
        "name": "Parts per million",
        "topic": "chemistry",
        "expression": "ppm = mg per kg (or mg per litre for dilute solutions)",
        "symbols": "1% = 10,000 ppm; 1 ppm = 1 mg per kg",
        "units": "ppm, mg/kg",
        "how": "For trace elements in soil and feed, nitrate in water, and "
               "anything described as 'trace'. A soil test of 30 ppm copper is "
               "very different from 30 percent.",
        "example": "1 g per tonne = 1 ppm.",
        "tags": "ppm,trace,soil,water,analysis",
    },
    {
        "slug": "stoichiometry",
        "name": "Stoichiometry from a balanced equation",
        "topic": "chemistry",
        "expression": "moles of product = moles of reactant x the ratio of "
                      "coefficients",
        "symbols": "read the coefficients off the balanced equation",
        "units": "mol, g",
        "how": "For making a solution of a known strength, for a lime "
               "neutralisation calculation, and for anything where the "
               "reaction has to be right rather than roughly right.",
        "example": "CaCO3 + 2HCl gives CaCl2, so 1 mole of chalk needs 2 moles "
                   "of acid.",
        "tags": "stoichiometry,reaction,balanced equation,chemistry",
    },
    {
        "slug": "percent-yield",
        "name": "Percentage yield",
        "topic": "chemistry",
        "expression": "yield % = (actual amount / theoretical amount) x 100",
        "symbols": "theoretical = what the equation says you should get; "
                   "actual = what you ended up with",
        "units": "%",
        "how": "How well a process actually ran. A lime neutralisation that "
               "only reaches 80% means you need more lime than the label says.",
        "example": "You need 50 kg of chalk and get 41 kg of product = 82% "
                   "yield.",
        "tags": "yield,efficiency,lime,reaction",
    },
    {
        "slug": "ideal-gas-law",
        "name": "Ideal gas law",
        "topic": "chemistry",
        "expression": "P x V = n x R x T",
        "symbols": "P = pressure (Pa); V = volume (m3); n = moles; R = 8.314 "
                   "J/mol K; T = temperature (K)",
        "units": "Pa m3",
        "how": "The rule behind a pressure cooker, a tyre, a gas cylinder and a "
               "fermenting barrel. Pressure rises with temperature and with "
               "the amount of gas, and falls as the volume grows.",
        "example": "A 20 L bottle at 20 C and 2 bar holds roughly 0.8 moles.",
        "tags": "gas,pressure,cooker,cylinder,temperature",
    },
    {
        "slug": "gas-laws",
        "name": "Boyle's, Charles's and Gay-Lussac's laws",
        "topic": "chemistry",
        "expression": "Boyle: P x V = constant ; Charles: V / T = constant ; "
                      "Gay-Lussac: P / T = constant",
        "symbols": "T must be in kelvin (C + 273)",
        "units": "varies",
        "how": "Each one holds the other two constant. A cold bottle warms in "
               "the sun and the pressure goes up, which is why a bottle left "
               "in a hot shed can go off.",
        "example": "Gas at 10 C in a bottle warms to 30 C and its pressure "
                   "rises by about 7%.",
        "tags": "gas,boyle,charles,pressure,temperature",
    },
    {
        "slug": "avogadros-law",
        "name": "Avogadro's law",
        "topic": "chemistry",
        "expression": "V is proportional to n at constant temperature and "
                      "pressure",
        "symbols": "equal volumes of gas at the same temperature and pressure "
                   "contain equal numbers of molecules",
        "units": "varies",
        "how": "The rule that lets you scale up a gas reaction - a bottle of "
               "gas and a cylinder of gas behave the same way.",
        "example": "Double the moles in a fixed vessel and you double the "
                   "pressure.",
        "tags": "gas,avogadro,moles,volume",
    },
    {
        "slug": "law-of-conservation-of-mass",
        "name": "Law of conservation of mass",
        "topic": "chemistry",
        "expression": "mass of reactants = mass of products",
        "symbols": "in a closed system, nothing is created or destroyed",
        "units": "g, kg",
        "how": "The reason a sealed compost bin gains mass (it gains the "
               "carbon dioxide that leaves) and the reason a fire seems to "
               "lose mass - the carbon dioxide and water vapour have left "
               "the shed.",
        "example": "A burning log loses mass as gases escape, not because "
                   "matter vanished.",
        "tags": "mass,conservation,compost,fire",
    },
    {
        "slug": "enthalpy-change",
        "name": "Enthalpy change of a reaction",
        "topic": "chemistry",
        "expression": "dH = sum of the enthalpy of the products - sum of the "
                      "enthalpy of the reactants",
        "symbols": "negative means exothermic (gives out heat), positive means "
                   "endothermic (takes heat in)",
        "units": "kJ/mol",
        "how": "Why a compost heap gets hot, why a lime slurry in a slurry tank "
               "warms, and why a soaking cold feed makes the animal cold.",
        "example": "Fermenting fruit releases heat; the vat warms by a few "
                   "degrees.",
        "tags": "enthalpy,heat,reaction,compost,lime",
    },
    {
        "slug": "buffer-ph",
        "name": "Buffer pH (Henderson-Hasselbalch)",
        "topic": "chemistry",
        "expression": "pH = pKa + log10 of (base / acid)",
        "symbols": "pKa = the pH at which the acid is half turned into base",
        "units": "pH units",
        "how": "How a milk, a must, or a soil stays at a steady pH while "
               "things are added to it. A brine is a buffer, and so is the "
               "lime in a soil.",
        "example": "A phosphate buffer with pKa 6.8 and equal parts has a "
                   "pH of 6.8.",
        "tags": "buffer,ph,milk,brine,soil",
    },
    {
        "slug": "freezing-point-depression",
        "name": "Freezing point depression",
        "topic": "chemistry",
        "expression": "dT(freeze) = i x Kf x m",
        "symbols": "i = the number of particles the solute splits into; Kf = "
                   "the freezing constant of the solvent (water 1.86 K per "
                   "mol/kg); m = molality in mol per kg of solvent",
        "units": "degrees C",
        "how": "Why salt melts ice on a road, why a brine freezes below zero, "
               "and why a freezer with a brine tank is colder than one with "
               "water.",
        "example": "A 10% salt brine freezes at about -6 C.",
        "tags": "freezing,brine,salt,ice,antifreeze",
    },
    {
        "slug": "water-hardness",
        "name": "Water hardness",
        "topic": "chemistry",
        "expression": "hardness (mg/L as CaCO3) = (mg/L of Ca x 2.5) + "
                      "(mg/L of Mg x 4.1)",
        "symbols": "hard water is over 200 mg/L; very hard is over 400 mg/L",
        "units": "mg/L",
        "how": "To decide whether a borehole needs a softener, and why soap "
               "will not lather and the kettle furs up.",
        "example": "40 mg/L of calcium gives 100 mg/L of hardness.",
        "tags": "water,hardness,softener,borehole,kettle",
    },
    {
        "slug": "titration",
        "name": "Titration",
        "topic": "chemistry",
        "expression": "c1 x V1 = c2 x V2",
        "symbols": "c1, V1 = the solution in the burette; c2, V2 = the flask",
        "units": "mol/L, mL",
        "how": "For working out the strength of a bought solution, and for "
               "checking a soil or water test against the method. The end point "
               "is the colour change, so get it right before you read the "
               "burette.",
        "example": "25 mL of unknown acid neutralised by 20 mL of 0.1 mol/L "
                   "alkali is 0.08 mol/L.",
        "tags": "titration,acid,alkali,neutralisation,test",
    },

    # ----------------------------------------------------------------- energy
    {
        "slug": "ohms-law",
        "name": "Ohm's law",
        "topic": "energy",
        "expression": "V = I x R   (so I = V / R and R = V / I)",
        "symbols": "V = volts; I = current (A); R = resistance (ohms)",
        "units": "V, A, ohm",
        "how": "The starting point for any electrical fault finding. If the "
               "voltage is right and the lamp is dim, the current is low, so "
               "the resistance is too high. See [[electrical-fault-finding]].",
        "example": "12 V across a 6 ohm lamp draws 2 A.",
        "tags": "electricity,ohm,voltage,current,resistance",
    },
    {
        "slug": "electrical-power",
        "name": "Electrical power",
        "topic": "energy",
        "expression": "P = V x I = I2 x R = V2 / R",
        "symbols": "P = power (W); the other two forms are handy when you know "
                   "the resistance or the voltage instead of the current",
        "units": "watts (W), kilowatts (kW)",
        "how": "For working out what a heater, a motor or a charger really "
               "uses. 1 hp is about 746 W, so a 1.5 kW heater is 2 hp of heat "
               "going into the room.",
        "example": "A 2,300 W kettle on 230 V draws 10 A.",
        "tags": "power,watts,electricity,heater,motor",
    },
    {
        "slug": "electrical-energy",
        "name": "Electrical energy and the kilowatt hour",
        "topic": "energy",
        "expression": "kWh = (kW x hours) ; cost = kWh x price per kWh",
        "symbols": "1 kWh = 3.6 megajoules",
        "units": "kWh, currency",
        "how": "What the meter on the wall measures. Everything electric in "
               "the farm is counted in kilowatt hours, and a 1,000 W heater "
               "running for ten hours uses 10 kWh.",
        "example": "A 2 kW heater for 5 hours a day costs 10 kWh a day.",
        "tags": "energy,kwh,meter,electricity,cost",
    },
    {
        "slug": "resistance-combinations",
        "name": "Resistance in series and parallel",
        "topic": "energy",
        "expression": "series: R = R1 + R2 + R3 ; "
                      "parallel: 1/R = 1/R1 + 1/R2 + 1/R3",
        "symbols": "in parallel the reciprocal of the total is the sum of the "
                   "reciprocals of the parts",
        "units": "ohm",
        "how": "For a string of lights, a trailer board, or when you are "
               "adding a second battery. Parallel adds power and series adds "
               "voltage.",
        "example": "Two 6 ohm bulbs in series give 12 ohm; in parallel they "
                   "give 3 ohm.",
        "tags": "resistance,series,parallel,lights,battery",
    },
    {
        "slug": "battery-capacity-and-charging",
        "name": "Battery capacity and charging time",
        "topic": "energy",
        "expression": "stored energy (Wh) = voltage x amp-hours ; "
                      "charging time (h) = amp-hours / charger current (A)",
        "symbols": "a 12 V 100 Ah battery holds 1,200 Wh",
        "units": "Wh, Ah, hours",
        "how": "For choosing a battery, and for working out how long a "
               "generator or a mains charger will take. A 12 V 100 Ah battery "
               "on a 10 A charger is about 10 hours, less the losses.",
        "example": "A 12 V 100 Ah battery charged at 10 A takes about 11 "
                   "hours.",
        "tags": "battery,charging,amp,ah,watt,generator",
    },
    {
        "slug": "solar-array-output",
        "name": "Solar array output",
        "topic": "energy",
        "expression": "P = irradiance x area x efficiency",
        "symbols": "irradiance in W/m2 - about 1,000 at midday on a clear "
                   "summer day, 200 on an overcast winter day; efficiency "
                   "typically 0.15 to 0.22 for a panel",
        "units": "watts (W)",
        "how": "For sizing a solar array for the electric fence, the lights or "
               "a small freezer. Multiply the panel area by the irradiance "
               "you can count on, not the best case.",
        "example": "2 m2 of panel at 800 W/m2 and 20% gives 320 W.",
        "tags": "solar,panel,irradiance,electric fence,power",
    },
    {
        "slug": "heat-pump-cop",
        "name": "Heat pump coefficient of performance",
        "topic": "energy",
        "expression": "COP = heat output (W) / electrical input (W)",
        "symbols": "a good heat pump has a COP of 3 to 4; an electric heater "
                   "has a COP of 1",
        "units": "dimensionless",
        "how": "How many units of heat you get for each unit of electricity. "
               "A COP of 3.5 means the heat pump heats three and a half times "
               "more than the resistance heater it replaced.",
        "example": "A 500 W heat pump with a COP of 3.5 gives 1,750 W of heat.",
        "tags": "heat pump,cop,efficiency,heating,electricity",
    },
    {
        "slug": "transformer-ratio",
        "name": "Transformer ratio",
        "topic": "energy",
        "expression": "Vs / Vp = Ns / Np",
        "symbols": "V = voltage; N = number of turns; p = primary, s = "
                   "secondary",
        "units": "dimensionless",
        "how": "For a welder, a battery charger, a lamp on a long lead, and "
               "any step-down or step-up. Power is roughly conserved, so a "
               "step-up gives you less current for the same watts.",
        "example": "Stepping 230 V down to 24 V gives about ten times the "
                   "current for the same power.",
        "tags": "transformer,voltage,turns,welder,charger",
    },
    {
        "slug": "three-phase-power",
        "name": "Three-phase power",
        "topic": "energy",
        "expression": "P = root 3 x V x I x power factor",
        "symbols": "root 3 = 1.732; V = line voltage; I = line current; power "
                   "factor typically 0.8 to 0.95",
        "units": "watts (W)",
        "how": "For the three-phase supply to a barn, a grain dryer, a "
               "milking parlour or a welder. The root 3 is the bit people "
               "forget.",
        "example": "415 V at 20 A and a power factor of 0.9 = 12,950 W.",
        "tags": "three phase,power,supply,barn,milking",
    },
]
