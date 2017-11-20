from random import *

class StateMachine(object):

    def __init__(self, number_of_nodes, alphabet, number_of_accepting=1):

        self.Number_of_nodes = number_of_nodes
        self.alphabet = Alphabet(alphabet)
        self.States = []
        self.States = [State(count) for count in range(0,number_of_nodes)]
        self.Walked = False

    def print_states(self):
        print "States: " + str(self.States)

    def random_walk(self):
        if not self.Walked:
            # Only allow one random walk, doesn't check for duplicate symbol transitions
            self.Walked = True
            shuffle(self.States)
            for index, item in enumerate(self.States[:-1]):
                # Get the position of a random symbol
                random_symbol = choice(self.alphabet.symbols)
                next_state = self.States[index + 1]
                item.add_transition(next_state, random_symbol)


    def print_machine_transitions(self):
        for state in self.States:
            state.print_transitions()


class State(object):

    def __init__(self, _id, accepting=False, is_start=False):
        self._id = _id
        self.Transitions = []
        self.is_accepting = accepting
        self.is_start = is_start
        self.degree = len(self.Transitions)

    def add_transition(self, state, symbol):
        self.Transitions.append(Transition(self, state, symbol))
        self.degree = len(self.Transitions)

    def print_transitions(self):
        print self.Transitions

    def __getitem__(self, item):
        return self

    def __str__(self):
        return str(self._id)

    def __repr__(self):
        return str(self._id)

    # TODO: Might need to be changed to check for a logical equivalence rather than an instance equivalence
    def __eq__(self, other):
        return self._id == other._id


class Transition(object):
    _ID = 0

    def __init__(self, state_1, state_2, symbol):
        self._id = self.__class__._ID
        self.__class__._ID += 1
        self.state_1 = state_1
        self.state_2 = state_2
        self.symbol = symbol

    def __str__(self):
        return '(ID: ' + str(self._id) + \
               ' This State:' + str(self.state_1) + \
               ' End State:' + str(self.state_2) + \
               ' Transition Symbol:' + str(self.symbol) + ')'

    def __repr__(self):
        return '(ID: ' + str(self._id) + \
               ' This State:' + str(self.state_1) + \
               ' End State:' + str(self.state_2) + \
               ' Transition Symbol:' + str(self.symbol) + ')'

    def __eq__(self, other):
        return (self.state_1 == other.state_2) and (self.symbol == other.symbol)


class Alphabet(object):

    def __init__(self, symbols):
        self.symbols = list(set(symbols))