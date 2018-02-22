from graphviz import Digraph
import os
if os.name == 'nt':
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'


class MachinePrinter(object):

    def __init__(self):
        pass

    def print_machine(self, name,MealyMachine=None):
        machine = MealyMachine
        f = Digraph('finite_state_machine', filename=name)
        f.attr(rankdir='LR', size='8,5')

        f.attr('node', shape='doublecircle')
        for states in machine.states:
            if states.is_start:
                f.node(str(states.id))

        f.attr('node', shape='circle')
        start_node = None
        for states in machine.states:
            for transitions in states.Transitions:
                name = str(transitions.symbol) +  ":" +  str(transitions.output)
                start = str(transitions.state_1.id)
                end = str(transitions.state_2.id)
                f.edge(start, end, label=name)

        f.view()



