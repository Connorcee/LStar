from random import *


class MealyMachine(object):
    def __init__(self, number_of_nodes, alphabet, outputs, number_of_accepting=1, randomise = False):

        self.number_of_nodes = number_of_nodes
        self.alphabet = Alphabet(alphabet)
        self.outputs = Outputs(outputs)
        self.starting_state = None
        self.Walked = False
        self.states = [State(count) for count in range(0, number_of_nodes)]
        self.transitionsListOrdered = True
        self.statesDict = self.build_state_dictionary()
        self.randomise = randomise
        if randomise:
            self.random_walk()
        else:
            self.build_machine()

    # TODO: Add error checking for user input to this function
    # TODO: Check if transfer state is legal
    # TODO: Check if symbol is legal
    # TODO: Check if output is legal
    # TODO: Check if transition doesn't already exist
    def build_machine(self):
        print self.statesDict
        # Build transitions
        for state in self.states:
            number_of_transitions = raw_input("Input number of transitions AWAY from the state:" + str(state) + "\n")
            for x in range(int(number_of_transitions)):
                transfer_state = raw_input("State ID to transfer to: \n")
                transfer_state = self.statesDict[int(transfer_state)]
                symbol =  raw_input("Symbol for this transition: \n")
                symbol = int(symbol)
                output = raw_input("Input the output for this transition: \n")
                output = int(output)
                state.add_transition(transfer_state,symbol,output)

        # TODO: Check that each state isn't already an acceptor
        i = raw_input("Number of accepting states")
        for y in range(int(i)):
            _id = raw_input("ID of state to be an acceptor")
            s = self.statesDict[int(_id)]
            s.is_accepting = True
            print s

        # TODO: Check that this is legal
        start = raw_input("ID of state state")
        self.statesDict[int(start)].is_start = True

    def print_states(self):
        print "States: " + str(self.states)

    def build_state_dictionary(self):
        x = {}
        for states in self.states:
            x[states.id] = states
        return x

    def make_acceptor(self,stateid):
        self.statesDict[stateid].is_accepting = True

    # Creates a random walk, makes initial state start and final state an acceptor
    def random_walk(self):
        if not self.Walked:
            # Only allow one random walk, doesn't check for duplicate symbol transitions
            self.Walked = True
            shuffle(self.states)
            for index, item in enumerate(self.states[:-1]):
                # Get the position of a random symbol
                if index == 0:
                    item.is_start = True
                    self.starting_state = item
                random_symbol = choice(self.alphabet.symbols)
                random_output = choice(self.outputs.outputs)
                next_state = self.states[index + 1]
                item.add_transition(next_state, random_symbol, random_output)
                if index == len(self.states) - 2:
                    print "Adding Acceptor"
                    next_state.is_accepting = True

    # Not completely pythonic because states should be a dictionary
    def create_random_legal_transition(self):
        self.transitionsListOrdered = False
        legal_states = [x for x in self.states if x.degree < len(self.alphabet)]
        state = choice(legal_states)
        state = self.states[self.states.index(state)]
        transition_state = choice([x for x in self.states if x.id != state.id])
        legal_symbols = [x for x in self.alphabet.symbols if x not in state.get_transition_symbols()]
        state.add_transition(transition_state,choice(legal_symbols),choice(self.outputs.outputs))

    def print_machine_transitions(self):
        for state in self.states:
            state.print_transitions()

    def random_acceptors(self, number_of_acceptors):
        if number_of_acceptors < len(self.states):
            temp = sample(self.states, number_of_acceptors)
            # Assign all the states in temp to accepting states
            [setattr(x, 'is_accepting', True) for x in temp]
            print "Acceptors: " + str(temp)

    def ending_acceptor(self):
        if self.transitionsListOrdered:
            self.states[len(self.states) - 1].is_accepting = True

    def transition_legal(self, state, symbol):
        if state in self.states:
            return any(x.symbol == symbol for x in state.Transitions)

    def next_state(self, state, symbol):
        if self.transition_legal(state, symbol):
            return state.get_transition(symbol).get_end_state()

    def transition_output(self, State, symbol):
        if self.transition_legal(State, symbol):
            return State.get_transition(symbol).output
        else:
            return "No Transition from this state: " + str(State) + " " + str(symbol)

    def is_accepted(self, word, logging=False):
        starting_state = [x for x in self.states if x.is_start is True][0]
        current_state = starting_state
        for symbols in word:
            if self.transition_legal(current_state,symbols):
                if logging: print str(symbols) + " " + "Is legal character, moving state"
                current_state = self.next_state(current_state,symbols)
            else:
                if logging: print "No legal transition from " + str(current_state) + " for the symbol " + str(symbols)
                return False
        return True

class State(object):
    def __init__(self, id, accepting=False, is_start=False):
        self.id = id
        self.Transitions = []
        self.is_accepting = accepting
        self.is_start = is_start
        self.degree = len(self.Transitions)

    def add_transition(self, state, symbol, output):
        self.Transitions.append(Transition(self, state, symbol, output))
        self.degree = len(self.Transitions)

    def print_transitions(self):
        print "Transitions: " + str(self.Transitions)

    def get_transition(self, symbol):
        # Get the transition for the above symbol
        transition = next(t for t in self.Transitions if t.symbol == symbol)
        return transition

    def get_transition_symbols(self):
        symbols = []
        for x in self.Transitions:
            symbols.append(x.symbol)
        return symbols

    def __getitem__(self, item):
        return self

    def __str__(self):
        return "( ID:" + str(self.id) + " Acceptor:" + str(self.is_accepting) + " Start:" + str(self.is_start) + ")"

    def __repr__(self):
        return "( ID:" + str(self.id) + " Acceptor:" + str(self.is_accepting) + " Start:" + str(self.is_start) + ")"

    # TODO: Might need to be changed to check for a logical equivalence rather than an instance equivalence
    def __eq__(self, other):
        return self.id == other.id


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

    def get_start_state(self):
        return self.state_1

    def get_end_state(self):
        return self.state_2

# Alphabet of the Mealy machine
class Alphabet(object):
    def __init__(self, symbols):
        self.symbols = list(set(symbols))

    def __len__(self):
        return len(self.symbols)

# Mealy Machines have outputs on transitions
class Outputs(object):
    def __init__(self, outputs):
        self.outputs = list(set(outputs))

    def __len__(self):
        return len(self.outputs)