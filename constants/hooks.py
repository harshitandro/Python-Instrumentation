'''This contains maps of callable to hook. Key is the name of module & value is the list of
    functions or Class.method to be hooked.
'''

BUILTIN_CALLABLES_TO_HOOK = {

    'subprocess': [
        "Popen.__init__", # System Command hook
    ],
    "os": [
        "system", # System Command hook
    ],

    # For Python 3.x
    "builtins": [
        # "open", # File Open hooks
        #"exec", # Dynamic python code execution hooks
    ],

    # For Python 2.x
    "__builtin__": [
        # "open", # File Open hooks
        #"exec", # Dynamic python code execution hooks
    ],
}

USER_CALLABLES_TO_HOOK = {

    # Test User Module
    "hooktest.test1": [
        "Test1.func_test_user_code", # User Method
        "func_test_user_code_non_class" # User Function
    ],

}


