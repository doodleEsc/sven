def import_module(module_str):
    index = module_str.rfind('.')
    try:
        if index == -1:
            module = __import__(module_str, globals(), locals())
        else:
            name = module_str[index+1:]
            module = getattr(__import__(module_str[:index], globals(), locals(), [name]), name)
        return module
    except (ImportError, AttributeError):
        raise ImportError('Module %s can not be found' % module_str)


def import_function(full_path):
    index = full_path.rfind('.')
    try:
        name = full_path[index+1:]
        func = getattr(__import__(full_path[:index], globals(), locals(), [name]), name)
        return func
    except (ImportError, AttributeError):
        raise ImportError('function %s cannot be found' % full_path)


