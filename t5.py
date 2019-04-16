from trafficlight import TrafficLight

PORT 		= 5005
SPEED_LIMIT = 60 
STATE 		= None

app = TrafficLight(__name__, PORT, STATE, SPEED_LIMIT)

if __name__ == '__main__':
	app.run(debug=True, port=PORT)