import eventlet

# need to monkey patch some standard functions in python since they don't natively support async mode
eventlet.monkey_patch()

# keep this import; even though unused, gunicorn needs it, otherwise it will not start
from labler.server import app, api

from labler import environ
environ.env.node = 'app'
environ.env.api = api
environ.env.app = app
