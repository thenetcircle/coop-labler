import datetime

from labler.config import ConfigKeys


class ExampleFields(object):
    ID = 'id'
    FILE_PATH = 'file_path'
    FILE_NAME = 'file_name'
    DISABLED = 'disabled'
    PROJECT_NAME = 'project_name'
    WIDTH = 'width'
    HEIGHT = 'height'


class ExampleRepr(object):
    def __init__(
            self,
            _id: int = None,
            file_path: str = None,
            file_name: str = None,
            disabled: bool = None,
            project_name: str = None,
            width: int = None,
            height: int = None,
    ):
        self.id = _id
        self.file_path = file_path
        self.file_name = file_name
        self.disabled = disabled
        self.project_name = project_name
        self.width = width
        self.height = height

    def to_dict(self):
        return {
            ExampleFields.ID: self.id or '',
            ExampleFields.FILE_PATH: self.file_path or '',
            ExampleFields.FILE_NAME: self.file_name or '',
            ExampleFields.DISABLED: self.disabled or '',
            ExampleFields.PROJECT_NAME: self.project_name or '',
            ExampleFields.WIDTH: self.width or '',
            ExampleFields.HEIGHT: self.height or '',
        }


class ProjectFields(object):
    ID = 'id'
    PROJECT_NAME = 'project_name'
    DIRECTORY = 'directory'
    CREATED = 'created'
    PROJECT_TYPE = 'project_type'
    CLASSES = 'classes'
    FINISHED = 'finished'


class ProjectRepr(object):
    def __init__(
            self,
            _id: int = None,
            project_name: str = None,
            directory: str = None,
            created: datetime = None,
            project_type: str = None,
            classes: int = None,
            finished: bool = None
    ):
        self.id = _id

        self.project_name = project_name
        self.directory = directory
        self.created = created
        self.project_type = project_type
        self.classes = classes
        self.finished = finished

    def to_dict(self):
        created = None
        if self.created is not None:
            created = self.created.strftime(ConfigKeys.DEFAULT_DATE_FORMAT)

        return {
            ProjectFields.ID: self.id or '',
            ProjectFields.PROJECT_NAME: self.project_name or '',
            ProjectFields.DIRECTORY: self.directory or '',
            ProjectFields.CREATED: created or '',
            ProjectFields.PROJECT_TYPE: self.project_type or '',
            ProjectFields.CLASSES: self.classes or '',
            ProjectFields.FINISHED: self.finished or '',
        }


class ClaimFields(object):
    ID = 'id'
    FILE_PATH = 'file_path'
    FILE_NAME = 'file_name'
    PROJECT_NAME = 'project_name'
    CLAIMED_AT = 'claimed_at'
    CLAIMED_BY = 'claimed_by'
    STATUS = 'status'


class ClaimStatuses(object):
    WAITING = 'waiting'
    CANCELLED = 'cancelled'
    FINISHED = 'finished'
    INVALID = 'invalid'


class ClaimRepr(object):
    def __init__(
            self,
            _id: int = None,
            file_path: str = None,
            file_name: str = None,
            project_name: str = None,
            claimed_at: datetime = None,
            claimed_by: str = None,
            status: str = None
    ):
        self.id = _id

        self.file_path = file_path
        self.file_name = file_name

        self.project_name = project_name
        self.claimed_at = claimed_at
        self.claimed_by = claimed_by

        self.status = status

    def to_dict(self):
        claimed_at = None
        if self.claimed_at is not None:
            claimed_at = self.claimed_at.strftime(ConfigKeys.DEFAULT_DATE_FORMAT)

        return {
            ClaimFields.ID: self.id,
            ClaimFields.FILE_PATH: self.file_path,
            ClaimFields.FILE_NAME: self.file_name,
            ClaimFields.PROJECT_NAME: self.project_name,
            ClaimFields.CLAIMED_AT: claimed_at,
            ClaimFields.CLAIMED_BY: self.claimed_by,
            ClaimFields.STATUS: self.status
        }


class LabelFields(object):
    ID = 'id'
    FILE_PATH = 'file_path'
    FILE_NAME = 'file_name'
    PROJECT_NAME = 'project_name'
    TARGET_CLASS = 'target_class'
    SUBMITTED_BY = 'submitted_by'
    SUBMITTED_AT = 'submitted_at'
    STATUS = 'status'
    XMIN = 'xmin'
    XMAX = 'xmax'
    YMIN = 'ymin'
    YMAX = 'ymax'


class LabelStatuses(object):
    WAITING = 'waiting'
    FINISHED = 'finished'
    REMOVED = 'removed'


class LabelRepr(object):
    def __init__(
            self,
            _id: int = None,
            file_path: str = None,
            file_name: str = None,
            project_name: str = None,
            target_class: str = None,
            submitted_by: str = None,
            submitted_at: datetime = None,
            status: str = None,
            xmin: int = None,
            xmax: int = None,
            ymin: int = None,
            ymax: int = None
    ):
        self.id = _id

        self.file_path = file_path
        self.file_name = file_name
        self.project_name = project_name

        self.target_class = target_class
        self.submitted_by = submitted_by
        self.submitted_at: datetime = submitted_at

        self.status = status

        self.xmin = xmin
        self.xmax = xmax

        self.ymin = ymin
        self.ymax = ymax

    def to_dict(self):
        submitted_at = None
        if self.submitted_at is not None:
            submitted_at = self.submitted_at.strftime(ConfigKeys.DEFAULT_DATE_FORMAT)

        return {
            LabelFields.ID: self.id or '',
            LabelFields.FILE_PATH: self.file_path or '',
            LabelFields.FILE_NAME: self.file_name or '',
            LabelFields.PROJECT_NAME: self.project_name or '',
            LabelFields.TARGET_CLASS: self.target_class or '',
            LabelFields.SUBMITTED_BY: self.submitted_by or '',
            LabelFields.SUBMITTED_AT: submitted_at or '',
            LabelFields.STATUS: self.status or '',
            LabelFields.XMIN: self.xmin or '',
            LabelFields.XMAX: self.xmax or '',
            LabelFields.YMIN: self.ymin or '',
            LabelFields.YMAX: self.ymax or ''
        }
