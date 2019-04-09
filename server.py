from flask import Flask
from functools import partial

registered_routes = {}
def register_route(route=None):
	def inner(fn):
		registered_routes[route] = fn
		return fn
	return inner

class MyServer(Flask):

    def __init__(self, name, integer):
        self.integer = integer
        super().__init__(self, name)
        for route, fn in registered_routes.items():
        	partial_fn = partial(fn, self)
        	partial_fn.__name__ = fn.__name__
        	self.route(route)(partial_fn)
        
    @register_route("/hello/")
    def index(self):
        return "Hello {}".format(self.integer)
    

