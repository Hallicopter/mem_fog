from trafficlight import TrafficLight

PORT 		= 5002
SPEED_LIMIT = 60 
STATE 		= None

app = TrafficLight(__name__, PORT, STATE, SPEED_LIMIT)

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=PORT)