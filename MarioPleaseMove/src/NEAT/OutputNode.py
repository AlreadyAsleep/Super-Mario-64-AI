# File: OutputNode.py
# Package: NEAT for Python3
# Author: Ben Heil
# Since: 2/18/18

from . import Node


class OutputNode(Node.Node):
	'''This class defines an output node
	in the topology'''

	tag = "Output"

	def __init__(self, title):
		super(OutputNode, self).__init__(title)
	