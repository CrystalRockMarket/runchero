"""Repair and equipment coverage: every kind and brand a farm is likely to meet.

Most entries are menu placeholders. The depot only shows a record when one has
been filed in the database; a brand with no models still gets a page so the
structure is ready for manuals, notes and specifications later.
"""
from __future__ import annotations

TRACTOR_BRANDS = [
    "AGCO", "Agria", "Aebi", "Allgaier", "Allis-Chalmers", "Antonio Carraro",
    "BCS", "Belarus (MTZ)", "Bolens", "Bolinder-Munktell", "Branson", "Case",
    "Case IH", "Challenger", "Chamberlain", "Claas", "Cockshutt", "County",
    "David Brown", "Daedong", "Deutz", "Deutz-Fahr", "Ebro", "Eicher",
    "Farmall", "Farmtrac", "Fendt", "Ferguson", "Fiat", "Foton", "Ford",
    "Fordson", "Goldoni", "Gravely", "Hako", "Hinomoto", "Holder", "Hurlimann",
    "IMT", "International Harvester", "Iseki", "JCB", "J.I. Case", "John Deere",
    "Kioti", "Kramer", "Kubota", "Lamborghini", "Landini", "Leyland", "Lindner",
    "LS", "Mahindra", "Marshall", "Massey Ferguson", "Massey-Harris",
    "McCormick", "Minneapolis-Moline", "Mitsubishi", "New Holland", "Nuffield",
    "Oliver", "Pasquali", "Porsche", "Renault", "Ransomes", "Same", "Satoh",
    "Shibaura", "Sonalika", "Steyr", "Swaraj", "Tafe", "TYM", "Universal",
    "Ursus", "Valmet", "Valtra", "Valpadana", "Versatile", "Volvo", "White",
    "Yanmar", "Zetor",
]

COMBINE_BRANDS = [
    "AGCO", "Allis-Chalmers", "Bizon", "Case", "Case IH", "Claas",
    "Cockshutt", "Deutz-Fahr", "Fendt", "Fortschritt", "Gleaner", "Grimme",
    "Horsch", "International Harvester", "John Deere", "Kubota", "Laverda",
    "Lely", "Lovol", "Massey Ferguson", "McCormick", "Minneapolis-Moline",
    "New Holland", "Oliver", "Rostselmash", "Sampo", "SAME", "Versatile",
    "Volvo", "White", "Yanmar", "Zoomlion",
]

TELEHANDLER_BRANDS = [
    "Bobcat", "Case", "Caterpillar", "Claas", "Dieci", "Faresin", "Gehl",
    "Genie", "Haulotte", "JCB", "JLG", "John Deere", "Kramer", "Liebherr",
    "Lull", "Magni", "Manitou", "Merlo", "Mustang", "New Holland", "Pettibone",
    "Schäffer", "Sennebogen", "Skyjack", "Terex", "Wacker Neuson", "Weidemann",
]

LOADER_BRANDS = [
    "ASV", "Avant", "Bobcat", "Boxer", "Case", "Caterpillar", "Ditch Witch",
    "Doosan", "Fermec", "Ford", "Gehl", "Giant", "Hitachi", "Huddig",
    "Hydrema", "Hyundai", "IHI", "JCB", "John Deere", "Kanga", "Kawasaki",
    "Komatsu", "Kubota", "Liebherr", "Manitou", "Mustang", "New Holland",
    "Schäffer", "Takeuchi", "Terex", "Thomas", "Venieri", "Volvo",
    "Wacker Neuson", "Weidemann", "Yanmar",
]

EXCAVATOR_BRANDS = [
    "Airman", "Bobcat", "Case", "Caterpillar", "Doosan", "Eurocomach",
    "Hitachi", "Hyundai", "IHI", "JCB", "John Deere", "Kato", "Kobelco",
    "Komatsu", "Kubota", "Liebherr", "Link-Belt", "LiuGong", "Mecalac", "Sany",
    "Sumitomo", "Sunward", "Takeuchi", "Terex", "Volvo", "Wacker Neuson",
    "XCMG", "Yanmar", "Yuchai", "Zoomlion",
]

CRAWLER_BRANDS = [
    "Allis-Chalmers", "Case", "Caterpillar", "Challenger", "Dressta",
    "Fiat-Allis", "Hanomag", "Hitachi", "International Harvester", "John Deere",
    "Komatsu", "Liebherr", "LiuGong", "Massey Ferguson", "New Holland",
    "Oliver", "Sany", "Shantui", "Stal", "Terex", "Volvo", "XCMG",
    "Zettelmeyer", "Zoomlion",
]

ATV_BRANDS = [
    "Access", "Adly", "Aeon", "Alpha Sports", "Apollo", "Arctic Cat",
    "Barossa", "Bennche", "Bombardier", "BRP", "Can-Am", "Cectek", "CFMOTO",
    "Coleman", "DRR", "E-Ton", "Goes", "Hammerhead", "Honda", "Hisun",
    "John Deere", "Kasea", "Kawasaki", "Kubota", "Kymco", "Linhai", "Massimo",
    "Odes", "PGO", "Polaris", "Segway", "Suzuki", "SYM", "Tao Motor",
    "Textron", "TGB", "TrailMaster", "Yamaha",
]

