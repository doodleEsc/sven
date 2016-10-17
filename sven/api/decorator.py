"""
decorator module

it contains some decorator for route info
"""

import functools


def get(path):
    """
    define @get('/path')
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper
    return decorator


def post(path):
    """
    define @post('/path')
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper
    return decorator

def delete(path):
    """
    define @delete('/path')
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper.__method__ = 'DELETE'
        wrapper.__route__ = path
        return wrapper
    return decorator


def put(path):
    """
    define @put('/path')
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper.__method__ = 'PUT'
        wrapper.__route__ = path
        return wrapper
    return decorator


