import inspect
import os
import subprocess
from time import time

import sys


def func_test_user_code_non_class(toPrint):
    print("==========================================================")
    print("Inside User function non-class : {}".format(toPrint))
    print("==========================================================")


class Test1:
    def __init__(self):
        pass

    def func_test_user_code(self, x, y, *argv, **kwargs):
        print("==========================================================")
        print("Method : {}".format(inspect.currentframe().f_code.co_name))
        print("\tx : ", x)
        print("\ty : ", y)
        print("\targsv are : ", argv)
        print("\tkwargs are : ", kwargs)
        print("==========================================================")
        return x/y

    def func_test_subprocess_init(self):
        print("==========================================================")
        print("Method : {}".format(inspect.currentframe().f_code.co_name))
        out = subprocess.Popen(['git', '--version'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        print(out.stdout.readlines())
        print("==========================================================")

        cmd = "git --version"

        returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix
        print('returned value:', returned_value)

        print("==========================================================")

    def func_test_os_system(self):
        print("==========================================================")
        print("Method : {}".format(inspect.currentframe().f_code.co_name))

        cmd = "git --version"

        returned_value = os.system(cmd)  # returns the exit code in unix
        print('returned value:', returned_value)
        print("==========================================================")

    def func_test_exec_os_system(self):
        print("==========================================================")
        print("Method : {}".format(inspect.currentframe().f_code.co_name))
        cmd = """import os;returned_value = os.system('git --version');print('returned value:', returned_value)"""

        exec(cmd)  # returns the exit code in unix
        print("==========================================================")


    class Test2:
        def __init__(self):
            pass

        def func_test_user_code(self, x, y, *argv, **kwargs):
            print("==========================================================")
            print("Method : {}".format(inspect.currentframe().f_code.co_name))
            print("\tx : ", x)
            print("\ty : ", y)
            print("\targsv are : ", argv)
            print("\tkwargs are : ", kwargs)
            print("==========================================================")
            return x / y

class Test3:
    def __init__(self):
        pass

    def func_test_user_code(self, x, y, *argv, **kwargs):
        print("==========================================================")
        print("Method : {}".format(inspect.currentframe().f_code.co_name))
        print("\tx : ", x)
        print("\ty : ", y)
        print("\targsv are : ", argv)
        print("\tkwargs are : ", kwargs)
        print("==========================================================")
        return x / y


def runner():
    obj = Test1()
    obj2 = Test1.Test2()
    obj3 = Test3()
    print("\nCommand args are : {}".format(sys.argv))

    print("Calling method Test1.func_test_user_code")
    start_time = time()
    print(obj.func_test_user_code(10, 2, 1, 1, name="Tester Name"))
    print("Time Taken: {0:.16f}".format(time() - start_time))
    print()
    print("Calling method Test1.func_test_user_code")
    start_time = time()
    try:
        print(obj.func_test_user_code(x=10, y=0, name="Tester Name"))
    except:
        print("Error caught")
    print("Time Taken: {0:.16f}".format(time() - start_time))
    print()
    print("Calling method func_test_user_code_non_class")
    start_time = time()
    print(func_test_user_code_non_class("Tester Name"))
    print("Time Taken: {0:.16f}".format(time() - start_time))
    print()
    print("Calling method Test1.func_test_subprocess_init")
    start_time = time()
    obj.func_test_subprocess_init()
    print("Time Taken: {0:.16f}".format(time() - start_time))
    print()
    print("Calling method Test1.func_test_os_system")
    start_time = time()
    obj.func_test_os_system()
    print("Time Taken: {0:.16f}".format(time() - start_time))
    print()
    print("Calling method Test1.func_test_exec_os_system")
    start_time = time()
    obj.func_test_exec_os_system()
    print("Time Taken: {0:.16f}".format(time() - start_time))
    print()
    print("Calling method Test1.Test2.func_test_user_code")
    start_time = time()
    print(obj2.func_test_user_code(10, 2, 1, 1, name="Tester Name"))
    print("Time Taken: {0:.16f}".format(time() - start_time))
    print()
    print("Calling method Test3.func_test_user_code")
    start_time = time()
    print(obj3.func_test_user_code(10, 2, 1, 1, name="Tester Name"))
    print("Time Taken: {0:.16f}".format(time() - start_time))
