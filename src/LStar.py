import itertools
import ast
from StateMachineComponents import MealyMachine
from StateMachineComponents import *


class ObservationTable(object):

    def __init__(self, alphabet, mealy, logging=False):
        self.states = [[]]
        self.experiments = [[s] for s in alphabet.symbols]
        self.possible_states = [[s] for s in alphabet.symbols]
        self.results = []
        self.top_dict = {}
        self.bottom_dict = {}
        self.logging = logging
        self.symbols = alphabet.symbols
        self.mq_counter = 0
        self.state_experiment_output(mealy)
        self.outputs = mealy.outputs
        self.equivalent_states = []

    @staticmethod
    def remove_a_from_b(a, b):
        for x in b:
            if a.__contains__(x):
                b.remove(x)

    @staticmethod
    def build_prefixes(symbols):
        return filter(None, [symbols[:i] for i in range(len(symbols) + 1)])

    @staticmethod
    def build_suffixes(symbols):
        return filter(None, [symbols[i:] for i in range(len(symbols) + 1)])

    def state_cover(self):
        return self.states[:]

    def distinguishing_elements(self):
        return self.experiments[:]

    def build_machine(self):
        number_of_states = len(self.different_states())
        transitions = []
        states = self.states[:]
        equivalent_choices = []
        equivalent_dict = {}
        # Map equivalent states to a random equivalent state
        if len(self.equivalent_states) > 0:
            for equiv in self.equivalent_states:
                if [] in equiv:
                    rand_state = []
                else:
                    rand_state = choice(equiv)
                for pairs in equiv:
                    equivalent_dict[str(pairs)] = rand_state

            for index, value in enumerate(states):
                if str(value) in equivalent_dict:
                    states[index] = ast.literal_eval(str(equivalent_dict[str(value)]))
        states = self.remove_dups(states)

        for state in states:
            for symbols in self.symbols:
                transitions.append([str(state),
                                    str(self.next_state(state, symbols)),
                                    str(symbols),
                                    str(self.table_output(state, [symbols]))])
        transitions = self.remove_dups(transitions)
        for index, value in enumerate(transitions):
            if value[1] in equivalent_dict:
                transitions[index][1] = str(equivalent_dict[str(value[1])])
        Mealy = MealyMachine(number_of_states, self.symbols, self.outputs.outputs, False, False, True, transitions)
        return Mealy

    def print_transitions_of_new_machine(self, transitions):
        print "TRANSITIONS"
        for x in transitions:
            print x

    def table_output(self, state=None, experiment=None):
        s = str(state) + ":" + str(experiment)
        return self.top_dict[s]

    def next_state(self, state, symbol):
        if not self.states.__contains__(state):
            print "LStar.next_state " + str(state) + " state no found"
            return None

        appended_state = state[:]
        appended_state.extend([symbol])
        line = self.get_line_from_table
        current_row_sequence = self.strip_line_of_labels(line(state))
        appended_row_sequence = self.strip_line_of_labels(line(appended_state))

        if current_row_sequence == appended_row_sequence:
            return state
        else:
            for state in self.states:
                output_row = self.strip_line_of_labels(line(state))
                if output_row == appended_row_sequence:
                    return state

    # Loop through the "states" and identify the different state rows
    def different_states(self):
        rows = []
        stripper = self.strip_line_of_labels
        for state in self.states:
            rows.append(self.get_line_from_table(state))
        rows.sort(key=len)
        rows = [stripper(s) for s in rows]
        rows = self.remove_dups(rows)
        return rows

    # Merges two dictionaries, x first and then y
    @staticmethod
    def merge_two_dicts(x, y):
        z = x.copy()  # start with x's keys and values
        z.update(y)  # modifies z with y's keys and values & returns None
        return z

    # Output from the state concatenated with the experiment
    def output_from_state_concat(self, mealy, state, experiment):
        self.mq_counter += 1
        return mealy.word_output(experiment, state)

    @staticmethod
    def remove_dups(_list):
        _list.sort()
        _list = list(_list for _list, _ in itertools.groupby(_list))
        return _list

    def add_experiment(self, experiment):
        self.experiments.append(experiment)
        self.suffix_close_experiments()

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
        top = self.top_dict.items()
        bottom = self.bottom_dict.items()
        top.sort(key=lambda tup: (len(tup[0]), tup[0], tup[0].split(":")[1]))
        bottom.sort(key=lambda tup: (len(tup[0]), tup[0], tup[0].split(":")[1]))
        print '------------------------------------------'
        print 'Observation Table'
        print '------------------------------------------'
        print "States: " + str(self.states)
        print "Experiments:" + str(self.experiments)
        print "Possible States:" + str(self.possible_states)
        print "Dictionary Top: "
        self.print_block(top)
        print "Dictionary Bottom: "
        self.print_block(bottom)
        print '------------------------------------------\n'

    def print_block(self, block):
        counter = 0
        for entries in block:
            print entries,
            counter += 1
            if counter == len(self.experiments):
                print
                counter = 0

    def suffix_close_experiments(self):
        current_experiements = self.experiments[:]
        sc_experiments = []
        for x in current_experiements:
            sc_experiments.extend(self.build_suffixes(x))
        sc_experiments = self.remove_dups(sc_experiments)
        self.experiments = sc_experiments

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
    def state_experiment_output(self, mealy):
        self.top_dict = {}
        self.bottom_dict = {}
        for state in self.states:
            for exp in self.experiments:
                self.results.append(self.output_from_state_concat(mealy, state, exp))
                self.top_dict[str(state) + ":" + str(exp)] = self.output_from_state_concat(mealy, state, exp)

        for state in self.possible_states:
            for exp in self.experiments:
                self.results.append(self.output_from_state_concat(mealy, state, exp))
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
            outputs_for_line.append(str(x) + ":" + str(joint_dict[x]))

        return outputs_for_line

    def strip_line_of_labels(self, line):
        line.sort(key=lambda s: s.split(":")[1])
        return [t.split(":")[2] for t in line]

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
                if self.logging:
                    print "Closure: " + str(x)
                return ast.literal_eval(x)
        return None

    def is_consistent(self):
        equiv = self.all_equivalent_states()
        self.save_consistent_states(equiv)
        if self.logging:
            print "EQUIVALENT: " + str(equiv)
        states = self.equivalence_test(equiv)
        if not states:
            return None
        else:
            return states

    def save_consistent_states(self, states):
        self.equivalent_states = []
        for state_pairs in states:
            temp = []
            for pair in state_pairs:
                temp.append(ast.literal_eval(pair))
            self.equivalent_states.append(temp)

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
                print "EQUIVALENT STATES: " + str(matches)
            # self.equivalent_rows = matches[:]
        return matches.values()

    def equivalence_test(self, states):
        total_to_add = []
        for equivalent in states:
            # choose two random equivalent states
            combinations = itertools.combinations(equivalent, 2)
            for x in combinations:
                for symbols in self.symbols:
                    temp1 = ast.literal_eval(x[0])
                    temp2 = ast.literal_eval(x[1])
                    temp1.append(symbols)
                    temp2.append(symbols)
                    total_to_add.extend(self.check_state_equivalence(temp1, temp2, symbols))
        total_to_add = self.remove_dups(total_to_add)
        if self.logging:
            print "TOTAL TO ADD: " + str(total_to_add)
        return total_to_add

    def check_state_equivalence(self, state_1, state_2, symbol):
        state1_line = self.get_line_from_table(state_1)
        state1_line.sort(key=lambda s: s.split(":")[1])
        state2_line = self.get_line_from_table(state_2)
        state2_line.sort(key=lambda s: s.split(":")[1])

        experiment_to_add = []
        for out_1, out_2 in zip(state1_line, state2_line):
            if out_1.split(":")[2] != out_2.split(":")[2]:
                extended = symbol
                experiment = out_1.split(":")[1]
                experiment = ast.literal_eval(experiment)
                experiment.insert(0, extended)
                experiment_to_add.append(experiment)

        return experiment_to_add
