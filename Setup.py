from StateMachineComponents import *

if __name__ == '__main__':
    print 'Generating Machine'
    print '------------------------------------------'

    # Create the machine
    states = 3
    accepting = 1
    symbols = [1, 2]
    outputs = [0,1]

    test_word = [1,2,3]

    # Create the alphabet object to pass to the state machine
    alphabet = Alphabet(symbols)
    # Create a state machine with the states and symbols
    Mealy = MealyMachine(states, symbols, outputs)
    Mealy.random_walk()
    Mealy.print_states()
    Mealy.print_machine_transitions()

    print 'Generation Complete'
    print '------------------------------------------'
    print Mealy.is_accepted(test_word)
