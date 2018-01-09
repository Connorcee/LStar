from StateMachineComponents import *

if __name__ == '__main__':
    logging = True
    print 'Generating Machine'
    print '------------------------------------------'

    # Create the machine
    states = 400
    accepting = 1
    symbols = [1,2,3,4,5,6,7,8,9]
    outputs = [0,1]
    randomise = True

    test_word = [1,2,1]

    # Create the alphabet object to pass to the state machine
    alphabet = Alphabet(symbols)
    # Create a state machine with the states and symbols
    Mealy = MealyMachine(states, symbols, outputs, accepting, randomise)
    if logging:
        Mealy.print_states()
        Mealy.print_machine_transitions()

    print 'Generation Complete'
    print '------------------------------------------'
    Mealy.is_accepted(test_word,logging)
    Mealy.create_random_legal_transition()
