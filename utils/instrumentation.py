import sys
import traceback
from importlib import import_module

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

    # Invoking hooking logic at time of module loading
    try:
        if module.__name__ in list(HOOK_MAP.keys()):
            for func_string in HOOK_MAP[module.__name__]:
                source_string = module.__name__ + "." + func_string
                cls = None
                func_str = func_string
                if func_str.find(".") != -1:
                    func_str_parts = func_str.split(".")
                    for part_i in range(len(func_str_parts) - 1):
                        class_str = func_str_parts[part_i]
                        func_str = func_str_parts[part_i + 1]
                        if cls is None:
                            cls = getattr(module, class_str)
                        else:
                            cls = getattr(cls, class_str)
                if cls is not None:
                    func = getattr(cls, func_str)
                    setattr(cls, func_str,
                            instrument(func, source_string, start_callback, end_callback,
                                       error_callback, isMethod=True))
                else:
                    func = getattr(module, func_str)
                    setattr(module, func_str,
                            instrument(func, source_string, start_callback, end_callback,
                                       error_callback))
    except:
        print("Error caught in hooking : {}".format(sys.exc_info()))
        traceback.print_exc()
    return module
