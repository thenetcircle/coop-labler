import click
import gnenv

# create the environment, will load the secrets file and populate the config
env = gnenv.environ.create_env(
    gn_environment='local'
)


@click.command()
@click.option('', prompt='project name', help='The name of the project.')
def create(name):
    print(f'creating new project {name}')
