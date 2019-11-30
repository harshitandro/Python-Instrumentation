import mysql.connector

def runner():
    print("Starting mysql test")
    mydb = mysql.connector.connect(
        host="db4free.net",
        user="hstest123",
        passwd="hstest123",
        database="hstest123"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SHOW TABLES")
    mydb.commit()
    for x in mycursor:
        print(x)
