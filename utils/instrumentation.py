import inspect
import sys
from importlib import import_module

from constants.hooks import BUILTIN_CALLABLES_TO_HOOK


def instrument(func, startCallback, endCallback, errorCallback):
    """This function is used to instrument the given method/function 'func'."""
    old_func = func
    spec = inspect.getfullargspec(func)
    args = spec.args
    source = "UNKNOWN"
    def new_func(*args,**kwargs):
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
        module = import_module(module_str)
        for func_string in BUILTIN_CALLABLES_TO_HOOK[module_str]:
            cls = None
            func_str = func_string
            if func_str.find(".") != -1:
                class_str, func_str = func_str.split(".")
                cls = getattr(module, class_str)
            if cls is not None:
                func = getattr(cls, func_str)
                setattr(cls, func_str, instrument(func, start_callback, end_callback, error_callback))
            else:
                func = getattr(module, func_str)
                setattr(module, func_str,
                        instrument(func, start_callback, end_callback, error_callback))


def start_callback(source, *args, **kwargs):
    """Callback which is called before the start of any instrumented method/function.
    The args to this callback are the args passed to the instrumented method/function."""
    print("StartCallback for {} :: args : {} :: kwargs : {}".format(source, args, kwargs))


def end_callback(source, *ret_val):
    """Callback which is called after the end of any instrumented method/function.
    The args to this callback is the return value of the instrumented method/function"""
    print("EndCallback for {} :: return val : {}".format(source, ret_val))


def error_callback(source, type, value, traceback):
    """Callback which is called after the end of any instrumented method/function if it raises any unhandled error.
    The args to this callback are the details about the raised error"""
    print("ErrorCallback for {} :: type : {} :: value : {} :: traceback : {}".format(source, type, value, traceback))
