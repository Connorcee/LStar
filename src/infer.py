from StateMachineComponents import *
from copy import deepcopy
import MachinePrinter
import itertools
import random
import uuid
import os
from sys import platform
import time
from LStar import ObservationTable
import argparse



def main():

    parser = argparse.ArgumentParser(description="Generate a Random Mealy Machine and Infer with L*, Default Test is W")
    generate_group = parser.add_mutually_exclusive_group()
    generate_group.add_argument('-gs', '--generateSave', action='store_true',
                                help='Generate and save a machine or multiple machines')
    generate_group.add_argument('-gi', '--generateInfer', action='store_true',
                                help='Generate and infer a single machine for a defined number of states')
    generate_group.add_argument('-li', '--loadInferSingle', action='store_true',
                                help='Load a single machine from a text file for inference')
    generate_group.add_argument('-lmi', '--loadMultipleInfer', action='store_true',
                                help='Load multiple machines from text files for inference')
    args = parser.parse_args()

    try:
        if args.generateSave:
            print "GENERATE AND SAVE A MACHINE"
            while True:
                try:
                    no_states = int(input("Input the number of states for the machine: "))
                    no_inputs = int(input("Input the number of inputs the machine should have: "))
                    no_outputs = int(input("Input number of outputs the machine should have: "))
                except (ValueError, NameError):
                    print "Enter Integers for the States, Inputs and Outputs"
                    continue
                else:
                    if no_states < 1:
                        print "More than 1 state required"
                    elif no_inputs < 2:
                        print "More that 1 input required"
                    elif no_outputs < 2:
                        print "More than 1 output required"
                    else:
                        generate_machine(no_states,no_inputs,no_outputs)
                        break

        elif args.generateInfer:
            print "GENERATE AND INFER A SINGLE MACHINE INPUT THE NECESSARY INFORMATION"
            while True:
                try:
                    no_states = int(input("Input the number of states for the machine: "))
                    no_inputs = int(input("Input the number of inputs the machine should have: "))
                    no_outputs = int(input("Input number of outputs the machine should have: "))
                    assumed = int(input("Assumed Number of states for the test method (This is number above or below that of the SUT): "))
                    test_method = raw_input("Random or W Testing Method: ")
                    test_method = str(test_method).lower()
                except (ValueError, NameError):
                    print "Enter Integers for the States, Inputs and Outputs"
                    continue
                else:
                    if no_states < 1:
                        print "More than 1 state required"
                    elif no_inputs < 2:
                        print "More that 1 input required"
                    elif no_outputs < 2:
                        print "More than 1 output required"
                    elif test_method != "w" and test_method != "random":
                        print "Please enter a valid test method: " + str(test_method)
                    else:
                        iterate(no_states,assumed,True,test_method,no_inputs,no_outputs,False,True)
                        break

        elif args.loadInferSingle:
            print "LOAD INFER SINGLE"
            while True:
                try:
                    machine_name = raw_input("Input the name of the machine with the file extension: ")
                    no_states = int(input("Input the number of states for the machine: "))
                    no_inputs = int(input("Input the number of inputs the machine should have: "))
                    no_outputs = int(input("Input number of outputs the machine should have: "))
                    assumed = int(input("Assumed Number of states for the test method (This is number above or below that of the SUT): "))
                    test_method = raw_input("Random or W Testing Method: ")
                    test_method = str(test_method).lower()
                except (ValueError, NameError):
                    print "Enter Integers for the States, Inputs and Outputs"
                    continue
                except AttributeError:
                    print "LOADED MACHINE DOES NOT MATCH SPECIFIED PARAMETERS"
                    continue
                else:
                    if no_states < 1:
                        print "More than 1 state required"
                    elif no_inputs < 2:
                        print "More that 1 input required"
                    elif no_outputs < 2:
                        print "More than 1 output required"
                    elif test_method != "w" and test_method != "random":
                        print "Please enter a valid test method: " + str(test_method)
                    else:
                        try:
                            iterate(no_states,assumed,False,test_method,no_inputs,no_outputs,machine_name,True)
                        except IOError:
                            print "MACHINE {} NOT FOUND CHECK FOLDER STRUCTURE AND NAME".format(machine_name)
                            continue
                        break

        elif args.loadMultipleInfer:
            print "LOAD MULTIPLE INFER"
            while True:
                try:
                    state_start = int(input("Input smallest number of states in a machine to be tested: "))
                    state_end = int(input("Input largest number of states in a machine to be tested: "))
                    no_inputs = int(input("Input the number of inputs the machine should have: "))
                    no_outputs = int(input("Input number of outputs the machine should have: "))
                    assumed = int(input("Assumed Number of states for the test method (This is number above or below that of the SUT): "))
                    test_method = raw_input("Random or W Testing Method: ")
                    test_method = str(test_method).lower()
                except (ValueError, NameError):
                    print "Enter Integers for the States, Inputs and Outputs"
                    continue
                except AttributeError:
                    print "LOADED MACHINE DOES NOT MATCH SPECIFIED PARAMETERS"
                    continue
                else:
                    if no_inputs < 2:
                        print "More that 1 input required"
                    elif no_outputs < 2:
                        print "More than 1 output required"
                    elif test_method != "w" and test_method != "random":
                        print "Please enter a valid test method: " + str(test_method)
                    else:
                        for x in range(state_start,state_end+1):
                            states = x
                            try:
                                folder = machines_from_folder(states)
                            except:
                                print "FOLDER ERROR, CHECK BOUNDS"
                                break
                            for machines in folder:
                                try:
                                    iterate(states,assumed,False,test_method,no_inputs,no_outputs,machines,False)
                                except IOError:
                                    print "MACHINE OR FOLDER NOT FOUND CHECK FOLDER STRUCTURE AND NAME"
                                except:
                                    print "INCORRECT NUMBER OF OUTPUTS OR INPUTS DEFINED"
                                    break
                        break
        else:
            print "NO VALID OPTION PROVIDED QUITTING"
            exit()
    except AttributeError:
        print "NO VALID OPTION PROVIDED QUITTING"
        exit()

