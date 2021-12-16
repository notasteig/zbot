# TASK GLOBALS
# keep track of everyone in line; indexed by order #
CUSTOMER_QUEUE = {}

'''
McSweeneys' Restaurant: Customer Service Counter

Your job is to take orders from and serve meals to a queue of         
customers.  You can have as many orders open at once as you like, but 
customers will not hang around forever so you should manage your time 
accordingly.  The job breaks down into a few basic tasks: Start taking
an order, add the cost of the order to the till (subtract costs if    
required), charge the customer and refund them their change, make the 
drinks for orders using the imp-powered drinks machine and serve the  
order, first getting the drinks from the machine and the dishes from  
the chute.'''


menu_txt = '''You read the menu:

Appetisers
    Boiled McRice                       A$1.40
    Fried McRice                        A$1.40
    Boiled McNoodles                    A$2
    Fried McNoodles                     A$2.12

Main Courses
    McKlatchian Kebab                   A$2.45
    McRib and McNoodles                 A$2.50
    McChopsuey and McNoodles            A$2.67
    McPrawn balls and McNoodles         A$2.67
    McCrunchy bits in orange sauce with McNoodles A$2.67
    McChowmein and McNoodles            A$2.75
    McSlice Porker                      A$3
    McCrispy Duck and McNoodles         A$3.25
    McDwarven Ratburger                 A$3.25
    McMorpork BigDibbler                A$4.37

Soft Drinks
    McCola                              A$2.67
    Strawberry McWobbler                A$3
    McJasmin Tea                        A$3
    McWater                             A$10
'''

ACTIVATE = 'Mr. O.L. Harribal says: Put yer uniform on and we can get started.'

''' take order
The queue moves forward as a pretentious old fellow and a sensitive schoolgirl approach the counter.
take order
They stare up at the sign and begin choosing what they'd like to order.
You haven't finished taking the current customers' order yet.
The sensitive schoolgirl lets the pretentious old fellow know what she'd like.
The pretentious old fellow says: We think we'd like a McRib, McChopsuey, two Boiled McRice and two McColas, if it's not too much trouble.
The pretentious old fellow asks: Think you can handle that?  How much will that be?

We think we'd like a McRib, McChopsuey, two Boiled McRice and two McColas, if it's not too much trouble.

==============
The thin mature gentleman says: We want McCrunchy bits in orange sauce, McChopsuey, a McKlatchian Kebab, Fried McNoodles, a McCola and a Strawberry McWobbler, and that's all.  Nothing else.

list McCrunchy
list McChopsuey
list McKlatchian
list McNoodles
list McCola
list McWobbler
'''

# hold all the tasks and logic to manage the counter
class McCounter:
	
	ROOM_ID = 'd2265a457a2d8adec9d30100fa6302e8477f045e'
	
	# keep track of all drink orders
	DRINKS = []
	
	def __init__(self):
		print('initing!!!')
		# run pre-req functions...
		self.methods = [m for m in dir(self) if not m.startswith('__')]
		print(self.methods)
	
	def _list(self, data):
		print('parse the menu.....')
		print('list data:', data)
		
	
	# handles 'take' command's response...
	# runs whenever a 'take' command is completed...
	def _take(self, data):
		# keep track of all food items
		order_items = []
		
		order_txt = data['order']['txt']
		
		# get item names from order text
		order_txt = order_txt.replace(' and ', ', ')
		order_list = order_txt.split(', ')

		# all items should have Mc somewhere in them...
		mc_items = [item for item in order_list if 'Mc' in item]

		for item in mac_items:
			new_item = {}
			
			# normalize 
			item = item.replace(' like ', ' want ')
			if ' want ' in item:
				item = item.split(' want ')[1].strip()
		
			# how many of these?
			for num_word in word_num.keys():
				if item.startswith(num_word):
					# remove number from item name
					new_item['name'] = item.replace(num_word+' ', '')
					# get quantity
					new_item['quantity'] = word_num[num_word]
				
			# fallback to a quantity of 1
			if 'quantity' not in new_item:
				new_item['name'] = item
				new_item['quantity'] = 1
			
			order_items.append(new_item)

		[print(item) for item in order_items]
		# queue making drinks...
	
	# handles 'charge' command's response
	def _charge(self, data):
		order = data['order']['txt']
