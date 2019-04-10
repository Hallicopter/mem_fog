from flask import Flask, request 	# create custom server
from functools import partial		# for registering routes 

import random						# generate random data for speed
import requests						# send http requests
import json
import time
import csv							# log data

THRESHOLD_VALUE = 50 		# point at which load balancing is required
LOG_FILE_NAME	= "log.csv"

ACK 			= "ACK"

registered_routes = {}
def register_route(route=None):
	"""
		Create the decorator to allow us to 
		register routes in the subclass of Flask
	"""
	def inner(fn):
		registered_routes[route] = fn
		return fn
	return inner

"""
TEMPLATE FOR A STATE JSON:

state = {
	'active_siblings' 	: []
	'inactive_siblings' : []
	'parents'			: []
	'children'			: []
	'aspects'			: {
							'port':
						}
}

"""

class TrafficLight(Flask):
	"""
		Custom Server inheriting from Flask
	"""
	def __init__(self, name, port, state, speed_limit):
		self.port 			= port
		self.state 			= state
		self.speed_limit 	= speed_limit
		self.vehicle_set	= set()
		Flask.__init__(self, name)
		# register routes
		for route, fn in registered_routes.items():
			partial_fn = partial(fn, self)
			partial_fn.__name__ = fn.__name__
			self.route(route)(partial_fn)

		with open(LOG_FILE_NAME, mode='w') as csv_file:
			fieldnames 		= ['elapsed_time', 'no_of_messages']
			self.writer		= csv.DictWriter(csv_file, fieldnames=fieldnames)

	def divide(self, number_of_additions):
		"""
			Execute the divide operation is of our coordination model
		"""
		
		# keeps track of number of messages sent
		no_of_messages 		= 0

		# list all the siblings to activate	
		siblings_to_add 	= []
		for sib in self.state['inactive_siblings'][:number_of_additions]:
			siblings_to_add.append(sib)

		# send activation requests to list of siblings
		payload = self.state
		for s_url in siblings_to_add:
			ret = requests.get(s_url + 'service_coordination/notify_divide', 
								params={'json':json.dumps(payload)})
			if ret:
				# updates the message count
				no_of_messages += 1
				# update state json
				self.state['inactive_siblings'].remove(s_url)
				self.state['active_siblings'].append(s_url)

		children			= self.state['children']
		parents				= self.state['parents']

		payload				= {'active_siblings':self.state['active_siblings'],
								'port':self.port}

		# notify the divide operation to parent
		for url in parents:
			ret = requests.get(url + 'service_coordination/notify_divide', 
								params={'json':json.dumps(payload)})
			if not ret:
				print("Divide broadcast not sent to {} with error code = {}".format(url,ret))
			else:
				# updates the message count
				no_of_messages += 1

		# notify the divide operation to children
		for url in children:
			for id in self.vehicle_set:
				ret = requests.get(url + 'service_coordination/notify_divide',
									params={'json':json.dumps(payload)})
				if not ret:
					print("Divide broadcast not sent to {} with error code = {}".format(url,ret))
				else:
					# updates the message count
					no_of_messages += 1

		return no_of_messages

		
	@register_route('/recv_data/')
	def recv_data(self):
		"""
			Recieve data from vehicles about their ID and speed
		"""
		self.state['aspects']['request_count'] += 1

		# call divide if threshold has been reached
		if self.state['aspects']['request_count'] > THRESHOLD_VALUE:
			time_before_division 					= time.time()
			no_of_messages 							= self.divide(1)	
			self.vehicle_set 						= set()
			self.state['aspects']['request_count']	= 0
			time_after_division 					= time.time()
			elapsed_time 							= time_after_division - time_before_division

			# logs information into file
			self.writer.writeheader()
			self.writer.writerow({'elapsed_time':elapsed_time,'no_of_messages':no_of_messages})

		payload = json.loads(request.args['json'])
		self.vehicle_set.add(payload['id'])

		# if vehicle is speeding, notify the authorities
		if payload['speed'] > self.speed_limit:
			print("Speed of {} is too fast".format(payload['speed']))

			# select a random parent out of the list and send the data to it
			parent_index	= random.randint(0, len(self.state['parents'])-1)
			ret 			= requests.get(self.state['parents'][parent_index]+'recv_data/', 
												params={'json':json.dumps(payload)})
			if ret:
				print("Data about vehicle {} successfully sent to {}.".format(payload['id'], 
						self.state['parents'][parent_index]))
			else:
				print("Data about vehicle {} couldn't be sent to {}".format(payload['id'],
						self.state['parents'][parent_index]))
		else:
			print("Good speed of {}".format(payload['speed']))

		print("Counter: ", str(self.state['aspects']['request_count']))
		return ACK
		

	@register_route('/service_coordination/notify_divide')
	def divide_request(self):
		"""
			handle the divide notification that might come from
			a sibling, parent or child
		
		"""
		payload = json.loads(request.args['json'])

		url = 'http://' + request.remote_addr + ':' + str(payload['port']) + '/'

		# update states according to the sender type
		if url in self.state['parents']:
			self.state['parents'] = payload['active_siblings']
		elif url in self.state['children']:
			self.state['children'] = payload['active_siblings']
		elif url in self.state['active_siblings']:
			self.state = payload
			self.state['aspects']['request_count'] = 0

		return ACK	