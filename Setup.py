from StateMachineComponents import *

if __name__ == '__main__':
    print 'Initial Generation of Machine'
    # Number of states the state machine should have
    states = 5
    # Number of accepting states
    accepting = 3
    # Symbols for the alphabet
    symbols = [1, 2, 3]
    # Outputs attached to each transition
    outputs = [0,1]
    # Create the alphabet object to pass to the state machine
    alphabet = Alphabet(symbols)
    # Create a state machine with the states and symbols
    Mealy = MealyMachine(states, symbols, outputs)
    # Assign some states to be random
    Mealy.random_acceptors(accepting)

    Mealy.print_states()
    Mealy.random_walk()
    Mealy.print_machine_transitions()
    print 'Generation Complete'
    print '------------------------------------------'
    print Mealy.transition_legal(Mealy.States[0], 1)
    #print Mealy.States[0].print_transitions()
    if Mealy.transition_legal(Mealy.States[0], 1):
        print Mealy.next_state(Mealy.States[0],1)
    print Mealy.transition_legal(Mealy.States[0], 2)
    print Mealy.transition_legal(Mealy.States[0], 3)
    print Mealy.transition_legal(Mealy.States[0], 4)
