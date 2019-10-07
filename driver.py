from __future__ import print_function

import sys

from setuptools.sandbox import _execfile

from utils.import_hook import enable_module_hook_on_load
from utils.instrumentation import instrument_system_api

# The magic happens behind the curtain.
enable_module_hook_on_load()
instrument_system_api()

# Manipulate the current argv to be used by user application code.
sys.argv = sys.argv[1:]

# Transparently call the user code with all the given command line parameters.
if sys.argv[0].endswith(".py") :
    _execfile(sys.argv[0], globals(), locals())
else:
    print("Unsupported file to execute.", file=sys.stderr)
    print("Sys args are : {}".format(sys.argv), file=sys.stderr)
