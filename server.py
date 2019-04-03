from flask import Flask
from flask import request
from multiprocessing import Value

counter = Value('i', 0)
app = Flask(__name__)

@app.route('/')
def hello_world():
	with counter.get_lock():
		counter.value += 1
	data = request.args.get('data')
	return '''<h1>The data is: {}, count: {}</h1>'''.format(data, counter.value)

# @app.route('/service_coordination')
# def get_request_from_parent():
# 	if (request.args.get_url() not in state_json[parents])

if __name__ == '__main__':
   app.run(debug=True,host='0.0.0.0',port=5000)