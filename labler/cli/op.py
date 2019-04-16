import traceback
import sys

from labler.cli import errors
from labler.cli.opts import AppSession


def operate(app: AppSession, call):
    try:
        call(app, app.args[1:])
    except errors.FatalException as e:
        app.printer.error(str(e))
        sys.exit(1)
    except Exception as e:
        app.printer.error(str(e))
        print(traceback.format_exc())
