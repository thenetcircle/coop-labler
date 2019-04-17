import gnenv
from gnenv.environ import GNEnvironment

from labler.api import IClaimer
from labler.db import IDatabase
from labler.db.rdmbs.manager import DatabaseRdbms


class LablerEnvironment(GNEnvironment):
    db: IDatabase = None
    claimer: IClaimer = None

    def __init__(self, gn_env: GNEnvironment):
        super(LablerEnvironment, self).__init__(root_path=None, config=gn_env.config)


env: LablerEnvironment = None


# create the environment, will load the secrets file and populate the config
def create_env(gn_environment, quiet=False):
    gn_env = gnenv.environ.create_env(gn_environment=gn_environment, quiet=quiet)
    lb_env = LablerEnvironment(gn_env)
    lb_env.db = DatabaseRdbms(lb_env)

    return lb_env