# Generate a machine and save it into the according folder for the path
def generate_machine(nostates, nosymbols, nooutputs):
    states = nostates
    symbols = range(0,nosymbols)
    outputs = range(0,nooutputs)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print "Saving Machine to: "  + str(dir_path)
    if platform != "win32":
        path = "{}/State/{}/machine-{}.txt".format(dir_path,nostates,uuid.uuid4())
    else:
        path = "{}\\State-{}-machine-{}.txt".format(dir_path, nostates, uuid.uuid4())
    Mealy = MealyMachine(states, symbols, outputs, path, True)
    for i in symbols:
        Mealy.random_transition_pass()
    Mealy.build_loopbacks()
    Mealy.save_machine(path)

def machines_from_folder(no_states):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print "Loading: " + str(dir_path)
    if platform != "win32":
        path = dir_path + "/State/{}".format(no_states)
    else:
        path = dir_path + "\\State\\{}".format(no_states)
        print path
    dirls = os.listdir(path)
    return dirls


def iterate(no_states, assumed, randomise, mode, no_inputs=2, no_outputs=2, path=False, print_machine=False):
    logging = False
    # Create the machine
    states = no_states
    assumed_states = no_states + assumed
    symbols = range(0,no_inputs)
    outputs = range(0,no_outputs)
    randomise = randomise
    alphabet = Alphabet(symbols)

    print '------------------------------------------\n'
    print 'Generating Machine'
    # Create a state machine with the states and symbols and run the initial membership checks
    mealy_machine = MealyMachine(states, symbols, outputs, path, randomise)
    if randomise:
        for i in symbols:
            mealy_machine.random_transition_pass()
        mealy_machine.build_loopbacks()
    mealy_machine = mealy_machine.minimise(mealy_machine, True)
    if len(mealy_machine.states) != no_states:
        print "MACHINE NOT MINIMAL, RETURNING"
        return None

    print 'Generation Complete'
    print 'Initializing Observation Table'
    ot = ObservationTable(alphabet,mealy_machine,logging)
    print 'Observation Table Initialized to Mealy'

    # Inital run of L Start
    start = time.time()
    run_l_star(ot, mealy_machine)
    new_machine = ot.build_machine()
    equivalent = machines_equivalent(mealy_machine, new_machine)
    if mode == 'random':
        counterexample = random_machine_tests(mealy_machine, new_machine, assumed_states, symbols, ot)
    elif mode == 'w':
        counterexample = run_w_test(ot, assumed_states, mealy_machine, new_machine)
    else:
        print "NO TEST MODE SELECTED"
        exit()

    # While there is a counterexample, keep adding it to the observation table and run l star again
    EQ_counter = 0
    if counterexample is not None and not equivalent:
        EQ_counter += 1
    while counterexample is not None and not equivalent:
        ot.add_state(counterexample)
        ot.state_experiment_output(mealy_machine)
        run_l_star(ot, mealy_machine)
        new_machine = ot.build_machine()
        print "SUT States: " + str(len(mealy_machine.states))
        print "Conjecture States: " + str(len(new_machine.states))
        equivalent = machines_equivalent(mealy_machine,new_machine)
        if equivalent:
            break
        EQ_counter += 1
        if mode == 'random':
            counterexample = random_machine_tests(mealy_machine, new_machine,assumed_states, symbols, ot)
        elif mode == 'w':
            counterexample = run_w_test(ot, assumed_states, mealy_machine, new_machine)

    # No counterexample has been produced, clean up
    print "Equivalence Queries: " + str(EQ_counter)
    print "Membership Query Counter: " + str(ot.mq_counter)
    print "Inferred: " + str(machines_equivalent(mealy_machine,new_machine))
    end = time.time()

    if print_machine:
        printer = MachinePrinter.MachinePrinter()
        printer.print_machine("ZSUT " + str(uuid.uuid4()),mealy_machine)
        printer.print_machine("ZInferred " + str(uuid.uuid4()),new_machine)
    # open a file with the modes
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = dir_path + "/State/QueryData"
    m = open('{}/{}-{}-assumed{}-data.txt'.format(dir_path,mode,states,assumed), "a+")
    m.write(str(states) + ',' + str(ot.mq_counter) + ',' + str(machines_equivalent(mealy_machine,new_machine)) + ',' +
            str(EQ_counter) + ',' +
            str(end - start) + '\n')
    m.close()
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


