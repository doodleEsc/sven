from sven.api.exception import PathError


class PathNotFoundError(PathError):
    def __init__(self, message):
        super().__init__('path:NotFound', message=message)
