from functools import wraps

from gnenv.environ import GNEnvironment

from labler.cli import AppSession, errors
from labler.config import ConfigKeys
from labler.db import IDatabase
from labler.db.rdmbs.dbman import Database
from labler.db.rdmbs.models import Projects, Claims


def with_session(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        session = DatabaseRdbms.db.Session()
        try:
            kwargs['session'] = session
            return view_func(*args, **kwargs)
        except:
            session.rollback()
            raise
        finally:
            DatabaseRdbms.db.Session.remove()
    return wrapped


class DatabaseRdbms(IDatabase):
    db = None

    def __init__(self, env: GNEnvironment):
        self.env = env
        DatabaseRdbms.db = Database(env)

    @with_session
    def create_project(self, name, app: AppSession, session=None):
        project = Projects()
        project.project_name = name
        project.classes = app.lambdaenv.classes or 2
        project.project_type = app.lambdaenv.project_type or 'classification'
        project.directory = app.lambdaenv.directory

        session.add(project)
        session.commit()

    @with_session
    def update_project(self, name, app: AppSession, session=None):
        project = session.query(Projects).filter_by(project_name=name).first()
        if project is None:
            raise errors.FatalException(f'no project exist for name {name}')

        project.project_name = name
        project.classes = app.lambdaenv.classes or project.classes
        project.project_type = app.lambdaenv.project_type or project.project_type
        project.directory = app.lambdaenv.directory or project.directory

        session.add(project)
        session.commit()

    @with_session
    def project_exists(self, name, session=None):
        project = session.query(Projects).filter_by(project_name=name).first()
        return project is not None

    @with_session
    def get_all_claims(self, session=None):
        return [{
            'project': claim.project_name,
            'file_name': claim.file_name,
            'claimed_by': claim.claimed_by,
            'claimed_at': claim.claimed_at.strftime(ConfigKeys.DEFAULT_DATE_FORMAT)
        } for claim in session.query(Claims).all()]

    @with_session
    def get_claims_for_user(self, user, session=None):
        return [{
            'project': claim.project_name,
            'file_name': claim.file_name,
            'claimed_by': claim.claimed_by,
            'claimed_at': claim.claimed_at.strftime(ConfigKeys.DEFAULT_DATE_FORMAT)
        } for claim in session.query(Claims).filter_by(claimed_by=user).all()]

    @with_session
    def get_claims_for_project(self, name, session=None):
        return [{
            'project': claim.project_name,
            'file_name': claim.file_name,
            'claimed_by': claim.claimed_by,
            'claimed_at': claim.claimed_at.strftime(ConfigKeys.DEFAULT_DATE_FORMAT)
        } for claim in session.query(Claims).filter_by(project_name=name).all()]

    @with_session
    def get_claims_for_project_and_user(self, name, user, session=None):
        return [{
            'project': claim.project_name,
            'file_name': claim.file_name,
            'claimed_by': claim.claimed_by,
            'claimed_at': claim.claimed_at.strftime(ConfigKeys.DEFAULT_DATE_FORMAT)
        } for claim in session.query(Claims).filter_by(project_name=name).filter_by(claimed_by=user).all()]

    def get_claims(self, name=None, user=None):
        if name is None and user is None:
            return self.get_all_claims()

        if name is not None and user is not None:
            return self.get_claims_for_project_and_user(name, user)

        if name is not None:
            return self.get_claims_for_project(name)

        return self.get_claims_for_user(user)

    @with_session
    def get_projects(self, session=None):
        return [{
            'project_name': project.project_name,
            'project_type': project.project_type,
            'classes': project.classes,
            'directory': project.directory
        } for project in session.query(Projects).all()]

    @with_session
    def get_project_names(self, session=None):
        return [project.project_name for project in session.query(Projects).all()]
