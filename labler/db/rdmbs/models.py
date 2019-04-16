from datetime import datetime as dt

from sqlalchemy import Column, Integer, String, DateTime, Boolean, text

from labler.db.rdmbs import DeclarativeBase


class Projects(DeclarativeBase):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)

    name = Column('name', String(128), nullable=False, index=True, unique=True)
    directory = Column('directory', String(128), nullable=True, index=False, unique=False)
    created = Column('created', DateTime, nullable=False, default=dt.utcnow)
    project_type = Column('project_type', String(32), nullable=False, server_default='classification')
    classes = Column('classes', Integer, nullable=False, server_default=text('2'))
    finished = Column('finished', Boolean, nullable=False, server_default=text('false'))
