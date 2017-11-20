from StateMachineComponents import *

if __name__ == '__main__':

    # Number of states the state machine should have
    states = 5
    # Symbols for the alphabet
    symbols = [0, 1, 2, 3]
    # Create the alphabet object to pass to the state machine
    alphabet = Alphabet(symbols)
    # Create a state machine with the states and symbols
    FSM = StateMachine(states,symbols)

    FSM.print_states()
    # print FSM.alphabet.symbols

    FSM.random_walk()
    FSM.print_machine_transitions()
