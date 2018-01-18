import StateMachineComponents

class ObservationTable(object):
    def __init__(self):
        empty = "lambda"
        self.S = [empty]
        self.E = [empty]
        self.T = []

    def initialse_table(self, alphabet, logging=False):
        symbols = alphabet.symbols

        for s in symbols:
            self.S.append(s)

        if logging:
            print "STATE SET: " + str(self.S)

