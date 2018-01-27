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
        current_experiments = self.experiments[:]
        suffix_closed_experiments = []
        for x in current_experiments:
            suffix_closed_experiments.append(self.build_suffixes_fixes_for_symbol(x))



    def prefix_close_states(self):
        # Create one list for top and bottom of the table
        current_states = self.states[:]
        prefixed_closed_states = []
        for x in current_states:
            prefixed_closed_states.extend(self.build_prefixes_for_symbol(x))

        prefixed_closed_states = [i for i in prefixed_closed_states if i not in self.states]
        prefixed_closed_states = [i for i in prefixed_closed_states if i not in self.possible_states]
        if prefixed_closed_states:
            self.experiments.append(prefixed_closed_states)

    # def suffix_close_experiments(self):

    # Output from when we combine the state from the column and the experiment
    def output_from_state_concat(self, mealy, state, experiment):
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










