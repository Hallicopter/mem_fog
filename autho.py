from flask import Flask
from flask import request
from multiprocessing import Value

counter = Value('i', 0)
app = Flask(__name__)

state = {
	'parents'	: [],
	'children'	: ["http://127.0.0.1:5000/collect_data?data="],
	'siblings'	: [],
	'aspects'	: []
}

@app.route('/recieve_data')
def recv_data():
	with counter.get_lock():
		counter.value += 1
	data = request.args.get('params')
	print(data)


if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0',port=8000)