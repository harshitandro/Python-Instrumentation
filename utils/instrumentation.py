import sys
from importlib import import_module

from constants.hooks import BUILTIN_CALLABLES_TO_HOOK
from utils.callbacks import start_callback, end_callback, error_callback


def instrument(func, startCallback, endCallback, errorCallback, isMethod=False):
    """This function is used to instrument the given method/function 'func'."""
    old_func = func

    def new_func(*args, **kwargs):
        if isMethod:
            source = func.__module__ + "." + args[0].__class__.__name__ + "." + func.__name__
        else:
            source = func.__module__ + "." + func.__name__
        startCallback(source, *args, **kwargs)
        try:
            ret = old_func(*args, **kwargs)
        except:
            errorCallback(source, *sys.exc_info())
            # raise so that the user code can handle the thrown error
            raise
        endCallback(source, ret)
        return ret

    print("Hooked method : {} of {}".format(func.__name__, func.__module__))
    return new_func


def instrument_system_api():
    """This will instrument the core python's methods/functions."""
    for module_str in BUILTIN_CALLABLES_TO_HOOK.keys():
        try:
            module = import_module(module_str)
            for func_string in BUILTIN_CALLABLES_TO_HOOK[module_str]:
                cls = None
                func_str = func_string
                if func_str.find(".") != -1:
                    class_str, func_str = func_str.split(".")
                    cls = getattr(module, class_str)
                if cls is not None:
                    func = getattr(cls, func_str)
                    setattr(cls, func_str, instrument(func, start_callback, end_callback, error_callback, isMethod=True))
                else:
                    func = getattr(module, func_str)
                    setattr(module, func_str,
                            instrument(func, start_callback, end_callback, error_callback))
        except:
            pass