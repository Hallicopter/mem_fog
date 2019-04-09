from flask import Flask
import requests

counter = Value('i', 0)
app = Flask(__name__)

PORT = 6000

ACK = "ACK"

@app.route('/recv_data', methods=['POST','GET'])
def recv_data():
	return ACK

@app.route('/service_coordination/divide', methods=['POST','GET'])
def divide_request():
	return ACK

if __name__ == '__main__':
	app.run(debug=True,port=PORT)