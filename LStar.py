import StateMachineComponents
import itertools

class ObservationTable(object):

    def __init__(self, alphabet, logging=False):

        self.states = [[]]
        self.experiments = [[s] for s in alphabet.symbols]
        self.possible_states = [[s] for s in alphabet.symbols]
        self.results = {}

        print "States: " + str(self.states)
        print "Experiments:" + str(self.experiments)
        print "Possible States:" + str(self.possible_states)

    @staticmethod
    def build_prefixes_for_symbol(symbols):
        return filter(None,[symbols[:i] for i in range(len(symbols) + 1)])

    def prefix_close_ot(self):
        new_list = []
        for x in self.possible_states:
            new_list.extend(self.build_prefixes_for_symbol(x))
        flist = []
        for x in new_list:
            if x not in flist:
                flist.append(x)
        self.possible_states = flist

    def build_query_strings(self):
        print self.states
        print self.possible_states
        print self.experiments







