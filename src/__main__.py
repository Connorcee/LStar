from StateMachineComponents import *
import MachinePrinter
import itertools
import random
from src.LStar import ObservationTable


def main(args=None):
    logging = False
    # Create the machine
    states = 15
    assumed_states = 17
    symbols = [0, 1]
    outputs = [0, 1]
    randomise = True
    alphabet = Alphabet(symbols)

    print 'Generating Machine'
    print '------------------------------------------\n'
    # Create a state machine with the states and symbols and run the initial membership checks
    Mealy = MealyMachine(states, symbols, outputs, randomise)
    if randomise:
        for i in symbols:
            Mealy.random_transition_pass()
        Mealy.build_loopbacks()
        # Make the machine minimal
        Mealy.minimise()

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
    counterexample = random_machine_tests(Mealy,new_machine,symbols)
    while counterexample is not None:
        ot.add_state(counterexample)
        ot.state_experiment_output(Mealy)
        run_l_star(ot, Mealy)
        new_machine = ot.build_machine()
        counterexample = run_w_test(ot, assumed_states - len(new_machine.states), Mealy, new_machine)
        # counterexample = random_machine_tests(Mealy,new_machine,symbols)

    # run_w_test(ot,4,Mealy,new_machine)

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
    counter = 100
    temp = 0
    test_length = 7
    while temp < counter:
        temp += 1
        x = random_test(test_length,symbols)
        if not Mealy1.word_output(x) == Mealy2.word_output(x):
            print "COUNTER EXAMPLE: " + str(x)
            return x

def random_test(length, symbols):
    test = []
    for x in range(length):
        random_c = random.choice(symbols)
        test.append(random_c)
    return test

def run_w_test(ObservationTable, assumed_states, Mealy1, Mealy2):
    W = ObservationTable.distinguishing_elements()
    Cover = ObservationTable.state_cover()
    counterexample = w_test(W, Cover, assumed_states, Mealy1, Mealy2)
    return counterexample

def w_test(W, C, N, Mealy1, Mealy2):
    if C.__contains__([]):
        C.remove([])
    set_const = [W,C]
    print "SET CONST: " + str(set_const)
    print "W " + str(set_const[0])
    print "C " + str(set_const[1])
    for y in range(N):
        set_const.append(C)
        for p in set_const:
            print "SC: " + str(p)
        for element in itertools.product(*set_const):
            x = list(itertools.chain.from_iterable(element))
            if not Mealy1.word_output(x) == Mealy2.word_output(x):
                print "COUNTER EXAMPLE" + str(x)
                return x

    print "NO COUNTEREXAMPLE FOUND"
    return None

if __name__ == '__main__':
    main()


