from flask import Flask
from flask import request

import random	# generate random data
import requests # send http requests
import time		# time stamp and sleep
import json
import ip_address

EXP_TIME 	= 120 # seconds
SLEEP_TIME 	= 1
app 		= Flask(__name__)
PORT 		= 4000
parents 	= [ip_address.IP_T1]
ACK			= 'ACK'

class Vehicle:
	def __init__(self, id):
		self.id = id
	def send_data(self):
		"""
			generate random speed data and send it to the parent
			each second for 100 seconds
		"""
		global parents
		
		speed 			= random.randint(1, 101) 				# select a random speed
		parent_index 	= random.randint(0, len(parents)-1) 	# select a parent out of the available with eq probability
		payload			= {'id':self.id, 'speed':speed}
		ret 			= requests.get(parents[parent_index] + 'recv_data/', 
							params={'json':json.dumps(payload)})
		
		if ret:
			print("Vehicle {} successfully sent data to {}".format(self.id, parents[parent_index]))
		else:
			print("Vehicle {} counldn't send data to {}".format(self.id, parents[parent_index]))


@app.route('/simulate_vehicles', methods=['GET','POST'])
def send_data():
	for i in range(EXP_TIME):
		time.sleep(SLEEP_TIME)
		for j in range(int(request.data)):
			# rand_vehicle_id = random.randint(0, int(request.data)-1) 
			Vehicle(j).send_data()
	return ACK

@app.route('/service_coordination/notify_divide')
def get_divide_notification():
	global parents
	payload = json.loads(request.args['json'])
	parents = payload['active_siblings']
	return ACK

if __name__ == '__main__':
	app.run(debug=True, port=PORT)