"""Formulas: measurement, maths, money, data and health.

Every entry is a plain dict so the seeder can drop it straight into the
database and the formulas page can filter it by topic.

    slug, name, topic, expression, symbols, units, how, example, tags
"""

from __future__ import annotations

FORMULAS: list[dict] = [
    # ---------------------------------------------------------------- measure
    {
        "slug": "area-of-a-rectangle",
        "name": "Area of a rectangle",
        "topic": "measurement",
        "expression": "A = L x W",
        "symbols": "A = area; L = length; W = width",
        "units": "m2, hectares, acres",
        "how": "The workhorse of farm measurement: field areas, yard areas, "
               "floor areas and the size of a sheet of plywood. Multiply the two "
               "sides, then convert.",
        "example": "A 40 m x 25 m yard = 1,000 m2, which is 0.1 hectare.",
        "tags": "area,rectangle,length,width,field",
    },
    {
        "slug": "area-of-a-circle",
        "name": "Area of a circle",
        "topic": "measurement",
        "expression": "A = pi x r2",
        "symbols": "A = area; pi = 3.14159; r = radius (half the diameter)",
        "units": "m2, cm2, mm2",
        "how": "Used for round tanks, silage pits, feed bins, pipe ends and "
               "round bales. Measure the diameter, halve it for the radius.",
        "example": "A tank of 2 m diameter: r = 1 m, A = 3.14 m2 of base.",
        "tags": "area,circle,tank,round",
    },
    {
        "slug": "area-of-a-triangle",
        "name": "Area of a triangle",
        "topic": "measurement",
        "expression": "A = (b x h) / 2",
        "symbols": "A = area; b = base; h = perpendicular height",
        "units": "m2, cm2",
        "how": "For wedges, gussets, triangular yard patches, roof end bays and "
               "the spread of a spray boom on a slope.",
        "example": "A 10 m base with 4 m of height = 20 m2.",
        "tags": "area,triangle,gusset",
    },
    {
        "slug": "area-of-a-trapezoid",
        "name": "Area of a trapezoid",
        "topic": "measurement",
        "expression": "A = ((a + b) / 2) x h",
        "symbols": "A = area; a = short parallel side; b = long parallel side; "
                   "h = perpendicular height",
        "units": "m2",
        "how": "A field with one square end, a yard that narrows, the cross "
               "section of a ditch bank, a hipped roof panel.",
        "example": "A field 30 m at the top, 50 m at the bottom, 60 m deep = "
                   "2,400 m2.",
        "tags": "area,trapezoid,field",
    },
    {
        "slug": "circumscribed-circle-perimeter",
        "name": "Circumference of a circle",
        "topic": "measurement",
        "expression": "C = 2 x pi x r  (or C = pi x d)",
        "symbols": "C = circumference; r = radius; d = diameter",
        "units": "m, mm, ft",
        "how": "Cutting circles from sheet, sizing a round pen, measuring belt "
               "length round a pulley, the girth of a bale.",
        "example": "A 600 mm disc: C = 1,885 mm, so a 1,885 mm belt fits it.",
        "tags": "circle,circumference,belt",
    },
    {
        "slug": "volume-of-a-box",
        "name": "Volume of a box",
        "topic": "measurement",
        "expression": "V = l x w x h",
        "symbols": "V = volume; l = length; w = width; h = height",
        "units": "m3, litres (1 m3 = 1000 litres)",
        "how": "Trailer load volume, feed bin capacity, water tank volume, "
               "concrete for a footing.",
        "example": "A 3 x 1.5 x 1.2 m trailer = 5.4 m3 = 5,400 litres.",
        "tags": "volume,box,trailer,tank",
    },
    {
        "slug": "volume-of-a-cylinder",
        "name": "Volume of a cylinder",
        "topic": "measurement",
        "expression": "V = pi x r2 x h",
        "symbols": "V = volume; r = radius; h = height (or length)",
        "units": "m3, litres",
        "how": "Round water tanks, silos, drums, milk churns, water troughs and "
               "fuel drums. The single most useful tank calculation there is.",
        "example": "A 1.5 m diameter, 2 m tall tank holds 3,534 litres.",
        "tags": "volume,cylinder,tank,silo,trough",
    },
    {
        "slug": "volume-of-a-cone",
        "name": "Volume of a cone",
        "topic": "measurement",
        "expression": "V = (1/3) x pi x r2 x h",
        "symbols": "V = volume; r = radius; h = perpendicular height",
        "units": "m3, litres",
        "how": "Grain heaps, fertiliser heaps, sand and gravel cones, and conical "
               "feed piles. A third of the cylinder of the same base and height.",
        "example": "A 3 m radius, 2 m high heap of grain = 18.85 m3 = 18,850 kg "
                   "at 750 kg/m3.",
        "tags": "volume,cone,heap,grain,fertiliser",
    },
    {
        "slug": "mass-from-volume-and-density",
        "name": "Mass from volume and density",
        "topic": "measurement",
        "expression": "m = V x rho",
        "symbols": "m = mass; V = volume; rho = density",
        "units": "kg, tonnes; m3; kg/m3 or kg/litre",
        "how": "Turn a heap into tonnes. Water is 1 kg per litre. Wheat is about "
               "0.75 kg per litre, fertiliser about 1.1, soil about 1.3-1.5, "
               "sand about 1.6, concrete about 2.4.",
        "example": "A 10 m3 heap of wheat at 750 kg/m3 = 7.5 tonnes.",
        "tags": "mass,density,volume,tonnage,weight",
    },
    {
        "slug": "speed-distance-time",
        "name": "Speed from distance and time",
        "topic": "measurement",
        "expression": "v = d / t",
        "symbols": "v = speed; d = distance; t = time",
        "units": "km/h, m/s, mph",
        "how": "Work out how fast you are actually travelling. A hectare in a "
               "day, a round of the field in an afternoon, or whether a load of "
               "sheep will get to the market in time.",
        "example": "12 km in 3 hours = 4 km/h.",
        "tags": "speed,distance,time",
    },
    {
        "slug": "fuel-consumption",
        "name": "Fuel consumption (litres per 100 km)",
        "topic": "measurement",
        "expression": "L/100km = (fuel used / distance) x 100",
        "symbols": "fuel used in litres; distance in km",
        "units": "L/100km, or litres per hour",
        "how": "The standard way to compare machines. Fill the tank, work all "
               "day, refill and measure. Divide litres by kilometres and "
               "multiply by 100.",
        "example": "25 litres over 10 km = 25 L/100km.",
        "tags": "fuel,diesel,consumption,tractor",
    },
    {
        "slug": "fuel-cost-per-hour",
        "name": "Fuel cost per hour",
        "topic": "measurement",
        "expression": "cost/hour = (litres per hour x price per litre)",
        "symbols": "litres per hour from the engine spec or a tank test; "
                   "price per litre from the pump",
        "units": "currency per hour",
        "how": "The number that decides whether a job is worth doing. Measure "
               "litres per hour by running the machine for an hour with a full "
               "tank and a full tank afterwards.",
        "example": "18 L/h at 1.60 per litre = 28.80 per hour.",
        "tags": "fuel,cost,machine,rate",
    },
    {
        "slug": "mm-to-inches",
        "name": "Millimetres to inches",
        "topic": "measurement",
        "expression": "inches = mm / 25.4",
        "symbols": "mm = millimetres; 25.4 = exact mm in one inch",
        "units": "mm, inches",
        "how": "For spanners, tyres, pipe sizes and imported parts. Divide by "
               "25.4. 12.7 mm is half an inch, 25.4 mm is an inch, 19.05 mm is "
               "three quarters.",
        "example": "A 19 mm spanner = 0.75 inch.",
        "tags": "conversion,millimetres,inches,spanner",
    },
    {
        "slug": "psi-to-bar",
        "name": "Pounds per square inch to bar",
        "topic": "measurement",
        "expression": "bar = psi / 14.5038   (psi = bar x 14.5038)",
        "symbols": "psi = pounds per square inch; bar = 1 bar = 100,000 Pa",
        "units": "psi, bar, kPa",
        "how": "Tyre pressures, sprayer pressures, grease guns and air tools. "
               "Modern tyres quote bar; old manuals quote psi. 30 psi = 2.07 bar, "
               "which is roughly a car tyre.",
        "example": "A sprayer at 3 bar = 43.5 psi.",
        "tags": "conversion,pressure,psi,bar,tyre",
    },
    {
        "slug": "litres-to-imperial-gallons",
        "name": "Litres to imperial gallons",
        "topic": "measurement",
        "expression": "gallons = litres / 4.54609",
        "symbols": "1 imperial gallon = 4.54609 litres; 1 US gallon = 3.785 litres",
        "units": "litres, gallons",
        "how": "Old manuals, old recipes and old spray tables are all in "
               "imperial gallons. Divide litres by 4.546.",
        "example": "20 L of fuel = 4.4 imperial gallons.",
        "tags": "conversion,litres,gallons,fuel",
    },
    {
        "slug": "kg-to-pounds",
        "name": "Kilograms to pounds",
        "topic": "measurement",
        "expression": "lb = kg x 2.20462",
        "symbols": "kg = kilograms; lb = pounds",
        "units": "kg, lb",
        "how": "Stocking rates, feed weights, seed rates and older books in "
               "pounds. Multiply by 2.2046.",
        "example": "500 kg of fertiliser = 1,102 lb.",
        "tags": "conversion,kilograms,pounds,weight",
    },
    {
        "slug": "celsius-to-fahrenheit",
        "name": "Celsius to Fahrenheit",
        "topic": "measurement",
        "expression": "F = (C x 9 / 5) + 32   (C = (F - 32) x 5 / 9)",
        "symbols": "C = degrees Celsius; F = degrees Fahrenheit",
        "units": "degrees",
        "how": "Oven temperatures, animal temperatures, weather and old American "
               "books. Multiplication and addition beat a table every time.",
        "example": "200 C = 392 F, the usual temperature for a hot oven.",
        "tags": "conversion,temperature,celsius,fahrenheit,oven",
    },
    {
        "slug": "acres-and-hectares",
        "name": "Acres and hectares",
        "topic": "measurement",
        "expression": "acres = m2 / 4046.86 ; hectares = acres x 0.404686 ; "
                      "m2 = hectares x 10,000",
        "symbols": "1 hectare = 10,000 m2 = 2.471 acres; 1 acre = 4046.86 m2",
        "units": "m2, hectares, acres",
        "how": "Old books are in acres, new ones in hectares, and field maps in "
               "acres. Learn both. A hectare is about 2.5 acres, which is close "
               "enough for a rough job but not for a rent calculation.",
        "example": "5 acres = 2.023 hectares.",
        "tags": "conversion,acres,hectares,field,area",
    },
    {
        "slug": "slope-and-gradient",
        "name": "Slope and gradient",
        "topic": "measurement",
        "expression": "gradient = rise / run ; slope % = (rise / run) x 100",
        "symbols": "rise = vertical change; run = horizontal distance",
        "units": "m/m, %, degrees",
        "how": "For land drainage, roof pitch, silage clamp faces, ramps, and "
               "whether a load will get up the yard. A 1 in 10 slope is 10%.",
        "example": "1 m rise over 20 m = a gradient of 1 in 20, or 5%.",
        "tags": "slope,gradient,drainage,roof,ramp",
    },
    {
        "slug": "percentage-by-mass-remaining",
        "name": "Percentage of a quantity",
        "topic": "measurement",
        "expression": "amount = (percentage / 100) x quantity",
        "symbols": "percentage = the part per hundred; quantity = the whole",
        "units": "varies",
        "how": "Salt in a brine, protein in a feed, moisture in a crop, "
               "discount on a sale. Divide the percentage by 100 and multiply.",
        "example": "2.5% salt on 10 kg of meat = 250 g of salt.",
        "tags": "percentage,concentration,salt,moisture",
    },

    # ------------------------------------------------------------------ maths
    {
        "slug": "percentage-change",
        "name": "Percentage change",
        "topic": "maths",
        "expression": "change % = ((new - old) / old) x 100",
        "symbols": "old = the starting value; new = the finishing value",
        "units": "%",
        "how": "Feed price moves, growth rate, water use, milk yield, a price "
               "rise at the mart. Always state the direction with a sign.",
        "example": "Feed went from 220 to 260 a tonne: (40/220) x 100 = 18.2% "
                   "more.",
        "tags": "percentage,change,price,growth",
    },
    {
        "slug": "rule-of-three",
        "name": "Rule of three (direct proportion)",
        "topic": "maths",
        "expression": "x = (a x b) / c",
        "symbols": "if a of something gives b, then c of it gives x",
        "units": "varies",
        "how": "The workhorse of farm arithmetic. Seed rate per hectare scaled "
               "to your patch, fertiliser from the label, spray mix from a "
               "test plot, feed per animal per day.",
        "example": "If 5 kg of seed covers 2 hectares, 1.5 hectares needs "
                   "(1.5 x 5) / 2 = 3.75 kg.",
        "tags": "proportion,rule of three,seed,fertiliser,scaling",
    },
    {
        "slug": "ratio-proportions",
        "name": "Ratio and proportion",
        "topic": "maths",
        "expression": "a:b = c:d means a/b = c/d, so x = (c x b) / d",
        "symbols": "a, b, c, d = the parts of each ratio",
        "units": "varies",
        "how": "Mixing feed, splitting a bale, scaling a recipe, dividing a "
               "field between two crops, blending a concentrate with a "
               "home-grown protein.",
        "example": "A 3:1 mix of concentrate to grain: 12 kg of concentrate "
                   "needs 4 kg of grain.",
        "tags": "ratio,proportion,mixing,feed,recipe",
    },
    {
        "slug": "pythagoras",
        "name": "Pythagoras' theorem",
        "topic": "maths",
        "expression": "c2 = a2 + b2  (so c = square root of (a2 + b2))",
        "symbols": "c = the longest side (hypotenuse); a, b = the other sides",
        "units": "m, mm, ft",
        "how": "Bracing a gate, checking a diagonal, setting out a rectangle, "
               "working the length of a rafter, checking that a frame is "
               "square.",
        "example": "A 3 m by 4 m rectangle has a 5 m diagonal.",
        "tags": "triangle,diagonal,square,bracing,rafter",
    },
    {
        "slug": "compound-interest",
        "name": "Compound interest",
        "topic": "maths",
        "expression": "A = P x (1 + r/n)^(n x t)",
        "symbols": "A = final amount; P = principal; r = annual rate as a "
                   "decimal; n = times compounded per year; t = years",
        "units": "currency",
        "how": "On a loan, an investment, or a hire-purchase agreement. The "
               "difference from simple interest is that the interest itself "
               "earns interest.",
        "example": "1,000 at 6% compounded yearly for 5 years = 1,338.23.",
        "tags": "interest,loan,money,investment",
    },
    {
        "slug": "simple-interest",
        "name": "Simple interest",
        "topic": "maths",
        "expression": "I = P x r x t ; A = P + I",
        "symbols": "I = interest; P = principal; r = rate per year as a decimal; "
                   "t = years",
        "units": "currency",
        "how": "The old hire-purchase and the short-term loan. Easy to check by "
               "hand against the paperwork.",
        "example": "500 at 8% for 2 years = 80 of interest.",
        "tags": "interest,loan,money",
    },
    {
        "slug": "rule-of-72",
        "name": "Rule of 72",
        "topic": "maths",
        "expression": "years to double = 72 / annual rate %",
        "symbols": "annual rate as a whole number percentage",
        "units": "years",
        "how": "How long money takes to double, and how long a debt takes to "
               "double as well. Rough, and right to within a few months at "
               "normal rates.",
        "example": "At 9% a debt doubles in 8 years.",
        "tags": "interest,double,money,quick",
    },
    {
        "slug": "average-mean",
        "name": "Average (arithmetic mean)",
        "topic": "maths",
        "expression": "mean = (sum of the values) / (number of values)",
        "symbols": "add every reading, then divide by how many there are",
        "units": "varies",
        "how": "Average daily milk yield, average egg weight, average tractor "
               "hours a week, average weight at weaning.",
        "example": "Weights of 180, 200, 220 and 240 kg give a mean of 210 kg.",
        "tags": "average,mean,records,milk",
    },
    {
        "slug": "exponent-laws",
        "name": "Exponent laws",
        "topic": "maths",
        "expression": "a(m) x a(n) = a(m+n) ; (a(m))(n) = a(m x n) ; "
                      "a(m) / a(n) = a(m-n) ; a(0) = 1 ; a(1/n) = the nth root",
        "symbols": "a = the base; m, n = the powers",
        "units": "varies",
        "how": "For compound growth, interest, scaling up a feed rate, and "
               "working out how many times a treatment covers a flock.",
        "example": "2(3) x 2(4) = 2(7) = 128.",
        "tags": "powers,exponents,growth",
    },
    {
        "slug": "logarithms",
        "name": "Logarithms",
        "topic": "maths",
        "expression": "log(b)(x) = the power b must be raised to give x, so "
                      "b(y) = x means log(b)(x) = y",
        "symbols": "b = the base (10 or e); x = the number; y = the exponent",
        "units": "varies",
        "how": "They are the reverse of powers. They are how you find a "
               "compound interest time, a half-life, a pH, a decibels level or "
               "a Richter magnitude.",
        "example": "log(10)(1000) = 3.",
        "tags": "log,power,interest,ph,half-life",
    },
    {
        "slug": "scientific-notation",
        "name": "Scientific notation",
        "topic": "maths",
        "expression": "number = a x 10(n)",
        "symbols": "a = a number from 1 to 10; n = the power of ten",
        "units": "varies",
        "how": "For very small and very large numbers: soil test results in "
               "parts per million, feed analysis in milligrams per kilogram, "
               "money in the billions.",
        "example": "0.00042 kg/m3 = 4.2 x 10(-4) kg/m3.",
        "tags": "notation,large,numbers,ppm",
    },
    {
        "slug": "slope-of-a-line",
        "name": "Slope of a line",
        "topic": "maths",
        "expression": "m = (y2 - y1) / (x2 - x1)",
        "symbols": "m = slope (rise over run); x1, y1 and x2, y2 = two points "
                   "on the line",
        "units": "varies",
        "how": "For a roof pitch, a drain run, a graph of growth against time, "
               "or checking whether a field really does slope the way you "
               "think.",
        "example": "From (0, 0) to (10, 2) the slope is 0.2, or 1 in 5.",
        "tags": "slope,graph,roof,drain",
    },

    # ------------------------------------------------------------------ money
    {
        "slug": "break-even",
        "name": "Break-even point",
        "topic": "money",
        "expression": "break-even units = fixed costs / (price per unit - "
                      "variable cost per unit)",
        "symbols": "fixed costs = costs you pay anyway (rent, insurance, "
                   "depreciation); variable cost = cost per unit sold",
        "units": "units",
        "how": "Before you buy pigs, take on a shed, or start selling eggs. If "
               "the margin per unit is negative, the answer is no, however many "
               "units you sell.",
        "example": "Fixed costs 2,400 a year, eggs at 40p with 20p of cost: "
                   "2,400 / 0.20 = 12,000 eggs a year, or 33 a day.",
        "tags": "break-even,business,costs,eggs,planning",
    },
    {
        "slug": "gross-margin",
        "name": "Gross margin and markup",
        "topic": "money",
        "expression": "margin % = ((price - cost) / price) x 100 ; "
                      "markup % = ((price - cost) / cost) x 100",
        "symbols": "price = what you charge; cost = what it cost you",
        "units": "%",
        "how": "Margin is measured against the selling price, markup against "
               "the cost. They are not the same number and confusing them is "
               "how people lose money. A 50% markup is a 33% margin.",
        "example": "Bought at 2 and sold at 3: a 50% markup, a 33% margin.",
        "tags": "margin,markup,price,profit",
    },
    {
        "slug": "return-on-investment",
        "name": "Return on investment",
        "topic": "money",
        "expression": "ROI % = ((gain - cost) / cost) x 100",
        "symbols": "gain = what you got back; cost = what you put in",
        "units": "%",
        "how": "Compare a new freezer, a new shed or a flock of sheep against "
               "what they actually return each year.",
        "example": "Cost 4,000, returns 1,600 a year in extra sales: 40% a year.",
        "tags": "roi,investment,profit,comparison",
    },
    {
        "slug": "payback-period",
        "name": "Payback period",
        "topic": "money",
        "expression": "payback = investment / annual net cash flow",
        "symbols": "investment = the capital cost; net cash flow = what comes "
                   "back in a year after running costs",
        "units": "years",
        "how": "How long before the machine pays for itself. A payback under "
               "three years is usually good for a working tool.",
        "example": "Cost 9,000, nets 1,800 a year: 5 years to pay back.",
        "tags": "payback,investment,machine,cashflow",
    },
    {
        "slug": "cost-per-unit-of-land",
        "name": "Cost per hectare or acre",
        "topic": "money",
        "expression": "cost per hectare = total cost / hectares",
        "symbols": "total cost = rent, inputs, labour, machinery; hectares = "
                   "the area worked",
        "units": "currency per hectare",
        "how": "The only way to compare two crops, or two fields, fairly. "
               "Divide the whole year's cost by the area, not just the "
               "variable bits.",
        "example": "12,000 of costs over 8 hectares = 1,500 a hectare.",
        "tags": "cost,hectare,acre,crops,comparison",
    },
    {
        "slug": "gross-margin-per-hectare",
        "name": "Gross margin per hectare",
        "topic": "money",
        "expression": "margin per hectare = (yield per hectare x price per unit) "
                      "- (variable cost per hectare)",
        "symbols": "yield per hectare; price per unit; variable cost per "
                   "hectare = seed, fertiliser, sprays, variable machinery",
        "units": "currency per hectare",
        "how": "The number that decides what you plant next year. Always leave "
               "the fixed costs out of this figure and add them back at the "
               "whole-farm level, or you will chase the wrong crop.",
        "example": "6 t/ha at 180 a tonne = 1,080, less 480 of variable cost = "
                   "600 a hectare.",
        "tags": "gross margin,crops,yield,planning",
    },
    {
        "slug": "price-per-unit-from-bulk",
        "name": "Price per unit from a bulk load",
        "topic": "money",
        "expression": "price per unit = total cost / number of units",
        "symbols": "total cost = what you paid; units = weight, count or volume",
        "units": "currency per unit",
        "how": "Working out whether a bulk buy of feed, fuel or seed is cheaper "
               "than the retail price, including the delivery.",
        "example": "600 for 1,500 kg of feed = 40 a 100 kg bag equivalent.",
        "tags": "price,bulk,feed,fuel,comparison",
    },
    {
        "slug": "compound-annual-growth",
        "name": "Compound annual growth rate",
        "topic": "money",
        "expression": "CAGR % = ((end / start)^(1/years) - 1) x 100",
        "symbols": "end = the value now; start = the value before; years = how "
                   "long it took",
        "units": "%",
        "how": "For a flock, a herd, a customer list or a tree that is being "
               "improved each year. Shows the real rate behind a rising "
               "number.",
        "example": "20 sheep to 50 in 5 years: (2.5^(1/5) - 1) = 20.1% a year.",
        "tags": "growth,cagr,flock,herd,plan",
    },

    # ------------------------------------------------------------------- data
    {
        "slug": "median-and-range",
        "name": "Median and range",
        "topic": "data",
        "expression": "median = middle value when sorted ; range = highest - "
                      "lowest",
        "symbols": "sort the readings first",
        "units": "varies",
        "how": "Averages lie when one reading is odd. The median tells you the "
               "typical day; the range tells you how variable the month was. "
               "Use both for milk records, daily temperatures and yields.",
        "example": "10, 12, 12, 13, 20 litres: median 12, range 10.",
        "tags": "median,range,records,statistics",
    },
    {
        "slug": "standard-deviation",
        "name": "Standard deviation",
        "topic": "data",
        "expression": "sigma = square root of ( sum of (x - mean)2 / n )",
        "symbols": "x = each reading; mean = the average; n = number of "
                   "readings",
        "units": "same as the readings",
        "how": "How spread out a set of readings is. A 500 litre herd with a "
               "standard deviation of 20 is steady; one with 120 is not. It is "
               "how you tell a genuinely consistent flock from a lucky "
               "average.",
        "example": "Readings 98, 100, 102, 100 give a mean of 100 and a "
                   "standard deviation of about 1.6.",
        "tags": "deviation,variation,statistics,records",
    },
    {
        "slug": "weighted-average",
        "name": "Weighted average",
        "topic": "data",
        "expression": "weighted mean = sum of (value x weight) / sum of weights",
        "symbols": "weight = how much of the total each value represents",
        "units": "varies",
        "how": "Average feed analysis across different batches, average yield "
               "across fields of different sizes, average price across "
               "different volumes sold.",
        "example": "Field A: 10 ha at 6 t/ha, field B: 4 ha at 4 t/ha gives "
                   "(60 + 16) / 14 = 5.43 t/ha.",
        "tags": "average,weighted,yield,mix",
    },
    {
        "slug": "per-unit-error",
        "name": "Percentage error and accuracy",
        "topic": "data",
        "expression": "error % = ((measured - true) / true) x 100",
        "symbols": "true = the reference value; measured = what you read",
        "units": "%",
        "how": "For a sprayer that does not deliver its rated volume, a scale "
               "that reads light, or a soil test that is out by a tenth of a "
               "point. Know the error and you can correct for it.",
        "example": "A 20 L/min sprayer that delivers 18: error = -10%.",
        "tags": "error,accuracy,sprayer,calibration",
    },

    # ----------------------------------------------------------------- health
    {
        "slug": "drug-dose-by-weight",
        "name": "Drug dose from body weight",
        "topic": "health",
        "expression": "dose = (mg per kg x body weight in kg) / 1000",
        "symbols": "mg per kg from the label or the vet; body weight in kg",
        "units": "milligrams, or millilitres once you have the concentration",
        "how": "For any medicine given by weight. First work out the animal's "
               "weight, then multiply, then convert to millilitres using the "
               "concentration on the label. Always confirm the dose with your "
               "vet before the first use.",
        "example": "A drug at 10 mg/kg for a 400 kg cow = 4,000 mg, which is "
                   "4 mL of a 1,000 mg/mL solution.",
        "tags": "dose,medicine,weight,veterinary,dosage",
    },
    {
        "slug": "fluid-requirement",
        "name": "Fluid requirement",
        "topic": "health",
        "expression": "maintenance fluid (mL/day) = 50 x body weight (kg)",
        "symbols": "body weight in kg; 50 mL per kg per day is the usual "
                   "maintenance figure for cattle and horses",
        "units": "millilitres per day, litres per day",
        "how": "The starting point for how much water or IV fluid an animal "
               "needs. Add losses for fever, heat, exercise and any "
               "diarrhoea. A cow drinking less than this is a cow that will "
               "go down.",
        "example": "A 500 kg cow needs about 25 L a day.",
        "tags": "fluid,water,dehydration,vet,intake",
    },
    {
        "slug": "dehydration-estimated-loss",
        "name": "Dehydration deficit",
        "topic": "health",
        "expression": "deficit (L) = (body weight in kg x percent dehydration "
                      "from normal) / 10",
        "symbols": "10% dehydrated means 10% of body weight has been lost",
        "units": "litres",
        "how": "Sunken eyes, tight skin and a tacky mouth in a calf or a dog "
               "mean a percentage of body weight has gone. A 5% loss in a 40 kg "
               "calf is 2 L to put back.",
        "example": "A 40 kg calf 5% dehydrated: (40 x 5) / 10 = 2 L short.",
        "tags": "dehydration,calf,fluid,vet",
    },
    {
        "slug": "body-mass-index",
        "name": "Body mass index",
        "topic": "health",
        "expression": "BMI = mass (kg) / (height in m)2",
        "symbols": "a rough guide only; it does not work for cattle or pigs",
        "units": "kg/m2",
        "how": "A rough guide for people, and a reminder that a weight without "
               "a condition score is only half a judgement. Use body condition "
               "scoring for stock, and the tape for pigs.",
        "example": "70 kg at 1.75 m gives a BMI of about 23.",
        "tags": "bmi,weight,condition,people",
    },
    {
        "slug": "gestation-and-due-date",
        "name": "Gestation length and due date",
        "topic": "health",
        "expression": "due date = service date + gestation length",
        "symbols": "ewe 144-147 days; cow 280-283 days; sow 114 days; mare "
                   "336 days; goat 150 days",
        "units": "days",
        "how": "To plan the yard, the lambing shed, the farrowing crate and the "
               "calving pen. Add a few days to the average for a first-time "
               "animal, because first pregnancies run long.",
        "example": "A sow served on 1 March is due around 23 June.",
        "tags": "gestation,pregnancy,due date,lambing,farrowing",
    },
    {
        "slug": "energy-from-food",
        "name": "Energy in food",
        "topic": "health",
        "expression": "kJ = kcal x 4.184 ; kcal = joules / 4.184",
        "symbols": "kJ = kilojoules; kcal = kilocalories (food Calories)",
        "units": "kJ, kcal",
        "how": "Feed energy is quoted in megajoules of net energy, and food "
               "labels in kilocalories. The conversion lets you compare the "
               "two. A megajoule is 239 kcal.",
        "example": "10 MJ of net energy = 2,390 kcal.",
        "tags": "energy,calories,joule,feed",
    },
    {
        "slug": "protein-requirement",
        "name": "Protein requirement from live weight",
        "topic": "health",
        "expression": "daily protein (g) = body weight (kg) x requirement "
                      "(g per kg) x condition factor",
        "symbols": "requirement from a feed table; condition factor 1.0 for a "
                   "fit animal, 1.1 for a growing one, 1.2 for a lactating one",
        "units": "grams per day",
        "how": "To check a ration against a feed table. Growers and lactating "
               "stock need more protein than dry stock, and the tables are "
               "always in digestible protein.",
        "example": "A 600 kg lactating cow at 1.2 g/kg needs 720 g of "
                   "digestible protein a day.",
        "tags": "protein,ration,feed,lactation",
    },
    {
        "slug": "unit-conversion-medicine",
        "name": "Converting between medicine units",
        "topic": "health",
        "expression": "1 g = 1000 mg ; 1 mg = 1000 micrograms ; "
                      "1 L = 1000 mL ; 1 kg = 1000 g",
        "symbols": "the metric ladder",
        "units": "g, mg, micrograms, L, mL",
        "how": "Almost every medicine error is a unit error. Learn the ladder "
               "by heart and write the unit next to every number you copy off "
               "a label.",
        "example": "2.5 g = 2,500 mg = 2,500,000 micrograms.",
        "tags": "conversion,medicine,dosage,safety",
    },
]
