import threading


def start_callback(source, *args, **kwargs):
    """Callback which is called before the start of any instrumented method/function.
    The args to this callback are the args passed to the instrumented method/function."""
    print("StartCallback for {} :: threadID : {} :: args : {} :: kwargs : {}".format(source, threading.current_thread().ident, args, kwargs))


def end_callback(source, *ret_val):
    """Callback which is called after the end of any instrumented method/function.
    The args to this callback is the return value of the instrumented method/function"""
    print("EndCallback for {} :: return val : {} :: threadID : {}".format(source, ret_val, threading.current_thread().ident))


def error_callback(source, type, value, traceback):
    """Callback which is called after the end of any instrumented method/function if it raises any unhandled error.
    The args to this callback are the details about the raised error"""
    print("ErrorCallback for {} :: threadID : {} :: type : {} :: value : {} :: traceback : {}".format(source, threading.current_thread().ident, type, value, traceback))