UTV_BRANDS = [
    "Arctic Cat", "Bennche", "Bobcat", "BRP", "Can-Am", "Case", "CFMOTO",
    "Club Car", "Cushman", "Daihatsu", "E-Z-GO", "Ford", "Gravely", "Honda",
    "Hisun", "Isuzu", "JCB", "John Deere", "Kawasaki", "Kioti", "Kubota",
    "Kymco", "Land Rover", "Mahindra", "Massimo", "Mitsubishi", "New Holland",
    "Odes", "Piaggio", "Polaris", "Suzuki", "Textron", "Toro", "Toyota",
    "Yamaha", "Yanmar",
]

TRUCK_BRANDS = [
    "Ashok Leyland", "Autocar", "Avia", "BharatBenz", "BYD", "Chevrolet",
    "Chery", "Citroën", "Dacia", "DAF", "Daihatsu", "Dodge", "Eicher",
    "Fiat", "Ford", "Foton", "Freightliner", "GAZ", "GMC", "Great Wall",
    "GWM", "Hino", "Hyundai", "International", "Isuzu", "Iveco", "JAC",
    "Jeep", "JMC", "Kamaz", "Kenworth", "Kia", "Land Rover", "LDV", "Liaz",
    "Mack", "MAN", "Maxus", "Mazda", "Mercedes-Benz", "Mitsubishi",
    "Mitsubishi Fuso", "Nissan", "Opel", "Peugeot", "Peterbilt", "Praga",
    "RAM", "Renault", "Rivian", "Scania", "SsangYong", "Sterling", "Subaru",
    "Suzuki", "Tata", "Tatra", "Tesla", "Toyota", "UD", "Ural", "Vauxhall",
    "Volkswagen", "Volvo", "Western Star", "ZIL",
]

TRAILER_BRANDS = [
    "ACE", "Agriquip", "Al-Ko", "Anssems", "Bailey", "Bateson", "Böckmann",
    "Bradley", "Brenderup", "Brian James", "Cooks", "Debon", "Flatbed",
    "Futura", "Graham Edwards", "Gull", "Hudson", "Humbaur", "Ifor Williams",
    "Indespension", "K-Two", "Knott", "Marston", "McCauley", "Meredith & Eyre",
    "Metaltech", "Nugent", "Palmse", "Portequip", "Pronar", "Respo", "Saris",
    "Stewart", "Tickners", "Tuffmac", "Unsinn", "Walsh", "Wessex",
    "Westfalia", "Woodford", "Wylie",
]

MOWER_BRANDS = [
    "Allett", "Ariens", "Atco", "Bad Boy", "Baroness", "Billy Goat", "Bob-Cat",
    "Bolens", "Bosch", "Bunton", "Castelgarden", "Claas", "Club Car", "Cobra",
    "Country Clipper", "Craftsman", "Cub Cadet", "Cushman", "Dennis", "DeWalt",
    "Dixie Chopper", "EGO", "Einhell", "E-Z-GO", "Exmark", "Ferris", "Flymo",
    "Ford", "Gardena", "Gravely", "Greenworks", "Grasshopper", "Hayter",
    "Honda", "Husqvarna", "Hustler", "Hyundai", "Iseki", "Jacobsen",
    "John Deere", "Kawasaki", "Kobalt", "Kubota", "Lawn-Boy", "Lesco",
    "Makita", "Masport", "Mountfield", "MTD", "Murray", "New Holland",
    "ParkerBrand", "Qualcast", "Ransomes", "Rover", "Ryobi", "Scag",
    "Simplicity", "Spartan", "Stiga", "STIHL", "Toro", "Troy-Bilt", "Victa",
    "Walker", "Webb", "Worx", "Wright", "Yanmar", "Yard Machines",
]

FORESTRY_BRANDS = [
    "Alstor", "Bandit", "Caterpillar", "Cranab", "Eco Log", "Epsilon", "FTG",
    "Hitachi", "Hultdins", "Husqvarna", "Iron Baltic", "John Deere", "Kesla",
    "Komatsu", "Kranman", "Loglift", "Logset", "Malwa", "Moheda", "Palfinger",
    "Palms", "Ponsse", "Rottne", "STIHL", "Terri", "Tigercat", "Timberjack",
    "Valmet", "Vimek", "Welte",
]

IMPLEMENT_BRANDS = [
    "Amazone", "Bednar", "Bourgault", "BvL", "Brillion", "Case IH", "Claas",
    "Dalbo", "DeLaval", "Deutz-Fahr", "Dairymaster", "Einböck", "Fendt",
    "Flexi-Coil", "Fullwood", "GEA", "Great Plains", "Gregoire-Besson",
    "Horsch", "John Deere", "Keenan", "Kockerling", "Köckerling", "Krone",
    "Kuhn", "Kverneland", "Landoll", "Lemken", "Lely", "Mandako", "McHale",
    "McFarlane", "Meyer", "Milkline", "Morris", "New Holland", "Overum",
    "Pöttinger", "Rite Way", "Seed Hawk", "Siloking", "Simba", "Strautmann",
    "Sunflower", "Summers", "Trioliet", "Vaderstad", "Vermeer", "Vicon",
    "Welger", "Westfalia",
]

CHAINSAW_BRANDS = [
    "Alpina", "Bluebird", "Bosch", "Castelgarden", "Clarke", "Craftsman",
    "DeWalt", "Dolmar", "Draper", "Echo", "Efco", "EGO", "Einhell",
    "Greenworks", "Hitachi", "Honda", "Homelite", "Husqvarna", "Hyundai",
    "Jonsered", "Kawasaki", "Kobalt", "Makita", "Maruyama", "McCulloch",
    "Metabo", "Milwaukee", "Oleo-Mac", "ParkerBrand", "Partner", "Pellenc",
    "Poulan", "Poulan Pro", "RedMax", "Ryobi", "Scheppach", "Sealey",
    "Shindaiwa", "Solo", "STIHL", "Tanaka", "Titan", "Timberpro", "Worx",
    "Yamaha",
]

