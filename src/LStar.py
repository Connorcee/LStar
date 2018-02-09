import StateMachineComponents
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
        print self.states
        for x in self.states:
            outputstring = self.get_line_from_table(x)
            outputstring.sort(key=lambda s: s.split(":")[1])
            out = [t.split(":")[2] for t in outputstring]
            state_output_dict[str(x)] = str(out)
        print "STATE OUTPUT: " + str(state_output_dict)

        for x in self.possible_states:
            outputstring = self.get_line_from_table(x)
            outputstring.sort(key=lambda s: s.split(":")[1])
            out = [t.split(":")[2] for t in outputstring]
            possible_output_dict[str(x)] = str(out)
        print "POSSIBLE STATE OUTPUT: " + str(possible_output_dict)

        for x in possible_output_dict:
            print possible_output_dict[x] in state_output_dict.values()
            if not possible_output_dict[x] in state_output_dict.values():
                print "IS: " + str(possible_output_dict[x])
                print "IN: " + str(state_output_dict.values())
                print "ADDING: " + x
                return ast.literal_eval(x)

        return None

    def is_consistent(self):
        pass

    def all_equivalent_states(self):
        state_lines = {}
        for state in self.states:
            out = self.get_line_from_table(state)
            out.sort(key=lambda s: s.split(":")[1])
            out = [t.split(":")[2] for t in out]
            state_lines[str(state)] = str(out)
            