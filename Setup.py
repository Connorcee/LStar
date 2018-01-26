from StateMachineComponents import *
from LStar import ObservationTable

if __name__ == '__main__':

    logging = True
    # Create the machine
    states = 4
    symbols = [0, 1, 2]
    outputs = [0, 1]
    randomise = True
    test_word = [1, 2, 1]
    alphabet = Alphabet(symbols)

    print 'Generating Machine'
    print '------------------------------------------\n'
    # Create a state machine with the states and symbols
    Mealy = MealyMachine(states, symbols, outputs, randomise)
    Mealy.random_transition_pass()
    Mealy.build_loopbacks()

    if logging:
        Mealy.print_states()
        Mealy.print_machine_transitions()

    print 'Generation Complete'
    print '------------------------------------------'
    print 'Initializing Observation Table'
    print '------------------------------------------'
    ot = ObservationTable(alphabet,logging)
    print 'Observation Table Initialized'
    print '------------------------------------------\n'

    ot.add_state([0, 1])
    ot.add_state([1, 0, 1, 1])
    ot.add_state([1, 0, 2, 1])
    ot.add_state([1, 0])
    ot.print_table()

    ot.prefix_close_states()


