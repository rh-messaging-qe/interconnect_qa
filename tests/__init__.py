import inspect

def get_func_name():
    return inspect.stack()[1][3]  # return caller's name
