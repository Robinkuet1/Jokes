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

    order = request.args.get('order')
    if(order == None or order == ""):
        order = "top"

    user = request.args.get('user')
    if(user == None or user == ""):
        user = "%"

    userId = request.args.get('userId')
    userVoteQuery = ""
    if(userId == None or userId == ""):
        userVoteQuery = f", (SELECT COUNT(*) FROM vote WHERE JokeId = joke.Id AND UserId = {userId} AND Up=1) as \"userUpvote\", (SELECT COUNT(*) FROM vote WHERE JokeId = joke.Id AND UserId = {userId} AND Up=0) as \"userDownvote\""

    if order == "top": order = "(SELECT COUNT(*) FROM vote WHERE JokeId = joke.Id AND Up = 1) - (SELECT COUNT(*) FROM vote WHERE JokeId = joke.Id AND Up = 0) DESC"
    if order == "rand": order = "RAND()"
    if order == "new": order = "joke.Date DESC"
    if order == "hot": order = "((SELECT COUNT(*) FROM vote WHERE JokeId = joke.Id AND Up = 1) - (SELECT COUNT(*) FROM vote WHERE JokeId = joke.Id AND Up = 0))/((DATEDIFF(CURRENT_DATE, joke.Date)+1)/7) DESC"

    querry = '''
    SELECT joke.Id, joke.Text, DATE_FORMAT(joke.Date,'%d %M %Y')  as date, (SELECT count(*) FROM vote WHERE JokeId = joke.Id AND up = 1) as upvotes, (SELECT count(*) FROM vote WHERE JokeId = joke.Id AND up = 0) as downvotes, c.Name, u.Username, u.Id, c2.Name, c2.CODE 
    {0}
    FROM joke
    LEFT OUTER JOIN category c on c.Id = joke.CategoryId
    LEFT JOIN user u on u.Id = joke.UserId
    cross join country c2 on u.CountryId = c2.Id
    WHERE c.Name LIKE "{1}" AND u.Id LIKE "{2}" AND u.Username LIKE "{3}"
    ORDER BY {4}
    '''.format(userVoteQuery ,category, userId, user, order)

    result = select(querry, limit, skip)
    return json.dumps(result)

@app.route("/upvote")
def upvote():
    jokeId = request.args.get('jokeId')
    userId = request.args.get('userId')
    userToken = request.args.get('userToken')
    up = request.args.get('up')

    authorized = len(select(f"SELECT * FROM user WHERE Id = \"{userId}\" AND Token = \"{userToken}\"")) == 1
    if not authorized:
        return str("Unautorized"), 401

    insert("DELETE FROM vote WHERE UserId = %s AND JokeId = %s", (userId, jokeId))

    if up != None and up != "":
        insert("INSERT INTO vote (UserId, JokeId, Up) VALUES (%s, %s, %s)", (userId, jokeId, up))

    return str(authorized), 200

@app.route("/autocomplete/topics")
def autocompleteTopics():
    searchParam = request.args.get("name")
    result = select(f"SELECT Name FROM category WHERE Name LIKE \"%{searchParam}%\"")
    resultList = []
    for i in result:
        resultList.append(i[0])
    return json.dumps(resultList)

@app.route("/autocomplete/users")
def autocompleteUsers():
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
        return "Not all required parameters provided", 401
    token = sha256(uname + pwd + str(random.randint(10000000,99999999999)))
    if(uname == "" or pwd == ""):
        return "Error", 401
    exists = select(f"SELECT Id FROM user WHERE Username = '{uname}'")
    if(len(exists) != 0):
        return "User already exists", 404
    result = insert(f"INSERT INTO user (Username, Password, Token, CountryId, NSFW) VALUES (%s, %s, %s, %s, %s)", (uname, pwd, token, countryId, nsfw))
    return str(result), 200
    
@app.route("/login")
def login():
    uname = request.args.get("username")
    pwd = request.args.get("password")
    exists = select(f"SELECT Id FROM user WHERE Username = '{uname}'")
    if(len(exists) == 0):
        return "User not found", 404
    result = select(f"SELECT Id, Token FROM user WHERE Username = '{uname}' AND Password = '{pwd}'")
    if(len(result) == 0):
        return "Unauthorized", 401
    return result
    
@app.route("/isNSFW")
def isNSFW():
    uname = request.args.get("username")
    nsfw = select(f"SELECT NSFW FROM user WHERE Username = '{uname}'")
    print(nsfw)
    if(len(nsfw) != 0):
        return str(nsfw[0][0])
    return "0"
    

app.run(host="0.0.0.0",port=5678)