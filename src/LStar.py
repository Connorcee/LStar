import StateMachineComponents
from random import shuffle
import itertools
import ast
from collections import Counter

class ObservationTable(object):

    def __init__(self, alphabet, logging=False):

        self.states = [[]]
        self.experiments = [[s] for s in alphabet.symbols]
        self.possible_states = [[s] for s in alphabet.symbols]
        self.results = []
        self.top_dict = {}
        self.bottom_dict = {}
        self.logging = logging
        self.symbols = alphabet.symbols

        self.print_table()

    @staticmethod
    def remove_a_from_b(a,b):
        for x in b:
            if a.__contains__(x):
                b.remove(x)

    @staticmethod
    def build_prefixes(symbols):
        return filter(None,[symbols[:i] for i in range(len(symbols) + 1)])

    @staticmethod
    def build_suffixes(symbols):
        return filter(None,[symbols[i:] for i in range(len(symbols) + 1)])

    def prepare_table(self, mealy):
        pass

    # Merges two dictionaries, x first and then y
    @staticmethod
    def merge_two_dicts(x, y):
        z = x.copy()  # start with x's keys and values
        z.update(y)  # modifies z with y's keys and values & returns None
        return z

    # Output from the state concatenated with the experiment
    @staticmethod
    def output_from_state_concat(mealy, state, experiment):
        return mealy.word_output(experiment, state)

    @staticmethod
    def remove_dups(_list):
        _list.sort()
        _list = list(_list for _list, _ in itertools.groupby(_list))
        return _list

    def add_experiment(self, experiment):
        self.experiments.append(experiment)

    def add_state(self, state):
        self.states.append(state)
        self.prefix_close_states()
        self.extend_states()
        self.remove_states_from_possible_states()

    def remove_states_from_possible_states(self):
        for x in self.states:
            if self.possible_states.__contains__(x):
                self.possible_states.remove(x)

    def print_table(self):
        print '------------------------------------------'
        print 'Observation Table'
        print '------------------------------------------'
        print "States: " + str(self.states)
        print "Experiments:" + str(self.experiments)
        print "Possible States:" + str(self.possible_states)
        print "Dictionary Top: " + str(self.top_dict)
        print "Dictionary Bottom: " + str(self.bottom_dict)
        print '------------------------------------------\n'

    def suffix_close_experiments(self):
        current_experiments = self.experiments
        sc_experiments = []
        for x in current_experiments:
            sc_experiments.extend(self.build_suffixes(x))
        # remove duplicate states
        sc_experiments = self.remove_dups(sc_experiments)
        # Only add suffixes that are not in the list
        for x in sc_experiments[:]:
            if self.experiments.__contains__(x):
                sc_experiments.remove(x)
                # If there are no suffixes to add, do nothing
        if len(sc_experiments) > 0:
            self.experiments.extend(sc_experiments)
        self.experiments.sort(key=len)

    def prefix_close_states(self):
        # Create one list for top and bottom of the table
        current_states = self.states[:]
        pc_states = []
        for x in current_states:
            pc_states.extend(self.build_prefixes(x))
        pc_states = self.remove_dups(pc_states)
        self.states = pc_states
        self.states.append([])

    def extend_states(self):
        for x in self.states:
            for y in self.symbols:
                new_x = x + [y]
                if not self.states.__contains__(new_x):
                    self.possible_states.append(new_x)
        self.possible_states = self.remove_dups(self.possible_states)

    # Output for all states listed in the observation table
    def state_experiment_output(self,mealy):
        self.diction = {}
        for state in self.states:
            for exp in self.experiments:
                self.results.append(self.output_from_state_concat(mealy, state, exp))
                self.top_dict[str(state) + ":" + str(exp)] = self.output_from_state_concat(mealy, state, exp)

        for state in self.possible_states:
            for exp in self.experiments:
                self.results.append(self.output_from_state_concat(mealy,state,exp))
                self.bottom_dict[str(state) + ":" + str(exp)] = self.output_from_state_concat(mealy, state, exp)

    # returns the output for a line in the table for a given state row
    def get_line_from_table(self, state_line):
        joint_dict = self.merge_two_dicts(self.top_dict, self.bottom_dict)
        all_keys = joint_dict.keys()
        state_keys = []
        for x in all_keys:
            if str(state_line) in x.split(":")[0]:
                state_keys.append(x)
        outputs_for_line = []
        for x in state_keys:
            outputs_for_line.append(str(x) + ":" +str(joint_dict[x]))

        return outputs_for_line

    def is_closed(self):
        state_output_dict = {}
        possible_output_dict = {}
        for x in self.states:
            outputstring = self.get_line_from_table(x)
            outputstring.sort(key=lambda s: s.split(":")[1])
            out = [t.split(":")[2] for t in outputstring]
            state_output_dict[str(x)] = str(out)

        for x in self.possible_states:
            outputstring = self.get_line_from_table(x)
            outputstring.sort(key=lambda s: s.split(":")[1])
            out = [t.split(":")[2] for t in outputstring]
            possible_output_dict[str(x)] = str(out)

        for x in possible_output_dict:
            if not possible_output_dict[x] in state_output_dict.values():
                return ast.literal_eval(x)
        return None

    def is_consistent(self):
        equiv = self.all_equivalent_states()
        print "EQUIVALENT: " + str(equiv)
        self.equivalence_test(equiv)

    def all_equivalent_states(self):
        state_output_dict = {}
        for x in self.states:
            outputstring = self.get_line_from_table(x)
            outputstring.sort(key=lambda s: s.split(":")[1])
            out = [t.split(":")[2] for t in outputstring]
            state_output_dict[str(x)] = str(out)
        items = sorted(state_output_dict.items(), key=lambda x: x[1])
        matches = {}
        for value, group in itertools.groupby(items, lambda x: x[1]):
            keys = [kv[0] for kv in group]
            if len(keys) > 1:
                matches[value] = keys
        if self.logging:
            print "EQUIVALENT STATES UNTESTED: " + str(matches)
        return matches.values()
    
    # TODO: Possible endless loop here, need a way to mark that some states ARE equivalent even after test
    def equivalence_test(self, states):
        for equivalent in states:
            # choose two random equivalent states
            shuffle(equivalent)
            state1 = equivalent.pop()
            state2 = equivalent.pop()
            state1 = ast.literal_eval(state1)
            state2 = ast.literal_eval(state2)
            print "STATE: " + str(state1)
            print "STATE " + str(state2)
            for symbols in self.symbols:
                temp1 = state1[:]
                temp2 = state2[:]
                temp1.append(symbols)
                temp2.append(symbols)
                print "----------------"
                print temp1
                print temp2
                print "EXPERIMENTS TO ADD: " + str(self.check_state_equivalence(temp1, temp2, symbols))
                print "----------------"

    def check_state_equivalence(self,state_1, state_2, symbol):
        state1_line = self.get_line_from_table(state_1)
        state1_line.sort(key=lambda s: s.split(":")[1])
        state2_line = self.get_line_from_table(state_2)
        state2_line.sort(key=lambda s: s.split(":")[1])

        experiment_to_add = []
        for out_1, out_2 in zip(state1_line, state2_line):
            if out_1.split(":")[2] != out_2.split(":")[2]:
                extended = symbol
                print "APPENDED SYMBOL: " + str(extended)
                experiment = out_1.split(":")[1]
                experiment = ast.literal_eval(experiment)
                print "EXPERIMENT: " + str(experiment)
                experiment.insert(0,extended)
                experiment_to_add.append(experiment)

        return experiment_to_add

    def extract_and_extend_experiments(self, state):
        pass
