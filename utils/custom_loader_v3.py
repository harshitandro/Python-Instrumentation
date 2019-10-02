import sys
from importlib.machinery import PathFinder, ModuleSpec, SourceFileLoader

from constants.hooks import USER_CALLABLES_TO_HOOK
from utils.callbacks import start_callback, end_callback, error_callback
from utils.instrumentation import instrument


class CustomFinder(PathFinder):
    def __init__(self, module_name):
        self.module_name = module_name

    def find_spec(self, fullname, path=None, target=None):
        if fullname == self.module_name:
            spec = super().find_spec(fullname, path, target)
            loader = CustomLoader(fullname, spec.origin)
            return ModuleSpec(fullname, loader)


class CustomLoader(SourceFileLoader):
    def exec_module(self, module):
        super().exec_module(module)
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
                        setattr(cls, func_str, instrument(func, start_callback, end_callback, error_callback, isMethod=True))
                    else:
                        func = getattr(module, func_str)
                        setattr(module, func_str,
                                instrument(func, start_callback, end_callback, error_callback))
        except:
            print("Error caught : {}".format(sys.exc_info()))
        return module


def enable_module_hook_on_load():
    """This will enable the instrumentation of user modules upon load."""
    sys.meta_path.insert(0, CustomFinder('module'))
    sys.path_importer_cache.clear()


def disable_module_hook_on_load():
    """Counter function of enable_module_hook_on_load"""
    sys.meta_path = sys.meta_path[1:]
    sys.path_importer_cache.clear()
