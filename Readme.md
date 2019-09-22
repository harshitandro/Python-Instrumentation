## Python Instrumentation

An extensible framework that instruments (modifies the bytecode at loading time) python programs at runtime, with the purpose of capturing method invocation events (start, finish, errors ...) and notifying custom listeners.

Hence this framework uses dynamic instrumentation of python achieved by monkey patching.

This framework runs as a wrapper for any python script/program.

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
- Python 3.4 & above

### Test & Demo:
```bash
$ git clone https://github.com/harshitandro/Python-Instrumentator.git
$ cd Python-Instrumentator
$ python driver.py test_runner.py TestArg1 TestArg2
```
 This should output something like this:
```text
Hooked method : __init__ of subprocess
Hooked method : system of posix
Hooked method : open of io
StartCallback for UNKNOWN :: args : ('/mnt/Workspace/Pycharm-Workspace/Python-Instrumentator/test_runner.py',) :: kwargs : {}
EndCallback for UNKNOWN :: return val : (<_io.TextIOWrapper name='/mnt/Workspace/Pycharm-Workspace/Python-Instrumentator/test_runner.py' mode='r' encoding='UTF-8'>,)
StartCallback for UNKNOWN :: args : ('/mnt/Workspace/Pycharm-Workspace/Python-Instrumentator/hooktest/test1.py',) :: kwargs : {}
EndCallback for UNKNOWN :: return val : (<_io.TextIOWrapper name='/mnt/Workspace/Pycharm-Workspace/Python-Instrumentator/hooktest/test1.py' mode='r' encoding='UTF-8'>,)
Hooked method : func_test_user_code of hooktest.test1
Hooked method : func_test_user_code_non_class of hooktest.test1
StartCallback for UNKNOWN :: args : ('/tmp/test.txt',) :: kwargs : {}
EndCallback for UNKNOWN :: return val : (<_io.TextIOWrapper name='/tmp/test.txt' mode='r' encoding='UTF-8'>,)
Command args are : ['/mnt/Workspace/Pycharm-Workspace/Python-Instrumentator/test_runner.py', 'arg1', 'arg2']
StartCallback for UNKNOWN :: args : (<hooktest.test1.Test1 object at 0x7f6ea2ec3cc0>, 10, 2, 1, 1) :: kwargs : {'name': 'harshit'}
==========================================================
Method : func_test_user_code
	x :  10
	y :  2
	argsv are :  (1, 1)
	kwargs are :  {'name': 'harshit'}
==========================================================
EndCallback for UNKNOWN :: return val : (5.0,)
5.0

StartCallback for UNKNOWN :: args : (<hooktest.test1.Test1 object at 0x7f6ea2ec3cc0>,) :: kwargs : {'x': 10, 'y': 0, 'name': 'harshit'}
==========================================================
Method : func_test_user_code
	x :  10
	y :  0
	argsv are :  ()
	kwargs are :  {'name': 'harshit'}
==========================================================
ErrorCallback for UNKNOWN :: type : <class 'ZeroDivisionError'> :: value : division by zero :: traceback : <traceback object at 0x7f6e9a195dc8>
fata re

StartCallback for UNKNOWN :: args : ('harshit',) :: kwargs : {}
==========================================================
Inside User function non-class : harshit
==========================================================
EndCallback for UNKNOWN :: return val : (None,)
None

==========================================================
Method : func_test_subprocess_init
StartCallback for UNKNOWN :: args : (<subprocess.Popen object at 0x7f6ea6def6a0>, ['ls', '-la', '/']) :: kwargs : {'stdout': -1, 'stderr': -2}
EndCallback for UNKNOWN :: return val : (None,)
[b'total 260\n', b'dr-xr-xr-x.  23 root root   4096 Jun 30 23:18 .\n', b'dr-xr-xr-x.  23 root root   4096 Jun 30 23:18 ..\n', b'-rw-r--r--    1 root root      0 Jul 30  2018 .autorelabel\n', b'lrwxrwxrwx    1 root root      7 Feb 11  2019 bin -> usr/bin\n', b'dr-xr-xr-x.   7 root root   4096 Sep 14 10:49 boot\n', b'drwxr-xr-x    2 root root   4096 Feb 10  2019 data\n', b'drwxr-xr-x   22 root root   4760 Sep 17 23:44 dev\n', b'drwxr-xr-x. 171 root root  12288 Sep 21 19:54 etc\n', b'drwxr-xr-x.   4 root root   4096 Feb 11  2019 home\n', b'lrwxrwxrwx    1 root root      7 Feb 11  2019 lib -> usr/lib\n', b'lrwxrwxrwx    1 root root      9 Feb 11  2019 lib64 -> usr/lib64\n', b'drwx------.   2 root root  16384 Apr 25  2018 lost+found\n', b'drwxr-xr-x.   2 root root   4096 Feb 11  2019 media\n', b'drwxr-xr-x    3 root root      0 Sep 17 22:42 misc\n', b'drwxr-xr-x.   7 root root   4096 Feb 11  2019 mnt\n', b'drwxr-xr-x    2 root root      0 Sep 17 22:42 net\n', b'drwxrwxrwx.  15 root root   4096 Jul 21 20:06 opt\n', b'dr-xr-xr-x  464 root root      0 Sep 18 04:12 proc\n', b'dr-xr-x---.  22 root root   4096 Sep 16 00:17 root\n', b'drwxr-xr-x.   2 root root   4096 May  3  2018 .root.only\n', b'drwxr-xr-x   50 root root   1500 Sep 21 19:54 run\n', b'lrwxrwxrwx    1 root root      8 Feb 11  2019 sbin -> usr/sbin\n', b'drwxr-xr-x.   2 root root   4096 Feb 11  2019 srv\n', b'dr-xr-xr-x   13 root root      0 Sep 18 04:12 sys\n', b'drwxrwxrwt. 125 root root 180224 Sep 21 20:51 tmp\n', b'drwxrwxrwt.   2 root root   4096 May  3  2018 tmp.new\n', b'drwxr-xr-x.  13 root root   4096 Jun 30 23:18 usr\n', b'drwxr-xr-x.  21 root root   4096 Jun 30 23:40 var\n']
==========================================================
StartCallback for UNKNOWN :: args : (<subprocess.Popen object at 0x7f6e9aaf6ac8>, 'git --version') :: kwargs : {'shell': True}
EndCallback for UNKNOWN :: return val : (None,)
git version 2.21.0
returned value: 0
==========================================================

==========================================================
Method : func_test_os_system
StartCallback for UNKNOWN :: args : ('git --version',) :: kwargs : {}
git version 2.21.0
EndCallback for UNKNOWN :: return val : (0,)
returned value: 0
==========================================================

==========================================================
Method : func_test_exec_os_system
StartCallback for UNKNOWN :: args : ('git --version',) :: kwargs : {}
git version 2.21.0
EndCallback for UNKNOWN :: return val : (0,)
returned value: 0
==========================================================
```

### References:
- https://stackoverflow.com/questions/5626193/what-is-monkey-patching
- https://filippo.io/instance-monkey-patching-in-python/