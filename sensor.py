"""
filename: sensor.py
author: asteig
license: public domain

The Sensor class listens for the beginning and ending regexes of a particular command and returns the named capture groups from the regexes.
"""
# standard libraries
import json
import re
import time

# my stuff
from captures import *
from utils import *

STATUS_QUEUED = 'queued'
STATUS_ACTIVE = 'active'
STATUS_SUCCESS = 'success'
STATUS_FAILED = 'failed'

class Sensor:
	
	# queue all commands waiting for a response
	CAPTURE_QUEUE = []
	CAPTURE_HISTORY = []
	
	# keep track of current room
	CURRENT_ROOM_ID = False
	
	# state data; initially False
	state = False
	
	# set capture groups
	def __init__(self, captures=False):
		# set default captures
		self.captures = CMD_CAPTURES
		
		# add any task-specific captures
		if captures:
			for cmd in captures:
				self.captures[cmd] = captures
		
	"""
	return: data of a completed capture or False
	"""
	def read(self, packet):
		# unpack the packet
		# TODO: handle bad packets
		self.data = json.loads(packet)
		
		# send all commands to the capture queue
		if 'cmd_txt' in self.data:
			return self._queueCapture(self.data['cmd_txt'])
		
		# extract data from MUD response text
		if 'response_txt' in self.data:
			if captured_data := self._handleResponseTxt():
				print('FOUND!', captured_data)
				if 'room' in captured_data:
					self.CURRENT_ROOM_ID = captured_data['room']['identifier']
					print('CHANGING ROOM:', self.CURRENT_ROOM_ID)
				return captured_data
				
		# no data yet...
		return False
		
	# collapse to WORLDSTATE data
	# UNIVERSAL FORMATTING (should apply to all MUDs)
	# NOTHING MUD-SPECIFIC BELOW THIS LINE!!!!!
	def _format(self, captured_data):
		nested_data = {}
		# let's go through all the captured results...
		for key in captured_data:
			key_path = key.split('_')
			raw_value = captured_data[key]
			
			# check for basic formatting...
			if key_path[-1] == 'json':
				key_path = key_path[:-1]
				raw_value = json.loads(raw_value)
			elif key_path[-1] == 'list':
				key_path = key_path[:-1]
				raw_value = splitTxtList(raw_value)
			
			# get a nested data object with specified key path
			setNestedValue(nested_data, raw_value, key_path)
			
			# TODO: proper place? :(
			# add action to captured data
			nested_data['action'] = self.active['action']
			
		return nested_data
		
	# TODO: make sure the data isn't being overwritten...
	def _getNamedCaptures(self):
		# get current captures and response text
		captures = self.active['captures']
		response = self.active['response']

		# combine all data
		all_captured = {}
		
		# stack items
		items = []
		
		# search each line of the response for named captures
		for line in response:
			for regex in captures:
				if result := re.search(regex, line):
					groups = result.groupdict()
					captured = {k:v.strip() for k,v in groups.items() if v is not None}
					
					# only if there's data
					if captured:
						# TODO: too specific; should stack any repeated keys
						if 'item' in groups.keys():
							items.append(captured)
						else:
							all_captured.update(captured)
		
		# add item stack to captured data
		if items:
			if self.active['args']:
				all_captured[self.active['args'][0]] = items
			else:
				all_captured['items'] = items

		# filter raw matches 
		return self._format(all_captured)
		
	# extract any data out of the response text
	def _handleResponseTxt(self):
		# get most recent line of output
		sText = self.data['response_txt']

		# ignore blank lines
		if sText.isspace():
			return False
		
		# should we start the capture?
		if self._start():
			# starting capture; no data yet
			return False
		
		# only add response when sensor is actively capturing
		if self.active and self.active['status'] == STATUS_ACTIVE:
			# add response text to capture
			self.active['response'].append(sText)

			# ending capture; save results
			if self._stop(sText):
				# get captured data
				captured = self._getNamedCaptures()
				
				# set new room id
				if 'room' in captured:
					print('changing room...')
					self.CURRENT_ROOM_ID = captured['room']['identifier']
				
				return captured
					

	# add recognized commands to the capture queue
	def _queueCapture(self, cmd_txt):
		new_cmd = False
		
		# parse command line
		cmd_root = cmd_txt.split(' ')[0]
		cmd_args = cmd_txt.split(' ')[1:]
		
		action = cmd_root.lower()
		
		# expand alias
		for cmd in CMD_ALIASES:
			if cmd_root in CMD_ALIASES[cmd]:
				cmd_root = cmd
				
		# add recognized command to queue
		if cmd_root in self.captures or cmd_root:
		
			# make a new command
			new_cmd = {
				'action': action,
				'args': cmd_args if cmd_args else False,
				'cmd_root': cmd_root,
				'captures': self.captures[cmd_root],
				'data': {},
				'response': [],
				'status': STATUS_QUEUED,
			}
			
				# override default capture groups with room-specific ones
		if self.CURRENT_ROOM_ID in ROOM_CAPTURES:
			print('CUSTOM !!!!')
			if action in ROOM_CAPTURES[self.CURRENT_ROOM_ID]:
				if not new_cmd:
					# make a new command
					new_cmd = {
						'action': action,
						'args': cmd_args if cmd_args else False,
						'cmd_root': cmd_root,
						'captures': ROOM_CAPTURES[self.CURRENT_ROOM_ID][action],
						'data': {},
						'response': [],
						'status': STATUS_QUEUED,
					}
				else:
					new_cmd['captures'] = ROOM_CAPTURES[self.CURRENT_ROOM_ID][action]
		
		if new_cmd:
			# add command capture to the queue
			self.CAPTURE_QUEUE.append(new_cmd)

			# no data to return yet
			return False
				
		# wtf do you want me to do with this???
		print('I don\'t know that command!!!!!!', cmd_root)
		return False
	
	def _start(self):
		# get active capture
		self.active = self.CAPTURE_QUEUE[0] if self.CAPTURE_QUEUE else False

		# only queued captures can be started...
		if self.active and self.active['status'] == STATUS_QUEUED:
			# if the first regex matches current line
			start_regex = self.active['captures'][0]
			if re.search(start_regex, self.data['response_txt']):
				self.active['status'] = STATUS_ACTIVE
				self.active['response'].append(self.data['response_txt'])
				return True

		# probably already started
		return False
	
	def _status(self):
		if self.CAPTURE_QUEUE:
			return self.CAPTURE_QUEUE[0]['status']
		else:
			return False

	def _stop(self, sText):
		# only an active capture can be stopped...
		if self.active['status'] != STATUS_ACTIVE:
			return False
		
		# is this the ending capture?
		if re.search(self.active['captures'][-1], sText):
			self.active['status'] = STATUS_SUCCESS
			self.CAPTURE_HISTORY.append(self.active)
			self.CAPTURE_QUEUE.pop(0)
			return True
			
		# not the end of the capture
		return False