# Authoritative structure: Carol's per-file listing (left column of the sheet).
# Names are as she wrote them, with clear typos corrected — see TYPO_FIXES.
FILES = {
 1: ["AKO", "Ambassador Hotel", "An Inspector Calls", "Beachcroft (1967)",
     "Beis Din Guidelines of Kashrus & Food Ingredients", "Beis Din Review",
     "BestFoods / Unilever", "Biotechnology and Kashrus", "Blooms", "Bugs"],
 2: ["Carmine", "Carmelli", "Cheese", "Chestnuts", "Cigarettes – Cigars",
     "Chief Rabbinate", "Conjoint Relating to Pesach ’88–’02"],
 3: ["Dayan Lerner", "El Al"],
 4: ["Factory Visits Review (Certification Process Project)", "Gelatine",
     "Spielsinger & Abraham / Wagner / Kinloss", "Kavana"],
 5: ["Hillel House", "Hindquarters", "Holland", "Honey", "Innocent Drinks", "Israel",
     "Isinglass", "Kashrus Commission", "Kashrus for the Community",
     "Kashrus List (Confectionary) 1962", "Marriage", "Marmite"],
 6: ["Halacha Files", "Magazine Articles", "Newspaper Articles"],
 7: ["Marketing", "MBD", "Medicines", "Misc", "Milk", "Norwood Ravenswood",
     "Overview of Kashrus Division Procedure", "Obituaries / Memorial Addresses"],
 8: ["Pesach", "OU"],
 9: ["Rakusens", "Paris Beis Din", "Shmita", "Shomer Seminar 2002",
     "Various Correspondence", "Whisky Research & Articles AOP", "Wines"],
 10: ["Chief Rabbinate Strasbourg", "Review of Financial Structure of LBD 1994",
      "The White House", "Travel", "Vinegar", "Waxing of Fruit & Veg", "Xanthan Gum",
      "Zhangjiagang Legal"],
 11: ["Sugar – Tate & Lyle – Cube Sugar – Pesach", "Tartaric Acid", "Tomor Margarine",
      "Transactions of the Jewish Historical Society of England",
      "Very Interesting Articles"],
 12: ["Queries – Shaalos", "The Mesorah of Kosher Birds & Mammals", "Shellac"],
 13: ["Rabbi Conway: Presentation, Synopsis and Brief Biography", "Kitnios",
      "Important Papers", "Feasibility of National Kosher UK Certification",
      "Buckingham Palace Goes Kosher", "Kashrus Meeting of the Beis Din",
      "Report: Kashrus & Shechita Activities", "Letters & Kashrus Regulations",
      "Court Cases (JFS, Rosie Ben Shushan)", "Legal (CER)"],
 14: ["Kashrus / KLBD Review", "Kashrus Certificates", "Kashrus Committee Meetings",
      "Kashrus Financial Issues", "Kashrus Issues", "Kashrus Promotion Campaign",
      "KLBD Articles", "Policy Decisions with Regard to the Kashrus Guide"],
 15: ["Factory Visits"],
 16: ["CDs", "Cassettes", "Photos"],
 17: ["Rabbi Conway's Notebooks"],
 18: ["Rabbi Silver – Part 1"],
 19: ["Rabbi Silver – Part 2"],
 20: ["Fish List", "Analysis of Vertebrate Structure"],
 21: ["Scales", "Oils", "British Museum", "Fish Found in Italy",
      "List & Info of Fish B–K"],
 22: ["List & Info of Fish L–S"],
 23: ["Newspapers", "Tuna Rabbinic Material (1)"],
 24: ["Tuna: Scientific Material (2)", "Tuna: Scientific Material (3)"],
 25: ["Tuna + Fish: Miscellaneous incl. Specimen of Bonito Scales (4)", "Miscellaneous (5)",
      "W. Simon & Sons Tuna Production", "List of Fish (T)",
      "Fishes & Crustaceans of Cyprus", "Kosher & Non-Kosher Fish in Various Countries"],
 26: ["Tuna: Scientific Names, Description, Illustrations (6 & 7)",
      "Correspondence (8)", "Biblical / Talmudical (9)",
      "Rabbinical Literature (10)", "Nomenclature (11)"],
 27: ["Turbot – Part 1"],
 28: ["Turbot – Part 2"],
 29: ["Shechita", "Divrei Torah", "JFS", "Kedassia"],
 30: ["Eruv"],
}

