"""
API exception
"""


class APIBaseError(Exception):
    """
    base API exception
    """

    def __init__(self, error, data='', message=''):
        """
        :param error:
        :param data:
        :param message:
        :return: Exception
        """
        super().__init__(message)
        self.error = error
        self.data = data
        self.message = message


class APIValueError(APIBaseError):
    '''
    Indicate the input value has error or invalid. The data specifies the error field of input form.
    '''
    def __init__(self, field, message=''):
        super(APIValueError, self).__init__('value:invalid', field, message)


class APIResourceNotFoundError(APIBaseError):
    '''
    Indicate the resource was not found. The data specifies the resource name.
    '''
    def __init__(self, field, message=''):
        super(APIResourceNotFoundError, self).__init__('value:notfound', field, message)


class APIPermissionError(APIBaseError):
    '''
    Indicate the api has no permission.
    '''
    def __init__(self, message=''):
        super(APIPermissionError, self).__init__('permission:forbidden', 'permission', message)
