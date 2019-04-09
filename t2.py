from trafficlight import TrafficLight

PORT 		= 5001
SPEED_LIMIT = 60 
STATE = {
	'active_siblings' 	: ['http://127.0.0.1:5000/'],
	'inactive_siblings' : ['http://127.0.0.1:5001/'],
	'parents'			: ['http://127.0.0.1:6000/'],
	'children'			: ['http://127.0.0.1:4000/'],
	'aspects'			: {
							'port':5001
						}
}

app = TrafficLight(__name__, PORT, STATE, SPEED_LIMIT)

if __name__ == '__main__':
	app.run(debug=True, port=PORT)