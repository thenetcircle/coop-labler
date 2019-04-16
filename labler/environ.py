import gnenv

from labler.db.rdmbs.manager import DatabaseRdbms

# create the environment, will load the secrets file and populate the config
env = gnenv.environ.create_env(gn_environment='local', quiet=True)
env.db = DatabaseRdbms(env)
