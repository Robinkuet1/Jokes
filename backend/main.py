import mysql.connector
from flask import Flask, request
from flask_cors import CORS
import json
import hashlib
import random
import json
import requests

def select(querry, limit = 10, skip = 0):
    db = mysql.connector.connect(host = 'db', user = 'foo', password = 'bar', port = 3306, database = 'jokes')
    cursor = db.cursor()
    cursor.execute(querry+f" LIMIT {int(skip)}, {int(skip)+int(limit)}")
    return cursor.fetchmany(int(limit))

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

@app.route("/categories")
def categories():
    limit = request.args.get('limit')
    if(limit == None or limit == ""):
        limit = "10"
    
    skip = request.args.get('skip')
    if(skip == None or skip == ""):
        skip = "0"


    querry = '''
    SELECT * FROM category
    '''

    result = select(querry, limit, skip)
    return json.dumps(result)





@app.route("/jokes")
def jokes():
    category = request.args.get('category')
    if(category == None or category == ""):
        category = "%"
    
    limit = request.args.get('limit')
    if(limit == None or limit == ""):
        limit = "10"
    
    skip = request.args.get('skip')
    if(skip == None or skip == ""):
        skip = "0"

    sort = request.args.get('sort')


    querry = '''
    SELECT joke.Id, joke.Text, DATE_FORMAT(joke.Date,'%d %M %Y')  as date, (SELECT count(*) FROM vote WHERE JokeId = joke.Id AND up = 1) as upvotes, (SELECT count(*) FROM vote WHERE JokeId = joke.Id AND up = 0) as downvotes, c.Name, u.Username, u.Id, c2.Name, c2.CODE FROM joke
    LEFT OUTER JOIN category c on c.Id = joke.CategoryId
    LEFT JOIN user u on u.Id = joke.UserId
    cross join country c2 on u.CountryId = c2.Id
    WHERE c.Name LIKE "{0}"
    '''.format(category)

    result = select(querry, limit, skip)
    return json.dumps(result)

@app.route("/upvote")
def upvote():
    userId = request.args.get('userId')
    userToken = request.args.get('userToken')
    return ""

@app.route("/autocomplete/topics")
def autocompleteTopics():
    searchParam = request.args.get("name")
    result = select(f"SELECT Name FROM category WHERE Name LIKE \"%{searchParam}%\"")
    resultList = []
    for i in result:
        resultList.append(i[0])
    return json.dumps(resultList)

@app.route("/autocomplete/users")
def categories():
    searchParam = request.args.get("name")
    result = select(f"SELECT Username FROM user WHERE Username LIKE \"%{searchParam}%\"")
    resultList = []
    for i in result:
        resultList.append(i[0])
    return json.dumps(resultList)

@app.route("/register")
def register():
    uname = request.args.get("username")
    pwd = request.args.get("password")
    nsfw = request.args.get("nsfw")

    country = requests.get(f"http://ip-api.com/json/{request.remote_addr}").json()["countryCode"]
    countryId = select(f"SELECT Id FROM country WHERE code = \"{country}\"")[0][0]

    if(uname == None or pwd == None or nsfw == None):
        return "Not all required parameters provided"
    token = sha256(uname + pwd + str(random.randint(10000000,99999999999)))
    if(uname == "" or pwd == ""):
        return "Error"
    exists = select(f"SELECT Id FROM user WHERE Username = '{uname}'")
    if(len(exists) != 0):
        return "User already exists"
    result = insert(f"INSERT INTO user (Username, Password, Token, CountryId, NSFW) VALUES (%s, %s, %s, %s, %s)", (uname, pwd, token, countryId, nsfw))
    return str(result)
    
@app.route("/login")
def login():
    uname = request.args.get("username")
    pwd = request.args.get("password")
    exists = select(f"SELECT Id FROM user WHERE Username = '{uname}'")
    if(len(exists) == 0):
        return "User not found", 404
    token = select(f"SELECT Token FROM user WHERE Username = '{uname}' AND Password = '{pwd}'")
    if(len(token) == 0):
        return "Unauthorized", 401
    return token[0][0]
    
@app.route("/isNSFW")
def isNSFW():
    uname = request.args.get("username")
    nsfw = select(f"SELECT NSFW FROM user WHERE Username = '{uname}'")
    print(nsfw)
    if(len(nsfw) != 0):
        return str(nsfw[0][0])
    return "0"
    

app.run(host="0.0.0.0",port=5678)
