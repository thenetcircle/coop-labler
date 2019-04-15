import logging
import os
from typing import List
from typing import Union

from flask import jsonify
from git.cmd import Git

from labler.server import app

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

home_dir = os.environ.get('LB_HOME', default=None)
environment = os.environ.get('LB_ENVIRONMENT', default=None)

if home_dir is None:
    home_dir = '.'
tag_name = Git(home_dir).describe()


def is_blank(s: str):
    return s is None or len(s.strip()) == 0


def api_response(code, data: Union[dict, List[dict]] = None, message: Union[dict, str] = None):
    if data is None:
        data = dict()
    if message is None:
        message = ''

    return jsonify({
        'status_code': code,
        'data': data,
        'message': message
    })


@app.route('/', methods=['GET'])
def index():
    return api_response(
        code=200,
        data=dict(),

    )
