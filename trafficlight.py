from flask import Flask
from flask import request
from multiprocessing import Value
import random
import requests


# counter = Value('i', 0)
app = Flask(__name__)

state = {
	'children'	: [],
	'parents'	: ["http://127.0.0.1:8000/"],
	'siblings'	: [],
	'aspects'	: {
		"request_count": Value('i', 0)
	}
}

@app.route('/recieve_data', methods=['POST','GET'])
def recv_data():
	with state['aspects']['request_count'].get_lock():
		state['aspects']['request_count'].value += 1
	data = request.json
	if data['velocity'] > 60:
		print("Speed of {} is too fast".format(data['velocity']))
		parent = random.randint(0, len(state['parents'])-1)
		# r = requests.post(state['parents'][parent]+'recieve_data', json=dat)
	else:
		print("Good speed of {}".format(data['velocity']))
	print("Counter: ", str(state['aspects']['request_count'].value))
	return 'Velocity : ' + str(data['velocity'])


# @app.route('/service_coordination/merge')
# def merge_request():
	

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0',port=5000)