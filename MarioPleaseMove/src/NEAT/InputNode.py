# File: InputNode.py
# Package: NEAT for Python3
# Author: Ben Heil
# Since: 2/16/18


from . import Node


class InputNode(Node.Node):
	'''This class defines an input node
	in the topology'''

	tag = "Input"

	def __init__(self, title):
		super(InputNode, self).__init__(title)



