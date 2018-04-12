# File: convert_output.py
# Author: Ben Heil
# Since: 4/10/18
# This module takes the neural net output and converts in into a format to be written to a FrameInput object


from src import load_input_file
from bitstring import BitArray as ba

BEGIN_FRAME = 3657  # this is where real game-play actually starts


HEADER = "[Input]\n" + \
    "LogKey:#Reset|Power|#P1 X Axis|P1 Y Axis|P1 A Up|P1 A Down" + \
    "|P1 A Left|P1 A Right|P1 DPad U|P1 DPad D|P1 DPad L|P1 DPad R|P1 Start" + \
    "|P1 Z|P1 B|P1 A|P1 C Up|P1 C Down|P1 C Right|P1 C Left|P1 L|P1 R|\n"
FOOTER = "[\Input]"


def write_to_file(file, strings):
    """just writes a string list to
    a file delimited by newlines"""
    with open(file, "w") as f:
        for string in strings:
            f.write(string + '\n')


def convert_outstring(string):
    """converts an outstring to a
    FrameInput object"""
    strings = string.split("][")
    binary = strings[0][1:]
    binary = int(binary, 2)
    x = strings[1]
    y = strings[2][:len(strings[2]) - 2]
    try:
        frame = load_input_file.FrameInput(binary=binary, x="0b" + x, y="0b" + y)
    except:
        print(string, binary, x, y)
        exit(1)
    return frame


def convert(file, out_file):
    """converts file to a format
    that can be used as FrameInput"""
    outs = []
    with open(file, "r") as f:
        for line in f.readlines():
            outs.append(convert_outstring(line))
    with open(out_file, "w") as f:
        lines = load_preset("Input Log.txt", BEGIN_FRAME)
        for line in lines:
            f.write(str(line))
        for out in outs:
            f.write(str(out) + '\n')
        f.write(FOOTER)

def load_preset(file, frame_count):
    """Loads the first frame_count frames
    from a preset so the net doesn't train against menu
    navigation"""
    with open(file, "r") as f:
        lines = f.readlines()
    return lines[:frame_count]


