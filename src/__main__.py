from StateMachineComponents import *
import MachinePrinter
import itertools
import random
import uuid
from src.LStar import ObservationTable


def main(args=None):
    iterate(5, 1, False)
    '''
    for n in range(5,41):
        
        print "RUNNING FOR {} STATES".format(n)
        iterate(n, 0, False)
        iterate(n, 0, False, "random")
    '''

def iterate(no_states,assumed,randomise,filename=""):
    logging = False
    # Create the machine
    states = no_states
    assumed_states = states + assumed
    symbols = [0, 1, 2]
    outputs = [0, 1, 2]
    randomise = randomise
    alphabet = Alphabet(symbols)
    path = "STATES " + str(states)

    print '------------------------------------------\n'
    print 'Generating Machine'
    # Create a state machine with the states and symbols and run the initial membership checks
    Mealy = MealyMachine(states, symbols, outputs, path, randomise)
    if randomise:
        for i in symbols:
            Mealy.random_transition_pass()
        Mealy.build_loopbacks()
        # Make the machine minimal
        Mealy.minimise()

    # Mealy.save_machine()

    if logging:
        Mealy.print_states()
        Mealy.print_machine_transitions()

    print 'Generation Complete'
    print 'Initializing Observation Table'
    ot = ObservationTable(alphabet,Mealy,logging)
    print 'Observation Table Initialized to Mealy'

    run_l_star(ot, Mealy)
    new_machine = ot.build_machine()
    counterexample = run_w_test(ot, assumed_states - len(new_machine.states), Mealy, new_machine)
    EQ_counter = 0
    while counterexample is not None:
        ot.add_state(counterexample)
        ot.state_experiment_output(Mealy)
        run_l_star(ot, Mealy)
        new_machine = ot.build_machine()
        EQ_counter += 1
        if filename == 'random':
            counterexample = random_machine_tests(Mealy, new_machine,assumed_states, symbols)
        else:
            counterexample = run_w_test(ot, assumed_states - len(new_machine.states), Mealy, new_machine)


    printer = MachinePrinter.MachinePrinter()
    printer.print_machine("ZSUT " + str(uuid.uuid4()),Mealy)
    printer.print_machine("ZInferred " + str(uuid.uuid4()),new_machine)
    print "Equivalence Queries: " + str(EQ_counter)
    print "Membership Query Counter: " + str(ot.mq_counter)
    m = open(filename + "membership.txt", "a")
    e = open(filename + "equivalence.txt", "a")
    m.write(str(states) + ' ' + str(ot.mq_counter) + '\n')
    e.write(str(EQ_counter)+ '\n')
    m.close()
    e.close()
    print '------------------------------------------\n'

def run_l_star(ot,Mealy):
    closed_consistent = False
    while not closed_consistent:
        consistent = ot.is_consistent()
        closed = ot.is_closed()
        if consistent is not None:
            [ot.add_experiment(x) for x in consistent]
            ot.state_experiment_output(Mealy)
            continue
        if closed is not None:
            ot.add_state(closed)
            ot.state_experiment_output(Mealy)
            continue
        closed_consistent = True

def random_machine_tests(Mealy1, Mealy2,assumed, symbols):
    print "RANDOMLY TESTING"
    counter = 10000
    temp = 0
    test_length = assumed
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
    for y in range(N):
        set_const.append(C)
        for p in set_const:
            pass
            # print "SC: " + str(p)
        for element in itertools.product(*set_const):
            x = list(itertools.chain.from_iterable(element))
            if not Mealy1.word_output(x) == Mealy2.word_output(x):
                # print "COUNTER EXAMPLE" + str(x)
                return x

    # print "NO COUNTEREXAMPLE FOUND"
    return None

if __name__ == '__main__':
    main()