# Sub-lists Carol enumerated inside an entry — indexed so they are findable.
SUBLISTS = {
 "List of Fish (T)": ["Talapia", "Tea-Time Fish Pastes", "Torbay Solex", "Tobis Fish",
                      "Trigger Fish", "Trout", "Turbot", "Tunny"],
 "Kosher & Non-Kosher Fish in Various Countries": [
    "Britain", "Australia", "Belgium", "Caribbean", "Czech Republic & Slovakia",
    "Denmark", "Fiji", "Finland", "France", "Gibraltar", "Greece", "Hawaii",
    "Hong Kong", "Holland", "Italy", "Malta", "Norway", "Peru", "Portugal", "India",
    "Romania", "Russia", "Spain", "South Africa", "Sri Lanka", "Sweden", "Thailand",
    "Turkey", "USA", "Uruguay", "West Indies", "Yugoslavia"],
 "List & Info of Fish B–K": ["Billfishes", "Buckling", "Brisling", "Brill", "Bonito",
    "Cod Roe", "Chubs", "Chinchard", "Coley", "Coalfish", "Caviar", "Catfish", "Carp",
    "Cadascura", "Eels", "Flatfish", "Frozen Fish", "Garfish", "Haddock", "John Dory",
    "Kingklip"],
 "List & Info of Fish L–S": ["Ling", "Lumpfish", "Lumpsucker", "Lungfish", "Mackerel",
    "Marlin", "Megrim", "Mock Halibut", "Mullet", "Smooth Oreodori", "Orange Roughy",
    "Plaice", "Pilot Fish", "Rock Salmon", "Saithe", "Sailfish", "Salmon", "Sardines",
    "Scad", "Shibuta", "Skipjack", "Snoek", "Sild", "Sturgeon", "Swordfish"],
 "Court Cases (JFS, Rosie Ben Shushan)": ["Rosie Ben Shushan", "JFS", "Solinsky – JD Plitnick", "Blooms"],
}

# Settled by the finished shelf: the spine labels are the final organisation and
# agree with the per-file listing in every case the two source sheets disputed.
RESOLVED = [
 ("Photos", "File 16 — confirmed on the spine"),
 ("Fish List", "File 20 — confirmed on the spine"),
 ("List of Fish (T)", "File 25 — confirmed on the spine"),
 ("Fishes & Crustaceans of Cyprus", "File 25 — confirmed on the spine"),
 ("Kosher & Non-Kosher Fish in Various Countries", "File 25 — confirmed on the spine"),
 ("Wines", "File 9 — confirmed on the spine; there is no separate Wine at File 10"),
]

# The one entry on Carol's sheet that is not named on a spine label.
OUTSTANDING = [
 ("Marriage", "File 5", "On Carol's sheet (Rabbi Shindler, meeting of 28 July 1905) but not named on the spine of File 5. Kept in the catalogue."),
]

TYPO_FIXES = [
 ("Biotecnology", "Biotechnology"), ("Uniliver", "Unilever"), ("Magasine", "Magazine"),
 ("Orbituaries / Orbiruaries", "Obituaries"), ("MBDE", "MBD"), ("Wagmer", "Wagner"),
 ("Bukingham", "Buckingham"), ("Cetification / Feasibilty", "Certification / Feasibility"),
 ("Zhangiagang", "Zhangjiagang"), ("Sri Lanca", "Sri Lanka"), ("Urugway", "Uruguay"),
 ("Yugoslavi", "Yugoslavia"), ("Cadascura", "left as written"),
]