SMALL_ENGINE_BRANDS = [
    "Alpina", "Bahco", "Billy Goat", "Bosch", "Castelgarden", "Clarke", "Cobra",
    "DeWalt", "Dolmar", "Draper", "Echo", "Efco", "EGO", "Einhell", "Fiskars",
    "Gardena", "Greenworks", "Hitachi", "Honda", "Hozelock", "Husqvarna",
    "Hyundai", "Jonsered", "Kawasaki", "Makita", "Milwaukee", "Oleo-Mac",
    "ParkerBrand", "RedMax", "Ryobi", "Scheppach", "Sealey", "Shindaiwa",
    "Silverline", "Solo", "STIHL", "Tanaka", "Titan", "Toro", "Wolf-Garten",
    "Worx", "Yamaha",
]

GENERATOR_BRANDS = [
    "Atlas Copco", "Bauweg", "Briggs & Stratton", "Champion", "Clarke",
    "Cummins", "Deutz", "Doosan", "Draper", "DuroMax", "Einhell", "Firman",
    "Generac", "Gesan", "Himoinsa", "Honda", "Hyundai", "Ingersoll Rand",
    "Isuzu", "John Deere", "Kohler", "Kubota", "Lister", "MacGen", "Mase",
    "Mitsubishi", "Onan", "ParkerBrand", "Perkins", "Petter", "Pramac",
    "Predator", "Pulsar", "SDMO", "Sealey", "Scheppach", "Sportsman",
    "Stephill", "Titan", "VISA", "Volvo Penta", "Wen", "Westinghouse",
    "Yamaha", "Yanmar",
]

PRESSURE_WASHER_BRANDS = [
    "Annovi Reverberi", "Bertolini", "Bosch", "Briggs & Stratton", "Cat Pumps",
    "Clarke", "Comet", "Craftsman", "DeWalt", "Draper", "EGO", "Einhell",
    "General Pump", "Generac", "Giant", "Greenworks", "Hawk", "Honda",
    "Husqvarna", "Hyundai", "Interpump", "Karcher", "Kobalt", "Kranzle",
    "MacAllister", "Makita", "Milwaukee", "Nilfisk", "ParkerBrand", "Ryobi",
    "Scheppach", "Sealey", "Simpson", "Speck", "STIHL", "Titan", "Udor",
    "Vax", "Worx", "Yamaha",
]

LOG_SPLITTER_BRANDS = [
    "Al-ko", "Atika", "Balfor", "Binderberger", "Boss Industrial", "Brave",
    "Brown", "Champion", "Clarke", "CountyLine", "Cramer", "Craftsman",
    "Cub Cadet", "Dirty Hand Tools", "Draper", "Earthquake", "Eastonmade",
    "Efco", "Einhell", "Forest Master", "Generac", "Gude", "Handy", "Husqvarna",
    "Hyundai", "Iron & Oak", "Jansen", "Kretzer", "Lumag", "MTD", "Oleo-Mac",
    "Oxdale", "ParkerBrand", "Posch", "Powerhouse", "Ramsplitter",
    "Rock Machinery", "Scheppach", "Sealey", "Solo", "Split-Fire", "STIHL",
    "Sun Joe", "Supersplit", "Swisher", "Titan", "Toro", "Troy-Bilt",
    "Wallenstein", "WEN", "Wolfe Ridge", "Yard Machines", "Zipper",
]

CHIPPER_BRANDS = [
    "Bandit", "Bear Cat", "Billy Goat", "Bosch", "Brush Master", "Champion",
    "Clarke", "Craftsman", "Cub Cadet", "DeWalt", "Dirty Hand Tools", "Draper",
    "Earthquake", "Eliet", "Einhell", "Forest Master", "Forst", "Generac",
    "GreenMech", "Handy", "Honda", "Husqvarna", "Hyundai", "Japa", "Jensen",
    "Kretzer", "Linddana", "Lumag", "MacAllister", "Makita", "Morbark", "MTD",
    "ParkerBrand", "Posch", "Powerhouse", "Ryobi", "Scheppach", "Schliesing",
    "Sealey", "STIHL", "Sun Joe", "Titan", "Toro", "TP", "Troy-Bilt",
    "Vermeer", "Wallenstein", "WEN", "Worx", "Yard Machines", "YARDMAX",
]

STUMP_GRINDER_BRANDS = [
    "Bandit", "Barreto", "Billy Goat", "Bluebird", "Bobcat", "Carlton",
    "Caterpillar", "Dosko", "Echo", "Fecon", "Husqvarna", "Hydra-Mac",
    "J.P. Carlton", "John Deere", "Kanga", "Kubota", "Morbark", "Olathe",
    "Predator", "Rayco", "Roken", "STIHL", "Stump Master", "Takeuchi", "Toro",
    "Torrent", "Vermeer", "Wallenstein", "Yanmar",
]

