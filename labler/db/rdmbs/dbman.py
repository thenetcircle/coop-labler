from gnenv.environ import GNEnvironment
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from labler.config import ConfigKeys

# need to keep these here even if "unused", otherwise create_all(engine) won't find the models
from labler.db.rdmbs.models import *


class Database(object):
    def __init__(self, env: GNEnvironment):
        self.env = env
        self.driver = self.env.config.get(ConfigKeys.DRIVER, domain=ConfigKeys.DATABASE, default='postgres+psycopg2')
        self.engine = self.db_connect()
        self.create_tables(self.engine)
        session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(session_factory)

    def db_connect(self):
        domain = ConfigKeys.DATABASE
        params = {
            'drivername': self.driver,
        }

        host = self.env.config.get(ConfigKeys.HOST, default=None, domain=domain)
        port = self.env.config.get(ConfigKeys.PORT, default=None, domain=domain)
        username = self.env.config.get(ConfigKeys.USER, default=None, domain=domain)
        password = self.env.config.get(ConfigKeys.PASSWORD, default=None, domain=domain)
        database = self.env.config.get(ConfigKeys.DB, default=None, domain=domain)
        pool_size = self.env.config.get(ConfigKeys.POOL_SIZE, default=10, domain=domain)

        if host is not None and host != '':
            params['host'] = host
        if port is not None and port != '':
            params['port'] = port
        if username is not None and username != '':
            params['username'] = username
        if password is not None and password != '':
            params['password'] = password
        if database is not None and database != '':
            params['database'] = database

        return create_engine(URL(**params), pool_recycle=280, pool_size=pool_size)

    def truncate(self):
        DeclarativeBase.metadata.drop_all(self.engine)

    def create_tables(self, engine):
        DeclarativeBase.metadata.create_all(engine)
