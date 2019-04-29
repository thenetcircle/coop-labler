import logging
import os
from uuid import uuid4 as uuid

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from werkzeug.middleware.proxy_fix import ProxyFix

from labler.api.claimer import Claimer
from labler.api.imager import Imager
from labler.config import ConfigKeys
from labler.data.handler import DataHandler
from labler.db.rdmbs.manager import DatabaseRdbms

logging.basicConfig(
    level=getattr(logging, os.environ.get('LOG_LEVEL', 'DEBUG')),
    format='%(asctime)s - %(name)-18s - %(levelname)-7s - %(message)s')

logger = logging.getLogger(__name__)
logging.getLogger('kafka').setLevel(logging.WARNING)
logging.getLogger('kafka.conn').setLevel(logging.WARNING)


class ReverseProxied(object):
    """
    Wrap the application in this middleware and configure the
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
    }

    :param app: the WSGI application
    """
    def __init__(self, _app):
        self.app = _app

    def __call__(self, env, start_response):
        script_name = env.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            env['SCRIPT_NAME'] = script_name
            path_info = env['PATH_INFO']
            if path_info.startswith(script_name):
                env['PATH_INFO'] = path_info[len(script_name):]

        scheme = env.get('HTTP_X_SCHEME', '')
        if scheme:
            env['wsgi.url_scheme'] = scheme
        return self.app(env, start_response)


def create_app():
    from labler.environ import create_env
    import labler

    environment = os.environ.get('LB_ENVIRONMENT', default=None)
    env = create_env(environment, quiet=False)
    labler.environ.env = env

    secret = env.config.get(ConfigKeys.SECRET_KEY, default=str(uuid()))

    _app = Flask(import_name=__name__)
    CORS(_app, resources={r"/api/*": {"origins": "*"}})

    _app.wsgi_app = ReverseProxied(ProxyFix(_app.wsgi_app))
    _app.config['SECRET_KEY'] = secret
    env.app = _app

    return _app, Api(_app)


app, api = create_app()

# keep this, otherwise flask won't find any routes
import labler.api.routes
