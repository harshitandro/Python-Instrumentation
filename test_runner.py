from hooktest import user_code_builtin_test, mysql_test

if __name__ == '__main__':
    print("Starting User Code & builtin API Hook Test")
    user_code_builtin_test.runner()

    print("Starting MySQL API Hook Test")
    mysql_test.runner()
