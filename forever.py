# python packages
from sh import tail
import json
import re

# my includes
from agent import Agent
from environment import Environment


# queue of commands waiting for captures
CMD_QUEUE = []
CMD_HISTORY = []

# output directly from the MUD client
LOG_FILE = '/home/zaya/Apps/MUSHclient/x/sync.in'

# messages from python bot to client
MSG_FILE = 'data/messages.json'

# AGENT = Agent({
# 		# ... agent params go here ...
# 		# missions:
# 	})

if __name__ == "__main__":
	
	# create a new game from Environment config
	game = Environment({
		'agent': {
			# ... agent params go here ...
		},
		# TODO: world-specific details 
		'world': {
			# ... world params go here ...
			# REQUIRED: Regex Captures
			'captures': ['todo']
		},
		# all missions the agent can choose from
		'missions': [],
	})
	
	# let's go!!
	game.start()

