"""Deep-dive source books for the demo.

These are real public-domain titles selected from the Project Gutenberg
catalogue to give the Cattle and Tomato depots enough primary material to be
useful. Nothing here is written by the depot: every entry is a catalogue
record for a public-domain book or government report.

    (gutenberg_id, slug, title, author, category, summary, motif, base,
     accent, year)
"""

from __future__ import annotations

BOOKS: list[tuple] = [
    # ---------------------------------------------------------- tomato ----
    (28011, "tomato-culture-a-practical-treatise-on-the-tomato",
     "Tomato Culture: A Practical Treatise on the Tomato",
     "W. W. Tracy", "lib-rural",
     "A practical growing guide: soil, seed, transplanting, staking, harvesting "
     "and the varieties grown in the United States at the turn of the century.",
     "tomato", "tomato", "grass", 1907),
    (38051, "the-tomato-work",
     "The Tomato",
     "Paul Work", "lib-rural",
     "A complete crop monograph covering botany, varieties, propagation, field "
     "culture, pests and the market side of tomato growing.",
     "tomato", "tomato", "sun", 1919),
    (52867, "experiments-on-the-spoilage-of-tomato-ketchup",
     "Experiments on the Spoilage of Tomato Ketchup",
     "A. W. Bitting", "lib-kitchen",
     "A government experiment-station study of why tomato ketchup spoils and "
     "what processing and acidity do to keep it stable.",
     "jar", "tomato2", "cream", 1909),
    (65287, "the-manufacture-of-tomato-products",
     "The Manufacture of Tomato Products",
     "W. G. Hier", "lib-kitchen",
     "Factory practice for tomato pulp, puree, catsup, chili sauce, soup and "
     "trimming pulp, including grading and yield.",
     "jar", "tomato2", "sun", 1911),
    (70456, "tomato-products-pulp-ketchup-and-chili-sauce",
     "Tomato Products: Pulp, Ketchup, and Chili Sauce",
     "W. D. Bigelow", "lib-kitchen",
     "A bulletin on the preparation, composition and keeping quality of the "
     "main commercial tomato products.",
     "jar", "tomato2", "cream", 1914),
    (21682, "the-field-and-garden-vegetables-of-america",
     "The Field and Garden Vegetables of America",
     "Fearing Burr", "lib-rural",
     "The great nineteenth-century vegetable catalogue: varieties, culture and "
     "history of the field and garden crops of America.",
     "carrot", "orange", "cream", 1863),
    (16232, "the-culture-of-vegetables-and-flowers-from-seeds-and-roots",
     "The Culture of Vegetables and Flowers From Seeds and Roots",
     "Sutton & Sons Ltd.", "lib-rural",
     "A seed-house manual on propagation, soil preparation and the culture of "
     "garden vegetables and flowers.",
     "seedling", "grass", "cream", 1913),
    (43531, "the-vegetable-garden-what-when-and-how-to-plant",
     "The Vegetable Garden: What, When, and How to Plant",
     "Anonymous", "lib-rural",
     "A concise planting calendar and culture guide for the home vegetable "
     "garden.",
     "carrot", "orange", "grass2", 1917),
    (36064, "farm-gardening-with-hints-on-cheap-manuring",
     "Farm Gardening with Hints on Cheap Manuring",
     "Anonymous", "lib-rural",
     "Quick cash crops and how to grow them, with practical notes on cheap "
     "manures and market gardening.",
     "seedling", "grass2", "soil", 1900),
    (15517, "acetaria-a-discourse-of-sallets",
     "Acetaria: A Discourse of Sallets",
     "John Evelyn", "lib-kitchen",
     "A seventeenth-century discourse on salad greens, herbs and the kitchen "
     "garden, with recipes and household directions.",
     "jar", "grass3", "cream", 1699),
    (2355, "the-formation-of-vegetable-mould-through-the-action-of-worms",
     "The Formation of Vegetable Mould Through the Action of Worms",
     "Charles Darwin", "lib-science",
     "Darwin's study of earthworms and the making of vegetable mould: the "
     "foundational text on soil biology and garden fertility.",
     "seedling", "soil", "grass", 1881),
    (4342, "organic-gardeners-composting",
     "Organic Gardener's Composting",
     "Steve Solomon", "lib-rural",
     "A practical handbook on compost making, materials, fertility and the "
     "soil life that feeds a garden.",
     "seedling", "soil2", "grass", 1993),
    (4512, "gardening-without-irrigation",
     "Gardening Without Irrigation",
     "Steve Solomon", "lib-agriculture",
     "Dryland vegetable growing: moisture conservation, mulching and choosing "
     "crops where irrigation is not available.",
     "droplet", "sky", "grass", 1993),
    (29058, "a-new-orchard-and-garden",
     "A New Orchard and Garden",
     "William Lawson", "lib-rural",
     "An early English orchard and garden manual: planting, grafting, pruning "
     "and the making of a fruitful ground.",
     "tree", "grass2", "cream", 1618),

    # ------------------------------------------------------- preserving ---
    (13775, "every-step-in-canning-the-cold-pack-method",
     "Every Step in Canning: The Cold-Pack Method",
     "Grace Viall Gray", "lib-kitchen",
     "A complete home-canning course using the cold-pack method, with "
     "timetables for fruit, vegetables and meat.",
     "jar", "tomato2", "cream", 1919),
    (30441, "canned-fruit-preserves-and-jellies",
     "Canned Fruit, Preserves, and Jellies: Household Methods of Preparation",
     "Maria Parloa", "lib-kitchen",
     "A household guide to canning fruit, making preserves, jams and jellies, "
     "and keeping the results sound.",
     "jar", "plum", "cream", 1905),
    (59977, "canning-freezing-storing-garden-produce",
     "Canning, Freezing, Storing Garden Produce",
     "United States Department of Agriculture", "lib-kitchen",
     "USDA home-preservation directions for the garden surplus: canning, "
     "freezing, drying and cool storage.",
     "jar", "grass2", "sun", 1977),
    (66136, "home-canning-of-fruits-and-vegetables",
     "Home Canning of Fruits and Vegetables",
     "United States Department of Agriculture", "lib-kitchen",
     "The classic USDA bulletin on safe home canning of fruit and vegetables, "
     "including acid, processing times and spoilage.",
     "jar", "tomato", "cream", 1943),
    (48722, "making-fermented-pickles",
     "Making Fermented Pickles",
     "United States Department of Agriculture", "lib-kitchen",
     "A short government bulletin on salt-brine fermentation of cucumbers and "
     "other vegetables, with spoilage notes.",
     "jar", "grass3", "sun", 1944),
    (52551, "the-art-of-preserving-all-kinds-of-animal-and-vegetable-substances",
     "The Art of Preserving All Kinds of Animal and Vegetable Substances",
     "Nicolas Appert", "lib-kitchen",
     "Appert's foundational treatise on preserving food by heat in sealed "
     "containers, the beginning of modern canning.",
     "jar", "tomato2", "cream", 1812),
    (24510, "the-production-of-vinegar-from-honey",
     "The Production of Vinegar from Honey",
     "Gerard W. Bancks", "lib-kitchen",
     "A practical account of making vinegar from honey, with fermentation and "
     "equipment notes.",
     "jar", "sun2", "cream", 1912),
    (72394, "home-made-cider-vinegar",
     "Home-made Cider Vinegar",
     "United States Department of Agriculture", "lib-kitchen",
     "A farm bulletin on making cider vinegar at home, from juice to finished "
     "acid vinegar.",
     "jar", "brown", "sun", 1922),
    (44848, "a-little-preserving-book-for-a-little-girl",
     "A Little Preserving Book for a Little Girl",
     "Amy L. Waterman", "lib-kitchen",
     "A simple household preserving book for jams, jellies, pickles and "
     "stored fruit, written for beginners.",
     "jar", "plum", "cream", 1920),
    (71687, "the-art-and-mystery-of-curing-preserving-and-potting-meats",
     "The Art and Mystery of Curing, Preserving, and Potting All Kinds of Meats, Game, and Fish",
     "Anonymous", "lib-kitchen",
     "A nineteenth-century trade manual on dry-salting, pickling, potting and "
     "preserving meat, game and fish.",
     "meat", "tomato", "cream", 1860),
    (62859, "pork-slaughtering-cutting-preserving-and-cooking-on-the-farm",
     "Pork Slaughtering, Cutting, Preserving, and Cooking on the Farm",
     "H. Russell Cross and E. Curtis Green", "lib-kitchen",
     "A USDA farm guide to slaughtering, cutting, curing and cooking pork.",
     "meat", "pink", "cream", 1977),
    (62838, "lamb-slaughtering-cutting-preserving-and-cooking-on-the-farm",
     "Lamb Slaughtering, Cutting, Preserving, and Cooking on the Farm",
     "H. Russell Cross and E. Curtis Green", "lib-kitchen",
     "A USDA farm guide to slaughtering, cutting, preserving and cooking lamb.",
     "meat", "tomato2", "cream", 1977),
    (65020, "the-complete-distiller",
     "The Complete Distiller",
     "A. Cooper", "lib-kitchen",
     "An eighteenth-century distiller's manual covering fermentation, stills "
     "and the making of spirits and strong waters.",
     "jar", "brown", "cream", 1760),
    (65506, "certo-a-short-cut-to-better-jams-and-jellies",
     "Certo: A Short Cut to Better Jams and Jellies",
     "Anonymous", "lib-kitchen",
     "A small commercial recipe booklet for jams, jellies and marmalades made "
     "with fruit pectin.",
     "jar", "plum", "cream", 1930),

    # ---------------------------------------------------------- cattle ----
    (30310, "special-report-on-diseases-of-cattle",
     "Special Report on Diseases of Cattle",
     "United States Bureau of Animal Industry", "lib-livestock",
     "The federal veterinary reference on cattle disease: causes, symptoms, "
     "diagnosis and treatment, with plates.",
     "firstaid", "tomato2", "cream", 1908),
    (35258, "contagious-abortion-of-cows",
     "Contagious Abortion of Cows",
     "Ward J. MacNeal", "lib-livestock",
     "A scientific and practical study of brucellosis in cattle and the "
     "measures used to control it in a herd.",
     "firstaid", "tomato2", "sun", 1912),
    (62852, "how-to-select-cows",
     "How to Select Cows",
     "Willis P. Hazard", "lib-livestock",
     "The Guenon system of judging dairy cows, simplified and applied to "
     "selection for the dairy herd.",
     "cow", "brown", "cream", 1880),
    (43323, "hints-on-cheese-making",
     "Hints on Cheese-Making",
     "T. D. Curtis", "lib-kitchen",
     "A practical cheesemaker's manual for the dairyman, factoryman and "
     "manufacturer, from milk handling to the press.",
     "milk", "cream", "sun", 1890),
    (27975, "delineations-of-the-ox-tribe",
     "Delineations of the Ox Tribe",
     "George Vasey", "lib-livestock",
     "The natural history of bulls, bisons and buffaloes, with the known "
     "species and varieties of the genus Bos.",
     "cow", "soil2", "cream", 1851),
    (33972, "florida-an-ideal-cattle-state",
     "Florida: An Ideal Cattle State",
     "Florida State Live Stock Association", "lib-livestock",
     "A regional survey of cattle raising in Florida: climate, forage, breeds "
     "and the business of a southern herd.",
     "cow", "grass2", "sun", 1915),
    (66061, "the-story-of-milk",
     "The Story of Milk",
     "J. D. Frederiksen", "lib-livestock",
     "Milk from the cow to the dairy: composition, handling, cream, butter and "
     "the bacteriology of a clean supply.",
     "milk", "cream", "sky", 1914),
    (78261, "a-city-milk-and-cream-contest",
     "A City Milk and Cream Contest",
     "Clarence B. Lane", "lib-livestock",
     "A practical method for improving the milk supply through inspection, "
     "scoring and producer education.",
     "milk", "sky", "cream", 1914),
    (36645, "louisiana-beef-cattle",
     "Louisiana Beef Cattle",
     "William Carter Stubbs", "lib-livestock",
     "A regional beef-cattle bulletin on breeds, feeding, pastures and the "
     "economics of beef production in Louisiana.",
     "cow", "tomato", "grass", 1900),
    (50420, "history-of-the-beef-cattle-industry-in-illinois",
     "History of the Beef Cattle Industry in Illinois",
     "Frank Webster Farley", "lib-livestock",
     "The rise of the beef cattle trade in Illinois: breeds, feeding, markets "
     "and the industry that grew around them.",
     "cow", "brown", "cream", 1918),
    (62848, "beef-slaughtering-cutting-preserving-and-cooking-on-the-farm",
     "Beef Slaughtering, Cutting, Preserving, and Cooking on the Farm",
     "H. Russell Cross and E. Curtis Green", "lib-kitchen",
     "A USDA farm guide to slaughtering, cutting, preserving and cooking beef, "
     "written for the household that raises its own animal.",
     "meat", "tomato2", "cream", 1977),
    (58495, "secrets-of-meat-curing-and-sausage-making",
     "Secrets of Meat Curing and Sausage Making",
     "B. Heller & Co.", "lib-kitchen",
     "Curing hams, shoulders, bacon, corned beef and sausage, with the "
     "ingredient and handling rules of the trade.",
     "meat", "tomato", "sun", 1920),
    (63056, "home-canning-of-meat-and-poultry",
     "Home Canning of Meat and Poultry",
     "United States Agricultural Research Service", "lib-kitchen",
     "USDA directions for pressure canning meat and poultry safely at home.",
     "jar", "tomato2", "cream", 1944),
]
