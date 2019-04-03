from flask import Flask
from flask import request
from multiprocessing import Value
import requests
from membrane_operations import *

counter = Value('i', 0)
app = Flask(__name__)

state = {
	'parents'			: [],
	'children'			: ["http://127.0.0.1:5000/"],
	'active_siblings'	: [],
	'inactive_siblings'	: [],
	'aspects'			: []
}

@app.route('/recieve_data', methods=['POST','GET'])
def recv_data():
	with counter.get_lock():
		counter.value += 1
	data = request.json
	# print(data['ve'])
	return 'Velocity : ' + str(data['velocity'])

@app.route('/service_coordination/divide', methods=['POST','GET'])
def divide_request():
	# global state
	# #url = 'http://' + request.remote_addr + ':' + str(request.environ.get('REMOTE_PORT')) + '/'
	# state['parents'] = requests.json['active_siblings']
	# print(state['parents'])
	return 'Ack'

if __name__ == '__main__':
	app.run(debug=True,port=6000)