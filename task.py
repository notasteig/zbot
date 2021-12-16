from tasks.mccounter import *

class Task:
	
	def __init__(self, task_name):
		print('TASK', task_name)
		self.current = self._load(task_name)
		print('test', self.current.ROOM_ID)

	def _load(self, task_name):
		self.actions = [method for method in dir(McCounter) if callable(getattr(McCounter, method)) and not method.startswith('__')]
		return McCounter

	def next(self, percept):
		print('im da task, choosing next action...')
		current_action = percept['action']
		print(self.actions)
		print('current action:', '_'+current_action)
		if '_'+current_action in self.actions:
			print('HUZZAH!')
		