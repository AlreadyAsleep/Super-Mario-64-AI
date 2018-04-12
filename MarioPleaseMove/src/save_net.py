# File: save_net.py
# Author: Ben Heil
# Since: 4/10/18
# This module saves a neural net configuration to be used later


from src import NEAT


def deconstruct_net(net):
    """Disassembles net into list of connections
    which can be written to file"""
    connections = []  # tuples with (inputTitle, outputTitle)
    for node in net.hiddens:
        n = net.get_node(node)
        for c in n.connections:
            con = (c.input_node, c.output_node)
            connections.append(con)
    return connections

def save(file, net):
    """Writes a net configuration to file"""
    size = len(net.hiddens)  # first item in file
    cons = deconstruct_net(net)
    with open(file, "w") as f:
        f.write(str(size) + '\n')
        for c in cons:
            f.write(str(c) + '\n')

def load(file, net):
    """Loads a previous configuration from
    file into net. The node topology must already
    be established (see Mario_NEAT)"""
    with open(file, "r") as f:
        lines = f.readlines()
        size = int(lines[0])
        for i in range(1, len(lines)):
            lines[i] = eval(lines[i])  # evalutes the string as a literal (not a safe op but RIP)
            c = NEAT.Connection.Connection(net.get_node(lines[i][0]),
                                           net.get_node(lines[i][1]), net)
    return net
