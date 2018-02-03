import StateMachineComponents
import itertools

class ObservationTable(object):

    def __init__(self, alphabet, logging=False):

        self.states = [[]]
        self.experiments = [[s] for s in alphabet.symbols]
        self.possible_states = [[s] for s in alphabet.symbols]
        self.results = []
        self.diction = {}
        self.top_dict = {}
        self.bottom_dict = {}
        self.logging = logging
        self.symbols = alphabet.symbols

        self.print_table()

    @staticmethod
    def build_prefixes(symbols):
        return filter(None,[symbols[:i] for i in range(len(symbols) + 1)])

    @staticmethod
    def build_suffixes(symbols):
        return filter(None,[symbols[i:] for i in range(len(symbols) + 1)])

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

    def add_experiment(self, experiment):
        self.experiments.append(experiment)

    def add_state(self, state):
        self.states.append(state)

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
        sc_experiments.sort()
        sc_experiments = list(s_c_experiments for s_c_experiments,_ in itertools.groupby(sc_experiments))
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
        pc_states.extend(self.possible_states)
        pc_states = list(pc_states for pc_states,_ in itertools.groupby(pc_states))
        for x in pc_states[:]:
            if self.states.__contains__(x):
                pc_states.remove(x)
            elif self.possible_states.__contains__(x):
                pc_states.remove(x)
        if len(pc_states) > 0:
            self.possible_states.extend(pc_states)

    def extend_states(self):
        new_list = []
        for state in self.states:
            if not state:
                continue
            for symbols in self.symbols:
                temp_s = state[:]
                temp_s.append(symbols)
                new_list.append(temp_s)
        new_states = self.possible_states[:]
        new_states.extend(new_list)
        new_states.sort()
        new_states = list(pc_states for pc_states,_ in itertools.groupby(new_states))
        self.possible_states = new_states


    # Output for all states listed in the observation table
    def state_experiment_output(self,mealy):
        self.diction = {}
        for state in self.states:
            for experiment in self.experiments:
                self.results.append(self.output_from_state_concat(mealy,state,experiment))
                self.top_dict[str(state) + ":" + str(experiment)] = self.output_from_state_concat(mealy,state,experiment)

        for state in self.possible_states:
            for experiment in self.experiments:
                self.results.append(self.output_from_state_concat(mealy,state,experiment))
                self.bottom_dict[str(state) + ":" + str(experiment)] = self.output_from_state_concat(mealy, state, experiment)

    # returns the output for a line in the table for a given state row
    def get_line_from_table(self, state_line):
        joint_dict = self.merge_two_dicts(self.top_dict, self.bottom_dict)
        all_keys = self.top_dict.keys()
        all_keys_bottom = self.bottom_dict.keys()
        all_keys.extend(all_keys_bottom)
        state_keys = []
        for x in all_keys:
            if str(state_line) in x.split(":")[0]:
                state_keys.append(x)
        outputs_for_line = []
        for x in state_keys:
            outputs_for_line.append(str(x) + ":" +str(joint_dict[x]))

        return outputs_for_line

    # boolean return on if the table is closed
    #TODO: Unfinished
    def is_closed(self):
        if self.logging:
            print '------------------------------------------'
            print "CHECKING CLOSURE..."
            print '------------------------------------------\n'

        for x in self.possible_states:
            states_to_add = []
            output_line = self.get_line_from_table(x)
            output_line.sort(key=lambda s: s.split(":")[1])
            outputs = [t.split(":")[2] for t in output_line]
            for y in self.states:
                t_output_line = self.get_line_from_table(y)
                t_output_line.sort(key=lambda s: s.split(":")[1])
                t_outputs = [y.split(":")[2] for y in t_output_line]

                if self.logging:
                    print "COMPARE:" + str(t_output_line) + " TO " + str(output_line)
                if t_outputs != outputs:
                    states_to_add.append(x)
                    break

            # Move from bottom half of table to the top half
            print "States to add:" + str(states_to_add)
            self.states.extend(states_to_add)
            for x in states_to_add:
                if self.possible_states.__contains__(x):
                    print "REMOVING: " + str(x)
                    self.possible_states.remove(x)

    # Get the output for a given state and experiment, returns a list with one elements
    def get_state_output(self, state, experiment):
        return self.diction[str(state) + str(experiment)]
