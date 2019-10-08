from __future__ import print_function

import sys

from utils.instrumentation import apply_hooks

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
    module = apply_hooks(module, is_system_hook=False)
    return module


def custom_reload(*args, **kwargs):
    module = old_reload(*args, **kwargs)
    module = apply_hooks(module, is_system_hook=False)
    return module


def enable_module_hook_on_load():
    """This will enable the instrumentation of user modules upon load."""
    builtin.__import__ = custom_import
    imp.reload = custom_reload
