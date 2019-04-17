from sqlalchemy import Column, Integer, String, Boolean, text

from labler.db import LabelRepr
from labler.db.rdmbs import DeclarativeBase
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime

from labler.db.rdmbs.repr import ClaimRepr, ExampleRepr, ProjectRepr


class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


@compiles(utcnow, 'mssql')
def ms_utcnow(element, compiler, **kw):
    return "GETUTCDATE()"


class Examples(DeclarativeBase):
    __tablename__ = 'examples'

    id = Column(Integer, primary_key=True)

    file_path = Column('file_path', String(256), nullable=False, index=True, unique=False)
    file_name = Column('file_name', String(256), nullable=False, index=True, unique=False)
    project_name = Column('project_name', String(256), nullable=False, index=True, unique=False)

    width = Column('width', Integer, nullable=False)
    height = Column('height', Integer, nullable=False)

    def to_repr(self) -> ExampleRepr:
        return ExampleRepr(
            _id=self.id,
            file_path=self.file_path,
            file_name=self.file_name,
            project_name=self.project_name,
            width=self.width,
            height=self.height
        )


class Projects(DeclarativeBase):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)

    project_name = Column('name', String(128), nullable=False, index=True, unique=True)
    directory = Column('directory', String(128), nullable=True, index=False, unique=False)
    created = Column('created', DateTime, nullable=False, server_default=utcnow())
    project_type = Column('project_type', String(32), nullable=False, server_default='classification')
    classes = Column('classes', Integer, nullable=False, server_default=text('2'))
    finished = Column('finished', Boolean, nullable=False, server_default=text('false'))

    def to_repr(self) -> ProjectRepr:
        return ProjectRepr(
            _id=self.id,
            project_name=self.project_name,
            directory=self.directory,
            created=self.created,
            project_type=self.project_type,
            classes=self.classes,
            finished=self.finished
        )


class Claims(DeclarativeBase):
    __tablename__ = 'claims'

    id = Column(Integer, primary_key=True)

    file_path = Column('file_path', String(256), nullable=False, index=True, unique=False)
    file_name = Column('file_name', String(256), nullable=False, index=True, unique=False)

    project_name = Column('project_name', String(256), nullable=False, index=True, unique=False)
    claimed_at = Column('claimed_at', DateTime, nullable=False, server_default=utcnow())
    claimed_by = Column('claimed_by', String(128), nullable=False, index=True, unique=False)

    status = Column('status', String(32), nullable=False, index=True, unique=False, server_default='waiting')

    def to_repr(self):
        return ClaimRepr(
            _id=self.id,
            file_path=self.file_path,
            file_name=self.file_name,
            project_name=self.project_name,
            claimed_at=self.claimed_at,
            claimed_by=self.claimed_by,
            status=self.status
        )


class Labels(DeclarativeBase):
    __tablename__ = 'labels'

    id = Column(Integer, primary_key=True)

    file_path = Column('file_path', String(256), nullable=False, index=True, unique=False)
    file_name = Column('file_name', String(256), nullable=False, index=True, unique=False)
    project_name = Column('project_name', String(256), nullable=False, index=True, unique=False)

    target_class = Column('target_class', Integer, nullable=True, index=False, unique=False)
    submitted_by = Column('submitted_by', String(128), nullable=True, index=False, unique=False)
    submitted_at = Column('submitted_at', DateTime, nullable=False, server_default=utcnow())

    status = Column('status', String(32), nullable=False, index=True, unique=False, server_default='waiting')

    xmin = Column('target_xmin', Integer, nullable=True, index=False, unique=False)
    xmax = Column('target_xmax', Integer, nullable=True, index=False, unique=False)

    ymin = Column('target_ymin', Integer, nullable=True, index=False, unique=False)
    ymax = Column('target_ymax', Integer, nullable=True, index=False, unique=False)

    def to_repr(self):
        return LabelRepr(
            _id=self.id,
            file_path=self.file_path,
            file_name=self.file_name,
            project_name=self.project_name,
            target_class=self.target_class,
            submitted_by=self.submitted_by,
            submitted_at=self.submitted_at,
            status=self.status,
            xmin=self.xmin,
            xmax=self.xmax,
            ymin=self.ymin,
            ymax=self.ymax
        )
