from __future__ import print_function

import sys

from setuptools.sandbox import _execfile

from utils.instrumentation import instrument_system_api

# The magic happens behind the curtain.

if sys.version_info[0] == 2:
    from utils.custom_loader_v2 import enable_module_hook_on_load
    enable_module_hook_on_load()
elif sys.version_info[0] == 3:
    from utils.custom_loader_v3 import enable_module_hook_on_load
    enable_module_hook_on_load()
else:
    print("Unsupported Python Major Version : {}".format(sys.version_info[0]), file=sys.stderr)
    exit(1)

instrument_system_api()

# Manipulate the current argv to be used by user application code.
sys.argv = sys.argv[1:]

# Transparently call the user code with all the given command line parameters.

if sys.argv[0].endswith(".py") :
    _execfile(sys.argv[0], globals(), locals())
else:
    print("Unsupported file to execute.", file=sys.stderr)