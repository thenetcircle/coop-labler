import getopt
import sys
import os

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
    'verbose': True,
    'classes': None,
    'project_type': None,
    'directory': None,
}


class AppSession:
    def read_argv(self, argv):
        from labler import errors

        try:
            opts, argv = getopt.gnu_getopt(
                argv,
                'pVsvhc:t:d:',
                [
                    'pretend',
                    'version',
                    'silent',
                    'verbose',
                    'help',
                    'classes=',
                    'type=',
                    'directory=',
                ]
            )

            return opts, argv
        except getopt.GetoptError as e:
            raise errors.FatalException(f'unknown option {e.opt}')

    def __init__(self, argv):
        from labler.config import ProjectTypes
        from labler import errors
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

            elif opt in ('-d', '--directory'):
                if not os.path.exists(arg):
                    raise errors.FatalException(f'data directory "{arg}" does not exist')

                self.lambdaenv.directory = arg

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
                self.lambdaenv.project_type = arg if len(arg) > 1 else ProjectTypes.get(arg)

                if arg not in ProjectTypes.shorts() and arg not in ProjectTypes.longs():
                    raise errors.FatalException(
                        'unknown project type "{arg}", must be in [{project_types}] or [{project_types_short}]'.format(
                            arg=arg,
                            project_types=', '.join(ProjectTypes.values()),
                            project_types_short=', '.join(ProjectTypes.keys()))
                    )

            else:
                self.printer.error(f'unknown option: {opt}')

        self.args = args
        self.configured = True


def usage():
    from labler.config import ProjectTypes

    return """
    labler - Cooperative labeling of images
    Usage: labler [option(s)] <operation [parameters]>

        Options:
            --version (or -V):
                Echo version information and exit.
            --pretend (or -p):
                Just pretend to do actions, telling what you would do.
            --silent (or -s):
                Suppresses what is defined in 'suppressed'.
            --verbose (or -v):
                Makes labler more talkative.
            --classes (or -c):
                Specify how many classes a project has.
            --dir (or -d):
                Specify where the training data exists for this project (local fs only as of now) 
            --type (or -t):
                Specify the type of project, one of [{project_types}]

        Operations:
            create <project name>
                Create a new project
            add <project name>
                Add training data to project
            update <project name>
                Update an existing project
            claims <project name>
                List claims for a project
            labels <project name>
                List labels for a project
            projects
                List information about all projects
            help
                Show the help text and exit.
    """.format(
        project_types=', '.join([f'{long} ({short})' for short, long in ProjectTypes.to_dict().items()])
    )
