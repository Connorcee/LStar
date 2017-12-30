from random import *


class MealyMachine(object):
    def __init__(self, number_of_nodes, alphabet, outputs, number_of_accepting=1):

        self.Number_of_nodes = number_of_nodes
        self.alphabet = Alphabet(alphabet)
        self.outputs = Outputs(outputs)
        self.States = []
        self.StartingState = None
        self.States = [State(count) for count in range(0, number_of_nodes)]
        self.Walked = False

    def print_states(self):
        print "States: " + str(self.States)

    # This also defines a starting state of 1
    def random_walk(self):
        if not self.Walked:
            # Only allow one random walk, doesn't check for duplicate symbol transitions
            self.Walked = True
            shuffle(self.States)
            for index, item in enumerate(self.States[:-1]):
                # Get the position of a random symbol
                if index == 0:
                    item.is_start = True
                    self.StartingState = item
                random_symbol = choice(self.alphabet.symbols)
                random_output = choice(self.outputs.outputs)
                next_state = self.States[index + 1]
                item.add_transition(next_state, random_symbol, random_output)

    def print_machine_transitions(self):
        print "Transitions:"
        for state in self.States:
            state.print_transitions()

    def random_acceptors(self, number_of_acceptors):
        if number_of_acceptors < len(self.States):
            temp = sample(self.States, number_of_acceptors)
            # Assign all the states in temp to accepting states
            [setattr(x, 'is_accepting', True) for x in temp]
            print "Acceptors: " + str(temp)

    # If there are no starting states, add a random one
    # Doesn't account for if all states can be reached from this state
    def random_starting(self):
        number_of_starts = len([s for s in self.States if s.is_accepting])
        if number_of_starts < 1:
            [setattr(x, 'is_starting', True) for x in self.States]

    def transition_legal(self, state, symbol):
        if state in self.States:
            return any(x.symbol == symbol for x in state.Transitions)

    def next_state(self, state, symbol):
        if self.transition_legal(state, symbol):
            return state.get_transition(symbol)

    def transition_output(self, State, symbol):
        if self.transition_legal(State, symbol):
            return State.get_transition(symbol).output
        else:
            return "No Transition from this state: " + str(State) + " " + str(symbol)

    def is_accepted(self, word):
        starting_state = [x for x in self.States if x.is_start == True][0]
        current_state = starting_state
        for symbols in word:
            self.transition_legal(current_state,symbols)

    # def process_string(self,string):
    # def process_transition(self,state, symbol):
    # def make_complete(self):


class State(object):
    def __init__(self, _id, accepting=False, is_start=False):
        self._id = _id
        self.Transitions = []
        self.is_accepting = accepting
        self.is_start = is_start
        self.degree = len(self.Transitions)
        self.is_starting = False

    def add_transition(self, state, symbol, output):
        self.Transitions.append(Transition(self, state, symbol, output))
        self.degree = len(self.Transitions)

    def print_transitions(self):
        print self.Transitions

    def get_transition(self, symbol):
        # Get the transition for the above symbol
        transition = next(t for t in self.Transitions if t.symbol == symbol)
        return transition

    def __getitem__(self, item):
        return self

    def __str__(self):
        return "( ID:" + str(self._id) + " " + str(self.is_accepting) + " )"

    def __repr__(self):
        return "( ID:" + str(self._id) + " " + str(self.is_accepting) + " )"

    # TODO: Might need to be changed to check for a logical equivalence rather than an instance equivalence
    def __eq__(self, other):
        return self._id == other._id


class Transition(object):
    _ID = 0

    def __init__(self, state_1, state_2, symbol, output):
        self._id = self.__class__._ID
        self.__class__._ID += 1
        self.state_1 = state_1
        self.state_2 = state_2
        self.symbol = symbol
        self.output = output

    def __str__(self):
        return '(ID: ' + str(self._id) + \
               ' Start State:' + str(self.state_1) + \
               ' End State:' + str(self.state_2) + \
               ' Transition Symbol:' + str(self.symbol) +\
               ' Outputs' + str(self.output) + ')'

    def __repr__(self):
        return '(ID: ' + str(self._id) + \
               ' Start State:' + str(self.state_1) + \
               ' End State:' + str(self.state_2) + \
               ' Transition Symbol:' + str(self.symbol) +\
               ' Output:' + str(self.output) + ')'

    def __eq__(self, other):
        return (self.state_1 == other.state_2) and (self.symbol == other.symbol)

# Alphabet of the Mealy machine
class Alphabet(object):
    def __init__(self, symbols):
        self.symbols = list(set(symbols))

# Mealy Machines have outputs on transitions
class Outputs(object):
    def __init__(self, outputs):
        self.outputs = list(set(outputs))
