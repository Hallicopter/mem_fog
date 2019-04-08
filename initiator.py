import requests
import sys

if __name__ == '__main__':
	requests.post('http://127.0.0.1:4000/simulate_vehicles', data=sys.argv[1])
