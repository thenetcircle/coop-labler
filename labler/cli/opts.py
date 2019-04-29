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
    'cores': 1,
    'verbose': True,
    'classes': None,
    'output': None,
    'project_type': None,
    'directory': None,
    'overwrite': False,
}


class AppSession:
    def read_argv(self, argv):
        from labler import errors

        try:
            opts, argv = getopt.gnu_getopt(
                argv,
                'pVsvohc:t:d:C:O:',
                [
                    'pretend',
                    'version',
                    'silent',
                    'verbose',
                    'overwrite',
                    'help',
                    'classes=',
                    'type=',
                    'dir=',
                    'cores=',
                    'output='
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

            elif opt in ('-d', '--dir'):
                if not os.path.exists(arg):
                    raise errors.FatalException(f'directory "{arg}" does not exist')

                self.lambdaenv.directory = arg

            elif opt in ('-v', '--verbose'):
                self.lambdaenv.verbose = True
                self.lambdaenv.suppressed = set()

            elif opt in ('-C', '--cores'):
                try:
                    cores = int(arg)
                except ValueError:
                    raise errors.FatalException(f'argument "{arg}" not a valid number of cores')
                if cores < 1:
                    cores = -1
                self.lambdaenv.cores = cores

            elif opt in ('-o', '--overwrite'):
                self.lambdaenv.overwrite = True

            elif opt in ('-O', '--output'):
                if not os.path.exists(arg):
                    raise errors.FatalException(f'output directory "{arg}" does not exist')

                self.lambdaenv.output = arg

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
            --overwrite (or -o):
                Overwrites output files when exporting if they already exist.
            --classes (or -c):
                Specify how many classes a project has.
            --cores (or -C):
                Number of CPU cores to use when processing training data.
            --dir (or -d):
                Specify where the training data exists for this project (local 
                fs only as of now), or where to export labels to. 
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
            export <project name>
                Export labels to files
            sync <project name>
                Sync all data directories fo a project, disabling examples of images no longer in the FS
            examples <project name>
                List examples for a project
            labels <project name>
                List labels for a project
            projects
                List information about all projects
            help
                Show the help text and exit.
    """.format(
        project_types=', '.join([f'{long} ({short})' for short, long in ProjectTypes.to_dict().items()])
    )
