import os
import sys
from importlib import invalidate_caches
from importlib._bootstrap_external import spec_from_file_location
from importlib.abc import MetaPathFinder, Loader

from constants.hooks import USER_CALLABLES_TO_HOOK
from utils.callbacks import start_callback, end_callback, error_callback
from utils.instrumentation import instrument


class CustomMetaFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if path is None or path == "":
            path = [os.getcwd()]  # top level import --
        if "." in fullname:
            parents, name = fullname.split(".")
        else:
            name = fullname
        for entry in path:
            if os.path.isdir(os.path.join(entry, name)):
                # this module has child modules
                filename = os.path.join(entry, name, "__init__.py")
                submodule_locations = [os.path.join(entry, name)]
            else:
                filename = os.path.join(entry, name + ".py")
                submodule_locations = None
            if not os.path.exists(filename):
                continue

            return spec_from_file_location(fullname, filename, loader=CustomLoader(filename),
                                           submodule_search_locations=submodule_locations)

        return None  # we don't know how to import this


class CustomLoader(Loader):
    def __init__(self, filename):
        self.filename = filename

    def create_module(self, spec):
        return None  # use default module creation semantics

    def exec_module(self, module):
        with open(self.filename) as f:
            data = f.read()
        exec(data, vars(module))

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
                        setattr(cls, func_str, instrument(func, start_callback, end_callback, error_callback))
                    else:
                        func = getattr(module, func_str)
                        setattr(module, func_str,
                                instrument(func, start_callback, end_callback, error_callback))
        except:
            print("Fata re : {}".format(sys.exc_info()))


def enable_module_hook_on_load():
    """This will enable the instrumentation of user modules upon load."""
    sys.meta_path.insert(0, CustomMetaFinder())
    sys.path_importer_cache.clear()
    invalidate_caches()


def disable_module_hook_on_load():
    """Counter function of enable_module_hook_on_load"""
    sys.meta_path = sys.meta_path[1:]
    sys.path_importer_cache.clear()
    invalidate_caches()