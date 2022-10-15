from flask import Flask, render_template, request
from pymongo import MongoClient

client = MongoClient('mongodb+srv://edwoolbert:h0meisb0ss@cluster0.ejycszy.mongodb.net/?')
db = client['tradewashu']
users = db['users']
users['username']
users['password']

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    index = 0
    username = str(request.form.get("username"))
    password = str(request.form.get("password"))

    usernames = [x for x in users['username'].find()]
    passwords = [x for x in users['password'].find()]

    for i in range(len(usernames)):
        if usernames[i]['username'] == username:
            index = i

    if passwords[index]['password'] == password:
        idDict = db.execute("SELECT id FROM 'UserInfo' WHERE username=:u", u=username)
        ID = idDict[0]['id']

        return render_template("site.html", name = username, userId = ID)
    else:
        return render_template("error.html")

@app.route("/signupPage", methods=["POST"])
def signupPage():
    return render_template("signup.html")

if __name__ == '__main__':
    app.run(use_debugger=False, use_reloader=False, passthrough_errors=True)

# myquery = { "username": "John" }
# query2 = {"username": "Wayne"}

# users.delete_many(myquery)
# users.delete_many(query2)

# :
#     print(x)

# myquery = { "address": "Park Lane 38" }

# mydoc = mycol.find(myquery)

# for x in mydoc:
#   print(x)

# mylist = [
#   { "name": "Amy", "address": "Apple st 652"},
#   { "name": "Hannah", "address": "Mountain 21"},
#   { "name": "Michael", "address": "Valley 345"},
#   { "name": "Sandy", "address": "Ocean blvd 2"},
#   { "name": "Betty", "address": "Green Grass 1"},
#   { "name": "Richard", "address": "Sky st 331"},
#   { "name": "Susan", "address": "One way 98"},
#   { "name": "Vicky", "address": "Yellow Garden 2"},
#   { "name": "Ben", "address": "Park Lane 38"},
#   { "name": "William", "address": "Central st 954"},
#   { "name": "Chuck", "address": "Main Road 989"},
#   { "name": "Viola", "address": "Sideway 1633"}
# ]

# x = mycol.insert_many(mylist)

# client.close()