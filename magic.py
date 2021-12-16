### MAGIC COMMANDS
MAP_START = False
MAP_HISTORY = []

def MAGIC_FN(phrase, map=False, state=False):
	print('phrase', phrase)
	# get camelcased function name
	s = "".join(word[0].upper() + word[1:].lower() for word in phrase.split(' '))
	fn_name = '_' + s[0].lower() + s[1:]
	print('fn_name', fn_name)
	
	# run function (if it exists)
	# TODO: how to get EXPLORED from agent???
	if fn_name in globals():
		globals()[fn_name]()
	else:
		print('*poof*')
		
### MAP STUFFZ
# just for development...
def _mapStart(graph=False, state=False):
	print('_mapStart')
	MAP_START = True
	return graph
	
def _mapShow(graph=False, state=False):
	print('_mapShow')
	
	if not graph:
		return False
	
	# TODO: less sloppy bounding...
	# make sure the grid is big enough...
	offset_x = abs(min([graph[n_id].x for n_id in graph])) + 5
	offset_y = abs(min([graph[n_id].y for n_id in graph])) + 5
	
	# make [y][x] grid with a width of 13
	display_grid = []
	for y in range(0, (20)):
		row = [' '] * (20)
		display_grid.append(row)

	for node_id in graph:
		node = graph[node_id]
		display_grid[node.y+offset_y][node.x+offset_y] = '#' if node.expanded else 'X'
		
	for row in display_grid:
		print(''.join(row))

def _mapStop(graph=False, state=False):
	print('_mapStop')
	MAP_START = False
	return graph
	
def _mapReset(graph=False, state=False):
	print('_mapReset')
	return []
	
# print data out using aima data representations... 
def _mapPrint(graph=False, state=False):
	flat_graph = []
	for node_id in graph:
		node = graph[node_id]
		flat_graph.append({
			'id': node.id,
			'parent_id': node.parent_id,
			'action': node.action,
			'path_cost': node.path_cost,
			'edges': node.edges
		})
	print('---graph data structure:')
	print(flat_graph)
	print('---')
	return graph
	
def _mapSave(graph=False, state=False):
	print('Save JSON data:')
	print(json.dumps(graph))
	print('--------------')

####### next
# recommend next action...
# (next unexplored action, closest to current position)
def _mapNext(graph=False, state=False):
	print('_mapNext')
	
	
MAGIC_FN('map start')