TILLER_BRANDS = [
    "AgriArgo", "Agria", "Alpego", "Alpina", "Antonio Carraro", "Barbieri",
    "BCS", "Berti", "Bosch", "Celli", "Champion", "Craftsman", "Del Morino",
    "DeWalt", "Dowdeswell", "Draper", "Earthquake", "Efco", "Einhell", "Falc",
    "Ferrari", "Firman", "Gardena", "Goldoni", "Grillo", "Honda", "Howard",
    "Husqvarna", "Hyundai", "Iseki", "Kubota", "Kuhn", "Makita", "Mantis",
    "Maschio", "Maxim", "Merry Tiller", "Milwaukee", "Mountfield",
    "Muratori", "Oleo-Mac", "ParkerBrand", "Pasquali", "Powermate", "Predator",
    "Ryobi", "Scheppach", "Sicma", "Stiga", "Tarantula", "Titan", "Troy-Bilt",
    "Wolf-Garten", "Yamaha", "Yanmar",
]

WATER_PUMP_BRANDS = [
    "Aermotor", "Atlas Copco", "Berkeley", "Briggs & Stratton", "Calpeda",
    "Champion", "DAB", "Davey", "DuroMax", "Ebara", "Firman", "Flint & Walling",
    "Flotec", "Flygt", "Franklin", "Generac", "Goulds", "Grindex", "Grundfos",
    "Hatz", "Homa", "Honda", "Karcher", "Kohler", "Kubota", "Liberty",
    "Little Giant", "Lowara", "Monarch", "Myers", "Nilfisk", "Onga",
    "Pedrollo", "Predator", "Pulsar", "Robin", "Simer", "Sportsman", "Sta-Rite",
    "Subaru", "Superior Pump", "Tsurumi", "Tsunami", "Wacker Neuson",
    "Waterax", "Wayne", "Weda", "Wen", "Westinghouse", "Yamaha", "Yanmar",
    "Zoeller",
]

HAND_TOOL_BRANDS = [
    "Amtech", "Axminster", "Bahco", "Bergen", "Beta", "Bosch", "Bowers",
    "Brown & Sharpe", "Charnwood", "Clarke", "Cornwell", "Craftsman", "Dasqua",
    "DeWalt", "DMT", "Draper", "Estwing", "Eze-Lap", "Facom", "Faithfull",
    "Festool", "Fiskars", "Fowler", "Gedore", "Hazet", "Hilka", "Hilti",
    "Incra", "Irwin", "Knipex", "Kobalt", "Kroeplin", "Lansky", "Laser",
    "Leatherman", "Mac Tools", "Makita", "Marples", "Matco", "Metabo",
    "Milwaukee", "Mitutoyo", "Moore & Wright", "Neilsen", "Neo Tools",
    "Parkside", "Proto", "Record", "Rolson", "Roughneck", "Scheppach",
    "Sealey", "Silverline", "SK Hand Tools", "Smith's", "Snap-on", "Stahlwille",
    "Stanley", "Starrett", "Teng Tools", "TESA", "Topex", "Tormek", "USAG",
    "Vaughan", "Victorinox", "Wera", "Wiha", "Woodpeckers", "Work Sharp",
    "Yato",
]

POWER_TOOL_BRANDS = [
    "AEG", "Axminster", "Black+Decker", "Bosch", "Charnwood", "Clarke",
    "Craftsman", "DeWalt", "Draper", "Dremel", "EGO", "Einhell", "Erbauer",
    "Evolution", "Fein", "Festool", "Flex", "Freud", "Greenworks", "HiKOKI",
    "Hitachi", "Hilti", "Kobalt", "Lamello", "Lumberjack", "Mafell", "Makita",
    "Metabo", "Milwaukee", "Panasonic", "Parkside", "Porter-Cable", "Proxxon",
    "Record Power", "Ridgid", "Ryobi", "Scheppach", "Sealey", "Senco",
    "Silverline", "Skil", "Stanley", "STIHL", "Titan", "Trend", "Triton",
    "Virutex", "Worx", "Bostitch", "Paslode",
]

AIR_TOOL_BRANDS = [
    "Aircat", "Apex", "Astro Pneumatic", "Atlas Copco", "ATS", "Buckeye",
    "Campbell Hausfeld", "Central Pneumatic", "Chicago Pneumatic", "Cleco",
    "Cooper", "Cornwell", "Desoutter", "Dotco", "Earthquake", "Florida Pneumatic",
    "Fuji", "General", "Husky", "Ingersoll Rand", "Kobalt", "Mac Tools",
    "Makita", "Matco", "Metabo", "Neiko", "NitroCat", "Nitto Kohki",
    "Paslode", "Porter-Cable", "Pro-Tek", "Ridgid", "Senco", "Sioux",
    "Snap-on", "SP Air", "Sunex", "Taylor", "Thunder", "Tooluxe",
    "Universal Tool", "Uryu", "Valu-Air", "Wynnsky",
]

WELDER_BRANDS = [
    "AHP", "Amico", "Andeli", "Campbell Hausfeld", "Cebora", "Century",
    "Chicago Electric", "Clarke", "Deca", "Draper", "Eastwood", "Einhell",
    "ESAB", "Everlast", "EWM", "Fimer", "Forney", "Fronius", "GYS", "Harris",
    "Hitbox", "Hobart", "HTP", "Hypertherm", "Jasic", "Kemppi", "Lincoln Electric",
    "Longevity", "Lorch", "Lotos", "Magmate", "Migatronic", "Miller",
    "Oerlikon", "Parweld", "Primeweld", "Razorweld", "Rehm", "Riland",
    "Scheppach", "Sealey", "SIP", "Stahlwerk", "Suncity", "Telwin",
    "Thermal Arc", "Titanium", "Tweco", "Vulcan", "Welbach", "Yeswelder",
]

