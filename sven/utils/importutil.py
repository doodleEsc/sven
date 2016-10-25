

def importmodule(module_str):
    index = module_str.rfind('.')
    if index == -1:
        module = __import__(module_str, globals(), locals())
    else:
        name = module_str[index+1:]
        module = getattr(__import__(module_str[:index], globals(), locals(), [name]), name)

    return module