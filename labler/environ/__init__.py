import gnenv

from labler.db.rdmbs.manager import DatabaseRdbms

env = None


# create the environment, will load the secrets file and populate the config
def create_env(gn_environment, quiet=False):
    gn_env = gnenv.environ.create_env(gn_environment=gn_environment, quiet=quiet)
    gn_env.db = DatabaseRdbms(gn_env)
    return gn_env
