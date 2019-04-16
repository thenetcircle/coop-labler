import getopt

import sys

from labler.cli import errors
from labler.config import ProjectTypesShort
from labler.config import ProjectTypes

version_str = 'Coop-Labler version {}'


class LambdaEnviron(dict):
    def __init__(self, d=None):
        super().__init__(d)

    def __getattr__(self, item):
        if item not in self:
            raise KeyError(f'no key {item} in LambdaEnvironment')
        return self.get(item)


LambdaTemplate = {
    'suppressed': set(),
    'pretend': False,
    'silent': False,
    'verbose': True
}


class AppSession:
    def read_argv(self, argv):
        try:
            opts, argv = getopt.gnu_getopt(
                argv,
                'pVsvhc:t:',
                [
                    'pretend',
                    'version',
                    'silent',
                    'verbose',
                    'help',
                    'classes=',
                    'type='
                ]
            )

            return opts, argv
        except getopt.GetoptError as e:
            raise errors.FatalException(f'unknown option {e.opt}')

    def __init__(self, argv):
        from labler.cli import printer

        self.configured = False
        self.args = None
        self.printer = printer.AppPrinter(self)
        self.lambdaenv = LambdaEnviron(LambdaTemplate)

        opts, args = self.read_argv(argv)

        for opt, arg in opts:
            if opt in ('-p', '--pretend'):
                self.lambdaenv.pretend = True

            elif opt in ('-V', '--version'):
                import pkg_resources
                version = pkg_resources.require('labler')[0].version
                print(version_str.format(version))
                return

            elif opt in ('-s', '--silent'):
                self.lambdaenv.silent = True
                self.lambdaenv.suppressed = {'all'}

            elif opt in ('-v', '--verbose'):
                self.lambdaenv.verbose = True
                self.lambdaenv.suppressed = set()

            elif opt in ('-c', '--classes'):
                try:
                    self.lambdaenv.classes = int(arg)
                except ValueError:
                    raise errors.FatalException('invalid argument for option "classes", need an integer value')

                if self.lambdaenv.classes < 1:
                    raise errors.FatalException(f'need at least one class, got "{arg}"')

            elif opt in ('-h', '--help'):
                print(usage())
                sys.exit(0)

            elif opt in ('-t', '--type'):
                self.lambdaenv.project_type = arg

                if arg not in ProjectTypes and arg not in ProjectTypesShort:
                    raise errors.FatalException(
                        'unknown project type "{arg}", must be in [{project_types}] or [{project_types_short}]'.format(
                            arg=arg,
                            project_types=', '.join(ProjectTypes),
                            project_types_short=', '.join(ProjectTypesShort))
                    )

            else:
                self.printer.error(f'unknown option: {opt}')

        self.args = args
        self.configured = True


def usage():
    return """
    labler - Cooperative labeling of images
    Usage: labler [option(s)] <operation [parameters]>

        Options:
            --version (or -V):
                Echo version information and exit.
            --pretend (or -p):
                Just pretend to do actions, telling what you would do.
            --silent (or -s):
                Supresses what is defined in 'suppressed'.
            --verbose (or -v):
                Makes labler more talkative.
            --classes (or -c):
                Specify how many classes a project has.
            --type (or -t):
                Specify the type of project, one of [{project_types}]

        Operations:
            create [name]
                Create a new project
            help
                Show the help text and exit.
    """.format(
        project_types=', '.join([f'{long} ({short})' for long, short in zip(ProjectTypes, ProjectTypesShort)])
    )
