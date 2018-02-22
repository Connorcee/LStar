from graphviz import Digraph


class MachinePrinter(object):

    def __init__(self):
        pass

    def print_machine(self, name,MealyMachine=None):
        machine = MealyMachine
        f = Digraph('finite_state_machine', filename=name)
        f.attr(rankdir='LR', size='8,5')
        f.attr('node', shape='circle')

        for states in machine.states:
            for transitions in states.Transitions:
                name = str(transitions.symbol) +  ":" +  str(transitions.output)
                start = str(transitions.state_1.id)
                end = str(transitions.state_2.id)
                f.edge(start, end, label=name)

        f.view()



