import requests 

data="test"
json = {
    'test':'chungus'
}
r = requests.post(url = 'http://127.0.0.1:5000/', data = data, json= json) 