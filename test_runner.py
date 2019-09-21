import sys

from hooktest.test1 import Test1, func_test_user_code_non_class

if __name__ == '__main__':
    open("/tmp/test.txt")
    obj = Test1()
    print("Command args are : {}".format(sys.argv))
    print(obj.func_test_user_code(10, 2, 1, 1, name="harshit"))
    print()
    try:
        print(obj.func_test_user_code(x=10, y=0, name="harshit"))
    except:
        print("fata re")
    print()
    print(func_test_user_code_non_class("harshit"))
    print()
    obj.func_test_subprocess_init()
    print()
    obj.func_test_os_system()
    print()
    obj.func_test_exec_os_system()


