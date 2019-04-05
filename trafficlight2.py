from flask import Flask
from flask import request
from multiprocessing import Value
import random
import requests
from membrane_operations import *

# counter = Value('i', 0)
app = Flask(__name__)

PORT = 5001

initial_state = {
	'children'	: ["http://127.0.0.1:4000/"],
	'parents'	: ["http://127.0.0.1:6000/"],
	'active_siblings'	: ["http://127.0.0.1:5000/"],
	'inactive_siblings'	: [],
	'aspects'	: {
		"request_count": 0
	}
}

state = initial_state

@app.route('/recieve_data', methods=['POST','GET'])
def recv_data():
	global state	
	state['aspects']['request_count']+= 1
	if state['aspects']['request_count']> 200:
		state = divide(state, 1, PORT)
		state['aspects']['request_count'] = 0
	data = request.json
	if data['velocity'] > 60:
		print("Speed of {} is too fast".format(data['velocity']))
		parent = random.randint(0, len(state['parents'])-1)
		r = requests.post(state['parents'][parent]+'recieve_data', json=data)
	else:
		print("Good speed of {}".format(data['velocity']))
	print("Counter: ", str(state['aspects']['request_count']))
	return 'Velocity : ' + str(data['velocity'])


@app.route('/service_coordination/merge', methods=['POST', 'GET'])
def merge_request():
	global state
	url = 'http://' + request.remote_addr + ':' + str(request.get_data()) + '/'
	if url in state['parents']:
		state['parents'] = requests.json['active_siblings']
	elif url in state['children']:
		state['children'] = requests.json['active_siblings']
	elif url in state['active_siblings']:
		state = initial_state
	return 'Ack'

@app.route('/service_coordination/divide', methods={'POST', 'GET'})
def divide_request():
	global state
	url = 'http://' + request.remote_addr + ':' + str(request.get_data()) + '/'
	print("This " + url)
	if url in state['parents']:
		state['parents'] = requests.json['active_siblings']
	elif url in state['children']:
		state['children'] = requests.json['active_siblings']
	elif url in state['active_siblings']:
		state = requests.json
		state['aspects']['request_count'].value = 0
	return 'Ack'

@app.route('/service_coordination/transform', methods={'POST', 'GET'})
def transform_request():
	global state
	url = 'http://' + request.remote_addr + ':' + str(request.get_data()) + '/'
	return 'Ack'

if __name__ == '__main__':
	app.run(debug=True,port=PORT)