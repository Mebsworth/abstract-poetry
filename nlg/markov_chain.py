import random

class MarkovChain:

    def __init__(self):
        self.chain = {} # dict of WORD to: dict of words that follow it with frequency

    # Add the connection from a to b to the Markov Chain
    def add_transition(self, a,b):
        if a in self.chain:
            if b in self.chain[a]:
                self.chain[a][b] = self.chain[a][b] + 1
            else:
                self.chain[a][b] = 1
        else:
            self.chain[a] = { b:1 }

    # Pick a transition leaving state v uniformly at random, and return the resulting state.
    def next(self, v):
        if v in self.chain:
            next = self.chain[v]
            adjusted_list = [ a for a in next for count in range(0,next[a]) ]
            index = int(random.uniform(0,len(adjusted_list)))
            return adjusted_list[index]
        else:
            return None

    # Return a string representation of this Markov chain.
    def to_string(self):
        return self.chain 

    def get_dict(self):
        return self.chain