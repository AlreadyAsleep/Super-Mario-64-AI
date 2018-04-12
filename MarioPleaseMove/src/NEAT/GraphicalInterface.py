# File: GraphicalInterace.py
# Package: NEAT for Python3
# Author: Ben Heil
# Since: 3/8/18


# uses the graphics library found http://mcsp.wartburg.edu/zelle/python/graphics.py
import graphics as gr
from . import Node
from . import NodeController as nc
from . import InputNode as inode
from . import HiddenNode as hnode
from . import OutputNode as onode
from . import Connection as con
import numpy as np

def create_window(title, sizex, sizey):
	'''returns a window of dimension
	(sizex, sizey) with title as title'''
	win = gr.GraphWin(title, width=sizex, height=sizey)
	return win

def _hold_window(win):
	''' Keeps the window from
	closing until the space bar
	is pressed (kind of a hack)'''
	while True:
		key = ""
		try:
			key = win.getKey()
		except:
			exit()
		if key == "space" :
			win.close()



def _add_object(win, obj):
	'''Adds a drawable object to the
	window'''
	if not(isinstance(obj, gr.GraphicsObject)):
		raise IncompatibleType(INCOMPATIBLE_TYPE_DRAW)
	obj.draw(win)
	try: #if object has a Text element draw it too
		obj.Text.draw(win)
	except AttributeError:
		pass




class IncompatibleType(Exception):
	'''Exveption raised when an incompatible object is passed to draw'''
	pass

INCOMPATIBLE_TYPE_NODE = "Object cannot be drawn as WinNode"
INCOMPATIBLE_TYPE_DRAW = "This object cannot be added to a window"
INCOMPATIBLE_TYPE_CON = "These objects are not a WinNode instance"
#=============================================================================================================
# Wrapper classes to display nodes
#=============================================================================================================


class WinNode(gr.Circle):
	'''This class represents
	a node in our topology as 
	a circle with a title and state
	value'''

	#see Node.py for better detail of node class
	title = ""
	tag = ""
	state = 0
	center = None
	Text = None

	#take a node object, a tuple, and an integer
	def __init__(self, node, center, radius):
		self.center = p = gr.Point(center[0], center[1])
		super(WinNode, self).__init__(p, radius)	
		if not (isinstance(node, Node.Node)):
			raise IncompatibleType(INCOMPATIBLE_TYPE_NODE)
		else:
			self.title = node.title
			self.tag = node.tag
			self.state = node.state
			self.Text = gr.Text(self.center, self.title + "\n" + str(self.state))

class WinCon(gr.Line):
	'''This class represents
	a connection in the topology
	as a line from node to node'''

	#see Connection.py for better detail
	inode = None # of type WinNode
	onode = None # see above

	def __init__(self, inode, onode):
		if not (isinstance(inode, WinNode) and isinstance(onode, WinNode)):
			raise IncompatibleType(INCOMPATIBLE_TYPE_CON)
		p1 = gr.Point(inode.center.x, inode.center.y)
		p2 = gr.Point(onode.center.x, onode.center.y)
		super(WinCon, self).__init__(p1, p2)


if __name__ == '__main__':
	n = inode.InputNode("Test")
	n2 = onode.OutputNode("Test2")
	node = WinNode(n, (50,50), 25)
	node2 = WinNode(n2, (150, 150), 25)
	con = WinCon(node, node2)
	win = create_window("Test", 1000, 500)
	_add_object(win, node)
	_add_object(win, node2)
	_add_object(win, con)
	_hold_window(win)
