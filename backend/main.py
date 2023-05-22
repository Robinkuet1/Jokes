import mysql.connector
from flask import Flask, request
from flask_cors import CORS
import json
import hashlib
import random
import json
import requests

def select(querry, size = 10):
    db = mysql.connector.connect(host = 'db', user = 'foo', password = 'bar', port = 3306, database = 'jokes')
    cursor = db.cursor()
    cursor.execute(querry)
    return cursor.fetchmany(size)

def insert(querry, values):
    db = mysql.connector.connect(host = 'db', user = 'foo', password = 'bar', port = 3306, database = 'jokes')
    cursor = db.cursor()
    cursor.execute(querry, values)
    db.commit()
    return cursor.rowcount

def sha256(data):
    x = hashlib.sha256(str(data).encode("UTF-8"))
    return x.hexdigest()

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
    result = sql("SELECT * FROM jokes")
    return json.dumps(result)

@app.route("/autocomplete/topics")
def autocompleteTopics():
    searchParam = request.args.get("category")
    result = select(f"SELECT Name FROM category WHERE Name LIKE \"%{searchParam}%\"")
    maxResult = 50
    resultList = []
    for i in result:
        maxResult += 1
        resultList.append(i[0])
    return json.dumps(resultList)

@app.route("/register")
def register():
    uname = request.args.get("username")
    pwd = request.args.get("password")
    nsfw = request.args.get("nsfw")
    if(uname == None or pwd == None or nsfw == None):
        return "Not all required parameters provided"
    token = sha256(uname + pwd + str(random.randint(10000000,99999999999)))
    if(uname == "" or pwd == ""):
        return "Error"
    exists = select(f"SELECT Id FROM user WHERE Username = '{uname}'")
    if(len(exists) != 0):
        return "User already exists"
    countryCode = requests.get(f"http://ip-api.com/json/{request.remote_addr}").text
    result = insert(f"INSERT INTO user (Username, Password, Token, CountryId, NSFW) VALUES (%s, %s, %s, %s, %s)", (uname, pwd, token, 1, nsfw))
    return str(result)

@app.route("/login")
def login():
    uname = request.args.get("username")
    pwd = request.args.get("password")
    exists = select(f"SELECT Id FROM user WHERE Username = '{uname}'")
    if(len(exists) == 0):
        return "User not found"
    token = select(f"SELECT Token FROM user WHERE Username = '{uname}' AND Password = '{pwd}'")
    if(len(token) == 0):
        return "Unauthorized"
    return token[0][0]

app.run(host="0.0.0.0",port=5678)
