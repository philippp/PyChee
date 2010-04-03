class ControllerNotFound(Exception):
    def __init__(self, value=None):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)
