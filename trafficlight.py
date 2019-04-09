from flask import Flask, request 	# create custom server
from functools import partial		# for registering routes 

import random						# generate random data for speed
import requests						# send http requests

THRESHOLD_VALUE = 100 # point at which load balancing is required

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
		self.speed_limit 	= speed_limits
		super().__init__(self, name)
		# register routes
		for route, fn in registered_routes.items():
			partial_fn = partial(fn, self)
			partial_fn.__name__ = fn.__name__
			self.route(route)(partial_fn)

	def divide(number_of_additions, port):
		"""
			Execute the divide operation is of our coordination model
		"""
		
		# list all the siblings to activate	
		siblings_to_add 	= []
		for sib in state['inactive_siblings'][:number_of_additions]:
			siblings_to_add.append(sib)

		# send activation requests to list of siblings
		payload = state
		for s_url in siblings_to_add:
			ret = requests.post(s_url + 'service_coordination/notify_divide', json=payload)
			if ret:
				# update state json
				state['inactive_siblings'].remove(s_url)
				state['active_siblings'].append(s_url)

		children			= state['children']
		parents				= state['parents']
		payload				= {'active_siblings':state['active_siblings'],
								'port':self.port}

		# notify the divide operation to all parents and children
		for url in children + parents:
			ret = requests.post(url + 'service_coordination/notify_divide', json=payload, 
								port_no=port)
			if not ret:
				print("Divide broadcast not sent to {} with error code = {}".format(url,r))

		return state	
		
	@register_route('/recv_data/', methods=['POST','GET'])
	def recv_data():
		"""
			Recieve data from vehicles about their ID and speed
		"""
		self.state['aspects']['request_count'] += 1

		# call divide if threshold has been reached
		if self.state['aspects']['request_count'].value > THRESHOLD_VALUE:
			self.state = self.divide(1)

		payload = request.json

		# if vehicle is speeding, notify the authorities
		if data['speed'] > self.speed_limit:
			print("Speed of {} is too fast".format(data['speed']))

			# select a random parent out of the list and send the data to it
			parent_index	= random.randint(0, len(self.state['parents'])-1)
			ret 			= requests.post(self.state['parents'][parent_index]+'recv_data/', 
												json=payload)
			if ret:
				print("Data about vehicle {} successfully sent to {}.".format(payload['id'], 
						self.state['parents'][parent_index]))
			else:
				print("Data about vehicle {} couldn't be sent to {}".format(payload['id']),
						self.state['parents'][parent_index])
		else:
			print("Good speed of {}".format(data['speed']))

		print("Counter: ", str(self.state['aspects']['request_count'].value))
		return ACK
		

	@register_route('/service_coordination/notify_divide')
	def divide_request():
		"""
			handle the divide notification that might come from
			a sibling, parent or child
		"""
		url = 'http://' + request.remote_addr + ':' + request.json['port'] + '/'

		# update states according to the sender type
		if url in self.state['parents']:
			self.state['parents'] = requests.json['active_siblings']
		elif url in self.state['children']:
			self.state['children'] = requests.json['active_siblings']
		elif url in self.state['active_siblings']:
			self.state = requests.json
			self.state['aspects']['request_count'].value = 0

		return ACK	