import pickle

def save_machine(machine, name):
        pickle_out = open(name, "w")
        pickle.dump(machine,pickle_out)
        pickle_out.close()

def load_machine(name):
        pickle_in = open(name, "r")
        machine = pickle.load(pickle_in)
        pickle_in.close()
        return machine