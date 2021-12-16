from utils import *

class Node:

	def __init__(self, state):
		parent_node = state['parent']
		
		self.id = state['identifier']
		self.action = state['action']
		self.edges = {}
		
		if parent_node:
			self.path_cost = parent_node.path_cost + 1
			self.parent_id = parent_node.id
		else:
			self.path_cost = 1
			self.parent_id = False
		
		# init all edges as unexplored
		available_actions = state['exits']
		for a in available_actions:
			if a in direction_alias:
				self.edges[direction_alias[a]] = False
		
		# edge back to parent...
		if self.parent_id and self.action in ALIAS_DIRECTION:
			self.edges[REVERSE_ACTION[self.action]] = self.parent_id
		
		# get x-y coords
		offset = {
			#'l': [  0,   0],
			'n': [  0,  -1],
			's': [  0,   1],
			'e': [  1,   0],
			'w': [ -1,   0],
		}
		
		# start at origin
		if not parent_node or self.action not in offset:
			self.x = 0
			self.y = 0
		else:
			offset_x, offset_y = offset[self.action]
			self.x = parent_node.x + offset_x
			self.y = parent_node.y + offset_y

	# def expand(self, node):
	# 	self.edges[node.action] = node.id
		
	def expanded(self):
		# look for any False (unexplored) actions
		return not [a for a in self.edges if not self.edges[a]]

	# get all available actions (directional only)
	def actions(self):
		return self.edges
		