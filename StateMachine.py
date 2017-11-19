class StateMachine:

    def __init__(self, number_of_nodes, alphabet, number_of_accepting=1):

        self.Number_of_nodes = number_of_nodes

        self.alphabet = Alphabet(alphabet)

        self.States = []
        self.States = [State(count) for count in range(0,number_of_nodes)]

    def print_states(self):
        print self.States


class State:

    def __init__(self, _id, accepting=False, is_start=False):
        self._id = _id
        self.Transitions = []
        self.is_accepting = accepting
        self.is_start = is_start

    def add_transition(self, state, symbol):
        self.Transitions.append(Transition(self, state, symbol))

    def print_transitions(self):
        print self.Transitions

    def set_accept(self, accepting):
        self.is_accepting = accepting

    def __str__(self):
        return str(self._id)

    def __repr__(self):
        return str(self._id)


class Transition:
    _ID = 0

    def __init__(self, state_1, state_2, symbol):
        self._id = self.__class__._ID
        self.__class__._ID += 1
        self.state_1 = state_1
        self.state_2 = state_2
        self.symbol = symbol

    def __str__(self):
        return '(ID: ' + str(self._id) + \
               ' Origin State:' + str(self.state_1) + \
               ' End State:' + str(self.state_2) + \
               ' Transition Symbol:' + str(self.symbol) + ')'

    def __repr__(self):
        return '(ID: ' + str(self._id) + \
               ' Origin State:' + str(self.state_1) + \
               ' End State:' + str(self.state_2) + \
               ' Transition Symbol:' + str(self.symbol) + ')'


class Alphabet:

    def __init__(self, symbols):
        self.symbols = symbols


def main(number_of_states):
    FSM = StateMachine(number_of_states)
    FSM.print_states()
    FSM.States[1].print_transitions()