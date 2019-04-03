import requests
import sys

if __name__ == '__main__':
	vehicles = sys.argv[1]
	requests.post('http://127.0.0.1:4000/generate_dummy_data', data=vehicles)
