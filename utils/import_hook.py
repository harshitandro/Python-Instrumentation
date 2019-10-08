from __future__ import print_function

import sys
import traceback

from constants.hooks import USER_CALLABLES_TO_HOOK
from utils.callbacks import start_callback, end_callback, error_callback
from utils.instrumentation import instrument

if sys.version_info[0] == 2:
    import __builtin__ as builtin
    import imp as imp
elif sys.version_info[0] == 3:
    import builtins as builtin
    import importlib as imp
else:
    print("Unsupported Python Major Version : {}".format(sys.version_info[0]), file=sys.stderr)
    exit(1)

old_imp = builtin.__import__
old_reload = imp.reload


def custom_import(*args, **kwargs):
    module = old_imp(*args, **kwargs)
    # Invoking hooking logic at time of module loading
    try:
        if module.__name__ in list(USER_CALLABLES_TO_HOOK.keys()):
            for func_string in USER_CALLABLES_TO_HOOK[module.__name__]:
                cls = None
                func_str = func_string
                if func_str.find(".") != -1:
                    func_str_parts = func_str.split(".")
                    for part_i in range(len(func_str_parts)-1):
                        class_str = func_str_parts[part_i]
                        func_str = func_str_parts[part_i+1]
                        if cls is None:
                            cls = getattr(module, class_str)
                        else:
                            cls = getattr(cls, class_str)
                if cls is not None:
                    func = getattr(cls, func_str)
                    setattr(cls, func_str,
                            instrument(func, start_callback, end_callback, error_callback, isMethod=True))
                else:
                    func = getattr(module, func_str)
                    setattr(module, func_str,
                            instrument(func, start_callback, end_callback, error_callback))
    except:
        print("Error caught in import hook : {}".format(sys.exc_info()))
        traceback.print_exc()
    return module


def custom_reload(*args, **kwargs):
    module = old_reload(*args, **kwargs)
    # Invoking hooking logic at time of module loading
    try:
        if module.__name__ in list(USER_CALLABLES_TO_HOOK.keys()):
            for func_string in USER_CALLABLES_TO_HOOK[module.__name__]:
                cls = None
                func_str = func_string
                if func_str.find(".") != -1:
                    class_str, func_str = func_str.split(".")
                    cls = getattr(module, class_str)
                if cls is not None:
                    func = getattr(cls, func_str)
                    setattr(cls, func_str,
                            instrument(func, start_callback, end_callback, error_callback, isMethod=True))
                else:
                    func = getattr(module, func_str)
                    setattr(module, func_str,
                            instrument(func, start_callback, end_callback, error_callback))
    except:
        print("Error caught : {}".format(sys.exc_info()))
    return module


def enable_module_hook_on_load():
    """This will enable the instrumentation of user modules upon load."""
    builtin.__import__ = custom_import
    imp.reload = custom_reload


# def disable_module_hook_on_load():
#     """Counter function of enable_module_hook_on_load"""
#     builtin.__import__ = old_imp
#     imp.reload = old_reload


def reload_modules():
    for mod in sys.modules.values():
        if mod is not None:
            print("Reloading module : {}".format(mod), file=sys.stderr)
            try:
                imp.reload(mod)
            except:
                print("Failed to reload module : {} : {}".format(mod, *sys.exc_info()), file=sys.stderr)
