import StateMachineComponents
import itertools
from terminaltables import AsciiTable

class ObservationTable(object):

    def __init__(self, alphabet, logging=False):

        self.states = [[]]
        self.experiments = [[s] for s in alphabet.symbols]
        self.possible_states = [[s] for s in alphabet.symbols]
        self.results = []
        self.diction = {}
        self.top_dict = {}
        self.bottom_dict = {}

        self.print_table()

    @staticmethod
    def build_prefixes_for_symbol(symbols):
        return filter(None,[symbols[:i] for i in range(len(symbols) + 1)])

    @staticmethod
    def build_suffixes_fixes_for_symbol(symbols):
        return filter(None,[symbols[i:] for i in range(len(symbols) + 1)])

    def add_experiment(self, experiment):
        self.experiments.append(experiment)

    def add_state(self, state):
        self.states.append(state)

    def print_table(self):
        print "States: " + str(self.states)
        print "Experiments:" + str(self.experiments)
        print "Possible States:" + str(self.possible_states)

    def suffix_close_experiments(self):
        current_experiments = [[1], [0,1], [1,1], [1,0,1,1]]
        s_c_experiments = []
        for x in current_experiments:
            s_c_experiments.extend(self.build_suffixes_fixes_for_symbol(x))

        s_c_experiments.sort()
        s_c_experiments = list(s_c_experiments for s_c_experiments,_ in itertools.groupby(s_c_experiments))
        print s_c_experiments



    def prefix_close_states(self):
        # Create one list for top and bottom of the table
        current_states = self.states[:]
        pc_states = []
        for x in current_states:
            pc_states.extend(self.build_prefixes_for_symbol(x))

        pc_states.extend(self.possible_states)
        pc_states = list(pc_states for pc_states,_ in itertools.groupby(pc_states))

        print "PREFIXED:" + str(pc_states)


    # def suffix_close_experiments(self):

    # Output from when we combine the state from the column and the experiment
    def output_from_state_concat(self, mealy, state, experiment):
        print "STATE: " + str(state) + " EXPERIMENT: " + str(experiment)
        return mealy.word_output(experiment, state)

    # Output for all states listed in the observation table
    def state_experiment_output(self,mealy):
        for state in self.states:
            for experiment in self.experiments:
                self.results.append(self.output_from_state_concat(mealy,state,experiment))
                self.diction[str(state) + str(experiment)] = self.output_from_state_concat(mealy,state,experiment)

        for state in self.possible_states:
            for experiment in self.experiments:
                self.results.append(self.output_from_state_concat(mealy,state,experiment))
                self.diction[str(state) + str(experiment)] = self.output_from_state_concat(mealy, state, experiment)

        print self.diction

    def get_state_output(self, state, experiment):
        return self.diction[str(state) + str(experiment)]










