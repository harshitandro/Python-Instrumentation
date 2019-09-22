import sys

# The magic happens behind the curtain.
from py._builtin import execfile

from utils.custom_loader import enable_module_hook_on_load
from utils.instrumentation import instrument_system_api

instrument_system_api()
enable_module_hook_on_load()

# Manipulate the current argv to be used by user application code.
sys.argv = sys.argv[1:]

# Transparently call the user code with all the given command line parameters.
execfile(sys.argv[0])
