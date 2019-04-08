from flask import Flask
from flask import request
from multiprocessing import Value
import random
import requests


class TrafficLight:

	def __init__(self, port, state):
		self.port = port
		self.state = state
		app = Flask(__name__)
		app.run(debug=True,port=self.port)
		
		@app.route('/recieve_data', methods=['POST','GET'])
		def recv_data():

			self.state['aspects']['request_count'] += 1
			if self.state['aspects']['request_count'].value > 10:
				self.state = self.divide(1)

			data = request.json
			if data['speed'] > 60:
				print("Speed of {} is too fast".format(data['speed']))
				parent = random.randint(0, len(self.state['parents'])-1)
				r = requests.post(self.state['parents'][parent]+'recieve_data', json=dat)
			else:
				print("Good speed of {}".format(data['speed']))
			print("Counter: ", str(self.state['aspects']['request_count'].value))
			return 'speed : ' + str(data['speed'])

		@app.route('/service_coordination/notify_divide')
		def divide_request():
			url = 'http://' + request.remote_addr + ':' + request.json['port'] + '/'
			if url in self.state['parents']:
				self.state['parents'] = requests.json['active_siblings']
			elif url in self.state['children']:
				self.state['children'] = requests.json['active_siblings']
			elif url in self.state['active_siblings']:
				self.state = requests.json
				self.state['aspects']['request_count'].value = 0
			return 'Ack'


	def divide(number_of_additions, port):
		siblings_to_add 	= []
		for sib in state['inactive_siblings'][:number_of_additions]:
			siblings_to_add.append(sib)

		payload = state
		for s_url in siblings_to_add:
			r = requests.post(s_url + 'service_coordination/notify_divide', json=payload)
			if r:
				state['inactive_siblings'].remove(s_url)
				state['active_siblings'].append(s_url)

		children			= state['children']
		parents				= state['parents']
		payload				= {'active_siblings':state['active_siblings'],
								'port':self.port}

		for url in children + parents:
			r = requests.post(url + 'service_coordination/notify_divide', json=payload, port_no=port)
			if not r:
				print("Divide broadcast not sent to {} with error code = {}".format(url,r))

		return state		

	

# counter = Value('i', 0)

if __name__ == '__main__':
	t1 = TrafficLight(5000)