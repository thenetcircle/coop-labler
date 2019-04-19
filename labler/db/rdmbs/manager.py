from functools import wraps
from typing import List, Union
from sqlalchemy import and_

from gnenv.environ import GNEnvironment

from labler.cli import AppSession
from labler import errors
from labler.db import IDatabase, ClaimRepr, ProjectRepr
from labler.db.rdmbs.dbman import Database
from labler.db.rdmbs.models import Projects, Claims, Labels, Examples
from labler.db.rdmbs.repr import LabelRepr, ClaimStatuses, LabelStatuses


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
    def _get_all_claims(self, session=None) -> List[ClaimRepr]:
        claims = session.query(Claims).all()

        return [claim.to_repr() for claim in claims]

    @with_session
    def _get_claims_for_user(self, user, session=None) -> List[ClaimRepr]:
        claims = session.query(Claims)\
            .filter_by(claimed_by=user)\
            .all()

        return [claim.to_repr() for claim in claims]

    @with_session
    def _get_claims_for_project(self, name, session=None) -> List[ClaimRepr]:
        claims = session.query(Claims)\
            .filter_by(project_name=name)\
            .all()

        return [claim.to_repr() for claim in claims]

    @with_session
    def _get_claims_for_project_and_user(self, name, user, session=None) -> List[ClaimRepr]:
        claims = session.query(Claims)\
            .filter_by(project_name=name)\
            .filter_by(claimed_by=user)\
            .all()

        return [claim.to_repr() for claim in claims]

    def get_claims(self, name=None, user=None) -> List[ClaimRepr]:
        if name is None and user is None:
            return self._get_all_claims()

        if name is not None and user is not None:
            return self._get_claims_for_project_and_user(name, user)

        if name is not None:
            return self._get_claims_for_project(name)

        return self._get_claims_for_user(user)

    @with_session
    def get_labels(self, project_name, session=None) -> List[LabelRepr]:
        labels = session.query(Labels)\
            .filter_by(project_name=project_name)\
            .all()

        return [label.to_repr() for label in labels]

    @with_session
    def get_projects(self, session=None) -> List[ProjectRepr]:
        return [project.to_repr() for project in session.query(Projects).all()]

    @with_session
    def get_project_names(self, session=None) -> List[str]:
        return [project.project_name for project in session.query(Projects).all()]

    @with_session
    def get_unclaimed(self, project, limit=10, session=None) -> List[LabelRepr]:
        examples = session.query(Examples)\
            .filter_by(project_name=project)\
            .outerjoin(Claims, and_(
                Examples.project_name == Claims.project_name,
                Examples.file_path == Claims.file_path,
                Examples.file_name == Claims.file_name
            ))\
            .filter(Claims.id.is_(None))\
            .limit(limit)\
            .all()

        return [example.to_repr() for example in examples]

    @with_session
    def claim_for(self, to_claim: List[LabelRepr], user: str, session=None) -> None:
        for label in to_claim:
            claim = Claims()
            claim.status = ClaimStatuses.WAITING
            claim.claimed_by = user
            claim.project_name = label.project_name
            claim.file_path = label.file_path
            claim.file_name = label.file_name
            session.add(claim)

        session.commit()

    @with_session
    def get_claim(self, claim_id: int, session=None) -> Union[ClaimRepr, None]:
        claim = session.query(Claims).filter_by(id=claim_id).first()
        if claim is None:
            return None

        return claim.to_repr()

    @with_session
    def finish_claim(self, claim_id: int, session=None) -> None:
        claim = session.query(Claims).filter_by(id=claim_id).first()
        if claim is None:
            return

        claim.status = ClaimStatuses.FINISHED
        session.add(claim)
        session.commit()

    @with_session
    def create_label_localization_or_detection(self, label_repr: LabelRepr, session=None) -> None:
        label = Labels()

        label.target_class = label_repr.target_class
        label.xmin = label_repr.xmin
        label.xmax = label_repr.xmax
        label.ymin = label_repr.ymin
        label.ymax = label_repr.ymax
        label.file_name = label_repr.file_name
        label.file_path = label_repr.file_path
        label.status = label_repr.status
        label.project_name = label_repr.project_name
        label.submitted_by = label_repr.submitted_by

        session.add(label)
        session.commit()
