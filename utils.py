from datetime import datetime, timezone
import uuid
import operator
import random
import time

# how long to wait for an action to execute before stopping...
# incremental, if not precisely "seconds"...
MAX_WAIT = 100


WORD_NUM = {
	'a': 1,
	'one': 1,
	'two': 2,
	'three': 3,
	'four': 4,
	'five': 5,
	'six': 6,
	'seven': 7,
	'eight': 8
}

# utils
def colorNote(txt, color=False, bg=False, bold=False):
	color = color if color else random.randint(1, 125)
	bg = bg if bg else random.randint(100, 255)
	color_code = '\033[38;5;%dm' % color
	bg_code = '\033[48;5;%dm' % bg if bg else ''
	print(color_code + bg_code + txt + '\033[0m')

def fold(element, data):
  return reduce(operator.getitem, element.split('_'), data)

def setNestedValue(dict, value, path):
	for level in path[:-1]:
		dict = dict.setdefault(level, {})
	dict[path[-1]] = value
	return dict

def splitTxtList(txt):
		
	txt = txt.replace(' and ', ', ')
	items = txt.split(', ')

	# all items
	all_items = []


	for item in items:
		# don't keep the position of the item...
		item = item.replace(' are ', ' is ')
		item = item.split(' is ')[0].lower()
	
		all_items.append(item)
	
	return all_items

# get seconds since the unix epoch, UTC
def UTC_UNIX_EPOCH():
	return int(datetime.now(timezone.utc).timestamp())

def WAIT(queue={}, cmd_id='0'):
	# mystery command; abort!!
	if cmd_id not in queue:
		# default to a little snore...
		SLEEP(5)
		return False
		
	# check the status of the queued command...
	status = queue[cmd_id]['status']
	# track how many times this loop runs...
	n_runs = 0
	while status != '' and count <= MAX_WAIT:
		n_runs = n_runs + 1
	
	print('out of runs!')


direction_alias = {
	'look': 'l',
	'north': 'n',
	'south': 's',
	'east': 'e',
	'west': 'w',
	'northeast': 'ne',
	'northwest': 'nw',
	'southeast': 'se',
	'southwest': 'sw',
}

def UNIQUE_ID():
	return uuid.uuid4()

ALIAS_DIRECTION = {v: k for k, v in direction_alias.items()}

REVERSE_ACTION = {
	'n': 's',
	's': 'n',
	'e': 'w',
	'w': 'e',
	'ne': 'sw',
	'nw': 'se',
	'se': 'nw',
	'sw': 'ne',
	'l': 'l',
	# 'up': 'down',
	# 'down': 'up'
}