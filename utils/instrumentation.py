import sys
import traceback
from importlib import import_module
from inspect import ismethod

from constants.hooks import BUILTIN_CALLABLES_TO_HOOK, USER_CALLABLES_TO_HOOK
from utils.callbacks import start_callback, end_callback, error_callback


def instrument(func, source_string, startCallback, endCallback, errorCallback, isMethod=False):
    """This function is used to instrument the given method/function 'func'."""
    old_func = func

    def new_func(*args, **kwargs):
        startCallback(source_string, *args, **kwargs)
        try:
            ret = old_func(*args, **kwargs)
        except:
            errorCallback(source_string, *sys.exc_info())
            # raise so that the user code can handle the thrown error
            raise
        endCallback(source_string, ret)
        return ret

    print("Hooked API : {}".format(source_string))
    return new_func


def instrument_system_api():
    """This will instrument the core python's methods/functions."""
    for module_str in BUILTIN_CALLABLES_TO_HOOK.keys():
        try:
            module = import_module(module_str)
            apply_hooks(module, is_system_hook=True)
        except:
            # print("Error caught in import hook : {}".format(sys.exc_info()))
            # traceback.print_exc()
            pass


def apply_hooks(module, is_system_hook=False):
    HOOK_MAP= {}
    if is_system_hook:
        HOOK_MAP = BUILTIN_CALLABLES_TO_HOOK
    else:
        HOOK_MAP = USER_CALLABLES_TO_HOOK
    try:
        if module.__name__ in list(HOOK_MAP.keys()):
            for callable_str in HOOK_MAP[module.__name__]:
                source_string = module.__name__ + "." + callable_str
                callable_str_parts = callable_str.split(".")
                func_str = callable_str_parts[-1]
                mod = module

                for part in callable_str_parts[:-1]:
                    mod = getattr(mod, part)

                func = getattr(mod, func_str)

                setattr(mod, func_str, instrument(func, source_string, start_callback, end_callback, error_callback, isMethod= ismethod(func)))
    except:
        print("Error caught in hooking : {}".format(sys.exc_info()))
        traceback.print_exc()
    return module
