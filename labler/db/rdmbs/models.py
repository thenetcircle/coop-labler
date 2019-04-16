from sqlalchemy import Column, Integer, String, DateTime, Boolean, text, func

from labler.db.rdmbs import DeclarativeBase
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime


class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


@compiles(utcnow, 'mssql')
def ms_utcnow(element, compiler, **kw):
    return "GETUTCDATE()"


class Projects(DeclarativeBase):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)

    name = Column('name', String(128), nullable=False, index=True, unique=True)
    directory = Column('directory', String(128), nullable=True, index=False, unique=False)
    created = Column('created', DateTime, nullable=False, server_default=utcnow())
    project_type = Column('project_type', String(32), nullable=False, server_default='classification')
    classes = Column('classes', Integer, nullable=False, server_default=text('2'))
    finished = Column('finished', Boolean, nullable=False, server_default=text('false'))


class Claims(DeclarativeBase):
    __tablename__ = 'claims'

    id = Column(Integer, primary_key=True)

    file_path = Column('file_path', String(256), nullable=False, index=True, unique=False)
    file_name = Column('file_name', String(256), nullable=False, index=True, unique=False)

    project_name = Column('project_name', String(256), nullable=False, index=True, unique=False)
    claim_time = Column('claim_time', DateTime, nullable=False, server_default=utcnow())
    claim_user = Column('claim_user', String(128), nullable=False, index=True, unique=False)


class Labels(DeclarativeBase):
    __tablename__ = 'labels'

    id = Column(Integer, primary_key=True)

    file_path = Column('file_path', String(256), nullable=False, index=True, unique=False)
    file_name = Column('file_name', String(256), nullable=False, index=True, unique=False)
    project_name = Column('project_name', String(256), nullable=False, index=True, unique=False)

    target_class = Column('target_class', Integer, nullable=True, index=False, unique=False)
    submitted_by = Column('submitted_by', String(128), nullable=True, index=False, unique=False)
    submitted_at = Column('submitted_at', DateTime, nullable=False, server_default=utcnow())

    xmin = Column('target_xmin', Integer, nullable=True, index=False, unique=False)
    xmax = Column('target_xmax', Integer, nullable=True, index=False, unique=False)

    ymin = Column('target_ymin', Integer, nullable=True, index=False, unique=False)
    ymax = Column('target_ymax', Integer, nullable=True, index=False, unique=False)
