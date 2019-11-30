'''This contains maps of callable to hook. Key is the name of module & value is the list of
    submodule.functions or submodule.Class.method to be hooked.
'''
# Place holder to be set by driver
from utils.callbacks import error_processing_callbacks, return_processing_callbacks, processing_callbacks

INSTRUMENTATION_DRIVER_PATH = ""

BUILTIN_CALLABLES_TO_HOOK = [

    {
        "module": "subprocess",  # System Command hook
        "callable": "Popen.__init__",
        "callback_handler": None,
        "callback_ret_handler": None,
        "callback_err_handler": None,
    },
    {
        "module": "os",  # System Command hook
        "callable": "system",
        "callback_handler": None,
        "callback_ret_handler": None,
        "callback_err_handler": None,
    },
    {
        "module": "builtins",  # For Python 3.x , Dynamic python code execution hooks
        "callable": "exec",
        "callback_handler": None,
        "callback_ret_handler": None,
        "callback_err_handler": None,
    },
    {
        "module": "__builtin__",  # For Python 2.x , Dynamic python code execution hooks
        "callable": "exec",
        "callback_handler": None,
        "callback_ret_handler": None,
        "callback_err_handler": None,
    },
]


USER_CALLABLES_TO_HOOK = [

    # Test User Module
    {
        "module": "hooktest",  # User Method
        "callable": "user_code_builtin_test.Test1.func_test_user_code",
        "callback_handler": None,
        "callback_ret_handler": None,
        "callback_err_handler": None,
    },
    {
        "module": "hooktest",  # User Function
        "callable": "user_code_builtin_test.func_test_user_code_non_class",
        "callback_handler": None,
        "callback_ret_handler": None,
        "callback_err_handler": None,
    },
    {
        "module": "hooktest",  # User Method - Nested Class
        "callable": "user_code_builtin_test.Test1.Test2.func_test_user_code",
        "callback_handler": None,
        "callback_ret_handler": None,
        "callback_err_handler": None,
    },
    {
        "module": "hooktest",  # User Method - Multiple class in single module
        "callable": "user_code_builtin_test.Test3.func_test_user_code",
        "callback_handler": None,
        "callback_ret_handler": None,
        "callback_err_handler": None,
    },

    # Django Request Hooks
    {
        "module": "django.core.handlers",
        "callable": "base.BaseHandler.get_response",
        "callback_handler": processing_callbacks.django_processing_callback,
        "callback_ret_handler": return_processing_callbacks.django_ret_processing_callback,
        "callback_err_handler": error_processing_callbacks.django_err_processing_callback,
    },
    {
        "module": "django.contrib.staticfiles.handlers",
        "callable": "StaticFilesHandler.get_response",
        "callback_handler": processing_callbacks.django_static_processing_callback,
        "callback_ret_handler": return_processing_callbacks.django_static_ret_processing_callback,
        "callback_err_handler": error_processing_callbacks.django_static_err_processing_callback,
    },

    # Flask Request Hooks
    {
        "module": "flask",
        "callable": "app.Flask.wsgi_app",
        "callback_handler": processing_callbacks.flask_processing_callback,
        "callback_ret_handler": return_processing_callbacks.flask_ret_processing_callback,
        "callback_err_handler": error_processing_callbacks.flask_err_processing_callback,
    },

]

