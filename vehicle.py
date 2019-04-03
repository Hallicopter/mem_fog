from flask import Flask
from flask import request
from multiprocessing import Value
import random
import requests
import time


counter = Value('i', 0)
app = Flask(__name__)

state = {
	'children'	: [],
	'parents'	: ["http://127.0.0.1:5000/recieve_data"],
	'siblings'	: [],
	'aspects'	: []
}

def generate_dummy_vehicle_data(vehicles):
	dat = {}
	for i in range(100):
		time.sleep(1)
		for v in vehicles:
			velocity = random.randint(1,101)
			dat['velocity'] = velocity
			for parent in state['parents']:
				r = requests.post(parent, json=dat)



# @app.route('/service_coordination/merge')
# def merge_request():
	

if __name__ == '__main__':
	vehicles input("Number of vehicles: ")
	generate_dummy_vehicle_data(vehicles)
	app.run(debug=True,host='0.0.0.0',port=5000)


