from random import *
import sys
import os
import itertools

class MealyMachine(object):
    def __init__(self, number_of_nodes, alphabet, outputs, path=False, randomise=False, from_table=False, transitions=None):
        sys.setrecursionlimit(1500)
        self.number_of_nodes = number_of_nodes
        self.alphabet = Alphabet(alphabet)
        self.outputs = Outputs(outputs)
        self.starting_state = None
        self.Walked = False
        self.states = [State(count) for count in range(0, number_of_nodes)]
        self.statesDict = self.build_state_dictionary()
        self.randomise = randomise
        self.empty = []

        # Handle machine generation
        if randomise:
            self.random_walk()
        elif not randomise and from_table:
            self.build_machine_from_ot(transitions)
        elif path is not False and randomise is False:
            self.load_machine(path)
        elif path is False and randomise is False:
            print "NO PATH PROVIDED, NO RANDOM ALLOWED, EXITING"
            exit()

    @staticmethod
    def remove_dups(_list):
        _list.sort()
        _list = list(_list for _list, _ in itertools.groupby(_list))
        return _list

    # Build a machine from an observation table
    def build_machine_from_ot(self, transitions):
        states = []
        state_mapping = {}
        for transition in transitions:
            states.append(transition[0])
        states = self.remove_dups(states)

        counter = 0
        for state in states:
            state_mapping[str(state)] = counter
            counter += 1
        for t in transitions:
            # State beginning transition
            t[0] = state_mapping[t[0]]
            # State targeting transition
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
            dir_path = os.path.dirname(os.path.realpath(__file__))
            if sys.platform == "win32":
                dir_path = dir_path + '\\State\\{}\\'.format(self.number_of_nodes)
            else:
                dir_path = dir_path + '/State/{}/'.format(self.number_of_nodes)
            file_object = open(dir_path + path,"r")
        else:
            print "LOAD PATH IS INCORRECT"
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

    def save_machine(self, path=False):
        if not path:
            name = "STATES " + str(len(self.states))
        else:
            name = path
        f=open(name,"w+")
        print self.states
        for s in self.states:
            for t in s.Transitions:
                if s.is_start:
                    f.write('{} {} {} {} S\n'.format(t.state_1.id,t.state_2.id,t.symbol,t.output))
                else:
                    f.write('{} {} {} {} N\n'.format(t.state_1.id, t.state_2.id, t.symbol, t.output))
        f.close()

    @staticmethod
    def minimise(mealy, logging):
        minimizer = Minimizer(mealy, logging)
        return minimizer.minimize()

    def combine_states(self, list_of_states):
        if list_of_states is None:
            return None
        if len(list_of_states) < 2:
            return None
        state_list = []
        for items in list_of_states:
            # Get all states to be combined
            state = next(x for x in self.states if x.id == items)
            state_list.append(state)
        # Check is any of the states are the start state
        start = [x for x in state_list if x.is_start]
        if not start:
            # List is empty, merge into any state
            start = state_list.pop()

        for elem in state_list:
            for s in self.states:
                for transitions in s.Transitions:
                    if transitions.state_2.id == elem.id:
                        transitions.state_2 = start
            self.states.remove(elem)
        self.statesDict = self.build_state_dictionary()

    def duplicate_keys(self, dic):
        rev_multidict = {}
        for key, value in dic.items():
            rev_multidict.setdefault(value, set()).add(key)
        x = [values for key, values in rev_multidict.items() if len(values) > 1]
        for index, ele in enumerate(x):
            x[index] = list(ele)
        return x

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
        self.Transitions.sort(key=lambda x: x.symbol)

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
        trans = self.Transitions[:]
        trans.sort(key=lambda x: x.symbol)
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


class Minimizer(object):
    def __init__(self, mealy_machine, logging=False):
        self.logging = logging
        self.empty = "empty"
        self.equivalent = "EQUIVALENT"
        self.cross = "X"
        self.mealy_machine = mealy_machine
        self.implication_table = self.generate_empty_table(len(mealy_machine.states))
        self.generate_implication_table()
        while self.reverse_pass():
            self.reverse_pass()
        self.remove_unequivalent()

    class TableRow(object):
        def __init__(self, state):
            self.state = state
            self.next_states = {}
            self.outputs = {}

        def add_next_state(self, symbol, state):
            self.next_states[symbol] = state

        def add_output(self,symbol, state):
            self.outputs[symbol] = state

        def __repr__(self):
            return "State: " + str(self.state) + " Next States: " \
                   + str(self.next_states) \
                   + " Outputs: " \
                   + str(self.outputs)

    def minimize(self):
        # Take first tuple and combine the two states, then replace ach occurence of the first element in the list
        # with the second, then remove the tuple
        # Convert list of tuples to list of lists
        states = [list(x) for x in self.implication_table.keys()]
        while len(states) != 0:
            active = states.pop()
            state_0 = active[0]
            state_1 = active[1]
            if state_1 == state_0:
                continue
            self.mealy_machine.combine_states(active)
            states = self.replace_elements(states, state_0, state_1)
        return self.mealy_machine

    def replace_elements(self, states, element_to_remove, element_to_replace):
        for ind, val in enumerate(states):
            for index, ele in enumerate(val):
                if states[ind][index] == element_to_remove:
                    states[ind][index] = element_to_replace
        return states

    def remove_unequivalent(self):
        self.implication_table = {k:v for k,v in self.implication_table.items() if v != "X"}

    # Iterate through the table removing anything associated with unequivalence
    def reverse_pass(self):
        change = False
        for key in self.implication_table.keys():
            if self.implication_table[key] == self.cross:
                for key_0, value in self.implication_table.iteritems():
                    if isinstance(self.implication_table[key_0],(list,)):
                        if key in value:
                            change = True
                            self.implication_table[key_0] = self.cross
            else:
                continue
        return change

    def generate_implication_table(self):
        ns = self.mealy_machine.next_state
        for key, value in self.implication_table.iteritems():
            state_1 = self.mealy_machine.statesDict[key[0]]
            state_2 = self.mealy_machine.statesDict[key[1]]
            # If they have the same outputs
            if self.output_check(state_1, state_2):
                # Create implied pairs
                pairs = []
                for symbols in self.mealy_machine.alphabet.symbols:
                    tup = (ns(state_1,symbols).id,ns(state_2,symbols).id)
                    if tup[0] != tup[1] and set(tup) != set(key):
                        tup = list(tup)
                        tup.sort()
                        tup = tuple(tup)
                        pairs.append(tup)
                if not pairs:
                    pairs = self.equivalent
                self.implication_table[key] = pairs
            else:
                # states are not equivalent
                self.implication_table[key] = self.cross

    def print_implication_table(self):
        for key,value in self.implication_table.iteritems():
            print str(key) + " - " + str(value)

    def generate_empty_table(self, no_states):
        columns = range(0,no_states - 1)
        rows = list(reversed(range(1,no_states)))
        table_dict = {}
        for column in columns:
            for row in rows:
                if column == row:
                    break
                key = (column,row)
                table_dict[key] = self.empty
        return table_dict

    @staticmethod
    def output_check(state1, state2):
        s1_o = state1.get_transition_outputs()
        s2_o = state2.get_transition_outputs()
        return s1_o == s2_o


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