# File: Mario_NEAT.py
# Since: 4/10/18
# Author: Ben Heil and Justin Butler
# This module performs neural net training and output on Mario 64 speed-run data


from src import NEAT, load_input_file, convert_output, save_net
import numpy as np


DATA_SIZE = 290274  # total number of input frames
TRAINING_SIZE = int(DATA_SIZE * .7)
TESTING_SIZE = int(DATA_SIZE * .3)
BEGIN_FRAME = 3657  # this is where real game-play actually starts


OUTPUT_DIR = "./out/"
RAW_OUTPUT = OUTPUT_DIR + "raw.txt"
FORMATTED_OUTPUT = OUTPUT_DIR + "format.txt"
NET_DATA = OUTPUT_DIR + "NETS/"
SAVED_NETS = "save/{0}.net"



def make_net(input_size, output_size):
    """initialize a neural net to
    work with"""
    nc = NEAT.NodeController.NodeController()
    for i in range(input_size):
        node = NEAT.InputNode.InputNode("input_node_" + str(i))
        nc.add_node(node)
    for i in range(output_size):
        node = NEAT.OutputNode.OutputNode("output_node_" + str(i))
        nc.add_node(node)
    return nc


def add_hiddens(net, size):
    """fills a net with hidden nodes"""
    for i in range(size):
        node = NEAT.HiddenNode.HiddenNode("hidden_node_" + str(i), net)
        net.add_node(node)

def set_inputs(nc, input):
    """sets the input node values
    based off the FrameInput object input

    first 18 are button string
    next 8 are x axis pitch
    final 8 are y axis pitch
    all in binary"""
    pos = 0
    binary = input.get_binary()
    for i in range(18):
        nc.get_node(nc.inputs[pos]).change_state(int(binary[i]))
        pos += 1
    x = input.get_xy()[0]
    for i in range(8):
        try:
            nc.get_node(nc.inputs[pos]).change_state(int(x[i]))
        except:
            print(input, input.get_xy())
            exit(1)
        pos += 1
    y = input.get_xy()[1]
    for i in range(8):
        try:
            nc.get_node(nc.inputs[pos]).change_state(int(y[i]))
        except:
            print(input, input.get_xy())
            exit(1)
        pos += 1


def set_outputs(nc):
    """processes all the inputs
    and sets the output nodes
    structure is exactly the same
    as input"""
    for i in range(len(nc.hiddens)):
        nc.get_node(nc.hiddens[i]).process()


def create_topology(nc, num):
    """fills the network with num hidden
    nodes"""
    rolls = ['Input', 'Output']
    for i in range(num):
        NEAT.GeneticOperation.add_hidden(nc, rolls[np.random.randint(0, 2)])


def get_output_string(nc):
    """returns an string representation of the
    output nodes of the form
    [0-17][18-25][26-33]"""
    first = ""
    for i in range(18):
        first += str(nc.get_node("output_node_" + str(i)).state)
    second = ""
    for i in range(18, 26):
        second += str(nc.get_node("output_node_" + str(i)).state)
    third = ""
    for i in range(26, 34):
        third += str(nc.get_node("output_node_" + str(i)).state)
    return "[{0}][{1}][{2}]".format(first, second, third)


def string_diff(a, b):
    """returns the number of positionally
    different characters in a and b"""
    count = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            count += 1
    return count


def accuracy(a, b):
    """returns string_diff as a number between
    0 and 1 (can be zero or one)"""
    return 1 - string_diff(a, b) / len(a)


def get_actual_outputs(frames):
    """returns a list of strings
    containing the actual data from the file
    referenced in load_input_file.py"""
    outputs = []
    for frame in frames:
        string = "[{0}][{1}][{2}]".format(frame.get_binary(), frame.get_xy()[0], frame.get_xy()[1])
        outputs.append(string)
    return outputs


def get_predicted_outputs(nc, frames):
    """returns a list of strings
    containing the neural networks
    estimate as to the next input"""
    outputs = []
    for frame in frames:
        set_inputs(nc, frame)
        set_outputs(nc)
        out = get_output_string(nc)
        outputs.append(out)
    return outputs

