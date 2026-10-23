"""The book archive catalogue.

Every entry is a real public domain title from Project Gutenberg. The seed
script pulls the plain-text edition, fingerprints it, and stores it in the
archive folder so the depot keeps working with no network at all.

    (gutenberg_id, slug, title, author, category, summary, motif, base,
     accent, year)
"""

from __future__ import annotations

GUTENBERG = "https://www.gutenberg.org"

#: Category slugs used by the archive shelves.
AGRICULTURE = "lib-agriculture"
LIVESTOCK = "lib-livestock"
MACHINERY = "lib-machinery"
RURAL = "lib-rural"

#: The library stays small on purpose: two books on each shelf.
#: The rest of the catalogue below is already downloaded and can be shown
#: later with ``python3 -m app.seed.run --all-books``.
CURATED: set[str] = {
    "the-farm-that-wont-wear-out",      # farming & soil
    "dry-farming",                      # farming & soil
    "cattle-and-their-diseases",         # livestock & animals
    "poultry-a-practical-guide",        # livestock & animals
    "farm-mechanics",                   # machinery & working horses
    "the-horse-shoe",                   # machinery & working horses
    "roman-farm-management",            # rural life & gardening
    "home-vegetable-gardening",         # rural life & gardening
}

BOOKS: list[tuple] = [
    (4525, "the-farm-that-wont-wear-out",
     "The Farm That Won't Wear Out",
     "Cyril G. Hopkins", AGRICULTURE,
     "The classic soil-fertility book. Hopkins explains how to feed the crop and "
     "the soil at the same time, and why a farm fed only with commercial fertiliser "
     "slowly starves itself.",
     "seedling", "grass", "soil", 1906),

    (4527, "the-story-of-the-soil",
     "The Story of the Soil",
     "Cyril G. Hopkins", AGRICULTURE,
     "Where soil comes from, how it is built by living things, and what destroys it. "
     "Written for farmers who wanted the biology as well as the recipe.",
     "seedling", "soil", "sun", 1911),

    (4924, "dry-farming",
     "Dry-Farming: A System of Agriculture for Countries under a Low Rainfall",
     "John A. Widtsoe", AGRICULTURE,
     "How to farm where the rain does not come: moisture conservation, the right "
     "crops, and the storage of water in the soil through a dry summer.",
     "wheat", "sun", "sky", 1920),

    (23682, "crops-and-methods-for-soil-improvement",
     "Crops and Methods for Soil Improvement",
     "Alva Agee", AGRICULTURE,
     "Rotation, cover crops and green manures - a practical programme for building "
     "fertility without buying it in a bag.",
     "wheat", "grass2", "cream", 1912),

    (25389, "right-use-of-lime-in-soil-improvement",
     "Right Use of Lime in Soil Improvement",
     "Alva Agee", AGRICULTURE,
     "Lime, its effect on the soil, how to test for the need, and how to apply it "
     "without wasting it. Pairs with any book on fertilisers.",
     "seedling", "silver", "sky", 1919),

    (20772, "agriculture-for-beginners",
     "Agriculture for Beginners",
     "Charles W. Burkett", AGRICULTURE,
     "The first farm textbook most American students ever read: soils, crops, "
     "livestock and farm management in one volume.",
     "book", "sky", "sun", 1903),

    (21022, "lessons-on-soil",
     "Lessons on Soil",
     "Edward J. Russell", AGRICULTURE,
     "Soil physics and soil chemistry in plain language - how a field holds water "
     "and why that decides what you can grow.",
     "seedling", "soil2", "sky", 1911),

    (12140, "roman-farm-management",
     "Roman Farm Management: The Treatises of Cato and Varro",
     "Marcus Porcius Cato and Marcus Terentius Varro", RURAL,
     "Cato and Varro on ploughing, grain, vines, cattle and the farm year, as "
     "translated in the Loeb edition. Two thousand years of practical advice from "
     "before the Roman empire.",
     "book", "brown", "cream", 1918),

    (22520, "cattle-and-cattle-breeders",
     "Cattle and Cattle-Breeders",
     "William S. McCombie", LIVESTOCK,
     "The history of our domesticated animals, the principles of breeding, and the "
     "breeds of cattle that make a living in Britain.",
     "cow", "tomato", "cream", 1911),

    (22771, "cattle-and-their-diseases",
     "Cattle and Their Diseases",
     "Robert Jennings", LIVESTOCK,
     "Symptoms, causes and treatment of cattle disease, written for the farmer who "
     "has to make the decision alone at four in the morning.",
     "firstaid", "tomato2", "cream", 1864),

    (37997, "the-american-reformed-cattle-doctor",
     "The American Reformed Cattle Doctor",
     "George H. Dadd", LIVESTOCK,
     "A mid-nineteenth century veterinary manual: recognising disease in the animal, "
     "preparing medicine, and looking after the young stock.",
     "firstaid", "tomato2", "sun", 1851),

    (26903, "determining-the-age-of-cattle-by-the-teeth",
     "Determining the Age of Cattle by the Teeth",
     "George W. Pope", LIVESTOCK,
     "Short and unbreakable: how to age a cow by looking in her mouth. Useful for "
     "anyone buying or selling stock.",
     "cow", "brown", "sun", 1919),

    (38189, "a-treatise-on-sheep",
     "A Treatise on Sheep",
     "Ambrose Blacklock", LIVESTOCK,
     "The best means for the improvement of sheep, their breeds, their management "
     "and the diseases that affect them.",
     "hay", "brown", "cream", 1853),

    (38995, "the-sheep-and-lamb",
     "The Sheep and Lamb",
     "Thomas Miller", LIVESTOCK,
     "An old shepherd's book on the care of sheep and lambs, from the rearing of "
     "the lambs to the shearing and the sale.",
     "hay", "soil", "cream", 1871),

    (39205, "sheep-swine-and-poultry",
     "Sheep, Swine, and Poultry",
     "Robert Jennings", LIVESTOCK,
     "History and varieties of each, with the practical management of all three on "
     "a mixed farm.",
     "hay", "orange", "cream", 1864),

    (38606, "poultry-a-practical-guide",
     "Poultry: A Practical Guide to the Choice, Breeding, Rearing and Management of Fowls",
     "Hugh Piper", LIVESTOCK,
     "Poultry keeping from scratch: choosing breeds, housing, brooding, feeding "
     "and the management of a laying flock.",
     "chicken", "sun2", "cream", 1911),

    (13254, "the-dollar-hen",
     "The Dollar Hen",
     "Milo S. Hastings", LIVESTOCK,
     "A practical guide to making money from poultry - how to buy, feed, breed and "
     "sell a flock that pays for itself.",
     "chicken", "sun", "tomato", 1911),

    (34175, "domestic-animals",
     "Domestic Animals: History and Description of the Horse, Mule, Cattle, Sheep, Swine and Goats",
     "Richard Lamb Allen", LIVESTOCK,
     "The standard nineteenth century reference on the farm animals of Britain: "
     "history, breeds, husbandry and management.",
     "cow", "grass2", "cream", 1865),

    (67477, "bee-keeping-for-the-many",
     "Bee-keeping for the Many",
     "J. H. Payne", LIVESTOCK,
     "A practical guide to keeping bees in common and Ligurian hives - the sort of "
     "book that got a hundred farm workers into the hobby.",
     "hay", "sun", "grass", 1883),

    (11204, "diseases-of-the-horses-foot",
     "Diseases of the Horse's Foot",
     "H. Caulton Reeks", MACHINERY,
     "The complete treatment of foot troubles in the working horse, from thrush and "
     "corns to the conditions that end a career.",
     "tool", "grey2", "cream", 1906),

    (39791, "farm-mechanics",
     "Farm Mechanics: Machinery and Its Use to Save Hand Labor on the Farm",
     "Herbert A. Shearer", MACHINERY,
     "An illustrated guide to farm machinery - ploughs, mowers, binders, wagons - "
     "and the upkeep each one needs.",
     "engine", "sky2", "sun", 1918),

    (13978, "the-horse-shoe",
     "The Horse Shoe",
     "Edward G. Flight", MACHINERY,
     "The horse shoe from the black smith's point of view: its history, its forms "
     "and its making. Half of this applies to good shoeing practice today.",
     "tool", "silver", "sky", 1871),

    (38321, "economy-of-the-round-dairy-barn",
     "Economy of the Round Dairy Barn",
     "Wilber J. Fraser", MACHINERY,
     "Why the round barn was built the way it was, and what a well set up dairy "
     "building does for the labour of milking.",
     "milk", "silver", "cyan", 1910),

    (77164, "walks-and-talks-of-an-american-farmer-in-england",
     "Walks and Talks of an American Farmer in England (Part 1 of 2)",
     "Frederick Law Olmsted", RURAL,
     "An American farmer tours English farming and asks awkward questions about "
     "why it is done differently. Part one of two.",
     "wheat", "grass", "sky", 1852),

    (16594, "a-short-history-of-english-agriculture",
     "A Short History of English Agriculture",
     "W. H. R. Curtler", RURAL,
     "From the open field system to the enclosures and after: how English farming "
     "actually changed, and why.",
     "book", "brown", "cream", 1909),

    (22973, "the-english-husbandman",
     "The English Husbandman",
     "Gervase Markham", RURAL,
     "Markham's husbandry manual, first published in the 1630s. Direct, opinionated "
     "and still readable.",
     "wheat", "soil2", "sun", 1613),

    (57457, "the-book-of-husbandry",
     "The Book of Husbandry",
     "Anthony Fitzherbert", RURAL,
     "One of the most influential agricultural books ever written, and the reason "
     "English farming looks the way it does.",
     "book", "orange", "cream", 1534),

    (7123, "home-vegetable-gardening",
     "Home Vegetable Gardening",
     "F. F. Rockwell", RURAL,
     "Growing your own vegetables from planning the plot to putting up the crop. "
     "Still the most readable vegetable book in English.",
     "seedling", "grass3", "soil", 1931),

    (9550, "manual-of-gardening",
     "Manual of Gardening",
     "L. H. Bailey", RURAL,
     "Bailey's practical manual of plant growing, written for the gardener who "
     "wants a result rather than a theory.",
     "seedling", "teal", "cream", 1910),

    (27778, "outlines-of-dairy-bacteriology",
     "Outlines of Dairy Bacteriology",
     "H. L. Russell", LIVESTOCK,
     "The bacteria that matter in milk, where they come from, and how to keep them "
     "out of the churn.",
     "milk", "cyan", "cream", 1907),
]
