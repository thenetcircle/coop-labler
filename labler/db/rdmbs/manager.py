from functools import wraps

from gnenv.environ import GNEnvironment

from labler.db import IDatabase
from labler.db.rdmbs.dbman import Database
from labler.db.rdmbs.models import Projects


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
    def create_project(self, name, session=None):
        project = Projects()
        project.name = name

        session.add(project)
        session.commit()