def fitness(nc, frames):
    """returns the average fitness
    of a net over a span of frames"""
    length = len(frames)
    reals = get_actual_outputs(frames)
    preds = get_predicted_outputs(nc, frames)
    sum = 0.0
    for i in range(length - 1):
        sum += accuracy(reals[i+1], preds[i])  # how well it predicts the next input based off last
    return sum / length


def get_net_str(net):
    """returns a string rep of the
    hidden nodes in a net"""
    string = ""
    for node in net.hiddens:
        string += str(net.get_node(node))
    return string


def train(pop_size, frames, starting=25, ending=200, delta=25):
    """Trains a group on nets on a
    range of frames and returns the most fit net
    at the end of the trainng.
    Configuration of nets will be
    logged in NET_DATA

    starting is how many hidden nodes the net starts
    with, ending is how many it finishes with
    and delta is how many to increase by at each
    epoch"""
    # Initialize environment
    nets = []
    count = starting
    nTypes = ['Input', 'Output']
    for i in range(pop_size):
        net = make_net(34, 34)
        create_topology(net, starting)
        nets.append((net, fitness(net, frames)))  # measure initial fitness
    nets.sort(key=lambda x: x[1], reverse=True)  # sorts high to low

    # loop for genetic operation, stop when #ending hidden nodes in each net
    while count <= ending:
        count += delta

        # log net data in files
        for i in range(pop_size):
            with open(NET_DATA  + str(i + 1) + "_net.txt", 'w') as file:  # ex. NET_DATA_7 for 7th member of nets
                file.write("Net " + str(i + 1) + " with count " + str(len(nets[i][0].hiddens)) + ":\n")
                file.write(get_net_str(nets[i][0]))

        keep_num = pop_size // 2
        for i in range(keep_num):  # create new population, only keep top half of last pop
            child = nets[i][0].copy()
            for i in range(delta):  # add delta many nodes
                NEAT.GeneticOperation.add_hidden(child, ntype=nTypes[np.random.randint(0,2)])
            nets[i] = (child, fitness(child, frames))
        # fill in the rest of the population size
        for i in range(keep_num, pop_size):
            child = make_net(34, 34)
            create_topology(child, count)
            nets[i] = (child, fitness(child, frames))

        nets.sort(key=lambda x : x[1], reverse=True)
    return nets[0]


def perform(net, frame_count, seed_frames, threshold):
    """Takes a trained net as input
    and generates frame_count many FrameInputs
    and writes them to the output file

    seed_frames are a set of frames with which to
    seed the network, so it has some initial
    input noise. If the net hangs on the same input
    for too long it will reseed itself"""
    sLength = len(seed_frames)
    set_inputs(net, seed_frames[np.random.randint(sLength)])
    outs = []
    repeat_counter = 0
    for i in range(frame_count):
        set_outputs(net)
        outs.append(get_output_string(net))
        last_frame = convert_output.convert_outstring(outs[i])
        if i > 0 and outs[i] == outs[i - 1]:
            repeat_counter += 1
        else:
            repeat_counter = 0
        if repeat_counter > threshold:
            repeat_counter = 0
            set_inputs(net, seed_frames[np.random.randint(sLength)])
        else:
            set_inputs(net, last_frame)
        if i % threshold == 0:
            set_inputs(net, seed_frames[np.random.randint(sLength)])
    convert_output.write_to_file(RAW_OUTPUT, outs)
    convert_output.convert(RAW_OUTPUT, FORMATTED_OUTPUT)






def print_net(nc):
    NEAT.GeneticOperation.print_current(nc)


if __name__ == '__main__':
    frames = load_input_file.read_range(50000, start=BEGIN_FRAME)
    # best = train(30, frames)  # tuple with fitness as it's second value
    # save_net.save(SAVED_NETS.format("50k_iter"), best[0])
    # print("Fitness: ", best[1], frames[0])
    # perform(best[0], 10000, frames, 60)
    net = make_net(34, 34)
    add_hiddens(net, 68)
    save_net.load("save/50k_iter.net", net)
    # print_net(net)
    perform(net, 50000, frames, 60)


    # set_inputs(net, frames[0])
    # set_outputs(net)
    # #print(convert_output.convert_outstring(get_output_string(net)))
    # #print_net(net)
    # #print(fitness(net, frames))
    # convert_output.convert(RAW_OUTPUT, FORMATTED_OUTPUT)