def random_machine_tests(Mealy1, Mealy2, assumed, symbols, ObservationTable):
    print "RANDOMLY TESTING"
    x = len(ObservationTable.distinguishing_elements())
    y = len(ObservationTable.state_cover())
    bound = len(Mealy1.states) - len(Mealy2.states) + assumed
    if bound <= 0:
        bound = 1
    counter = x * y * bound
    print "TEST SIZE: " + str(counter)
    temp = 0
    test_length = assumed
    print "ASSUMED:" + str(assumed)
    print "TEST LENGTH: " + str(test_length)
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
    set_const = [C,W]
    N = N - len(Mealy2.states)
    print "W: " + str(W)
    print "C: " + str(C)
    print "N: " + str(N)
    print "WC: " + str(set_const)
    print "CONJECTURED STATES: " + str(len(Mealy2.states))
    if N <= 0:
        N = 0
        for element in itertools.product(*set_const):
            x = list(itertools.chain.from_iterable(element))
            if not Mealy1.word_output(x) == Mealy2.word_output(x):
                print "COUNTER EXAMPLE: " + str(x)
                return x
    set_const.append(W)
    print "N LATER: " + str(Mealy2.states)
    for y in range(N):
        print "TESTING APPEND: " + str(y)
        for element in itertools.product(*set_const):
            x = list(itertools.chain.from_iterable(element))
            if not Mealy1.word_output(x) == Mealy2.word_output(x):
                print "COUNTER EXAMPLE: " + str(x)
                return x
        set_const.append(W)
    return None

def machines_equivalent(Mealy1, Mealy2, return_machine=False):
    # Inital checks to see if they are equivalent
    counter_1 = 0
    counter_2 = 0

    # Equal number of states and transitions
    for s0 in Mealy1.states:
        for t0 in s0.Transitions:
            counter_1 += 1
    for s1 in Mealy2.states:
        for t1 in s1.Transitions:
            counter_2 += 1
    if len(Mealy1.states) != len(Mealy2.states):
        print "Unequal number of states"
        return False

    elif counter_1 != counter_2:
        print "unequal number of transitions"
        return False

    # Create copy of the machines
    test_mealy = deepcopy(Mealy1)
    test_mealy_2 = deepcopy(Mealy2)

    # Offset to rename the states to allow machines to be combined
    state_offset = len(test_mealy.states)

    # Preserve the start ID's to connect the temp state
    machine_1_start = [x for x in test_mealy.states if x.is_start][0]
    machine_2_start = [x for x in test_mealy_2.states if x.is_start][0]

    # Offset one of the machines IDs
    for state in test_mealy.states:
        state.id += state_offset

    # Add all the states to the second machine
    for state in test_mealy.states:
        test_mealy_2.states.append(state)

    # Create a new initial state
    tempstate = State(len(test_mealy_2.states),False,True)

    # All necessary transitions
    tempstate.add_transition(machine_1_start,Mealy1.alphabet.symbols[0],Mealy1.outputs.outputs[0],False)
    tempstate.add_transition(machine_2_start, Mealy1.alphabet.symbols[1], Mealy1.outputs.outputs[1], False)
    if len(Mealy1.alphabet.symbols) > 2:
        for ele in Mealy1.alphabet.symbols[2:]:
            tempstate.add_transition(tempstate,ele,choice(Mealy1.outputs.outputs),True)

    # Make the old start states normal states
    machine_1_start.is_start = False
    machine_2_start.is_start = False

    # Add in the new state and rebuild the dictionary
    test_mealy_2.states.append(tempstate)
    test_mealy_2.statesDict = test_mealy_2.build_state_dictionary()

    # Minimise this machine
    test_mealy_2 = MealyMachine.minimise(test_mealy_2, True)
    print "NUMBER OF STATES IN TEST: " + str(len(test_mealy_2.states))

    target_states = len(Mealy1.states) + len(Mealy2.states) + 1
    uneven_states = len(Mealy1.states) + 1

    if target_states != len(test_mealy_2.states):
        print "EQUIVALENT MACHINES"
        return True
    elif uneven_states == len(test_mealy_2.states) and not return_machine:
        print "UNEVEN COMBINATION, EQUIVALENT STATES FOUND"
        return False
    elif uneven_states == len(test_mealy_2.states) and return_machine:
        print "UNEVEN COMBINATION, EQUIVALENT STATES FOUND"
        return test_mealy_2
    elif return_machine:
        print "NOT EQUIVALENT MACHINES"
        return test_mealy_2
    else:
        print "NOT EQUIVALENT MACHINES"
        return False

if __name__ == '__main__':
    main()


