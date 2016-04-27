from markov_chain import MarkovChain
import unicodedata


class ChainBuilder:

    def __init__(self):
        self.mc = MarkovChain()
        self.chars = chars = ['"', "-", "(", ")", "[", "]"]
        self.delimeters = [';',':','.','!','?']

    def build_chain(self):
        corpus = open('smaller_corpus.txt', 'r')
        for line in corpus:
            # line = line.lower()
            for c in self.chars:
                line = line.replace(c, '')
            line = line.split()
            if len(line) > 1:
                pre = line[0]
                for word in line[1:]:
                    self.mc.add_transition(pre, word)
                    pre = word
        corpus.close()

    def get_chain(self):
        return self.mc