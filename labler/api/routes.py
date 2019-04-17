import logging
import os
from typing import List
from typing import Union

from flask import jsonify
from git import GitCommandError
from git.cmd import Git

from labler.server import app
from labler.environ import env

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

home_dir = os.environ.get('LB_HOME', default=None)

if home_dir is None:
    home_dir = '.'

try:
    tag_name = Git(home_dir).describe()
except GitCommandError:
    tag_name = '<no version>'


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
        data=dict()
    )


@app.route('/claims/user/<user>', methods=['GET'])
def claims_for_user(user):
    claims = env.db.get_claims(name=None, user=user)
    claims_json = [claim.to_dict() for claim in claims]

    return api_response(
        code=200,
        data=claims_json
    )


@app.route('/claims/project/<project>', methods=['GET'])
def claims_for_project(project):
    claims = env.db.get_claims(name=project, user=None)
    claims_json = [claim.to_dict() for claim in claims]

    return api_response(
        code=200,
        data=claims_json
    )


@app.route('/claims/project/<project>/user/<user>', methods=['GET'])
def claims_for_project_and_user(project, user):
    claims = env.db.get_claims(name=project, user=user)
    claims_json = [claim.to_dict() for claim in claims]

    return api_response(
        code=200,
        data=claims_json
    )


@app.route('/claims', methods=['GET'])
def all_claims():
    claims = env.db.get_claims(name=None, user=None)
    claims_json = [claim.to_dict() for claim in claims]

    return api_response(
        code=200,
        data=claims_json
    )


@app.route('/claim/project/<project>/user/<user>', methods=['GET'])
def claim_new_labels(project, user):
    claims = env.claimer.claim(project=project, user=user)
    claims_json = [claim.to_dict() for claim in claims]

    return api_response(
        code=200,
        data=claims_json
    )


@app.route('/projects', methods=['GET'])
def projects():
    return api_response(
        code=200,
        data=env.db.get_projects()
    )
