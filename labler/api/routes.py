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
from labler.db.rdmbs.repr import LabelFields
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
    }), code


@app.route('/api/v1/', methods=['GET'])
def index():
    return api_response(code=200)


@app.route('/api/v1/claims/user/<user>', methods=['GET'])
def claims_for_user(user):
    claims = env.db.get_claims(name=None, user=user)
    claims_json = [claim.to_dict() for claim in claims]

    return api_response(code=200, data=claims_json)


@app.route('/api/v1/claim/project/<project>/user/<user>', methods=['GET'])
def claim_new_labels(project, user):
    claims = env.claimer.claim(project=project, user=user)
    claims_json = [claim.to_dict() for claim in claims]

    return api_response(code=200, data=claims_json)


@app.route('/api/v1/submit/<claim_id>', methods=['POST'])
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


@app.route('/api/v1/overview/project/<project_name>', methods=['GET'])
def get_overview(project_name):
    examples = env.db.get_examples(project_name)
    labels = env.db.get_labels(project_name)

    labels_by_name = dict()
    for label in labels:
        json_label = label.to_dict()
        del json_label[LabelFields.FILE_NAME]
        del json_label[LabelFields.FILE_PATH]
        del json_label[LabelFields.PROJECT_NAME]
        del json_label[LabelFields.SUBMITTED_AT]
        del json_label[LabelFields.SUBMITTED_BY]

        if label.file_name not in labels_by_name:
            labels_by_name[label.file_name] = [json_label]
        else:
            labels_by_name[label.file_name].append(json_label)

    output = {
        'done': list(),
        'remaining': list()
    }

    for example in examples:
        try:
            filename = example.file_name
            im_parts = filename.split(os.path.sep)[-1].split('.', maxsplit=1)
            rz_file_name = f'{im_parts[0]}_th.{im_parts[1]}'

            if not os.path.exists(os.path.join(example.file_path, rz_file_name)):
                continue

            labels_for_image = list()
            if filename in labels_by_name.keys():
                labels_for_image = labels_by_name[filename]

            b64image, width, height = env.imager.load_b64_and_dims(example.file_path, rz_file_name)
            json_image = {
                'base64': b64image,
                'width': width,
                'height': height,
                'labels': labels_for_image
            }

            if len(labels_for_image) == 0:
                output['remaining'].append(json_image)
            else:
                output['done'].append(json_image)

        except Exception as e:
            logger.error(f'could not get thumbnail: {str(e)}')
            logger.exception(e)

    return api_response(code=200, data=output)


@app.route('/api/v1/projects', methods=['GET'])
def list_projects():
    projects = env.db.get_projects()
    projects_json = [project.to_dict() for project in projects]

    return api_response(code=200, data=projects_json)


@app.route('/api/v1/image/<claim_id>', methods=['GET'])
def get_image_b64(claim_id):
    claim = env.db.get_claim(claim_id)
    if claim is None:
        return api_response(code=400, message='no such claim')

    try:
        b64image, width, height = env.imager.load_b64_and_dims(claim.file_path, claim.file_name)
    except Exception as e:
        logger.error(f'could not load image: {str(e)}')
        logger.exception(e)
        return api_response(code=500, message='could not load image for claim')

    labels = env.db.get_labels_for_example(claim.project_name, claim.file_path, claim.file_name)
    json_labels = list()
    for label in labels:
        json_labels.append({
            LabelFields.ID: label.id,
            LabelFields.XMIN: label.xmin,
            LabelFields.XMAX: label.xmax,
            LabelFields.YMIN: label.ymin,
            LabelFields.YMAX: label.ymax,
            LabelFields.TARGET_CLASS: label.target_class
        })

    return api_response(code=200, data={
        'base64': b64image,
        'labels': json_labels,
        'width': width,
        'height': height
    })

@app.route('/api/v1/label/<label_id>', methods=['DELETE'])
def delete_label(label_id):
    env.db.remove_label(label_id)
    return api_response(code=200)
