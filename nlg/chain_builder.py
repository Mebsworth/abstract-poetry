from markov_chain import MarkovChain

class ChainBuilder:

    delimeters = ";:.!?"

    def __init__(self):
        self.mc = MarkovChain()

    def build_chain(self):
        corpus = open('corpus.txt', 'r')
        for line in corpus:
            line = line.split()
            if len(line) > 1:
                pre = line[0]
                for word in line[1:]:
                    self.mc.add_transition(pre, word)
                    pre = word
        corpus.close()

    def get_chain(self):
        return self.mc