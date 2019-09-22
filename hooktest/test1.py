import inspect
import os
import subprocess


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
        out = subprocess.Popen(['ls', '-la', '/'],
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
