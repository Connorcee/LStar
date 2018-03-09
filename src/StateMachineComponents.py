from random import *
import LStar as tools
import ast
import uuid
from time import sleep

class MealyMachine(object):
    def __init__(self, number_of_nodes, alphabet, outputs, path=False, randomise=False, from_table=False, transitions=None):

        self.number_of_nodes = number_of_nodes
        self.alphabet = Alphabet(alphabet)
        self.outputs = Outputs(outputs)
        self.starting_state = None
        self.Walked = False
        self.states = [State(count) for count in range(0, number_of_nodes)]
        self.statesDict = self.build_state_dictionary()
        self.randomise = randomise
        self.empty = []

        if randomise:
            self.random_walk()
        elif not randomise and from_table:
            self.build_machine_from_ot(transitions)
        else:
            self.load_machine(path)

    # Build a machine from an observation table
    def build_machine_from_ot(self, transitions):
        states = []
        state_mapping = {}
        for transition in transitions:
            states.append(transition[0])
        states = tools.ObservationTable.remove_dups(states)

        counter = 0
        for state in states:
            state_mapping[str(state)] = counter
            counter += 1
        for t in transitions:
            # State beginning transition
            t[0] = state_mapping[t[0]]
            # State targetting transition
            t[1] = state_mapping[t[1]]
            # Symbol for transition
            t[2] = int(t[2])
            # Output for transition
            t[3] = int(filter(str.isdigit, t[3]))
        for t in transitions:
            try:
                if t[1] == t[0]:
                    self.statesDict[t[0]].add_transition(self.statesDict[t[1]],t[2],t[3],True)
                else:
                    self.statesDict[t[0]].add_transition(self.statesDict[t[1]], t[2], t[3], False)
            except KeyError:
                print "KEY ERROR ON: "
                print t
                exit()
        self.statesDict[state_mapping['[]']].is_start = True

    def load_machine(self,path):
        # All states present, contain no transitions
        if path:
            file_object = open(path,"r")
        else:
            print "PATH IS FALSE"
            exit()
        machine = []
        for line in file_object:
            line = line.split()
            if line:
                line = [i for i in line]
                # State, Symbol, output, loopback
                machine.append(line)
                if line[0] == line[1]:
                    self.states[int(line[0])].add_transition(self.states[int(line[1])],int(line[2]),int(line[3]),True)
                else:
                    self.states[int(line[0])].add_transition(self.states[int(line[1])], int(line[2]), int(line[3]),False)
                if line[4] == 'S':
                    self.states[int(line[0])].is_start = True
        self.build_state_dictionary()
        pass

    def save_machine(self):
        name = "STATES " + str(len(self.states))
        f=open(name,"w+")
        for s in self.states:
            for t in s.Transitions:
                if s.is_start:
                    f.write('{} {} {} {} S\n'.format(t.state_1.id,t.state_2.id,t.symbol,t.output))
                else:
                    f.write('{} {} {} {} N\n'.format(t.state_1.id, t.state_2.id, t.symbol, t.output))
        f.close()

    def minimise(self):
        equiv = self.equivalent_states()
        while equiv is not None:
            self.combine_states(equiv)
            equiv = self.equivalent_states()

    def combine_states(self, list_of_states):
        if list_of_states is None:
            return None
        if len(list_of_states) < 2:
            return None

        state_1 = [x for x in self.states if x.id == list_of_states[0]][0]
        state_2 = [x for x in self.states if x.id == list_of_states[1]][0]

        if state_2.is_start:
            state_1.is_start = True

        for s in self.states:
            for transitions in s.Transitions:
                if transitions.state_2.id == state_2.id:
                    transitions.state_2 = state_1

        self.states.remove(state_2)
        self.statesDict = self.build_state_dictionary()

    def equivalent_states(self):
        states = self.states[:]
        inputs = self.alphabet.symbols[:]
        outputs = {}
        next_states = {}
        state_output = {}
        for s in states:
            x = []
            y = []
            z = []
            for i in inputs:
                x.append(self.transition_output(s, i))
                y.append(self.next_state(s,i).id)
                z.extend(x)
                z.extend(y)
            outputs[s.id] = str(x)
            next_states[s.id] = str(y)
            state_output[s.id] = str(z)

        rev_multidict = {}
        for key, value in state_output.items():
            rev_multidict.setdefault(value, set()).add(key)
        parition = [values for key, values in rev_multidict.items() if len(values) > 1]
        if len(parition) > 0:
            return list(parition[0])

        rev_multidict = {}
        for key, value in outputs.items():
            rev_multidict.setdefault(value, set()).add(key)
        parition = [values for key, values in rev_multidict.items() if len(values) > 1]

        while True:
            states_to_remove_from_set = []
            for items in parition:
                for elements in items:
                    next_state = next_states[elements]
                    next_state = ast.literal_eval(next_state)
                    for ns in next_state:
                        if ns not in items:
                            states_to_remove_from_set.append(elements)
                            break
            if len(states_to_remove_from_set) == 0:
                break
            for index, value in enumerate(parition):
                for ele in states_to_remove_from_set:
                    if ele in parition[index]:
                        parition[index].discard(ele)

        if len(parition) > 0:
            temp = [list(x) for x in parition if len(x) > 1]
            if temp:
                return temp[0]

    def print_states(self):
        print "States: " + str(self.states)

    def build_state_dictionary(self):
        x = {}
        for states in self.states:
            x[states.id] = states
        return x

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

    def create_random_legal_transition(self, verbose=False):
        if verbose:
            print "Generating Random Transition"
        self.transitionsListOrdered = False
        # Legal states are those with less transitions than the length of the alphabet
        legal_states = [x for x in self.states if x.degree < len(self.alphabet)]

        if len(legal_states) == 1:
            state = legal_states[0]
            transition_state = legal_states[0]
        elif len(legal_states) == 0:
            return False
        else:
            choices = sample(legal_states,2)
            state = choices[0]
            transition_state = choices[1]

        legal_symbols = [x for x in self.alphabet.symbols if x not in state.get_transition_symbols()]
        legal_outputs = [x for x in self.outputs.outputs if x not in state.get_transition_outputs()]
        if len(legal_outputs) == 0 or len(legal_symbols) == 0:
            return False
        state.add_transition(transition_state,choice(legal_symbols),choice(legal_outputs))
        return True

    def random_transition_pass(self):
        for x in self.states:
            self.create_random_legal_transition(False)

    def build_loopbacks(self):
        print "Building Loopbacks"
        for state in self.states:
            legal_outputs = list(set(self.outputs.outputs) - set(state.get_transition_outputs()))
            if len(legal_outputs) == 0:
                while state.degree < len(self.alphabet):
                    current_symbols = state.get_transition_symbols()
                    legal_symbols = list(set(self.alphabet.symbols) - set(current_symbols))
                    output = choice(self.outputs.outputs)
                    state.add_transition(state,choice(legal_symbols),output,True)
                continue
            legal_outputs = choice(legal_outputs)
            while state.degree < len(self.alphabet):
                current_symbols = state.get_transition_symbols()
                legal_symbols = list(set(self.alphabet.symbols) - set(current_symbols))
                state.add_transition(state,choice(legal_symbols),legal_outputs,True)

    def print_machine_transitions(self):
        for state in self.states:
            state.print_transitions()

    def transition_legal(self, state, symbol):
        if state in self.states:
            return any(x.symbol == symbol for x in state.Transitions)

    def next_state(self, state, symbol):
        if symbol == self.empty:
            return state
        if self.transition_legal(state, symbol):
            return state.get_transition(symbol).get_end_state()

    def state_from_word(self,word):
        starting_state = [x for x in self.states if x.is_start is True][0]
        current_state = starting_state
        for symbols in word:
            current_state = self.next_state(current_state,symbols)
        return current_state

    def transition_output(self, state, symbol):
        if self.transition_legal(state, symbol):
            return state.get_transition(symbol).output
        else:
            return "No Transition from this state: " + str(State) + " " + str(symbol)

    def word_output(self, word, offset_word=None):
        if offset_word is not None:
            starting_state = self.state_from_word(offset_word)
        else:
            starting_state = [x for x in self.states if x.is_start is True][0]
        current_state = starting_state
        output_list = []
        for symbols in word:
            output = current_state.get_transition(symbols)
            current_state = self.next_state(current_state, symbols)
            if output is None:
                continue
            output = output.output
            output_list.append(output)
        return output_list


