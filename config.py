import mysql.connector
def connect():
    mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        password="aimlb2",
        database="bank_details"

    )
    return mydb
print(connect())