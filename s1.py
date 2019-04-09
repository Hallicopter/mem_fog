from server import TestView
from flask import Flask

app = Flask(__name__)
TestView(3).register(app)

if __name__ == '__main__':
    app.run()
