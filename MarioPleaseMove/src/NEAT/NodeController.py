# File: NodeController.py
# Package: NEAT for Python3
# Author: Ben Heil
# Since: 2/18/18

class NodeController:
	'''This class manages the
	current nodes in our topology'''

	nodes = {}			#A reference to every node in the topology via dictionary
	inputs = []
	outputs = []
	hiddens = []
	count = 0			#The total number of nodes

	def __init__(self):
		self.nodes = {}
		self.inputs = []
		self.outputs = []
		self.hiddens = []
		self.count = 0

	def __str__(self):
		return "\nInputs: " + str(len(self.inputs)) + "\nOutputs: " + str(len(self.inputs))

	def get_node(self, title):
		'''returns a node by its title'''
		return self.nodes[title]

	def get_count(self):
		self.count = len(self.nodes)
		return self.count

	def add_node(self, node):
		self.nodes[node.title] = node
		if node.tag == "Input":
			self.inputs.append(node.title)
		elif node.tag == "Hidden":
			self.hiddens.append(node.title)
		elif node.tag == "Output":
			self.outputs.append(node.title)

	def remove_node(self, title):
		self.nodes.pop(title)


	def process_inputs(self, func, **param):
		for i in range(len(self.inputs)):
			self.get_node(self.inputs[i]).get_input(func, self, **param)


	def copy(self):
		temp = NodeController()
		temp.nodes = self.nodes.copy()
		temp.inputs = self.inputs.copy()
		temp.outputs = self.outputs.copy()
		temp.hiddens = self.hiddens.copy()
		temp.count = self.count
		return temp