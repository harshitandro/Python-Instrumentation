import sys
from time import time

from hooktest.test1 import Test1, func_test_user_code_non_class

if __name__ == '__main__':
    open("/tmp/test.txt")
    obj = Test1()
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


