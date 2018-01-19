import StateMachineComponents
import itertools

class ObservationTable(object):
    def __init__(self):
        empty = []
        self.STA = [empty]
        self.EXP = [empty]
        self.OT = [[],[1],[1,2]]
        self.results = {}

    def initialse_table(self, alphabet, logging=False):
        symbols = alphabet.symbols

        if logging:
            print "STATE SET: " + str(self.STA)

    def build_prefixes_for_symbol(self, symbols):
        return filter(None,[symbols[:i] for i in range(len(symbols) + 1)])

    def prefix_close_ot(self):
        new_list = []
        for x in self.OT:
            new_list.extend(self.build_prefixes_for_symbol(x))
        flist = []
        for x in new_list:
            if x not in flist:
                flist.append(x)
        self.OT = flist

    def perform_queries(self, mealy):
        for word in self.OT:
            self.results[repr(word)] = mealy.word_output(word)

        print self.results




