# standard python libraries
import time
import json
import secrets

# my includes
from NLP import *
from node import *
from task import *
from utils import *

# TODO: obviously find a home for this with goals...
# lazy "modes"!
MODE_EXPAND = False

# possible statuses for a command... 
STATUS_QUEUED = 'queued'
STATUS_ACTIVE = 'active'
STATUS_SUCCESS = 'success'
STATUS_FAILED = 'failed'

CURRENT_TASK = 'McCounter'

class Agent:
	
	# for graph-solving problems
	# collection of nodes
	EXPLORED = {}
	
	# all percepts combined into a single worldstate
	WORLDSTATE = {}

	# current "view" of the agents
	percept = False
	
	def __init__(self, params):
		# TODO: auto-expand params
		#self.name = params['name']
		
		# test exec functionality...
		# start by looking around...
		self._exec('l')
		
		# task-specific logic
		if CURRENT_TASK:
			self.task = Task(CURRENT_TASK)
		
		# what does the agent want?
		self.goals = params['goals'] if 'goals' in params else False
		
		# TODO: have agent meander towards goals
		# handle existential crises
		# if not goals:
		# 	colorNote('ERROR: You don\'t know what you want! Try again.')
		# 	colorNote('It\'s okay! We\'ll just explore! :)')
	
	# get all actions
	# without state, returns ALL actions in the environment
	# with a state supplied, it returns ALL actions available at that moment.
	def _actions(self, state=False):
		return
	
	# TODO: move to tasks
	def _expand(self, percept):
		print(percept)
		
		# not room data...
		if 'room' not in percept:
			return False
		
		# get room info
		room = percept['room']
		
		# look for node in graph
		node_id = room['identifier']
		# "I member!"
		if node_id in explored:
			colorNote('EXISTING NODE!!! '+node_id)
			node = self.EXPLORED[node_id]
		else:
		# I need to add this one!
			colorNote('NEW NODE!!! '+node_id)
			parent_id = self.WORLDSTATE['prev_id'] if 'prev_id' in self.WORLDSTATE else False
			room['parent'] = self.EXPLORED[parent_id] if parent_id else False
			room['action'] = percept['action']
			node = Node(room)
		
		# update edges
		parent_id = node.parent_id
		if parent_id and node.action in REVERSE_ACTION:
			# parent to child
			self.EXPLORED[parent_id].edges[node.action] = node.id
			# child to parent
			node.edges[REVERSE_ACTION[node.action]] = parent_id
		
		# came in from a different direction...
		prev_id = self.WORLDSTATE['prev_id'] if 'prev_id' in self.WORLDSTATE else False
		if prev_id and prev_id != parent_id:
			prev_node = self.EXPLORED[prev_id]
			prev_node.edges[percept['action']] = node.id
			node.edges[REVERSE_ACTION[percept['action']]] = prev_id
			# TODO: double check I need this...
			self.EXPLORED[prev_id] = prev_node
		
		self.EXPLORED[node.id] = node
		print('EXPLORED', self.EXPLORED)
		
		# TODO: should I move this logic to a knowledge base?
		if not self._frontier():
			# already expanded; no need to expand any more!
			MODE_EXPAND = False
			
		# finally, set prev node to current node
		self.WORLDSTATE['prev_id'] = node.id

		# what direction now?
		# is the frontier empty?
		frontier = self._frontier()
		
		# nothing left to explore...
		if not frontier:
			return False
		
		# our current room has unexplored exits
		if node.id in frontier:
			# return first unexplored edge...
			for action in node.edges:
				if not node.edges[action]:
					return action
		
		# what about any unexplored nodes up the tree?
		check_node = node
		while check_node:
			if not check_node.expanded():
				for action in check_node.edges:
					if not check_node.edges[action]:
						print('check_node', check_node)
						return action
			# move on to the next node...
			parent_id = check_node.parent_id
			check_node = self.EXPLORED[parent_id] if parent_id else False

		return False
			
	def _frontier(self):
		return [n_id for n_id in self.EXPLORED if not self.EXPLORED[n_id].expanded()]
	
	# add a new command to the global queue; shared with environment...
	# WARNING: this will ACTUALLY SEND a command to the MUD!!!!
	# (make sure you're not calling this infinitely, etc...)
	# (or when you're not supposed to!!!)
	# TODO: handle that ^^^^
	def _exec(self, cmd_txt):
		
		# then go back to the original command...
		cmd_txt = cmd_txt

		# TODO: validate "action" before attempting execution...
		# is this a command we know already?
		action_args = cmd_txt.split(' ')
		action, args = action_args[0], action_args[1:]
		
		print('ACTION:', action)
		# if action not in MEMORY['cmds']:
		# 	# TODO: 
		# 	return False

		# add a timestamped command to the global queue to wait for execution...
		new_cmd = {
			# revert to the unmodified command text (ignores validation...)
			'cmd_txt': cmd_txt,
			'sent': UTC_UNIX_EPOCH(),
			# everything starts out at queued...
			# TODO: validate command before attempting execution...
			'status': STATUS_QUEUED
		}
		
		# get a unique id for this command (to handle timestamp collisions)
		new_cmd['id'] = UNIQUE_ID()
		
		# add to the global action sequence; 
		# TODO: merged with commands from the environment
		print('ACTION TO TAKE:', new_cmd)
		#ACTION_QUEUE.append(new_cmd)

	# update internal state, choose next action
	def next(self, percept):
		print(percept)
		# update internal state
		self.percept = percept
		
		# TODO: should be "task"
		# should we be expanding the map?
		if MODE_EXPAND:
			# expand the internal map
			next_action = self._expand(percept)
			
		if self.task: 
			# ALL tasks need a next function!!!
			self.task.next(percept)