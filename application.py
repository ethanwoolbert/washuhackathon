from flask import Flask, render_template, request
from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://edwoolbert:h0meisb0ss@cluster0.ejycszy.mongodb.net/?')
db = client['tradewashu']
users = db['users']

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = str(request.form.get("username"))
    password = str(request.form.get("password"))

    person = users.find_one({'username': username, 'password': password})

    posts = [{'username': "mo", 'message': "mo", 'time': "mo"}, {'username': "mo", 'message': "mo", 'time': "mo"}, {'username': "mo",
                                                                                                                    'message': "mo", 'time': "mo"}, {'username': "mo", 'message': "mo", 'time': "mo"}, {'username': "mo", 'message': "mo", 'time': "mo"}]

    if person:
        return render_template("site.html", name=username, posts=posts)

    return render_template('error.html')


@app.route("/signupPage", methods=["POST"])
def signupPage():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup():
    username = str(request.form.get("username"))
    password = str(request.form.get("password"))
    email = str(request.form.get("email"))

    users.insert_one({'id': [x for x in users.find()][-1]['id'] + 1,
                     'username': username, 'password': password, 'email': email})

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


if __name__ == '__main__':
    app.run(use_debugger=False, use_reloader=False, passthrough_errors=True)