class State(object):

    def __init__(self, id, accepting=False, is_start=False):
        self.id = id
        self.Transitions = []
        self.is_accepting = accepting
        self.is_start = is_start
        self.degree = len(self.Transitions)
        self.empty = []

    def add_transition(self, state, symbol, output, is_loopback=False):
        self.Transitions.append(Transition(self, state, symbol, output, is_loopback))
        self.degree = len(self.Transitions)

    def print_transitions(self):
        print "Transitions for State:" + str(self.id) + " " + str(self.Transitions)

    def get_transition(self, symbol):
        # Get the transition for the above symbol
        if symbol == self.empty:
            return None
        transition = next((t for t in self.Transitions if t.symbol == symbol),None)
        if transition is None:
            print "NO TRANSITION FOUND FOR STATE:" + str(self.id) + " " + "AND SYMBOL " + str(symbol)
        return transition

    def get_transition_symbols(self):
        symbols = []
        for x in self.Transitions:
            symbols.append(x.symbol)
        return symbols

    def get_transition_outputs(self):
        outputs = []
        for x in self.Transitions:
            outputs.append(x.output)
        return outputs

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

    def __init__(self, state_1, state_2, symbol, output, is_loopback):
        self._id = self.__class__._ID
        self.__class__._ID += 1
        self.state_1 = state_1
        self.state_2 = state_2
        self.symbol = symbol
        self.output = output
        self.is_loopback = is_loopback

    def __str__(self):
        return '(ID: ' + str(self._id) + \
               ' Start State:' + str(self.state_1) + \
               ' End State:' + str(self.state_2) + \
               ' Transition Symbol:' + str(self.symbol) +\
               ' Outputs' + str(self.output) + ')'

    def __repr__(self):
            return ' \n Start State:' + str(self.state_1) + \
                   ' End State:' + str(self.state_2) + \
                   ' Transition Symbol:' + str(self.symbol) + \
                   ' LB:' + str(self.is_loopback) + \
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
        self.symbols.sort()

    def __len__(self):
        return len(self.symbols)


# Mealy Machines have outputs on transitions
class Outputs(object):
    def __init__(self, outputs):
        self.outputs = list(set(outputs))
        self.outputs.sort()

    def __len__(self):
        return len(self.outputs)