import threading

def start_callback(source, handler_callback, *args, **kwargs):
    """Callback which is called before the start of any instrumented method/function.
    The args to this callback are the args passed to the instrumented method/function."""
    threadID = threading.current_thread().ident

    if handler_callback is not None:
        handler_callback(source, threadID, *args, **kwargs)
    else:
        # TODO: Remove this to make the hook look effectively absent when handler set to None
        print(
            "StartCallback for {} :: threadID : {} :: args : {} :: kwargs : {} :: handler : {}".format(source, threadID,
                                                                                                       args, kwargs,
                                                                                                       handler_callback))

def end_callback(source, handler_callback, *ret_val):
    """Callback which is called after the end of any instrumented method/function.
    The args to this callback is the return value of the instrumented method/function"""
    threadID = threading.current_thread().ident
    if handler_callback is not None:
        handler_callback(source, threadID, *ret_val)
    else:
        # TODO: Remove this to make the hook look effectively absent when handler set to None
        print("EndCallback for {} :: return val : {} :: threadID : {} :: handler : {}".format(source, ret_val, threadID,
                                                                                              handler_callback))


def error_callback(source, handler_callback, type, value, traceback):
    """Callback which is called after the end of any instrumented method/function if it raises any unhandled error.
    The args to this callback are the details about the raised error"""
    threadID = threading.current_thread().ident

    if handler_callback is not None:
        handler_callback(source, threadID, type, value, traceback)
    else:
        # TODO: Remove this to make the hook look effectively absent when handler set to None
        print(
            "ErrorCallback for {} :: threadID : {} :: type : {} :: value : {} :: traceback : {} :: handler : {}".format(
                source, threadID, type, value, traceback, handler_callback))