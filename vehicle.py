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

@app.route('/generate_dummy_data', methods=['POST','GET'])
def generate_dummy_vehicle_data():
	print(request.remote_addr)
	vehicles = int(request.get_data())
	dat = {}
	for i in range(100):
		time.sleep(1)
		for v in range(vehicles):
			print(state['parents'])
			velocity = random.randint(1,101)
			dat['velocity'] = velocity
			parent = random.randint(0, len(state['parents'])-1)
			r = requests.post(state['parents'][parent]+'recieve_data', json=dat)
	return 'Ack'

@app.route('/service_coordination/merge', methods=['POST','GET'])
def merge_request():
	global state
	url = 'http://' + request.remote_addr + ':' + str(request.get_data()) + '/'
	state['children'] = requests.json['active_siblings']
	return 'Ack'

@app.route('/service_coordination/divide', methods=['POST','GET'])
def divide_request():
	global state
	url = 'http://' + request.remote_addr + ':' + str(request.get_data()) + '/'
	state['parents'] = requests.json['active_siblings']
	return 'Ack'
	

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0',port=4000)
	


