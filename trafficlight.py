from flask import Flask
from flask import request
from multiprocessing import Value
import random
import requests


counter = Value('i', 0)
app = Flask(__name__)

state = {
	'children'	: [],
	'parents'	: ["http://127.0.0.1:8000/recieve_data"],
	'siblings'	: [],
	'aspects'	: []
}

@app.route('/recieve_data', methods=['POST','GET'])
def generate_dummy_vehicle_data():
	dat = {}
	for i in range(1):
		velocity = random.randint(1,101)
		dat['velocity'] = velocity
		for parent in state['parents']:
			r = requests.post(parent, json=dat)


# @app.route('/service_coordination/merge')
# def merge_request():
	

if __name__ == '__main__':
	generate_dummy_vehicle_data()
	app.run(debug=True,host='0.0.0.0',port=5000)