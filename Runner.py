from StateMachineComponents import *

if __name__ == '__main__':

    # Number of states the state machine should have
    states = 10
    # Symbols for the alphabet
    symbols = []
    # Create the alphabet object to pass to the state machine
    alphabet = Alphabet(symbols)
    # Create a state machine with the states and symbols
    FSM = StateMachine(states,symbols)

    print FSM.get_states()
