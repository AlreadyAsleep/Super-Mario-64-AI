# File: Node.py
# Package: NEAT for Python3
# Author: Ben Heil
# Since: 2/16/18

class Node:
	"""This class defines the basic structure
	of a NEAT node"""

	title = None				#The name of our node and its unique identifier in the topology
	state = 0					#The state it is in (-1,0,1)
	connections = []			#Refernce to all the connections the node has

	def __init__(self, title):
		self.title = title
		self.state = 0
		self.connections = []

	def __str__(self):
		return "\nTitle: " + self.title + "\nType: " + self.tag + \
		 	"\nState: " + str(self.state) + \
			"\nConnections: " + str([str(c) for c in self.connections])

	def get_title(self):
		'''Returns the name of the node'''
		return self.title

	def add_connection(self, c):
		'''adds a new connection to our node'''
		self.connections.append(c)

	def connection_count(self):
		'''returns the number of connections to our node'''
		return len(self.connections)

	def change_state(self, i):
		'''changes the state of our node (-1,0,1)'''
		self.state = i

		