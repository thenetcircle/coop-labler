import gnenv
from gnenv.environ import GNEnvironment

from labler.api import IClaimer, IImager
from labler.db import IDatabase
from labler.data import IDataHandler


class LablerEnvironment(GNEnvironment):
    db: IDatabase = None
    claimer: IClaimer = None
    imager: IImager = None
    data_handler: IDataHandler = None

    def __init__(self, gn_env: GNEnvironment):
        super(LablerEnvironment, self).__init__(root_path=None, config=gn_env.config)


env: LablerEnvironment = None


# create the environment, will load the secrets file and populate the config
def create_env(gn_environment, quiet=False):
    from labler.api.claimer import Claimer
    from labler.api.imager import Imager
    from labler.data.handler import DataHandler
    from labler.db.rdmbs.manager import DatabaseRdbms

    config_path = '/etc/labler/'
    gn_env = gnenv.environ.create_env(
        config_path=config_path,
        gn_environment=gn_environment,
        secrets_path=config_path + 'secrets/',
        quiet=quiet
    )
    lb_env = LablerEnvironment(gn_env)
    lb_env.db = DatabaseRdbms(lb_env)
    lb_env.claimer = Claimer(lb_env)
    lb_env.imager = Imager(lb_env)
    lb_env.data_handler = DataHandler(lb_env)

    return lb_env
