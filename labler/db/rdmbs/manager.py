from functools import wraps
from typing import List
from sqlalchemy import and_

from gnenv.environ import GNEnvironment

from labler.cli import AppSession, errors
from labler.db import IDatabase
from labler.db.rdmbs.dbman import Database
from labler.db.rdmbs.models import Projects, Claims, Labels
from labler.db.rdmbs.repr import LabelRepr


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
    def create_project(self, name, app: AppSession, session=None) -> None:
        project = Projects()
        project.project_name = name
        project.classes = app.lambdaenv.classes or 2
        project.project_type = app.lambdaenv.project_type or 'classification'
        project.directory = app.lambdaenv.directory

        session.add(project)
        session.commit()

    @with_session
    def update_project(self, name, app: AppSession, session=None) -> None:
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
    def project_exists(self, name, session=None) -> bool:
        project = session.query(Projects).filter_by(project_name=name).first()
        return project is not None

    @with_session
    def _get_all_claims(self, session=None):
        claims = session.query(Claims).all()

        return [claim.to_dict() for claim in claims]

    @with_session
    def _get_claims_for_user(self, user, session=None):
        claims = session.query(Claims)\
            .filter_by(claimed_by=user)\
            .all()

        return [claim.to_dict() for claim in claims]

    @with_session
    def _get_claims_for_project(self, name, session=None):
        claims = session.query(Claims)\
            .filter_by(project_name=name)\
            .all()

        return [claim.to_dict() for claim in claims]

    @with_session
    def _get_claims_for_project_and_user(self, name, user, session=None):
        claims = session.query(Claims)\
            .filter_by(project_name=name)\
            .filter_by(claimed_by=user)\
            .all()

        return [claim.to_dict() for claim in claims]

    def get_claims(self, name=None, user=None) -> List[dict]:
        if name is None and user is None:
            return self._get_all_claims()

        if name is not None and user is not None:
            return self._get_claims_for_project_and_user(name, user)

        if name is not None:
            return self._get_claims_for_project(name)

        return self._get_claims_for_user(user)

    @with_session
    def get_projects(self, session=None) -> List[dict]:
        return [{
            'project_name': project.project_name,
            'project_type': project.project_type,
            'classes': project.classes,
            'directory': project.directory
        } for project in session.query(Projects).all()]

    @with_session
    def get_project_names(self, session=None) -> List[str]:
        return [project.project_name for project in session.query(Projects).all()]

    @with_session
    def get_unclaimed(self, project, limit=10, session=None) -> List[LabelRepr]:
        labels = session.query(Labels)\
            .filter_by(project=project)\
            .filter_by(status=Labels.Statuses.WAITING)\
            .outerjoin(Claims, and_(
                Labels.project_name == Claims.project_name,
                Labels.file_path == Claims.file_path,
                Labels.file_name == Claims.file_name
            ))\
            .filter(Claims.id.is_(None))\
            .limit(limit)\
            .all()

        return [label.ro_repr() for label in labels]
