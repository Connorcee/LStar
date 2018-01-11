from StateMachineComponents import *
import MachineLoader
import sys

if __name__ == '__main__':

    logging = False
    # Create the machine
    states = 4
    accepting = 1
    symbols = [1,2,3,4,5,6,7,8,9]
    outputs = [0,1]
    randomise = False
    test_word = [1,2,1]
    alphabet = Alphabet(symbols)

    print 'Generating Machine'
    print '------------------------------------------'
    # Create a state machine with the states and symbols
    Mealy = MealyMachine(states, symbols, outputs, accepting, randomise)
    if logging:
        Mealy.print_states()
        Mealy.print_machine_transitions()

    print 'Generation Complete'
    print '------------------------------------------'
