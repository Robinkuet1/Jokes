import mysql.connector
from flask import Flask, request
import json

db = mysql.connector.connect(host = 'db', user = 'foo', password = 'bar', port = 3306, database = 'jokes')
cursor = db.cursor()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "test"

@app.route("/jokes")
def jokes():
    if(request.args.get('catergory')):
        return "todo"
    elif(request.args.get('id')):
        return "todo"
    cursor.execute("SELECT * FROM joke")
    result = cursor.fetchall()
    return json.dumps(result)

app.run(host="",port=5678)