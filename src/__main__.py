from StateMachineComponents import *

from src.LStar import ObservationTable


def main(args=None):
    logging = True
    # Create the machine
    states = 5
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

    ot.prefix_close_states()
    ot.suffix_close_experiments()
    ot.state_experiment_output(Mealy)
    ot.print_table()
    ot.is_closed()
    ot.prefix_close_states()
    ot.suffix_close_experiments()
    ot.state_experiment_output(Mealy)
    ot.print_table()


if __name__ == '__main__':
    main()


