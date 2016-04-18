from chain_builder import ChainBuilder

class PoemGenerator:

    def __init__(self, tags):
        self.tags = tags
        cb = ChainBuilder()
        cb.build_chain()
        self.chain = cb.get_chain()

    def get_poem(self):
        poem = ""
        for tag in self.tags:
            line = self.get_line(tag)
            if line != tag:
                poem = poem + line +'\n'
        return poem

    def get_line(self, tag):
        line = tag
        next_word = self.chain.next(tag)
        while next_word is not None:
            line = line + " " + next_word
            next_word = self.chain.next(next_word)
            if len(line) > 200:
                break
        return line
