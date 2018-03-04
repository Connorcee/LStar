from StateMachineComponents import *
import MachinePrinter
import random
from src.LStar import ObservationTable


def main(args=None):
    logging = False
    # Create the machine
    states = 9
    symbols = [0, 1]
    outputs = [0, 1]
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

    print "EQUIVALENT" + str(Mealy.equivalent_states())

    run_l_star(ot, Mealy)
    new_machine = ot.build_machine()
    new_machine.print_machine_transitions()
    counterexample = random_machine_tests(Mealy,new_machine,symbols)
    print "COUNTER EXAMPLE " + str(counterexample)
    while counterexample is not None:
        ot.add_state(counterexample)
        ot.state_experiment_output(Mealy)
        run_l_star(ot, Mealy)
        new_machine = ot.build_machine()
        new_machine.print_machine_transitions()
        counterexample = random_machine_tests(Mealy,new_machine,symbols)
        print "COUNTER EXAMPLE " + str(counterexample)

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

def random_machine_tests(Mealy1, Mealy2, symbols):
    print "RANDOMLY TESTING"
    counter = 20
    temp = 0
    while temp < counter:
        temp += 1
        x = random_test(20,symbols)
        print x
        if not Mealy1.word_output(x) == Mealy2.word_output(x):
            return x

def random_test(length, symbols):
    test = []
    for x in range(length):
        random_c = random.choice(symbols)
        test.append(random_c)
    return test


if __name__ == '__main__':
    main()


