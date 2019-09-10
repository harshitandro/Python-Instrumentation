import inspect
import sys
from importlib import invalidate_caches

from utils.custom_loader import MyMetaFinder


def instrument(func, startCallback, endCallback, errorCallback):
    """This function is used to instrument the given method/function 'func'."""
    old_func = func
    spec = inspect.getfullargspec(func)
    args = spec.args

    def new_func(*args,**kwargs):
        startCallback(*args, **kwargs)
        try:
            ret = old_func(*args, **kwargs)
        except:
            errorCallback(*sys.exc_info())
            # raise so that the user code can handle the thrown error
            raise
            # TODO: remove this return. It was placed for testing
            # return
        endCallback(ret)
        return ret
    print("Hooked method : {} of {}".format(func.__name__, func.__module__))
    return new_func


def enable_module_hook_on_load():
    """This will enable the instrumentation of user modules upon load."""
    sys.meta_path.insert(0, MyMetaFinder())
    sys.path_importer_cache.clear()
    invalidate_caches()


def disable_module_hook_on_load():
    """Counter function of enable_module_hook_on_load"""
    sys.meta_path = sys.meta_path[1:]
    sys.path_importer_cache.clear()
    invalidate_caches()


def instrument_system_api():
    """This will instrument the core python's methods/functions."""
    raise NotImplementedError


def start_callback(*args, **kwargs):
    """Callback which is called before the start of any instrumented method/function.
    The args to this callback are the args passed to the instrumented method/function."""
    print("StartCallback :: args : {} :: kwargs : {}".format( args, kwargs))


def end_callback(*ret_val):
    """Callback which is called after the end of any instrumented method/function.
    The args to this callback is the return value of the instrumented method/function"""
    print("EndCallback : return val : ", ret_val)


def error_callback(type, value, traceback):
    """Callback which is called after the end of any instrumented method/function if it raises any unhandled error.
    The args to this callback are the details about the raised error"""
    print("ErrorCallback :: type : {} :: value : {} :: traceback : {}".format(type, value, traceback))
