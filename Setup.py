from StateMachineComponents import *
from LStar import ObservationTable

if __name__ == '__main__':

    logging = False
    # Create the machine
    states = 4
    symbols = [1, 2, 3]
    outputs = [0, 1, 2]
    randomise = True
    test_word = [1, 2, 1]
    alphabet = Alphabet(symbols)
    ot = ObservationTable()

    print 'Generating Machine'
    print '------------------------------------------\n'
    # Create a state machine with the states and symbols
    Mealy = MealyMachine(states, symbols, outputs, randomise)

    print 'Initializing Observation Table'
    print '------------------------------------------'
    ot.initialse_table(alphabet, logging)
    print 'Observation Table Initialized'
    print '------------------------------------------\n'

    if logging:
        Mealy.print_states()
        Mealy.print_machine_transitions()

    print 'Generation Complete'
    print '------------------------------------------'

    Mealy.random_transition_pass()
    Mealy.build_loopbacks()
    Mealy.print_machine_transitions()
