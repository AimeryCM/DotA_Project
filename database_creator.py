import mysql.connector


DATABASE_PASSWORD_SOURCE = "./database_password.txt"

db_pass = open(DATABASE_PASSWORD_SOURCE).read()

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'aimery',
    password = db_pass,
    auth_plugin = 'mysql_native_password'
)

print(mydb)