COMPRESSOR_BRANDS = [
    "Aerzen", "Almig", "Atlas Copco", "Boge", "California Air Tools",
    "Campbell Hausfeld", "Champion", "Chicago Pneumatic", "Clarke", "CompAir",
    "Craftsman", "DeWalt", "Draper", "Eaton", "Einhell", "Emax", "FS-Curtis",
    "Gardner Denver", "Hertz", "Hitachi", "Husky", "Hydrovane", "Ingersoll Rand",
    "Jenny", "Kaeser", "Kellogg", "Kobalt", "LeRoi", "Makita", "Mattei",
    "Metabo", "Polar Air", "Porter-Cable", "Quincy", "Scheppach", "Sealey",
    "SIP", "Speedaire", "Sullair", "Wolf", "Worthington",
]

BENCH_MACHINERY_BRANDS = [
    "Axminster", "Bosch", "Charnwood", "Clarke", "Craftsman", "Delta", "DeWalt",
    "Draper", "Einhell", "Evolution", "Femi", "Festool", "Grizzly", "Holzmann",
    "Jet", "Kity", "Laguna", "Lumberjack", "Makita", "Metabo", "Milwaukee",
    "Optimum", "Parkside", "Powermatic", "Proxxon", "Record Power", "Rikon",
    "Ryobi", "Scheppach", "Sealey", "Silverline", "SIP", "Titan", "Triton",
    "Wen", "Wilton", "Woodpeckers", "Work Sharp",
]

LIFTING_BRANDS = [
    "Axminster", "Bahco", "Beaver", "Clarke", "CM", "Columbus McKinnon",
    "Draper", "Farm Jack", "Harrington", "Hi-Lift", "JET", "Kito",
    "Machine Mart", "Record", "Sealey", "SIP", "Stanley", "Tiger", "Wilton",
    "Yale",
]

MEASURING_BRANDS = [
    "Bahco", "Bosch", "Bowers", "Brown & Sharpe", "Craftsman", "Dasqua",
    "DeWalt", "Draper", "Empire", "Fisco", "Fowler", "Hultafors", "Husky",
    "Incra", "Irwin", "Johnson", "Kobalt", "Kroeplin", "Laser", "Lie-Nielsen",
    "Makita", "Milwaukee", "Mitutoyo", "Moore & Wright", "Neo Tools", "Record",
    "Sealey", "Shinwa", "Stanley", "Starrett", "Swanson", "TESA", "Topex",
    "Trend", "Veritas", "Vorel", "Woodpeckers", "Yato",
]

FASTENER_BRANDS = [
    "Arrow", "Bosch", "Bostitch", "DeWalt", "Einhell", "Fischer", "Hilti",
    "HiKOKI", "Makita", "Milwaukee", "Novus", "Paslode", "Porta-Nails",
    "Powernail", "Primatech", "Rapesco", "Rapid", "Rawlplug", "Rexel",
    "Ryobi", "Senco", "Simpson Strong-Tie", "Spit", "Stanley",
    "Stanley Bostitch", "Swingline", "Tacwise",
]

PAINT_BRANDS = [
    "3M", "Anest Iwata", "Apollo", "Bosch", "Brewers", "Briwax", "Chestnut",
    "Crown", "Cuprinol", "DeVilbiss", "DeWalt", "Dulux", "Earlex", "Epifanes",
    "Festool", "Fiddes", "Fuji", "Graco", "Hamilton", "Hammerite", "Harris",
    "HVLP", "International", "Johnstone's", "Krylon", "Leyland", "Liberon",
    "Makita", "Milwaukee", "Osmo", "Plasti-Kote", "Polyvine", "Purdy",
    "Ronseal", "Rust-Oleum", "Rustins", "Sadolin", "SATA", "Scotch", "Titan",
    "Wagner", "Wooster",
]

PLUMBING_BRANDS = [
    "Aqualisa", "Armitage Shanks", "Bahco", "Baxi", "Bosch", "Clarke", "DeWalt",
    "Dickie Dyer", "Draper", "Geberit", "Glow-worm", "Grant", "Grohe",
    "Hansgrohe", "Hep2O", "Hilti", "Ideal", "Ideal Standard", "JG Speedfit",
    "Knipex", "Makita", "Metabo", "Milwaukee", "Mira", "Monument", "Polypipe",
    "Potterton", "Record", "Rehau", "Ridgid", "Rothenberger", "Sealey",
    "SIP", "Stanley", "Triton", "Twyford", "Uponor", "Vaillant", "Viega",
    "Viessmann", "Wavin", "Wera", "Worcester", "Worcester Bosch",
]

ELECTRICAL_BRANDS = [
    "ABB", "BG", "Bosch", "Chauvin Arnoux", "Clarke", "Contactum", "Crabtree",
    "Danfoss", "DeWalt", "Di-Log", "Draper", "Drayton", "Eaton", "Extech",
    "Fluke", "Hager", "Honeywell", "Horstmann", "Ideal", "Kewtech", "Klein Tools",
    "Knipex", "Legrand", "Makita", "Martindale", "Megger", "MEM", "Metabo",
    "Metrel", "Milwaukee", "MK", "Sangamo", "Schneider", "Seaward", "Sealey",
    "Siemens", "SIP", "Stanley", "Timeguard", "Tower", "Volex", "Wera",
    "Wiha", "Wylex",
]

