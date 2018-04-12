# File: load_input_file.py
# Author: Ben Heil
# Since: 4/9/18
# this module loads an the text from a bk2 input file and parses it into a usable format


from bitstring import BitArray as ba


IN_FILE = "Input Log.txt"


class FrameInput:
    '''A wrapper to hold all the
    input values for one frame

    LogKey:#Reset|Power|#
    P1 X Axis|P1 Y Axis|P1 A Up|P1 A Down|P1 A Left|P1 A Right
    |P1 DPad U|P1 DPad D|P1 DPad L|P1 DPad R|P1 Start
    |P1 Z|P1 B|P1 A|P1 C Up|P1 C Down|P1 C Right|P1 C Left|P1 L|P1 R|
    '''

    XAxis = 0
    YAxis = 0

    string = ".................."
    binary = 0b000000000000000000
    mask = "UDLRUDLRSZBAudrllr"


    def __init__(self, string=None, binary=None, x=None, y=None):
        """loads a string of the form
        |..|    0,    0,..................|
        into a FrameInput"""
        if string is not None:
            self.XAxis = int(string[4:9])
            self.YAxis = int(string[10:15])
            self.string = string[16:34]
            self.generate_binary()
        """generates a FrameInput
        from a binary value"""
        if binary is not None:
            self.binary = bin(binary)
            self.generate_string()
            self.get_axes(x, y)

    def __str__(self):
        return '|..|' + str(self.XAxis).rjust(5) + ',' + str(self.YAxis).rjust(5) + \
                    ',{0}|'.format(self.string)

    def generate_binary(self):
        """Generates a binary representation
        of the input string"""
        length = len(self.string)
        for i in range(length):
            if self.string[i] == self.mask[i]:
                self.binary += pow(2, (length - i) - 1)
        self.binary = bin(self.binary)

    def generate_string(self):
        """generates a string representation
        from the binary"""
        binary = self.binary[2:]
        binary.zfill(18)# ignore the 0b
        length = len(binary)
        mString = list(self.string) # mutable string
        for i in range(length):
            if bool(int(binary[i])):
                 mString[i] = self.mask[i]
        self.string = "".join(mString)

    def get_axes(self, x, y):
        """generates the axes as
        from a binary value"""
        self.XAxis = ba(bin=x).int
        self.YAxis = ba(bin=y).int


    def get_binary(self):
        """returns a string representation
        of self.binary"""
        return self.binary[2:].zfill(18)

    def get_xy(self):
        """returns a string representation
        of XAxis and YAxis in binary"""
        if self.XAxis > -1:
            x = bin(self.XAxis)
        else:
            x = bin(self.XAxis % 255 + 1)  # twos compliment
        x = x[2:].zfill(8)
        if self.YAxis > -1:
            y = bin(self.YAxis)
        else:
            y = bin(self.YAxis % 255 + 1)  # twos compliment
        y = y[2:].zfill(8)
        return (x, y)


def read_range(offset, start=0):
    """reads offset number of frames
    from start, default is from zero"""
    frames = []
    with open(IN_FILE) as file:
        lines = file.readlines()
        for i in range(start+2, start + offset+2):  # +2 to account for header
            frame = FrameInput(lines[i])
            frames.append(frame)
    return frames


if __name__ == '__main__':
    f = FrameInput(string="|..|    0,    0,..................|")
    print(f.binary)
    f2 = FrameInput(string="|..| -128,   16,U...U....Z.A.....r|")
    print(f2.binary)
    f3 = FrameInput(binary=0b101000, x='0b10000000', y='0b01111111')
    print(f3)
    read_range(290724)



