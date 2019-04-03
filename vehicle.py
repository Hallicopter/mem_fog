from flask import Flask
from flask import request
from multiprocessing import Value
import random
import requests
import time
from membrane_operations import *


counter = Value('i', 0)
app = Flask(__name__)

state = {
	'children'	: None,
	'parents'	: ["http://127.0.0.1:5000/"],
	'active_siblings'	: None,
	'inactive_siblings'	: None,
	'aspects'	: None
}

def generate_dummy_vehicle_data(vehicles):
	dat = {}
	for i in range(100):
		time.sleep(1)
		for v in range(vehicles):
			velocity = random.randint(1,101)
			dat['velocity'] = velocity
			parent = random.randint(0, len(state['parents'])-1)
			r = requests.post(state['parents'][parent]+'recieve_data', json=dat)



@app.route('/service_coordination/merge')
def merge_request():
	url = 'http://' + request.remote_addr + '/' + request.environ.get('REMOTE_PORT') + '/'
	if url in state['parents']:
		state['parents'] = requests.json['active_siblings']
	elif url in state['children']:
		state['children'] = requests.json['active_siblings']

@app.route('service_coordination/divide')
def divide_request():
	url = 'http://' + request.remote_addr + '/' + request.environ.get('REMOTE_PORT') + '/'
	if url in state['parents']:
		state['parents'] = requests.json['active_siblings']
	elif url in state['children']:
		state['children'] = requests.json['active_siblings']
	

if __name__ == '__main__':
	vehicles = input("Number of vehicles: ")
	generate_dummy_vehicle_data(int(vehicles))
	app.run(debug=True,host='0.0.0.0',port=4000)


