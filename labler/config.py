from enum import Enum


class ErrorCodes(Enum):
    OK = 200
    UNKNOWN_ERROR = 250


class ConfigKeys(object):
    LOG_LEVEL = 'log_level'
    LOG_FORMAT = 'log_format'
    DEBUG = 'debug'
    TESTING = 'testing'
    SECRET_KEY = 'secret'

    DRIVER = 'driver'
    HOST = 'host'
    DSN = 'dsn'
    TYPE = 'type'
    PORT = 'port'
    PASSWORD = 'password'
    USER = 'username'
    NAME = 'name'
    HOSTS = 'hosts'
    POOL_SIZE = 'pool_size'
    DATABASE = 'database'
    DB = 'db'

    # will be overwritten even if specified in config file
    ENVIRONMENT = '_environment'
    VERSION = '_version'

    DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)-18s - %(levelname)-7s - %(message)s"
    DEFAULT_DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
    DEFAULT_LOG_LEVEL = 'INFO'


class ProjectTypes(Enum):
    CLASSIFICATION = 'classification'
    LOCALIZATION = 'localization'
    DETECTION = 'detection'
    SEGMENTATION = 'segmentation'

    @staticmethod
    def short(project_type):
        return project_type.value[0]

    @staticmethod
    def shorts():
        return [pt.value[0] for pt in ProjectTypes]

    @staticmethod
    def longs():
        return [pt.value for pt in ProjectTypes]

    @staticmethod
    def to_dict():
        return {pt.value[0]: pt.value for pt in ProjectTypes}
