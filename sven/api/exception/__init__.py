
class BaseError(Exception):
    """
    base API exception
    """

    def __init__(self, error, message):
        self.error = error
        self.message = message
        super().__init__(message)


class APIBaseError(BaseError):
    """
    base API exception
    """
    def __init__(self, error, data='', message=''):
        self.data = data
        super().__init__(error, message)


class PathError(BaseError):
    """
    base path exception
    """
    def __init__(self, error, message):
        super().__init__(error, message=message)
