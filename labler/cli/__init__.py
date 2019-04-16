from labler.cli import opts
from labler.cli import op
from labler.cli import errors
from labler.cli.errors import FatalException
from labler.cli.opts import AppSession
from labler.environ import env

import sys
import traceback


def op_create(app: AppSession, args):
    if len(args) == 0:
        raise errors.FatalException('no name specified when creating project')

    name = args[0]
    if env.db.project_exists(name):
        raise FatalException(f'project already exists with name {name}')

    if app.lambdaenv.pretend:
        app.printer.notice(f'would create new project called {name}')
    else:
        app.printer.action(f'creating project: {name}')
        env.db.create_project(name, app)


def main(app):
    if len(app.args) < 1:
        raise errors.FatalException('To few arguments')

    if app.args[0] in 'help':
        print(opts.usage())
        return 0

    elif app.args[0] == 'create':
        op.operate(app, op_create)

    return 0


def entrypoint():
    try:
        app = opts.AppSession(sys.argv[1:])
    except errors.FatalException as e:
        print(str(e))
        sys.exit(1)
    except Exception as e:
        print(f'error creating app session: {str(e)}')
        print(traceback.format_exc())
        sys.exit(1)

    if not app.configured:
        sys.exit(1)

    try:
        main(app)
    except errors.FatalException as e:
        print(f'error: {str(e)}')
        sys.exit(1)

    except SystemExit as e:  # interrupts and such
        sys.exit(e)

    except Exception as e:
        app.printer.error((str(e)))
        print(traceback.format_exc())
        sys.exit(1)

    sys.exit(0)
