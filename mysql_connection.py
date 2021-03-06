import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
    database = "mydatabase"
)

print(mydb)
mycursor = mydb.cursor()
# mycursor.execute("CREATE TABLE IF NOT EXISTS customers1 (name VARCHAR(255), address VARCHAR(255))")
# mycursor.execute("CREATE DATABASE mydatabase")
sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
val = ("am", "Highway 3")
mycursor.execute(sql, val)

mydb.commit()
#
# print(mycursor.rowcount, "record inserted.")
# name = "John"
# sql = "SELECT * FROM customers where name = '"+name+"'"
# mycursor.execute(sql)
#
# myresult = mycursor.fetchall()
#
# for x in myresult:
#     x1 = list(x)
#
#     print(x1)

sql = "SELECT * FROM customers ORDER BY name"

mycursor.execute(sql)

myresult = mycursor.fetchall()

for x in myresult:
  print(x)