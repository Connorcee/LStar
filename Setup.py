from StateMachineComponents import *

if __name__ == '__main__':

    # Number of states the state machine should have
    states = 10
    # Number of accepting states
    accepting = 3
    # Symbols for the alphabet
    symbols = [0, 1, 2, 3]
    # Create the alphabet object to pass to the state machine
    alphabet = Alphabet(symbols)
    # Create a state machine with the states and symbols
    FSM = StateMachine(states,symbols)
    # Assign some states to be random
    FSM.random_acceptors(accepting)

    FSM.print_states()
    FSM.random_walk()
    FSM.print_machine_transitions()
    FSM.print_states()