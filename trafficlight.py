from flask import Flask
from flask import request
from multiprocessing import Value
import random
import requests

state = {
	'children'	: [],
	'parents'	: ["http://127.0.0.1:8000/"],
	'active_siblings'	: [],
	'inactive_siblings'	: [],
	'aspects'	: {
		"request_count": Value('i', 0)
	}
}

class TrafficLight:
	def __init__(self, portNo):
		app = Flask(__name__)
		app.run(debug=True,host='0.0.0.0',port=portNo)
		
		@app.route('/recieve_data', methods=['POST','GET'])
		def recv_data():
			with state['aspects']['request_count'].get_lock():
				state['aspects']['request_count'].value += 1
			if state['aspects']['request_count'].value > 10:
				state = divide(state, 1)
			data = request.json
			if data['velocity'] > 60:
				print("Speed of {} is too fast".format(data['velocity']))
				parent = random.randint(0, len(state['parents'])-1)
				r = requests.post(state['parents'][parent]+'recieve_data', json=dat)
			else:
				print("Good speed of {}".format(data['velocity']))
			print("Counter: ", str(state['aspects']['request_count'].value))
			return 'Velocity : ' + str(data['velocity'])


		@app.route('/service_coordination/merge')
		def merge_request():
			ip = request.remote_addr
			if ip in state['parents']:
				state['parents'] = requests.json['active_siblings']
			elif ip in state['children']:
				state['children'] = requests.json['active_siblings']

		@app.route('/service_coordination/notify_divide')
		def divide_request():
			ip = request.remote_addr
			if ip in state['parents']:
				state['parents'] = requests.json['active_siblings']
			elif ip in state['children']:
				state['children'] = requests.json['active_siblings']

	

# counter = Value('i', 0)

if __name__ == '__main__':
	t1 = TrafficLight(5000)