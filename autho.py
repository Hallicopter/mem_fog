from flask import Flask
from flask import request
from multiprocessing import Value
import requests

counter = Value('i', 0)
app = Flask(__name__)

state = {
	'parents'	: [],
	'children'	: ["http://127.0.0.1:5000/collect_data?data="],
	'siblings'	: [],
	'aspects'	: []
}

@app.route('/recieve_data', methods=['POST','GET'])
def recv_data():
	with counter.get_lock():
		counter.value += 1
	data = request.json
	# print(data['ve'])
	return 'Velocity : ' + str(data['velocity'])


if __name__ == '__main__':
	app.run(debug=True,port=8000)