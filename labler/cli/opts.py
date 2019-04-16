import getopt

version_str = 'Coop-Labler version {}'


class LambdaEnviron(dict):
    def __init__(self, d=None):
        super(LambdaEnviron, self).__init__(d)

        if d is None:
            d = dict()
        self.__dict__.update(d)

    def __setattr__(self, key, val):
        self.__setitem__(key, val)

    def __getattr__(self, key):
        print(self.__dict__)
        if key in self.__dict__:
            self.__getitem__(key)
        raise Exception(f'No such key in lambda environ: {key}')

    def __hasattr__(self, key):
        return key in self


LambdaTemplate = {
    'suppressed': [],
    'pretend': False,
    'silent': False,
    'verbose': True
}


class AppSession:
    def read_argv(self, argv):
        try:
            opts, argv = getopt.gnu_getopt(
                argv,
                'pVsv',
                [
                    'pretend',
                    'version',
                    'silent',
                    'verbose'
                ]
            )

            return opts, argv
        except getopt.GetoptError as e:
            self.printer.error(f'unknown option: {e.opt}')
            return None, None

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

            elif opt in ('-v', '--verbose'):
                self.lambdaenv.verbose = True

            else:
                self.printer.error(f'unknown option: {opt}')

        self.args = args
        self.configured = True


def usage():
    return """
    labler - Cooperative labeling of images
    Usage: labler [option(s)] <operation>

        General:
            --version (or -V):
                Echo version information and exit.
        Options:
        syntax: *long-opt* (or *short-opt*) [*args*] '*conf-key*' (also *relevant*):
            --pretend (or -p) 'pretend':
                Just pretend to do actions, telling what you would do.
            --silent (or -s) 'silent':
                Supresses what is defined in 'suppressed'.
            --verbose (or -v) 'verbose':
                Makes musync more talkative.

        Operations:
            create [name]
                Create a new project
            help
                Show the help text and exit.
    """
