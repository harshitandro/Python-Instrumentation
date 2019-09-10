import sys

# The magic happens behind the curtain.
from utils.instrumentation import enable_module_hook_on_load

#instrument_system_api()
enable_module_hook_on_load()

# Manipulate the current argv to be used by user application code.
sys.argv = sys.argv[1:]

# Transparently call the user code with all the given command line parameters.
exec(open(sys.argv[0]).read())