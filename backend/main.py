import mysql.connector
db = mysql.connector.connect(host = 'db', user = 'foo', password = 'bar', port = 3306)


mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM joke")
myresult = mycursor.fetchall()
for i in myresult:
    print(i)