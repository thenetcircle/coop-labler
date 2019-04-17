import logging
import os
from typing import List
from typing import Union

from flask import jsonify
from flask import request
from git import GitCommandError
from git.cmd import Git

from labler import errors
from labler.config import ProjectTypes
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
    return api_response(code=200)


@app.route('/claims/user/<user>', methods=['GET'])
def claims_for_user(user):
    claims = env.db.get_claims(name=None, user=user)
    claims_json = [claim.to_dict() for claim in claims]

    return api_response(code=200, data=claims_json)


@app.route('/claims/project/<project>', methods=['GET'])
def claims_for_project(project):
    claims = env.db.get_claims(name=project, user=None)
    claims_json = [claim.to_dict() for claim in claims]

    return api_response(code=200, data=claims_json)


@app.route('/claims/project/<project>/user/<user>', methods=['GET'])
def claims_for_project_and_user(project, user):
    claims = env.db.get_claims(name=project, user=user)
    claims_json = [claim.to_dict() for claim in claims]

    return api_response(code=200, data=claims_json)


@app.route('/claims', methods=['GET'])
def all_claims():
    claims = env.db.get_claims(name=None, user=None)
    claims_json = [claim.to_dict() for claim in claims]

    return api_response(code=200, data=claims_json)


@app.route('/claim/project/<project>/user/<user>', methods=['GET'])
def claim_new_labels(project, user):
    claims = env.claimer.claim(project=project, user=user)
    claims_json = [claim.to_dict() for claim in claims]

    return api_response(code=200, data=claims_json)


@app.route('/submit/<claim_id>', methods=['PUT'])
def submit_label_for_claim(claim_id):
    if claim_id is None or len(claim_id) == 0:
        return api_response(400, message='blank claim id in submission')

    try:
        int(claim_id)
    except ValueError:
        return api_response(400, message='invalid claim id')

    try:
        content = request.json
    except Exception as e:
        logger.error(f'submit_label_for_claim() failed: {str(e)}')
        logger.exception(e)
        return api_response(400, message=f'bad request: {str(e)}')

    try:
        project_type = content.get('project_type', None)
        if project_type is None:
            return api_response(400, message='no project_type in data')

        if project_type == ProjectTypes.CLASSIFICATION.value:
            env.claimer.submit_classification(claim_id, content)

        elif project_type == ProjectTypes.DETECTION.value:
            env.claimer.submit_detection(claim_id, content)

        elif project_type == ProjectTypes.LOCALIZATION.value:
            env.claimer.submit_localization(claim_id, content)

        elif project_type == ProjectTypes.SEGMENTATION.value:
            env.claimer.submit_segmentation(claim_id, content)

        else:
            return api_response(400, message=f'unknown project type {project_type}')

    except errors.LablerException as e:
        logger.error(f'submit_label_for_claim() failed: {str(e)}')
        return api_response(400, message=str(e))

    except Exception as e:
        logger.error(f'submit_label_for_claim() failed: {str(e)}')
        logger.exception(e)
        return api_response(400, message=f'bad request: {str(e)}')

    return api_response(200)


@app.route('/projects', methods=['GET'])
def list_projects():
    projects = env.db.get_projects()
    projects_json = [project.to_dict() for project in projects]

    return api_response(code=200, data=projects_json)
