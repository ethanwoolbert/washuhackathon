from flask import Flask, render_template, request
from pymongo import MongoClient

client = MongoClient('mongodb+srv://edwoolbert:h0meisb0ss@cluster0.ejycszy.mongodb.net/?')
db = client['tradewashu']
users = db['users']
posts = db['posts']

for x in posts.find():
    print(x)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = str(request.form.get("username"))
    password = str(request.form.get("password"))

    person = users.find_one({'username': username, 'password': password})

    if person:
        return render_template("site.html", posts=list(reversed([x for x in posts.find()])))

    return render_template('error.html')

@app.route("/sitePage", methods=["POST"])
def sitePage():
    return render_template('site.html', posts=list(reversed([x for x in posts.find()])))

@app.route("/signupPage", methods=["POST"])
def signupPage():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup():
    username = str(request.form.get("username"))
    password = str(request.form.get("password"))
    email = str(request.form.get("email"))

    users.insert_one({'id': [x for x in users.find()][-1]['id'] + 1, 'username': username, 'password': password, 'email': email})

    return render_template("index.html")

@app.route("/changePasswordPage", methods=["POST"])
def chagePasswordPage():
    return render_template("changePassword.html")

@app.route("/changePassword", methods=["POST"])
def changePassword():
    username = str(request.form.get("username"))
    oldPassword = str(request.form.get("oldPassword"))
    newPassword = str(request.form.get("newPassword"))

    person = users.find_one({'username': username, 'password': oldPassword})

    if person:
        id = person['id']
        myquery = {'id': id}
        newvalues = {'$set': {'password': newPassword}}
        users.update_one(myquery, newvalues)
        return render_template('index.html')
    
    return render_template('error.html')

@app.route("/postPage", methods=["POST"])
def postPage():
    return render_template("createPost.html", userId=request.form.get("info"))

@app.route("/createPost", methods=["POST"])
def createPost():
    username = str(request.form.get("username"))
    message = str(request.form.get("message"))

    if [x for x in posts.find()]:
        id = [x for x in posts.find()][-1]['id'] + 1
    else:
        id = 0

    posts.insert_one({'id': id, 'username': username, 'message': message})

    return render_template("site.html", posts=list(reversed([x for x in posts.find()])))

if __name__ == '__main__':
    app.run(use_debugger=False, use_reloader=False, passthrough_errors=True)
