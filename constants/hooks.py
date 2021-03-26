'''This contains maps of callable to hook. Key is the name of module & value is the list of
    submodule.functions or submodule.Class.method to be hooked.
'''
from utils.callbacks import error_processing_callbacks, return_processing_callbacks, processing_callbacks
from utils.callbacks.error_processing_callbacks import empty_err_processing_callback
from utils.callbacks.processing_callbacks import mysql_processing_callback, empty_processing_callback
from utils.callbacks.return_processing_callbacks import empty_ret_processing_callback


########################################################################################################################
# Place holders to be set by instrumentor
INSTRUMENTATION_DRIVER_PATH = ""
APPLIED_HOOK_SOURCE_STRING_LIST = list()
########################################################################################################################


BUILTIN_CALLABLES_TO_HOOK = [

    {
        "module": "subprocess",  # System Command hook
        "callable": "Popen.__init__",
        "callback_handler": empty_processing_callback,
        "callback_ret_handler": empty_ret_processing_callback,
        "callback_err_handler": empty_err_processing_callback,
    },
    {
        "module": "os",  # System Command hook
        "callable": "system",
        "callback_handler": empty_processing_callback,
        "callback_ret_handler": empty_ret_processing_callback,
        "callback_err_handler": empty_err_processing_callback,
    },
    {
        "module": "builtins",  # For Python 3.x , Dynamic python code execution hooks
        "callable": "exec",
        "callback_handler": empty_processing_callback,
        "callback_ret_handler": empty_ret_processing_callback,
        "callback_err_handler": empty_err_processing_callback,
    },
    {
        "module": "__builtin__",  # For Python 2.x , Dynamic python code execution hooks
        "callable": "exec",
        "callback_handler": empty_processing_callback,
        "callback_ret_handler": empty_ret_processing_callback,
        "callback_err_handler": empty_err_processing_callback,
    },
]

USER_CALLABLES_TO_HOOK = [

    # Test User Module
    {
        "module": "hooktest",  # User Method
        "callable": "user_code_builtin_test.Test1.func_test_user_code",
        "callback_handler": empty_processing_callback,
        "callback_ret_handler": empty_ret_processing_callback,
        "callback_err_handler": empty_err_processing_callback,
    },
    {
        "module": "hooktest",  # User Function
        "callable": "user_code_builtin_test.func_test_user_code_non_class",
        "callback_handler": empty_processing_callback,
        "callback_ret_handler": empty_ret_processing_callback,
        "callback_err_handler": empty_err_processing_callback,
    },
    {
        "module": "hooktest",  # User Method - Nested Class
        "callable": "user_code_builtin_test.Test1.Test2.func_test_user_code",
        "callback_handler": empty_processing_callback,
        "callback_ret_handler": empty_ret_processing_callback,
        "callback_err_handler": empty_err_processing_callback,
    },
    {
        "module": "hooktest",  # User Method - Multiple class in single module
        "callable": "user_code_builtin_test.Test3.func_test_user_code",
        "callback_handler": empty_processing_callback,
        "callback_ret_handler": empty_ret_processing_callback,
        "callback_err_handler": empty_err_processing_callback,
    },

    # Django Request Hooks
    {
        "module": "django.core.handlers",
        "callable": "base.BaseHandler.get_response",
        "callback_handler": processing_callbacks.django_request_processing_callback,
        "callback_ret_handler": return_processing_callbacks.django_ret_processing_callback,
        "callback_err_handler": error_processing_callbacks.django_err_processing_callback,
    },
    {
        "module": "django.contrib.staticfiles.handlers",
        "callable": "StaticFilesHandler.get_response",
        "callback_handler": processing_callbacks.django_request_static_processing_callback,
        "callback_ret_handler": return_processing_callbacks.django_static_ret_processing_callback,
        "callback_err_handler": error_processing_callbacks.django_static_err_processing_callback,
    },

    # Flask Request Hooks
    {
        "module": "flask",
        "callable": "app.Flask.wsgi_app",
        "callback_handler": processing_callbacks.flask_request_processing_callback,
        "callback_ret_handler": return_processing_callbacks.flask_ret_processing_callback,
        "callback_err_handler": error_processing_callbacks.flask_err_processing_callback,
    },
    {
        "module": "flask",
        "callable": "app.Flask.process_response",
        "callback_handler": processing_callbacks.empty_processing_callback,
        "callback_ret_handler": return_processing_callbacks.flask_ret_response_processing_callback,
        "callback_err_handler": error_processing_callbacks.flask_err_processing_callback,
    },

    # MySQL DB Hooks
    {
        "module": "mysql.connector",
        "callable": "cursor_cext.CMySQLCursor.execute",
        "callback_handler": mysql_processing_callback,
        "callback_ret_handler": empty_ret_processing_callback,
        "callback_err_handler": empty_err_processing_callback,
    },
    {
        "module": "mysql.connector",
        "callable": "cursor.MySQLCursor.execute",
        "callback_handler": mysql_processing_callback,
        "callback_ret_handler": empty_ret_processing_callback,
        "callback_err_handler": empty_err_processing_callback,
    },
    {
        "module": "mysql.connector",
        "callable": "cursor.MySQLCursorPrepared.execute",
        "callback_handler": mysql_processing_callback,
        "callback_ret_handler": empty_ret_processing_callback,
        "callback_err_handler": empty_err_processing_callback,
    },
]
