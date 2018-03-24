from random import *
import sys
import LStar as tools
from operator import itemgetter
import itertools
import ast
import os
import uuid
from time import sleep

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
                    print '{} {} {} {} S\n'.format(t.state_1.id,t.state_2.id,t.symbol,t.output)
                    f.write('{} {} {} {} S\n'.format(t.state_1.id,t.state_2.id,t.symbol,t.output))
                else:
                    print '{} {} {} {} N\n'.format(t.state_1.id, t.state_2.id, t.symbol, t.output)
                    f.write('{} {} {} {} N\n'.format(t.state_1.id, t.state_2.id, t.symbol, t.output))
        f.close()

    def minimise(self):
        minimizer = Minimizer(self)
        exit()
        equiv = []
        if equiv is None:
            return None
        for item in equiv:
            self.combine_states(item)

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

class Minimizer(object):
    def __init__(self, mealy_machine):
        self.mealy_machine = mealy_machine
        self.table = self.generate_initial_table()
        self.table = self.Table(self.table, self.mealy_machine)

    class Row:
        def __init__(self, group, outputs, target_groups, state_id, target_states):
            self.group = group
            self.outputs = outputs
            self.target_groups = target_groups
            self.state_id = int(state_id)
            self.target_states = target_states

    class Table:
        def __init__(self, table, mealy):
            self.mealy = mealy
            self.largest_group = self.largest_group_number(table)
            self.original_table = table
            self.id_to_group_mapping = self.build_id_to_group_mapping(table)
            self.print_row_dict()
            print self.states_in_same_group()

        def build_id_to_group_mapping(self, table):
            row_dict = {}
            for row in table:
                row_dict[str(row.state_id)] = row.group
            return row_dict

        def print_row_dict(self):
            print self.id_to_group_mapping

        def largest_group_number(self, table):
            set_of_groups = set([])
            for rows in table:
                set_of_groups.add(rows.group)
            return max(set_of_groups)

        def new_group_id(self):
            self.largest_group += 1
            new_id = self.largest_group
            return new_id

        def groups(self):
            return self.largest_group

        def states_in_same_group(self):
            return self.mealy.duplicate_keys(self.id_to_group_mapping)

    # Create a table that shows the mealy machines grouped states and their outputs
    # This is used to identify equivalent states
    def generate_initial_table(self):
        states = self.mealy_machine.states[:]
        inputs = self.mealy_machine.alphabet.symbols[:]
        # Table to perform the reduction
        table = []
        # Get outputs and next states for each state
        for s in states:
            next_state_list = []
            output_list = []
            for i in inputs:
                output_list.append(self.mealy_machine.transition_output(s,i))
                next_state_list.append(self.mealy_machine.next_state(s,i).id)
            row = [s.id,next_state_list,str(output_list)]
            table.append(row)
        perms = []
        # Create the list of different output perms
        for line in table:
            if perms.__contains__(line[2]):
                pass
            else:
                perms.append(line[2])
        # make perms a dictionary, mapping each element to a number
        perms = {k: v for v, k in enumerate(perms)}
        # Add mappings to table
        for line in table:
            line.append(perms[line[2]])
        for line in table:
            temp = []
            for ele in line[1]:
                item = next(x for x in table if x[0] == ele)
                temp.append(item[3])
            line.append(temp)
        table.sort(key=lambda x: x[3])
        for line in table:
            print "Line " + str(line)

        objected_table = []
        for row in table:
            state_id = row[0]
            target_states = row[1]
            outputs = row[2]
            group = row[3]
            target_groups = row[4]
            objected_table.append(self.Row(group,outputs,target_groups,state_id,target_states))
        return objected_table


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