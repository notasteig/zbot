# matches everything EXCEPT player commands
REGEX_RESPONSE = r'^[\WA-Z]'

# matches basic user input (editors, etc. handled separately)
REGEX_COMMAND = r'^[a-z]'

# matches any error text
REGEX_FAILED = r'(?P<failed>(^That doesn\'t work\.$|^Try something else\.$|What\?$))'

CMD_CAPTURES = {
	'inventory': [
		r'^You are (unburdened|burdened) \((?P<inventory_burden>\d+)\%\) by\:$',
		r'^Holding \: (((?P<inventory_left>.+)) \(left hand\)|)((( and |)(?P<inventory_right>.+)) \(right hand\)\.$|)',
		r'^Wearing \: (?P<inventory_wearing_list>.+)\.$',
		r'^\(under\) \: (?P<inventory_under_list>.+)\.$',
		r'^Carrying\: (?P<inventory_carrying_list>.+)\.$',
		r'(^Your purse contains (?P<inventory_purse_list>.+)\.$|^You are just a disembodied (?P<char_dead>spirit))'
	],
	'list': [
		r'^The following items are for sale:$',
		r'^   (?P<id>.+)\: (?P<item>.+) for (?P<price>.+) \(.+\)\.$',
		r'^(.+) list From \d+ to \d+ of (?P<shop_total>\d+)',
		#r'(?!^   (?P<id>.+)\: (?P<shop_item>.+) for (?P<price>.+) \(.+\).*$)',
		r'^(?P<shop_keeper>.+) (says|exclaims|asks)\: (.+)$'
	],
	'locate': [
		r'^The (?P<item>.+) \((?P<id>\d+)\) is (?P<location>.+)\.$',
		r'^(?!^The .+ \(\d+\) is .+).*'
	],
	'look': [
		# TODO: parse any json...
		r'(?P<room_json>{\"identifier\".+$)',
		r'^\[(?P<room_name>.+)\]$',
		r'(?P<room_description>.+\.  .+\.)',
		r'^There (is|are) .+ obvious exit(s|)\: (?P<room_exits_list>.+)\.$'
	],
	'value': [
		r'^You estimate that the (?P<value_item>.+) is worth (?P<value_amount>.+)\.  ',
		r'^(?!You estimate that the .+ is worth .+\.)'
	],
	# 'help': {
	# 	r'((?P<help_type>.+) \b\w+\b room help|((?P<failed>There is no help available for this room\.$))',
	# 	r'(\w.+ - (?P<help_description>.+)',
	# 	r'^\ {5}(?P<help_cmd>\w+) (?P<help_syntax>([^\w]).+)',
	# 	r'^See also'
	# }
	
}

CMD_ALIASES = {
	'look': [
		'l',
		'n', 's', 'e', 'w', 
		'forward', 'backward',
		'left', 'right',
		'up', 'down',
		'out',
	],
	'inventory': ['i'],
}

RESPONSE_CAPTURES = {
	'prompt': [
		r'(?P<prompt>^.+(\:$|\? ))(\((?P<options>.+)\)$|)',
		r'(^(?P<response>[a-z].+)|^(?P<failed>[\WA-Z].+))'
	],
	'stats': [
		r'{\"alignment\":\"(?P<alignment>.+)\",\"maxhp\":(?P<maxhp>\d+),\"hp\":(?P<hp>\d+),\"xp\":(?P<xp>\d+),\"maxgp\":(?P<maxgp>\d+),\"burden\":(?P<burden>\d+),\"gp\":(?P<gp>\d+)}',
	]
}

# room-specific captures (sometimes overriding commands)
ROOM_CAPTURES = {
	'd2265a457a2d8adec9d30100fa6302e8477f045e': {
		'list': [
			r'Appetisers', # start expression
			r'    (?P<item_txt>.+) +A\$(?P<item_price>.+)', # parse captured data
			r'McWater' # end expression
		],
		# listen for the following updates...
		'take': [
			r'The queue moves forward as (?P<order_npc>.+) approach',
			r'says\: (?P<order_txt>.+)'
		],
		'charge': [
			r'The total comes to (?P<order_total>.+)\.',
			r'you (?P<order_paid>.+) which you place in the register',
		],
		'refund': [
			r'You tear the receipt for order \#(?P<order_num>\d+)',
		],
		'add': [
			r'add A\$(?P<register_add>\d+\.\d+).+A\$(?P<register_total>\d+\.\d+)'
		]
	}
}