GARDEN_TOOL_BRANDS = [
    "Allett", "Atco", "Bahco", "Bosch", "Bulldog", "Castelgarden", "Cobra",
    "DeWalt", "Dennis", "Draper", "Echo", "Einhell", "Felco", "Fiskars",
    "Flymo", "Gardena", "Hayter", "Honda", "Hozelock", "Husqvarna", "Hyundai",
    "Karcher", "Kawasaki", "Lawnflite", "Makita", "Milwaukee", "Mountfield",
    "Nilfisk", "ParkerBrand", "Qualcast", "Ransomes", "Ryobi", "Scheppach",
    "Sealey", "Sisis", "Spear & Jackson", "Stanley", "Stiga", "STIHL", "Titan",
    "Toro", "Webb", "Wilkinson Sword", "Wolf-Garten", "Yamaha",
]

WHEELBARROW_BRANDS = [
    "Ames", "Ariens", "Bosch", "Bulldog", "Clarke", "Craftsman", "DeWalt",
    "Draper", "Fiskars", "Gardena", "Gorilla", "Haemmerlin", "Hozelock",
    "Husky", "Jackson", "Kobalt", "Makita", "Milwaukee", "Sealey",
    "Silverline", "Spear & Jackson", "Stanley", "Toro", "True Temper", "Union",
    "Walsall", "Wolf-Garten",
]

PRUNING_BRANDS = [
    "ARS", "Bahco", "Bosch", "Corona", "DeWalt", "Draper", "Echo", "Einhell",
    "Felco", "Fiskars", "Gardena", "Hattori", "Honda", "Husqvarna", "Hyundai",
    "Kanzawa", "Kawasaki", "Makita", "Milwaukee", "Niwsaki", "Okatsune",
    "ParkerBrand", "Ryobi", "Scheppach", "Sealey", "Silky", "Spear & Jackson",
    "Stanley", "STIHL", "Titan", "Tobisho", "Wilkinson Sword", "Wolf-Garten",
    "Yamaha",
]

WATERING_BRANDS = [
    "Antelco", "Bosch", "Chapin", "Claber", "Clarke", "DeWalt", "Dramm",
    "Draper", "DripWorks", "Einhell", "Fiskars", "Gardena", "Gilmour", "Holman",
    "Honda", "Hozelock", "Hudson", "Hunter", "Hyundai", "Irritec", "Jain",
    "Karcher", "Makita", "Melnor", "Netafim", "Neta", "Nilfisk", "Orbit",
    "ParkerBrand", "Rain Bird", "Ryobi", "Scheppach", "Sealey", "Silverline",
    "Solo", "Spear & Jackson", "Titan", "Toro", "Wolf-Garten",
]

GROUPS = [
    {
        "slug": "vehicles",
        "name": "Vehicles & Machinery",
        "icon": "tractor",
        "blurb": "Tractors, harvesters, handlers, earthmovers, quads, trucks, "
                 "trailers and mowers. Every brand gets a slot, with records "
                 "added as manuals and specifications are filed.",
        "kinds": ["tractor", "combine", "telehandler", "loader", "excavator",
                  "crawler", "atv", "utv", "truck", "trailer", "mower",
                  "forestry"],
    },
    {
        "slug": "implements",
        "name": "Field Implements & Attachments",
        "icon": "wheat",
        "blurb": "Ploughs, harrows, drills, sprayers, balers, hay tools, slurry "
                 "kit, grain handling and irrigation. The working end of the farm.",
        "kinds": ["machine", "plough", "harrow", "seed-drill", "sprayer",
                  "baler", "hay-tools", "slurry", "grain-handling", "irrigation"],
    },
    {
        "slug": "outdoor",
        "name": "Outdoor Power & Small Engines",
        "icon": "saw",
        "blurb": "Chainsaws, brushcutters, blowers, generators, pressure washers, "
                 "log splitters, chippers, tillers and pumps.",
        "kinds": ["chainsaw", "brushcutter", "hedge-trimmer", "leaf-blower",
                  "generator", "pressure-washer", "log-splitter", "wood-chipper",
                  "stump-grinder", "tiller", "water-pump"],
    },
    {
        "slug": "workshop",
        "name": "Workshop Tools & Equipment",
        "icon": "wrench",
        "blurb": "Hand tools, power tools, air tools, welders, compressors, "
                 "bench machinery, lifting, measuring, fasteners, paint, "
                 "plumbing and electrical tools.",
        "kinds": ["hand-tools", "power-tools", "air-tools", "welder",
                  "compressor", "bench-machinery", "lifting", "measuring",
                  "fasteners", "paint", "plumbing-tools", "electrical-tools"],
    },
    {
        "slug": "garden",
        "name": "Garden, Yard & Hand Tools",
        "icon": "seedling",
        "blurb": "Digging, pruning, watering and barrowing: the tools that live "
                 "by the back door and get used every day.",
        "kinds": ["garden-tools", "wheelbarrow", "pruning", "watering"],
    },
]

