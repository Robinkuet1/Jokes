import mysql.connector
from flask import Flask
import json

db = mysql.connector.connect(host = 'db', user = 'foo', password = 'bar', port = 3306, database = 'jokes')
cursor = db.cursor()

app = Flask(__name__)

@app.route("/")
def hello_world():
    cursor.execute("SELECT * FROM joke")
    result = cursor.fetchall()
    return json.dumps(result)

app.run(host="0.0.0.0",port=5678)