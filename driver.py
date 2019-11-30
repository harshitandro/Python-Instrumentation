from __future__ import print_function
import os

from constants import hooks
setattr(hooks, "INSTRUMENTATION_DRIVER_PATH", os.path.abspath(__file__))
print("Python Instrumentor located at : {}".format(hooks.INSTRUMENTATION_DRIVER_PATH))

import sys
from setuptools.sandbox import _execfile
from utils.import_hook import enable_module_hook_on_load
from utils.instrumentation import instrument_system_api

# The magic happens behind the curtain.
enable_module_hook_on_load()
instrument_system_api()

# Manipulate the current argv to be used by user application code.
sys.argv = sys.argv[1:]
print("Python Instrumentor calling actual application")
# Transparently call the user code with all the given command line parameters.
if sys.argv[0].endswith(".py") :
    _execfile(sys.argv[0], globals(), locals())
elif sys.argv[0] == "-m" :
    # Run with the -m switch
    import runpy
    mod_name = sys.argv[1]
    sys.argv = sys.argv[1:]
    if hasattr(runpy, '_run_module_as_main'):
        # Newer versions of Python actually use this when the -m switch is used.
        if sys.version_info[:2] <= (2, 6):
            runpy._run_module_as_main(mod_name, set_argv0=False)
        else:
            runpy._run_module_as_main(mod_name, alter_argv=False)
    else:
        runpy.run_module(sys.argv[1])
else:
    print("Unsupported file to execute.", file=sys.stderr)
    print("Sys args are : {}".format(sys.argv), file=sys.stderr)
print("Python Instrumentor exiting.")