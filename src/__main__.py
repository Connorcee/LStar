from StateMachineComponents import *

from src.LStar import ObservationTable


def main(args=None):
    logging = False
    # Create the machine
    states = 10
    symbols = [0, 1]
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

    ot.add_state([1])
    ot.add_state([0])
    ot.add_state([1,1])
    ot.add_state([0,0])

    ot.state_experiment_output(Mealy)
    ot.print_table()
    temp = ot.is_closed()

    while temp is not None:
        ot.add_state(temp)
        ot.state_experiment_output(Mealy)
        temp = ot.is_closed()
    ot.print_table()

    ot.is_consistent()

if __name__ == '__main__':
    main()