KINDS = {
    "tractor": {
        "label": "Tractors", "icon": "tractor", "group": "vehicles",
        "description": "Farm tractors and compact tractors, from vintage models to modern loaders.",
        "brands": TRACTOR_BRANDS,
    },
    "combine": {
        "label": "Combine Harvesters", "icon": "wheat", "group": "vehicles",
        "description": "Combine harvesters, forage harvesters and specialist harvest machines.",
        "brands": COMBINE_BRANDS,
    },
    "telehandler": {
        "label": "Telehandlers", "icon": "tractor", "group": "vehicles",
        "description": "Telescopic handlers for loading, stacking and yard work.",
        "brands": TELEHANDLER_BRANDS,
    },
    "loader": {
        "label": "Loaders & Backhoes", "icon": "tractor", "group": "vehicles",
        "description": "Wheel loaders, skid steers, backhoe loaders and compact loaders.",
        "brands": LOADER_BRANDS,
    },
    "excavator": {
        "label": "Excavators", "icon": "tractor", "group": "vehicles",
        "description": "Mini and full-size excavators used for drainage, ditching and groundwork.",
        "brands": EXCAVATOR_BRANDS,
    },
    "crawler": {
        "label": "Crawler Tractors", "icon": "tractor", "group": "vehicles",
        "description": "Tracked tractors and dozers for soft ground and heavy pulling.",
        "brands": CRAWLER_BRANDS,
    },
    "atv": {
        "label": "ATVs & Quads", "icon": "truck", "group": "vehicles",
        "description": "All-terrain vehicles and farm quads.",
        "brands": ATV_BRANDS,
    },
    "utv": {
        "label": "UTVs & Utility Vehicles", "icon": "truck", "group": "vehicles",
        "description": "Side-by-side utility vehicles, 4x4s and farm runabouts.",
        "brands": UTV_BRANDS,
    },
    "truck": {
        "label": "Trucks & Transport", "icon": "truck", "group": "vehicles",
        "description": "Pickups, flatbeds, tippers, vans and heavy haulage.",
        "brands": TRUCK_BRANDS,
    },
    "trailer": {
        "label": "Trailers", "icon": "truck", "group": "vehicles",
        "description": "Farm trailers, livestock trailers, flatbeds, tippers and car transporters.",
        "brands": TRAILER_BRANDS,
    },
    "mower": {
        "label": "Mowers", "icon": "tool", "group": "vehicles",
        "description": "Ride-on mowers, lawn tractors, zero-turns and pasture mowers.",
        "brands": MOWER_BRANDS,
    },
    "forestry": {
        "label": "Forestry Machines", "icon": "tree", "group": "vehicles",
        "description": "Forwarders, harvesters, skidders and forestry trailers.",
        "brands": FORESTRY_BRANDS,
    },
    "machine": {
        "label": "Field Machinery", "icon": "tool", "group": "implements",
        "description": "General powered implements and yard machinery.",
        "brands": IMPLEMENT_BRANDS,
    },
    "plough": {
        "label": "Ploughs", "icon": "tool", "group": "implements",
        "description": "Reversible, mounted and trailed ploughs.",
        "brands": IMPLEMENT_BRANDS,
    },
    "harrow": {
        "label": "Harrows & Cultivators", "icon": "tool", "group": "implements",
        "description": "Disc harrows, tine harrows, rollers and cultivators.",
        "brands": IMPLEMENT_BRANDS,
    },
    "seed-drill": {
        "label": "Seed Drills & Planters", "icon": "seedling", "group": "implements",
        "description": "Grain drills, precision planters and seeders.",
        "brands": IMPLEMENT_BRANDS,
    },
    "sprayer": {
        "label": "Sprayers", "icon": "droplet", "group": "implements",
        "description": "Boom sprayers, orchard sprayers, knapsacks and ATV sprayers.",
        "brands": IMPLEMENT_BRANDS,
    },
    "baler": {
        "label": "Balers", "icon": "hay", "group": "implements",
        "description": "Round balers, square balers and wrappers.",
        "brands": IMPLEMENT_BRANDS,
    },
    "hay-tools": {
        "label": "Hay & Forage Tools", "icon": "hay", "group": "implements",
        "description": "Mower-conditioners, tedders, rakes and forage wagons.",
        "brands": IMPLEMENT_BRANDS,
    },
    "slurry": {
        "label": "Slurry & Manure Equipment", "icon": "droplet", "group": "implements",
        "description": "Slurry tankers, pumps, spreaders and muck handling.",
        "brands": IMPLEMENT_BRANDS,
    },
    "grain-handling": {
        "label": "Grain Handling & Storage", "icon": "wheat", "group": "implements",
        "description": "Augers, conveyors, dryers, cleaners and grain store kit.",
        "brands": IMPLEMENT_BRANDS,
    },
    "irrigation": {
        "label": "Irrigation Equipment", "icon": "droplet", "group": "implements",
        "description": "Reels, sprinklers, drip lines, pumps and water distribution.",
        "brands": WATER_PUMP_BRANDS,
    },
    "chainsaw": {
        "label": "Chainsaws", "icon": "saw", "group": "outdoor",
        "description": "Petrol, electric and battery chainsaws, plus pole saws.",
        "brands": CHAINSAW_BRANDS,
    },
    "brushcutter": {
        "label": "Brushcutters & Strimmers", "icon": "saw", "group": "outdoor",
        "description": "Brushcutters, line trimmers and clearing saws.",
        "brands": SMALL_ENGINE_BRANDS,
    },
    "hedge-trimmer": {
        "label": "Hedge Trimmers", "icon": "saw", "group": "outdoor",
        "description": "Petrol, electric and battery hedge cutters.",
        "brands": SMALL_ENGINE_BRANDS,
    },
    "leaf-blower": {
        "label": "Leaf Blowers & Vacuums", "icon": "saw", "group": "outdoor",
        "description": "Handheld, backpack and walk-behind blowers and vacuums.",
        "brands": SMALL_ENGINE_BRANDS,
    },
    "generator": {
        "label": "Generators", "icon": "bolt", "group": "outdoor",
        "description": "Portable, standby and PTO generators.",
        "brands": GENERATOR_BRANDS,
    },
    "pressure-washer": {
        "label": "Pressure Washers", "icon": "droplet", "group": "outdoor",
        "description": "Cold and hot pressure washers, surface cleaners and drain jets.",
        "brands": PRESSURE_WASHER_BRANDS,
    },
    "log-splitter": {
        "label": "Log Splitters", "icon": "saw", "group": "outdoor",
        "description": "Electric, petrol, PTO and manual log splitters.",
        "brands": LOG_SPLITTER_BRANDS,
    },
    "wood-chipper": {
        "label": "Wood Chippers & Shredders", "icon": "saw", "group": "outdoor",
        "description": "Chippers, shredders and garden mulchers.",
        "brands": CHIPPER_BRANDS,
    },
    "stump-grinder": {
        "label": "Stump Grinders", "icon": "saw", "group": "outdoor",
        "description": "Walk-behind, tracked and PTO stump grinders.",
        "brands": STUMP_GRINDER_BRANDS,
    },
    "tiller": {
        "label": "Tillers & Rotavators", "icon": "seedling", "group": "outdoor",
        "description": "Garden tillers, rotavators and bed formers.",
        "brands": TILLER_BRANDS,
    },
    "water-pump": {
        "label": "Water Pumps", "icon": "droplet", "group": "outdoor",
        "description": "Transfer, trash, borehole, submersible and PTO pumps.",
        "brands": WATER_PUMP_BRANDS,
    },
    "hand-tools": {
        "label": "Hand Tools", "icon": "tool", "group": "workshop",
        "description": "Spanners, sockets, screwdrivers, pliers, hammers, saws and files.",
        "brands": HAND_TOOL_BRANDS,
    },
    "power-tools": {
        "label": "Power Tools", "icon": "bolt", "group": "workshop",
        "description": "Drills, grinders, saws, sanders and battery platforms.",
        "brands": POWER_TOOL_BRANDS,
    },
    "air-tools": {
        "label": "Air Tools", "icon": "bolt", "group": "workshop",
        "description": "Impact wrenches, ratchets, sanders, spray guns and nailers.",
        "brands": AIR_TOOL_BRANDS,
    },
    "welder": {
        "label": "Welders & Plasma Cutters", "icon": "weld", "group": "workshop",
        "description": "MIG, TIG, stick, multi-process welders and plasma cutters.",
        "brands": WELDER_BRANDS,
    },
    "compressor": {
        "label": "Air Compressors", "icon": "bolt", "group": "workshop",
        "description": "Portable, workshop, screw and PTO compressors.",
        "brands": COMPRESSOR_BRANDS,
    },
    "bench-machinery": {
        "label": "Bench & Workshop Machinery", "icon": "wrench", "group": "workshop",
        "description": "Lathes, mills, drill presses, bandsaws, planers and jointers.",
        "brands": BENCH_MACHINERY_BRANDS,
    },
    "lifting": {
        "label": "Lifting & Jacking", "icon": "tool", "group": "workshop",
        "description": "Jacks, cranes, hoists, chain blocks and lifting gear.",
        "brands": LIFTING_BRANDS,
    },
    "measuring": {
        "label": "Measuring & Layout", "icon": "magnifier", "group": "workshop",
        "description": "Calipers, micrometers, levels, squares and marking tools.",
        "brands": MEASURING_BRANDS,
    },
    "fasteners": {
        "label": "Fasteners & Fixing Tools", "icon": "bolt", "group": "workshop",
        "description": "Nailers, staplers, riveters, anchors and fixing systems.",
        "brands": FASTENER_BRANDS,
    },
    "paint": {
        "label": "Paint & Finishing", "icon": "tool", "group": "workshop",
        "description": "Sprayers, brushes, rollers, paints, stains and wood finishes.",
        "brands": PAINT_BRANDS,
    },
    "plumbing-tools": {
        "label": "Plumbing Tools", "icon": "droplet", "group": "workshop",
        "description": "Pipe cutters, benders, press tools, drain machines and heating spares.",
        "brands": PLUMBING_BRANDS,
    },
    "electrical-tools": {
        "label": "Electrical Tools", "icon": "bolt", "group": "workshop",
        "description": "Testers, multimeters, insulation testers, cable tools and consumer units.",
        "brands": ELECTRICAL_BRANDS,
    },
    "garden-tools": {
        "label": "Garden Tools", "icon": "seedling", "group": "garden",
        "description": "Spades, forks, hoes, rakes, edgers and cultivators.",
        "brands": GARDEN_TOOL_BRANDS,
    },
    "wheelbarrow": {
        "label": "Wheelbarrows & Carts", "icon": "tool", "group": "garden",
        "description": "Wheelbarrows, garden carts, tippers and hand trucks.",
        "brands": WHEELBARROW_BRANDS,
    },
    "pruning": {
        "label": "Pruning & Cutting", "icon": "saw", "group": "garden",
        "description": "Secateurs, loppers, pruning saws, shears and pole pruners.",
        "brands": PRUNING_BRANDS,
    },
    "watering": {
        "label": "Watering & Irrigation", "icon": "droplet", "group": "garden",
        "description": "Hoses, reel sprinklers, drip kits, cans and sprayers.",
        "brands": WATERING_BRANDS,
    },
}
