from poem_generator import PoemGenerator

pg = PoemGenerator([ "glass",
    "drink",
    "cold",
    "no person",
    "wear",
    "cocktail",
    "fruit",
    "cool",
    "refreshment",
    "food",
    "ice",
    "juice",
    "color",
    "desktop",
    "vintage",
    "liquid",
    "abstract",
    "blur",
    "paper",
    "pattern"
    ])

poem = pg.get_poem()

print(poem)