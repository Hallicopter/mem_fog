from flask import Flask
from flask import request

import random	# generate random data
import requests # send http requests
import time		# time stamp and sleep

app 	= Flask(__name__)

PORT 	= 4000
parents = []

ACK		= 'ACKNOWLEDGED'

class Vehicle:
	def __init__(self, id):
		self.id = id
	def send_data(self):
		"""
			generate random speed data and send it to the parent
			each second for 100 seconds
		"""
		global parents
		for i in range(100):
			time.sleep(1)
			speed 			= random.randint(1, 101) 			# select a random speed
			parent_index 	= random.randint(0, len(parents)) 	# select a parent out of the available with eq probability
			json 			= {'id':self.id, 'speed':speed}
			ret 			= requests.post(parents[parent_index] + 'recieve_data', json=json)
			if ret:
				print(self.id + " sent data to " + parents[parent_index])
			else:
				print(self.id + " couldn't send data to " + parents[parent_index])


@app.route('/simulate_vehicles', methods=['GET', 'POST'])
def send_data():
	for i in range(int(request.data)):
		Vehicle(i).send_data();
	return ACK

@app.route('/service_coordination/notify_divide', methods=['GET','POST'])
def get_divide_notification():
	global parents
	parents = request.json['active_siblings']
	id  	= request.json['id']
	return ACK + ' id'

if __name__ == '__main__':
	app.run(debug=True, port=PORT)