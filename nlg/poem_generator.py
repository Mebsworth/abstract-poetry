from chain_builder import ChainBuilder

class PoemGenerator:

    def __init__(self, tags, chain):
        self.tags = set(tags)
        if chain is None:
            cb = ChainBuilder()
            cb.build_chain()
            self.chain = cb.get_chain()
        else:
            self.chain = chain

    def get_poem(self):
        poem = []
        for tag in self.tags:
            line = self.get_line(tag)
            if line != tag:
                poem.append(line)
        return poem

    def get_line(self, tag):
        line = tag
        next_word = self.chain.next(tag)
        while next_word is not None:
            print(line)
            print(next_word)
            line = line + " " + next_word.decode('utf-8')
            next_word = self.chain.next(next_word)
            if len(line) > 200:
                break
        return line
