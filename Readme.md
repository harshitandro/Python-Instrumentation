## Python Instrumentation

An extensible framework that instruments (modifies the bytecode at loading time) python programs at runtime, with the purpose of capturing method invocation events (start, finish, errors ...) and notifying custom listeners.

Hence this framework uses dynamic instrumentation of python achieved by monkey patching.

This framework runs as a wrapper for any python script/program.

### Key Features: 
- Support for both Python 2 & 3.
- Hooking of methods/functions on module loading. This ensure there is no inconsistency between multiple references of same module anywhere in user code.
- Each callback has complete info about the caller including the threadID.

### Run :
```bash
$ python ${ABSOLUTE_PATH_FOR_FRAMEWORK}/driver.py YOUR_ACTUALL_SCRIPT.py CMD_ARGS_TO_YOUR_SCRIPT
```
Note:  The above run command expects both the framework & your script being in the PYTHONPATH of your env. This can be set like any other env variable as ``` $ export PYTHONPATH=$PYTHONPATH:{PATHS_TO_BE_ADDED}```

### Details
#### Adding hooks to functions/methods:
For adding hook to any method/function, please add the module & function/Class.Method to `constants/hooks.py` under relevant sections.
The methods/functions present in `sys, io, os etc` internal & by default loaded modules shall go in `BUILTIN_CALLABLES_TO_HOOK` & all the rest shall go into `USER_CALLABLES_TO_HOOK`.

#### Custom Callbacks:
The framework calls the default callbacks defined in `utils/callbacks.py` . You can update/extend the functionality of these callbacks.
The name of callbacks are self explanatory:
 - `start_callback` is called whenever a hooked method/function call is intercepted. 
 - `end_callback` is called whenever a hooked method/function call has returned after normal execution. 
 - `error_callback` is called whenever a hooked method/function call has raised an error. 

### Current Support: 
- Python 2.7 & above

### Test & Demo:
- Bare Test without Python-Instrumentation framework :
    ```bash
    $ git clone https://github.com/harshitandro/Python-Instrumentation.git
    $ cd Python-Instrumentation
    $ python test_runner.py TestArg1 TestArg2
    ```
    
    This should output something like this for Python3 env:
    ```text    
    Command args are : ['/mnt/Workspace/Pycharm-Workspace/Python-Instrumentator/test_runner.py']
    Calling method Test1.func_test_user_code
    ==========================================================
    Method : func_test_user_code
        x :  10
        y :  2
        argsv are :  (1, 1)
        kwargs are :  {'name': 'Tester Name'}
    ==========================================================
    5.0
    Time Taken: 0.0000269412994385
    
    Calling method Test1.func_test_user_code
    ==========================================================
    Method : func_test_user_code
        x :  10
        y :  0
        argsv are :  ()
        kwargs are :  {'name': 'Tester Name'}
    ==========================================================
    Error caught
    Time Taken: 0.0000209808349609
    
    Calling method func_test_user_code_non_class
    ==========================================================
    Inside User function non-class : Tester Name
    ==========================================================
    None
    Time Taken: 0.0000083446502686
    
    Calling method Test1.func_test_subprocess_init
    ==========================================================
    Method : func_test_subprocess_init
    [b'git version 2.21.0\n']
    ==========================================================
    git version 2.21.0
    returned value: 0
    ==========================================================
    Time Taken: 0.0048534870147705
    
    Calling method Test1.func_test_os_system
    ==========================================================
    Method : func_test_os_system
    git version 2.21.0
    returned value: 0
    ==========================================================
    Time Taken: 0.0041146278381348
    
    Calling method Test1.func_test_exec_os_system
    ==========================================================
    Method : func_test_exec_os_system
    git version 2.21.0
    returned value: 0
    ==========================================================
    Time Taken: 0.0023276805877686
    ```
    
