from flask import Flask
from flask import request
app = Flask(__name__)


@app.route('/',methods=['POST','GET'])
def hello():
    d1 = request.json
    # d2 = request.data
    print(d1)
    return "Hello World!"

if __name__ == '__main__':
    app.run(port=5000)