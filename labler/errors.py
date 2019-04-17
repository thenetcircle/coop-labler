class WarningException(Exception):
    def __init__(self,string):
        Exception.__init__(self, string)


class FatalException(Exception):
    def __init__(self, string):
        Exception.__init__(self, string)


class LablerException(Exception):
    def __init__(self, string):
        Exception.__init__(self, string)
