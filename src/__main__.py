from StateMachineComponents import *

from src.LStar import ObservationTable


def main(args=None):
    logging = True
    # Create the machine
    states = 2
    symbols = [0, 1]
    outputs = [0, 1]
    randomise = False
    test_word = [1, 2, 1]
    alphabet = Alphabet(symbols)

    print 'Generating Machine'
    print '------------------------------------------\n'
    # Create a state machine with the states and symbols
    Mealy = MealyMachine(states, symbols, outputs, randomise)
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

    ot.state_experiment_output(Mealy)
    print ot.is_closed()
    ot.state_experiment_output(Mealy)
    ot.print_table()

    print ot.is_closed()
    ot.state_experiment_output(Mealy)
    ot.print_table()

    print ot.is_closed()
    ot.state_experiment_output(Mealy)
    ot.print_table()


if __name__ == '__main__':
    main()


