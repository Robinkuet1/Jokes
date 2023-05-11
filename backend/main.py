import mysql.connector
from flask import Flask, request
from flask_cors import CORS
import json

db = mysql.connector.connect(host = 'db', user = 'foo', password = 'bar', port = 3306, database = 'jokes')
cursor = db.cursor()

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "test"

@app.route("/jokes")
def jokes():
    if(request.args.get('category')):
        return "todo"
    elif(request.args.get('id')):
        return "todo"
    cursor.execute("SELECT * FROM joke")
    result = cursor.fetchall()
    return json.dumps(result)

@app.route("/autocomplete/topics")
def autocompleteTopics():
    searchParam = request.args.get("category")
    cursor.execute(f"SELECT Name FROM category WHERE Name LIKE \"%{searchParam}%\"")
    result = cursor.fetchall()
    result = cursor.fetchall()
    maxResult = 50
    resultList = []
    for i in result:
        maxResult += 1
        resultList.append(i[0])
    return json.dumps(resultList)

@app.route("/register")
def register():
    uname = request.args.get("username")
    pwd = request.args.get("pwd")
    if(uname == "" or pwd == ""):
        return "Error"
    
app.run(host="0.0.0.0",port=5678)