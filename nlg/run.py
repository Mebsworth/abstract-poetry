from poem_generator import PoemGenerator
from chain_builder import ChainBuilder

tags = [ "glass",
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
    ]

cb = ChainBuilder()
cb.build_chain()
chain = cb.get_chain()

pg = PoemGenerator(tags, chain)

poem = pg.get_poem()
