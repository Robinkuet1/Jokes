import mysql.connector
import json
import hashlib
import random
import csv
import requests
import time
from tqdm import tqdm

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

def get(url):
    return requests.get(url).json()

def newCategory(name):
    id = select(f"SELECT Id FROM category where Name = \"{name}\"")
    if(len(id) == 0):
        insert("INSERT INTO category (Name) VALUES (%s)", (name,))
        return select(f"SELECT Id FROM category where Name = \"{name}\"")[0][0]
    else:
        return id[0][0]

def createBotuser():
    botUsername = "bot"
    id = select(f"SELECT Id FROM user where Username = \"{botUsername}\"")
    if(len(id) == 0):

        insert("INSERT INTO user (Username, Password, NSFW, Token, CountryId) VALUES (%s,%s,%s,%s,%s)", (botUsername,"",True,"", 1))
        return select(f"SELECT Id FROM user where Username = \"{botUsername}\"")[0][0]
    else:
        return id[0][0]

def createJoke(text, categoryId, userId, nsfw):
    text = text.replace("'","`")
    try:
        querry = f"SELECT Id FROM joke where Text = '{text}'"
    except:
        return False
    id = select(querry)
    if(len(id) == 0):
        try:
            insert("INSERT INTO joke (Text, CategoryId, UserId, NSFW) VALUE (%s,%s,%s,%s)", (text, categoryId, userId, nsfw))
        except:
            return False
        return False
    else:
        return True

botuser = createBotuser()
total = 0

countryFile = open("data/countries.csv")
reader = csv.DictReader(countryFile)

for i in reader:
    code, name = i["\ufeffcountry;name"].split(";")
    id = select(f"SELECT Id FROM country where code = '{code}'")
    if(len(id) == 0):
        insert("INSERT INTO country (CODE, Name) VALUE(%s, %s)", (code, name,))

#programming
programming = newCategory("Programming")
pbar = tqdm(range(20), leave=True)
pbar.set_description(f"Programming")
for i in pbar:
    jokes = get("https://v2.jokeapi.dev/joke/Programming?amount=10")["jokes"]
    for joke in jokes:
        text = ""
        if(joke["type"] == "twopart"):
            text += joke["setup"] + "\n" + joke["delivery"]
        else:
            text += joke["joke"]
        if(createJoke(text, programming, botuser, 0)):
            total += 1
        time.sleep(0.05)


#dark
dark = newCategory("Dark")
pbar = tqdm(range(15), leave=True)
pbar.set_description(f"Dark")
for i in pbar:
    jokes = get("https://v2.jokeapi.dev/joke/Dark?amount=10")["jokes"]
    for joke in jokes:
        text = ""
        if(joke["type"] == "twopart"):
            text += joke["setup"] + "\n" + joke["delivery"]
        else:
            text += joke["joke"]
        if(createJoke(text, dark, botuser, 0)):
            total += 1
        time.sleep(0.05)


#chuck norris
chuck = newCategory("Chuck Norris")
pbar = tqdm(range(50), leave=True)
pbar.set_description(f"Chuck Norris")
for i in pbar:
    text = get("https://api.chucknorris.io/jokes/random")["value"]
    if(createJoke(text, chuck, botuser, 0)):
        total += 1
    time.sleep(0.05)


#general
pbar = tqdm(range(10), leave=True)
pbar.set_description(f"General")
for i in pbar:
    jokes = get("https://official-joke-api.appspot.com/jokes/ten")
    for joke in jokes:
        text = joke["setup"] + "\n" + joke["punchline"]
        category = newCategory(joke["type"])
        if(createJoke(text, category, botuser, 0)):
            total += 1
