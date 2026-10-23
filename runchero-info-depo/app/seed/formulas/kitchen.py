"""Formulas: kitchen, baking, preserving and food safety."""

from __future__ import annotations

FORMULAS: list[dict] = [
    {
        "slug": "bakers-percentage",
        "name": "Baker's percentages",
        "topic": "kitchen",
        "expression": "ingredient % = (weight of the ingredient / total "
                      "flour weight) x 100",
        "symbols": "flour is always 100%; everything else is measured "
                   "against it",
        "units": "%",
        "how": "The only sane way to scale a bread recipe, and the way "
               "professional bakers write them. Change the flour and "
               "everything scales with it.",
        "example": "A loaf with 1,000 g flour, 700 g water, 200 g starter "
                   "and 20 g salt is 70% hydration, 20% starter and 2% salt.",
        "tags": "baking,percentage,bread,flour,scaling",
    },
    {
        "slug": "hydration",
        "name": "Hydration",
        "topic": "kitchen",
        "expression": "hydration % = (water weight / flour weight) x 100",
        "symbols": "65% is easy, 75% is normal for a good loaf, 85% needs a "
                   "strong flour and a hot oven",
        "units": "%",
        "how": "More water means a more open crumb and a wetter dough that is "
               "harder to handle. A change of 5% hydration changes the dough "
               "a lot.",
        "example": "700 g water on 1,000 g flour is 70% hydration.",
        "tags": "hydration,bread,dough,flour,crumb",
    },
    {
        "slug": "scaling-a-recipe",
        "name": "Scaling a recipe up or down",
        "topic": "kitchen",
        "expression": "new weight = old weight x (target yield / current "
                      "yield)",
        "symbols": "work out the factor from the yield, not from the number "
                   "of people, and scale the seasoning by the same factor",
        "units": "factor",
        "how": "The quickest kitchen arithmetic. Divide by the factor for a "
               "smaller batch, and remember that a double batch does not "
               "cook in double the time.",
        "example": "A recipe for 6 with 300 g of flour, baked for 25 "
                   "minutes: for 4, multiply by 0.67, so 200 g of flour and "
                   "about 20 minutes.",
        "tags": "scaling,recipe,yield,batch,cooking",
    },
    {
        "slug": "dough-temperature-and-proofing",
        "name": "Dough temperature and proofing time",
        "topic": "kitchen",
        "expression": "doubling time (hours) = 4 - (dough temperature in C - "
                      "20) x 0.75",
        "symbols": "the rule of thumb: each 8 C above 20 C halves the "
                   "doubling time; below 20 C it roughly doubles",
        "units": "hours",
        "how": "A warm kitchen gives you a fast loaf and a sour one. The "
               "dough temperature at mixing decides how long you wait, not "
               "the clock on the wall.",
        "example": "Dough at 26 C: 4 - 4.5 = about 2.9 hours to double, "
                   "roughly half a normal rise.",
        "tags": "proofing,dough,temperature,rise,sourdough",
    },
    {
        "slug": "bulk-rise-percentage",
        "name": "How much to let the dough rise",
        "topic": "kitchen",
        "expression": "rise % = (weight after - weight before) / weight "
                      "before x 100",
        "symbols": "bulk fermentation 30-50% rise, final proof 50-75%, oven "
                   "spring adds another 20-30%",
        "units": "%",
        "how": "Weight is the only honest way to judge a rise, because a "
               "warm kitchen and a cold one both look different. Mark the "
               "bowl or use the scale.",
        "example": "800 g of dough that has gone to 1,000 g has risen 25%, "
                   "which is a third of the way there.",
        "tags": "rise,proofing,bulk,percentage,weight",
    },
    {
        "slug": "salt-in-bread",
        "name": "Salt in bread",
        "topic": "kitchen",
        "expression": "salt % = (salt weight / flour weight) x 100 ; "
                      "2% is the usual 20 g a kilo of flour",
        "symbols": "salt strengthens the gluten, controls the ferment and "
                   "makes the crust better; it also slows the dough",
        "units": "%",
        "how": "More salt does not mean better bread, it means a firmer "
               "crumb and a slower rise. Never add salt straight onto a "
               "wild yeast starter.",
        "example": "20 g of salt on 1 kg of flour is 2%.",
        "tags": "salt,bread,gluten,flour,ferment",
    },
    {
        "slug": "starter-refresh",
        "name": "Refreshing a sourdough starter",
        "topic": "kitchen",
        "expression": "starter to add (g) = flour weight x hydration x 0.1 to "
                      "0.2 of the starter's total weight",
        "symbols": "a 1:5:5 starter is 20% ripe starter; a 1:10:10 is 10%",
        "units": "g",
        "how": "A 1:5:5 feed doubles in 4-6 hours at 24 C. A 1:10:10 takes "
               "8-12 hours and tastes less sour.",
        "example": "100 g of ripe starter at 100% hydration is 50 g flour and "
                   "50 g water, so it makes 100 g of dough weight.",
        "tags": "starter,refresh,feed,sourdough,ratio",
    },
    {
        "slug": "sugar-substitution",
        "name": "Substituting sugar with honey or syrup",
        "topic": "kitchen",
        "expression": "for every 100 g of sugar use 75-85 g of honey, or 100 g "
                      "of syrup",
        "symbols": "honey adds moisture and flavour, so cut the water in the "
                   "recipe by 20 g for every 100 g of honey used",
        "units": "g",
        "how": "Honey is about 80% sugar and 20% water, and it is stickier, "
               "so cakes brown more and keep longer. Reduce the liquid in "
               "any recipe where you swap it in.",
        "example": "A cake with 150 g of sugar takes 120 g of honey and 30 g "
                   "less water.",
        "tags": "honey,sugar,substitution,cake,sweetener",
    },
    {
        "slug": "egg-weight",
        "name": "Egg weight and count",
        "topic": "kitchen",
        "expression": "eggs needed = (weight of egg in the recipe / average "
                      "egg weight) ; large 60 g, medium 50 g, small 42 g",
        "symbols": "in the kitchen it is 3 large eggs for 100 g of egg; in a "
                   "baking recipe weigh them",
        "units": "eggs, g",
        "how": "Weighing the eggs is the only reliable way, because the "
               "sizes in one box vary. A big egg in a cake is a wetter cake.",
        "example": "A recipe for 3 medium eggs (150 g) needs 3 large eggs "
                   "(180 g) or 2.8 large eggs, so 3.",
        "tags": "eggs,weight,baking,size,count",
    },
    {
        "slug": "baking-powder",
        "name": "Baking powder and raising agents",
        "topic": "kitchen",
        "expression": "1 level teaspoon (5 g) per cup (125 g) of flour for "
                      "single acting, 1/2 teaspoon for double acting",
        "symbols": "baking soda needs acid, so use it with buttermilk, "
                   "cocoa or molasses; baking powder works on its own",
        "units": "g",
        "how": "Double acting powder works twice, once in the mix and once "
               "in the oven, so it is more forgiving. Do not mix baking "
               "powder and bicarbonate of soda together.",
        "example": "A 3 cup cake mix needs 1.5 teaspoons of double acting "
                   "powder.",
        "tags": "baking powder,raising,spoon,sooda,cake",
    },
    {
        "slug": "tempering-chocolate",
        "name": "Tempering chocolate",
        "topic": "kitchen",
        "expression": "melt to 45-50 C for milk, 40-45 C for white, 45-50 C "
                      "for dark, then cool to 27-28 C (dark) or 29-31 C "
                      "(milk)",
        "symbols": "the final working temperature for dark is 31-32 C",
        "units": "degrees C",
        "how": "Good tempering gives a snap and a shine. A bad one gives a "
               "grey dull surface and blooms later. See "
               "[[working-with-chocolate]].",
        "example": "Dark chocolate at 45 C cooled to 31 C and worked back to "
                   "32 C sets with a shine.",
        "tags": "chocolate,tempering,melting,bloom,slate",
    },
    {
        "slug": "stock-ratio",
        "name": "Stock and broth ratios",
        "topic": "kitchen",
        "expression": "bones and meat to water by weight: 1:2 for a rich "
                      "stock, 1:3 for a light one; vegetables 1:1 by weight",
        "symbols": "skim the fat and the impurities off the top as it "
                   "simmers, and never boil it hard",
        "units": "by weight",
        "how": "Roast the bones first for a deeper flavour, and add the "
               "vegetables for the last hour so they do not turn to mush. "
               "See [[making-stock]].",
        "example": "1 kg of bones and 2 kg of cold water gives about 1.5 L of "
                   "stock after simmering and skimming.",
        "tags": "stock,broth,ratio,bones,simmer",
    },
    {
        "slug": "safe-cooking-temperature",
        "name": "Safe cooking temperatures",
        "topic": "kitchen",
        "expression": "beef and lamb 63 C for 3 minutes, pork 71 C, poultry "
                      "74 C, fish 63 C, reheated food 75 C",
        "symbols": "temperature at the thickest part, and for 3 minutes; a "
                   "food thermometer is the only way to be sure",
        "units": "degrees C",
        "how": "Colour is not proof. A meat thermometer costs almost nothing "
               "and settles every argument about dinner. See "
               "[[cooking-temperatures]].",
        "example": "Chicken breast cooked to 74 C in the thickest part is "
                   "safe; browned outside and pink inside is not.",
        "tags": "temperature,safe,meat,poultry,thermometer",
    },
    {
        "slug": "resting-time",
        "name": "Resting meat after cooking",
        "topic": "kitchen",
        "expression": "resting time (minutes) = 10 to 20 for a joint, 5 for "
                      "a steak, 30 for a whole bird",
        "symbols": "roughly half the cooking time",
        "units": "minutes",
        "how": "Resting lets the juice spread back into the meat. Cut it "
               "early and the juice ends up on the board.",
        "example": "A 90 minute roast rests for 30 minutes before carving.",
        "tags": "rest,meat,juice,roast,carving",
    },
    {
        "slug": "brine-percentage",
        "name": "Brine and salt percentage",
        "topic": "kitchen",
        "expression": "salt % = salt weight / total weight x 100 ; "
                      "a 10% brine is 100 g of salt per litre of water "
                      "(about 108 g a litre of finished brine)",
        "symbols": "for a meat brine, 0.5-0.7% of the bird's weight; for "
                   "pickling, 2% salt by weight of the vegetables",
        "units": "%",
        "how": "Weigh the salt and the water, or measure the water and use "
               "the figure for the salt. Ice brine is 20-25% for a fast "
               "pickle. See [[curing-bacon-and-sausages]].",
        "example": "To brine a 4 kg chicken at 0.6%: 24 g of salt in 1 L of "
                   "water.",
        "tags": "brine,salt,pickle,percentage,curing",
    },
    {
        "slug": "sugar-solubility",
        "name": "How much sugar dissolves",
        "topic": "kitchen",
        "expression": "at 20 C, about 200 g of sugar dissolves in 100 g of "
                      "water ; at 100 C, about 487 g",
        "symbols": "a saturated solution at room temperature is about 67% "
                   "sugar by weight",
        "units": "g per 100 g water",
        "how": "Anything more and the extra sugar sits at the bottom of the "
               "jar. For a simple syrup, dissolve equal weights of sugar "
               "and water and stop there.",
        "example": "A 1:1 syrup by weight is 50% sugar; a 1:2 syrup by weight "
                   "is 33%.",
        "tags": "sugar,solubility,syrup,saturated,preserving",
    },
    {
        "slug": "jam-setting-point",
        "name": "Jam setting point",
        "topic": "kitchen",
        "expression": "set at 65-68 C, or 104-105 C at sea level ; "
                      "1% more sugar or a 2% drop in pectin needs about "
                      "5-8 C less heat",
        "symbols": "the wrinkle test: put a cold saucer in the pan, drip "
                   "some syrup on it and it should wrinkle when you push it "
                   "with a finger",
        "units": "degrees C, %",
        "how": "A boiling thermometer is worth the money. Overcook the jam "
               "and it goes tough, undercook it and it runs. See "
               "[[jam-jelly-and-preserves]].",
        "example": "Add 1% extra sugar and the set comes at about 62 C "
                   "instead of 65 C.",
        "tags": "jam,setting,temperature,pectin,sugar",
    },
    {
        "slug": "jam-sugar-ratio",
        "name": "Sugar for jam and preserves",
        "topic": "kitchen",
        "expression": "sugar = fruit weight x 0.5 to 0.7 for a jam, x 1 for a "
                      "preserving syrup",
        "symbols": "the more pectin in the fruit, the less sugar you need",
        "units": "by weight",
        "how": "High pectin fruits like gooseberries and redcurrants need "
               "less sugar. Soft fruit such as strawberries need more, and "
               "more sugar means a firmer set.",
        "example": "2 kg of gooseberries with a litre of water needs about "
                   "1 kg of sugar.",
        "tags": "jam,sugar,pectin,fruit,preserves",
    },
    {
        "slug": "brix-and-specific-gravity",
        "name": "Brix, specific gravity and Baume",
        "topic": "kitchen",
        "expression": "SG = 1 + (Brix / 100) roughly at 20 C ; "
                      "Baume = Brix x 0.21 for a hydrometer marked in Baume",
        "symbols": "Brix reads the grams of sugar in 100 g of solution, so "
                   "it is weight, not volume; a refractometer reads it "
                   "instantly",
        "units": "Brix, SG",
        "how": "The way to know if your cider is fermenting and if your wine "
               "is ready. Sugar is the fuel for the yeast, and the falling "
               "reading tells you it is running out. See "
               "[[cider-and-perry]].",
        "example": "Cider at 8 Brix that falls to 2 Brix has used about 6% of "
                   "its sugar, and at 15% alcohol it is nearly done.",
        "tags": "brix,specific gravity,hydrometer,cider,ferment",
    },
    {
        "slug": "alcohol-from-sugar",
        "name": "Alcohol from sugar",
        "topic": "kitchen",
        "expression": "ABV % = 131 x (SG at start - SG at finish)",
        "symbols": "a gravity reading of 1.090 is about 9% potential "
                   "alcohol; 19 g of sugar a litre gives about 1% alcohol",
        "units": "%",
        "how": "A rough check on a ferment. If the drink is not as strong as "
               "the sugar suggested, the yeast ran out of food or something "
               "else ate the sugar. See [[cider-and-perry]].",
        "example": "Starting at 1.060 and finishing at 1.000 gives "
                   "131 x 0.06 = 7.9% alcohol.",
        "tags": "alcohol,abv,sugar,ferment,cider",
    },
    {
        "slug": "pickle-vinegar-acid",
        "name": "Vinegar for pickling",
        "topic": "kitchen",
        "expression": "a 5% acid vinegar is 50 g of acetic acid a litre ; "
                      "for safe pickling use 5% vinegar or a 10% salt brine",
        "symbols": "do not dilute vinegar below 5% for shelf-stable pickles",
        "units": "%",
        "how": "The acid does the preserving. If you cannot get a 5% vinegar, "
               "make a brine pickle instead. See [[kraut-and-kimchi]].",
        "example": "500 ml of 5% vinegar covers 1 kg of vegetables, but "
                   "submerge them fully.",
        "tags": "vinegar,acid,pickle,brine,preserving",
    },
    {
        "slug": "ferment-weight",
        "name": "Salt for a vegetable ferment",
        "topic": "kitchen",
        "expression": "salt = vegetable weight x 0.02 for a 2% ferment ; "
                      "the weight of the salt counts towards the total",
        "symbols": "2% salt and 2% garlic or herbs is a good starting point; "
                   "cabbage for kraut is 1.5-2%",
        "units": "% by weight",
        "how": "Weigh the vegetables, then weigh the salt. Too much salt "
               "stops the ferment, too little lets mould in. See "
               "[[kraut-and-kimchi]].",
        "example": "2 kg of cabbage at 2% is 40 g of salt, and the finished "
                   "jar weighs 2.04 kg before the water.",
        "tags": "ferment,salt,kraut,vegetable,weight",
    },
    {
        "slug": "butter-yield",
        "name": "Butter yield from cream",
        "topic": "kitchen",
        "expression": "butter (kg) = cream (L) x 0.09 to 0.11 ; "
                      "1 L of double cream gives about 100 g of butter",
        "symbols": "a 500 L churn of cream at 40% fat makes 65-70 kg of "
                   "butter",
        "units": "kg",
        "how": "The number to check a cream job against. See "
               "[[butter-and-cheese]].",
        "example": "10 L of double cream gives about 1 kg of butter, plus "
                   "the buttermilk left over.",
        "tags": "butter,cream,yield,churn,kilo",
    },
    {
        "slug": "cheese-yield",
        "name": "Cheese yield from milk",
        "topic": "kitchen",
        "expression": "hard cheese (kg) = milk (L) / 9 to 10 ; "
                      "soft cheese (kg) = milk (L) / 6",
        "symbols": "the yield depends on the milk fat, the protein and how "
                   "much whey you leave in",
        "units": "kg",
        "how": "Cheddar and hard farmhouse cheeses need about 9-10 litres of "
               "milk a kilo. A cream cheese or a cottage cheese needs far "
               "less. See [[butter-and-cheese]].",
        "example": "100 L of milk makes about 11 kg of cheddar and 90 L of "
                   "whey.",
        "tags": "cheese,yield,milk,whey,cheddar",
    },
    {
        "slug": "yoghurt-and-ferments",
        "name": "Yoghurt, kefir and cultured milk",
        "topic": "kitchen",
        "expression": "1 L of milk makes about 1 kg of yoghurt ; "
                      "use 2 tablespoons of starter per litre and keep it at "
                      "40-45 C for 6-12 hours",
        "symbols": "the same weight in and out, with the water evaporating "
                   "or being drawn off as whey",
        "units": "kg, hours",
        "how": "Warm the milk to 45 C, cool to 40 C, add the starter and "
               "keep it warm. See [[yoghurt-and-kefir]].",
        "example": "5 L of milk at 45 C with 100 ml of starter, kept at 45 C "
                   "for 8 hours, gives about 5 kg of yoghurt.",
        "tags": "yoghurt,kefir,starter,milk,ferment",
    },
    {
        "slug": "butter-temperature-and-ghee",
        "name": "Ghee and butter from cream",
        "topic": "kitchen",
        "expression": "ghee yield is about 25% of the cream weight ; "
                      "butter is 10% and the rest is buttermilk and water",
        "symbols": "ghee is made by heating butter until the milk solids "
                   "brown and the clear fat rises",
        "units": "%",
        "how": "Ghee keeps for months in a warm kitchen, which is why it is "
               "the useful one. See [[butter-and-cheese]].",
        "example": "1 kg of cream gives about 100 g of butter and 100 g of "
                   "ghee if you make the ghee from the butter.",
        "tags": "ghee,butter,cream,yield,clarified",
    },
    {
        "slug": "flour-milling-yield",
        "name": "Flour yield from grain",
        "topic": "kitchen",
        "expression": "flour % = flour weight / cleaned grain weight x 100 ; "
                      "wheat gives 70-75%, rye 65-70%, maize 70%, oats 60%",
        "symbols": "the rest is bran and germ, which are the best parts",
        "units": "%",
        "how": "The number that tells you whether a mill is worth setting up. "
               "See [[home-milling]].",
        "example": "100 kg of clean wheat gives about 72 kg of white flour "
                   "and 28 kg of bran and germ.",
        "tags": "milling,flour,yield,bran,wheat",
    },
    {
        "slug": "nixtamal-mass",
        "name": "Nixtamal for maize tortillas",
        "topic": "kitchen",
        "expression": "maize to lime water: 1 kg of maize per litre of water "
                      "with 15-20 g of lime, soaked 12-16 hours",
        "symbols": "the nixtamal is the ground maize, and it goes stale "
                   "quickly, so make it the same day",
        "units": "ratio",
        "how": "Lime makes the maize release its niacin, which is the whole "
               "point of treating it. See [[flint-corn-and-popcorn]].",
        "example": "1 kg of maize and 1 L of water with 15 g of lime makes "
                   "about 1.1 kg of nixtamal.",
        "tags": "nixtamal,maize,tortilla,lime,niacin",
    },
    {
        "slug": "popping-corn-yield",
        "name": "Popcorn yield",
        "topic": "kitchen",
        "expression": "popped volume (L) = dry maize (kg) x 30 to 40 ; "
                      "1 kg of dry popcorn makes about 30 litres popped",
        "symbols": "only flint corn pops; a good popping ratio is 40:1",
        "units": "L per kg",
        "how": "The test of a good flint variety, and the reason some maize "
               "will not pop at all. See [[flint-corn-and-popcorn]].",
        "example": "200 g of popcorn makes about 7 litres of popped corn, "
                   "which fills a large bowl.",
        "tags": "popcorn,maize,yield,flint,volume",
    },
    {
        "slug": "rice-water-ratio",
        "name": "Rice water ratio and absorption",
        "topic": "kitchen",
        "expression": "white rice 1:1.5 by weight, brown rice 1:2, and "
                      "pulao 1:1.75 ; after cooking the rice weighs 2.5 to 3 "
                      "times the dry weight",
        "symbols": "the ratio is by weight of dry rice to water, not by "
                   "volume",
        "units": "ratio by weight",
        "how": "Weigh the rice and the water and the result is the same "
               "every time. Salt the water, and let it rest before you "
               "cook it.",
        "example": "500 g of rice with 750 ml of water makes about 1.6 kg of "
                   "cooked rice.",
        "tags": "rice,water,ratio,cooking,absorption",
    },
    {
        "slug": "oil-in-dough",
        "name": "Oil and fat in a dough",
        "topic": "kitchen",
        "expression": "a dough takes up about 15-20% of the oil's weight in "
                      "fat ; a shortcrust pastry takes 20-25%",
        "symbols": "a dough with 100 g of oil and 500 g of flour will end up "
                   "with about 15 g of oil in every 100 g of dough",
        "units": "%",
        "how": "How to work out how much fat ends up in a pie crust, and how "
               "to make it flaky instead of short. See "
               "[[pastry-and-pies]].",
        "example": "A 500 g flour, 200 g butter pastry will have about 18% "
                   "fat by weight.",
        "tags": "oil,butter,dough,pastry,fat",
    },
    {
        "slug": "dehydrating-weight",
        "name": "Drying food and how much you get",
        "topic": "kitchen",
        "expression": "dried weight = fresh weight x 0.10 to 0.20 ; "
                      "herbs dry to about 10%, fruit to about 20%",
        "symbols": "the drier the food, the longer it keeps, but the more "
                   "flavour and vitamins you lose",
        "units": "%",
        "how": "For planning a dehydrator run and for expecting how much you "
               "will have in the jar at the end of it.",
        "example": "10 kg of apples make about 1.5 kg of dried rings.",
        "tags": "dehydrating,drying,weight,herbs,fruit",
    },
    {
        "slug": "food-storage-times",
        "name": "How long food keeps",
        "topic": "kitchen",
        "expression": "chilled at 0-5 C, frozen at -18 C, and every month "
                      "frozen loses about 5% of its quality",
        "symbols": "0-5 C is a domestic fridge, -18 C is a domestic freezer; "
                   "cool cooked food from 60 C to 20 C within 2 hours and "
                   "to 5 C within 4 hours",
        "units": "time",
        "how": "The rules that decide what goes in the freezer. Label "
               "everything with the date and what it is.",
        "example": "A joint frozen for 12 months is still good, but it has "
                   "lost its water and is better as a stew.",
        "tags": "storage,freezer,chill,shelf life,label",
    },
    {
        "slug": "food-safety-times",
        "name": "Food safety times and temperatures",
        "topic": "kitchen",
        "expression": "cold store at 0-5 C, hot hold above 60 C, "
                      "cook above 70 C, and never leave food in the danger "
                      "zone (5-60 C) for more than 2 hours",
        "symbols": "the danger zone is where bacteria multiply; cool cooked "
                   "food fast and fridge it within 2 hours",
        "units": "degrees C, hours",
        "how": "The whole of food safety in one line. See "
               "[[food-safety-in-the-kitchen]].",
        "example": "A stew left on the table for 3 hours in summer is not "
                   "safe, however long you then keep it in the fridge.",
        "tags": "safety,temperature,danger zone,fridge,cooling",
    },
    {
        "slug": "cost-per-portion",
        "name": "Cost per portion",
        "topic": "kitchen",
        "expression": "cost per portion = total cost of the batch / number of "
                      "portions",
        "symbols": "include the ingredients, the fuel and the time; 30 "
                   "minutes of work is worth putting a figure on",
        "units": "per portion",
        "how": "For working out what to charge at a gate sale or a market "
               "stall, and for seeing which dish actually earns.",
        "example": "A batch costing 34 euro that makes 20 portions costs "
                   "1.70 a portion.",
        "tags": "cost,portion,pricing,market,stall",
    },
    {
        "slug": "freezer-space",
        "name": "Freezer space needed",
        "topic": "kitchen",
        "expression": "space (L) = number of portions x 0.4 L for a meat "
                      "portion, 0.15 L for a pie portion",
        "symbols": "a domestic freezer holds about 200 L of food, or one "
                   "full harvest from a smallholding",
        "units": "litres",
        "how": "The honest test of whether you need a bigger freezer or "
               "fewer chickens.",
        "example": "A 60 kg dressed chicken is about 120 portions of 0.4 L "
                   "each, so 48 L of freezer space.",
        "tags": "freezer,space,volume,storage,harvest",
    },
    {
        "slug": "smoking-times",
        "name": "Smoking times and temperatures",
        "topic": "kitchen",
        "expression": "hot smoke 60-80 C, cold smoke 20-30 C ; "
                      "6-12 hours for a sausage, 4-6 for bacon, 12-20 for a "
                      "whole cheese",
        "symbols": "the internal temperature matters more than the clock: "
                   "sausages 70 C, bacon 65 C, cheese 40 C",
        "units": "hours, degrees C",
        "how": "Smoking is about getting the smoke into the meat and holding "
               "the temperature. See [[curing-bacon-and-sausages]].",
        "example": "A rolled bacon of 2 kg takes about 10 hours of hot "
                   "smoking at 70 C.",
        "tags": "smoking,salmon,bacon,sausage,time",
    },
]
