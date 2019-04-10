from flask import Flask
import requests

app = Flask(__name__)

PORT = 6000

ACK = "ACK"

@app.route('/recv_data/')
def recv_data():
	return ACK

@app.route('/service_coordination/notify_divide')
def divide_request():
	return ACK

if __name__ == '__main__':
	app.run(debug=True,port=PORT)