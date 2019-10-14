from hooktest import user_code_builtin_test, sqlite3_test

if __name__ == '__main__':
    print("Starting User Code & builtin API Hook Test")
    user_code_builtin_test.runner()

    print("Starting SQLite3 API Hook Test")
    sqlite3_test.runner()
