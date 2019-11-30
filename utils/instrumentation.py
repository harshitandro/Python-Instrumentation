import sys
from importlib import import_module

from constants.hooks import BUILTIN_CALLABLES_TO_HOOK, USER_CALLABLES_TO_HOOK, INSTRUMENTATION_DRIVER_PATH
from utils.callbacks.base_callbacks import start_callback, end_callback, error_callback



def instrument(func, source_string, startCallback, endCallback, errorCallback,
               processing_callback=None, ret_processing_callback=None, err_processing_callback=None):
    """This function is used to instrument the given method/function 'func'."""
    old_func = func

    def new_func(*args, **kwargs):
        if source_string == "flask.app.Flask.dispatch_request":
            pass
            # import inspect
            # print(getattr(inspect.currentframe().f_globals, "_request_ctx_stack".top.request)
        if source_string == "subprocess.Popen.__init__" and "python" in args[1][0]:
            new_args = list(args[1])
            new_args.insert(1, INSTRUMENTATION_DRIVER_PATH)
            args = list(args)
            args[1] = tuple(new_args)
            args = list(args)
        startCallback(source_string, processing_callback, *args, **kwargs)
        try:
            ret = old_func(*args, **kwargs)
        except:
            errorCallback(source_string, err_processing_callback, *sys.exc_info())
            # raise so that the user code can handle the thrown error
            raise
        endCallback(source_string, ret_processing_callback, ret)
        return ret

    print("Hooked API : {}".format(source_string))
    return new_func


def instrument_system_api():
    """This will instrument the core python's methods/functions."""
    for module_to_hook in BUILTIN_CALLABLES_TO_HOOK:
        module_str = module_to_hook["module"]
        try:
            module = import_module(module_str)
            apply_hooks(module, is_system_hook=True)
        except:
            # print("Error caught in import hook : {}".format(sys.exc_info()))
            # traceback.print_exc()
            pass


def apply_hooks(module, is_system_hook=False):
    HOOK_LIST= {}
    if is_system_hook:
        HOOK_LIST = BUILTIN_CALLABLES_TO_HOOK
    else:
        HOOK_LIST = USER_CALLABLES_TO_HOOK
    try:
        for hook_element in HOOK_LIST:
            if module.__name__ == hook_element['module']:
                print(hook_element)
                processing_callback = hook_element['callback_handler']
                err_processing_callback = hook_element['callback_err_handler']
                ret_processing_callback = hook_element['callback_ret_handler']
                callable_str = hook_element['callable']
                source_string = module.__name__ + "." + callable_str
                callable_str_parts = callable_str.split(".")
                func_str = callable_str_parts[-1]
                mod = module

                for part in callable_str_parts[:-1]:
                    mod = getattr(mod, part)

                func = getattr(mod, func_str)

                setattr(mod, func_str, instrument(func, source_string, start_callback, end_callback, error_callback,
                                                  processing_callback=processing_callback,
                                                  ret_processing_callback=ret_processing_callback,
                                                  err_processing_callback=err_processing_callback))
    except:
        print("Error caught in hooking : {}".format(sys.exc_info()))
        # traceback.print_exc()
    return module
