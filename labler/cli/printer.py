from labler.cli.opts import AppSession


class AppPrinter(object):
    def __init__(self, app: AppSession):
        self.app = app

    def warning(self, text):
        if self.is_suppressed('warning') or self.is_suppressed('all'):
            return

        print(f'[!] {text}')

    def error(self, text):
        if self.is_suppressed('error') or self.is_suppressed('all'):
            return

        print(f'[e] {text}')

    def notice(self, text):
        if self.is_suppressed('notice') or self.is_suppressed('all'):
            return;

        print(f'[:] {text}')

    def blanknotice(self, text):
        if self.is_suppressed('notice') or self.is_suppressed('all'):
            return

        print(f'    {text}')

    def action(self, text):
        if self.is_suppressed('action') or self.is_suppressed('all'):
            return

        print(f'[-] {text}')

    def is_suppressed(self, print_type):
        if not self.app.configured:
            return False

        if self.app.lambdaenv.silent and print_type.lower() in self.app.lambdaenv.suppressed:
            return True

        return False
