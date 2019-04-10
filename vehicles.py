from flask import Flask
from flask import request

import random	# generate random data
import requests # send http requests
import time		# time stamp and sleep
import json

app 	= Flask(__name__)

PORT 	= 4000
parents = ['http://127.0.0.1:5000/']

ACK		= 'ACK'

class Vehicle:
	def __init__(self, id):
		self.id = id
		self.send_data()
	def send_data(self):
		"""
			generate random speed data and send it to the parent
			each second for 100 seconds
		"""
		global parents
		for i in range(100):
			time.sleep(0.1)
			speed 			= random.randint(1, 101) 				# select a random speed
			parent_index 	= random.randint(0, len(parents)-1) 	# select a parent out of the available with eq probability
			payload			= {'id':self.id, 'speed':speed}
			ret 			= requests.get(parents[parent_index] + 'recv_data/', 
								params={'json':json.dumps(payload)})
			
			# url = parents[parent_index] #+ 'recieve_data'
			# print(url)
			# ret = requests.get(url)

			if ret:
				print("Vehicle {} successfully sent data to {}".format(self.id, parents[parent_index]))
			else:
				print("Vehicle {} counldn't send data to {}".format(self.id, parents[parent_index]))


@app.route('/simulate_vehicles', methods=['GET','POST'])
def send_data():
	for i in range(int(request.data)):
		Vehicle(i)
	return ACK

@app.route('/service_coordination/notify_divide')
def get_divide_notification():
	global parents
	payload = json.loads(request.args['json'])
	parents = payload['active_siblings']
	#id 		= payload['id']
	return ACK + ' id'

if __name__ == '__main__':
	app.run(debug=True, port=PORT)