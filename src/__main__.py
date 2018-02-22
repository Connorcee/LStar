from StateMachineComponents import *
import MachinePrinter
from src.LStar import ObservationTable


def main(args=None):
    logging = True
    # Create the machine
    states = 5
    symbols = [0, 1, 2]
    outputs = [0, 1, 2]
    randomise = True
    alphabet = Alphabet(symbols)

    print 'Generating Machine'
    print '------------------------------------------\n'
    # Create a state machine with the states and symbols and run the initial membership checks
    Mealy = MealyMachine(states, symbols, outputs, randomise)
    Mealy.random_transition_pass()
    Mealy.random_transition_pass()
    Mealy.random_transition_pass()
    Mealy.random_transition_pass()
    Mealy.random_transition_pass()
    Mealy.random_transition_pass()
    Mealy.build_loopbacks()

    if logging:
        Mealy.print_states()
        Mealy.print_machine_transitions()

    print 'Generation Complete'
    print '------------------------------------------'
    print 'Initializing Observation Table'
    print '------------------------------------------'
    ot = ObservationTable(alphabet,Mealy,logging)
    print 'Observation Table Initialized to Mealy'
    print '------------------------------------------\n'

    run_l_star(ot, Mealy)

    new_machine = ot.build_machine()
    new_machine.print_machine_transitions()

    printer = MachinePrinter.MachinePrinter()
    printer.print_machine("SUT",Mealy)
    printer.print_machine("Inferred",new_machine)

def run_l_star(ot,Mealy):
    closed_consistent = False
    while not closed_consistent:
        consistent = ot.is_consistent()
        closed = ot.is_closed()
        if consistent is not None:
            print "CONSISTENT: " + str(consistent)
            [ot.add_experiment(x) for x in consistent]
            ot.state_experiment_output(Mealy)
            continue
        if closed is not None:
            ot.add_state(closed)
            ot.state_experiment_output(Mealy)
            continue
        closed_consistent = True
        print "Closed and Consistent"
    ot.print_table()


if __name__ == '__main__':
    main()


