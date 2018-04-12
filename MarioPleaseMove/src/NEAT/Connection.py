# File: Connection.py
# Package: NEAT for Python3
# Author: Ben Heil
# Since: 2/18/18


class Connection:
	'''this class defines the connections
	made between nodes in the topology'''

	input_node = ""			#the titles of our input node
	output_node = ""		#the titles of our output node

	
	def __init__(self, inode, onode, controller):
		self.input_node = inode.title
		self.output_node = onode.title
		self.controller = controller
		inode.add_connection(self)
		onode.add_connection(self)

	def __str__(self):
		return self.input_node + "->" + self.output_node