- Test with Python-Instrumentation framework :
    ```bash
    $ git clone https://github.com/harshitandro/Python-Instrumentation.git
    $ cd Python-Instrumentation
    $ python driver.py test_runner.py TestArg1 TestArg2
    ```
     This should output something like this for Python3 env:
    ```text
    Hooked method : __init__ of subprocess
    Hooked method : system of posix
    Hooked method : open of io
    StartCallback for io.open :: threadID : 140176730859328 :: args : ('/mnt/Workspace/Pycharm-Workspace/Python-Instrumentation/test_runner.py', 'rb') :: kwargs : {}
    EndCallback for io.open :: return val : (<_io.BufferedReader name='/mnt/Workspace/Pycharm-Workspace/Python-Instrumentation/test_runner.py'>,) :: threadID : 140176730859328
    StartCallback for io.open :: threadID : 140176730859328 :: args : ('/tmp/test.txt',) :: kwargs : {}
    EndCallback for io.open :: return val : (<_io.TextIOWrapper name='/tmp/test.txt' mode='r' encoding='UTF-8'>,) :: threadID : 140176730859328
    
    Command args are : ['/mnt/Workspace/Pycharm-Workspace/Python-Instrumentation/test_runner.py', 'arg1', 'arg2']
    Calling method Test1.func_test_user_code
    ==========================================================
    Method : func_test_user_code
        x :  10
        y :  2
        argsv are :  (1, 1)
        kwargs are :  {'name': 'Tester Name'}
    ==========================================================
    5.0
    Time Taken: 0.0000395774841309
    
    Calling method Test1.func_test_user_code
    ==========================================================
    Method : func_test_user_code
        x :  10
        y :  0
        argsv are :  ()
        kwargs are :  {'name': 'Tester Name'}
    ==========================================================
    Error caught
    Time Taken: 0.0000305175781250
    
    Calling method func_test_user_code_non_class
    ==========================================================
    Inside User function non-class : Tester Name
    ==========================================================
    None
    Time Taken: 0.0000123977661133
    
    Calling method Test1.func_test_subprocess_init
    ==========================================================
    Method : func_test_subprocess_init
    StartCallback for subprocess.Popen.__init__ :: threadID : 140176730859328 :: args : (<subprocess.Popen object at 0x7f7d62319ac8>, ['git', '--version']) :: kwargs : {'stdout': -1, 'stderr': -2}
    EndCallback for subprocess.Popen.__init__ :: return val : (None,) :: threadID : 140176730859328
    [b'git version 2.21.0\n']
    ==========================================================
    StartCallback for subprocess.Popen.__init__ :: threadID : 140176730859328 :: args : (<subprocess.Popen object at 0x7f7d62dd6710>, 'git --version') :: kwargs : {'shell': True}
    EndCallback for subprocess.Popen.__init__ :: return val : (None,) :: threadID : 140176730859328
    git version 2.21.0
    returned value: 0
    ==========================================================
    Time Taken: 0.0068063735961914
    
    Calling method Test1.func_test_os_system
    ==========================================================
    Method : func_test_os_system
    StartCallback for posix.system :: threadID : 140176730859328 :: args : ('git --version',) :: kwargs : {}
    git version 2.21.0
    EndCallback for posix.system :: return val : (0,) :: threadID : 140176730859328
    returned value: 0
    ==========================================================
    Time Taken: 0.0034019947052002
    
    Calling method Test1.func_test_exec_os_system
    ==========================================================
    Method : func_test_exec_os_system
    StartCallback for posix.system :: threadID : 140176730859328 :: args : ('git --version',) :: kwargs : {}
    git version 2.21.0
    EndCallback for posix.system :: return val : (0,) :: threadID : 140176730859328
    returned value: 0
    ==========================================================
    Time Taken: 0.0042455196380615
    
    ```

### Latency:
Latency introduced by this framework per API hook is ~ ```0.53 ms```. <br>
This means for each hooked method/function, the above latency is introduced to the execution of the said method/function. <br>
This can be calculated from the above outputs by subtracting the time taken by each API with & without the framework. <br>

### References:
- https://stackoverflow.com/questions/5626193/what-is-monkey-patching
- https://filippo.io/instance-monkey-patching-in-python/