import sys
import traceback

import labler
from labler import errors
from labler.cli import op
from labler.cli import opts
from labler.db.rdmbs.repr import ClaimFields, LabelFields
from labler.errors import FatalException
from labler.cli.opts import AppSession


def op_create(app: AppSession, args):
    from labler.environ import env

    if len(args) == 0:
        raise errors.FatalException('no project name specified')

    name = args[0]
    if env.db.project_exists(name):
        raise FatalException(f'project already exists with name {name}')

    if app.lambdaenv.pretend:
        app.printer.notice(f'would create new project called {name}')
    else:
        app.printer.action(f'creating project: {name}')
        env.db.create_project(name, app)


def op_update(app: AppSession, args):
    from labler.environ import env

    if len(args) == 0:
        raise errors.FatalException('no project name specified')

    name = args[0]
    if not env.db.project_exists(name):
        raise FatalException(f'no project exist with name {name}')

    if app.lambdaenv.pretend:
        app.printer.notice(f'would update existing project called {name}')
    else:
        app.printer.action(f'updating project: {name}')
        env.db.update_project(name, app)


def op_projects(app: AppSession, _):
    from labler.environ import env

    app.printer.action(f'listing projects')
    projects = env.db.get_projects()

    app.printer.blanknotice('')
    header = 'project name \tproject type \tclasses \tdirectory'.expandtabs(tabsize=20)
    app.printer.blanknotice(header)
    app.printer.blanknotice('-' * len(header))

    for project in projects:
        pname = project.project_name
        ptype = project.project_type
        pcls = project.classes
        pdir = project.directory

        app.printer.blanknotice(
            f'{pname} \t{ptype} \t{pcls} \t{pdir}'.expandtabs(tabsize=20))


def op_claims(app: AppSession, args):
    from labler.environ import env

    if len(args) == 0:
        raise errors.FatalException('no project name specified')

    name = args[0]
    if not env.db.project_exists(name):
        raise FatalException(f'no project exist with name {name}')

    app.printer.action(f'listing claims for project {name}')
    claims = env.db.get_claims(name)

    app.printer.blanknotice('')
    header = 'file name \tstatus \tclaimed by \tclaimed at'.expandtabs(tabsize=20)

    app.printer.blanknotice(header)
    app.printer.blanknotice('-' * len(header))

    for claim in claims:
        claim_json = claim.to_dict()
        claimed_at = claim_json[ClaimFields.CLAIMED_AT]
        app.printer.blanknotice(
            f'{claim.file_name} \t{claim.status} \t{claim.claimed_by} \t{claimed_at}'.expandtabs(tabsize=20))


def op_labels(app: AppSession, args):
    from labler.environ import env

    if len(args) == 0:
        raise errors.FatalException('no project name specified')

    name = args[0]
    if not env.db.project_exists(name):
        raise FatalException(f'no project exist with name {name}')

    app.printer.action(f'listing labels for project {name}')
    labels = env.db.get_labels(name)

    app.printer.blanknotice('')
    header = 'file name \txmin \txmax \tymin \tymax \tsubmitted by \tsubmitted at'.expandtabs(tabsize=18)

    app.printer.blanknotice(header)
    app.printer.blanknotice('-' * len(header))

    for label in labels:
        label_json = label.to_dict()
        submitted_at = label_json[LabelFields.SUBMITTED_AT]
        file_name = label.file_name
        if len(file_name) > 15:
            file_name = file_name[:12] + '...'

        row_1 = f'{file_name} \t{label.xmin} \t{label.xmax} \t{label.ymin} \t'
        row_2 = f'{label.ymax} \t{label.submitted_by} \t{submitted_at}'
        full_row = row_1 + row_2

        app.printer.blanknotice(full_row.expandtabs(tabsize=18))


def main(app):
    from labler.environ import create_env
    labler.environ.env = create_env('local', quiet=True)

    if len(app.args) < 1:
        print(opts.usage())
        return 0

    if app.args[0] in 'help':
        print(opts.usage())
        return 0

    elif app.args[0] == 'create':
        op.operate(app, op_create)

    elif app.args[0] == 'update':
        op.operate(app, op_update)

    elif app.args[0] == 'projects':
        op.operate(app, op_projects)

    elif app.args[0] == 'labels':
        op.operate(app, op_labels)

    elif app.args[0] == 'claims':
        op.operate(app, op_claims)

    else:
        app.printer.error(f'unknown operation {app.args[0]}')
        sys.exit(1)

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
