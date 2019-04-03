from flask import Flask
from flask import request
from multiprocessing import Value
import random
import requests
from membrane_operations import *

# counter = Value('i', 0)
app = Flask(__name__)

initial_state = {
	'children'	: [],
	'parents'	: ["http://127.0.0.1:6000/"],
	'active_siblings'	: [],
	'inactive_siblings'	: ["http://127.0.0.1:5001/"],
	'aspects'	: {
		"request_count": Value('i', 0)
	}
}

state = initial_state

@app.route('/recieve_data', methods=['POST','GET'])
def recv_data():
	with state['aspects']['request_count'].get_lock():
		state['aspects']['request_count'].value += 1
	if state['aspects']['request_count'].value > 200:
		state = divide(state, 1)
		state['aspects']['request_count'].value = 0
	data = request.json
	if data['velocity'] > 60:
		print("Speed of {} is too fast".format(data['velocity']))
		parent = random.randint(0, len(state['parents'])-1)
		# r = requests.post(state['parents'][parent]+'recieve_data', json=dat)
	else:
		print("Good speed of {}".format(data['velocity']))
	print("Counter: ", str(state['aspects']['request_count'].value))
	return 'Velocity : ' + str(data['velocity'])


@app.route('/service_coordination/merge')
def merge_request():
	url = 'http://' + request.remote_addr + '/' + request.environ.get('REMOTE_PORT') + '/'
	if url in state['parents']:
		state['parents'] = requests.json['active_siblings']
	elif url in state['children']:
		state['children'] = requests.json['active_siblings']
	elif url in state['active_siblings']:
		state = initial_state

@app.route('/service_coordination/divide')
def divide_request():
	url = 'http://' + request.remote_addr + '/' + request.environ.get('REMOTE_PORT') + '/'
	if url in state['parents']:
		state['parents'] = requests.json['active_siblings']
	elif url in state['children']:
		state['children'] = requests.json['active_siblings']
	elif url in state['active_siblings']:
		state = requests.json
		state['aspects']['request_count'].value = 0

@app.route('/service_coordination/transform')
def transform_request():
	url = 'http://' + request.remote_addr + '/' + request.environ.get('REMOTE_PORT') + '/'

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0',port=5000)