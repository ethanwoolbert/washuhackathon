from flask import Flask, render_template, request
from pymongo import MongoClient

client = MongoClient('mongodb+srv://edwoolbert:h0meisb0ss@cluster0.ejycszy.mongodb.net/?')
db = client['tradewashu']
users = db['users']
posts = db['posts']

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/landingPage", methods=["POST"])
def landingPage():
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

    if users.find_one({'username': username}):
        return render_template("error.html")

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

@app.route("/forgotPasswordPage", methods=["POST"])
def forgotPasswordPage():
    return render_template("forgotPassword.html", message="")

@app.route("/forgotPassword", methods=["POST"])
def forgotPassword():
    username = str(request.form.get("username"))
    email = str(request.form.get("email"))

    person = users.find_one({'username': username, 'email': email})

    if person:
        message = 'Password: ' + person['password']
    else:
        message = 'That username/email combination does not exist.'

    return render_template("forgotPassword.html", message=message)

@app.route("/postPage", methods=["POST"])
def postPage():
    return render_template("createPost.html", userId=request.form.get("info"))

@app.route("/createPost", methods=["POST"])
def createPost():
    title = str(request.form.get("title"))
    username = str(request.form.get("username"))
    message = str(request.form.get("message"))
    image = str(request.form.get("image"))

    if [x for x in posts.find()]:
        id = [x for x in posts.find()][-1]['id'] + 1
    else:
        id = 0

    posts.insert_one({'id': id, 'title': title,'username': username, 'message': message, 'ip': request.remote_addr, 'image': image})

    return render_template("site.html", posts=list(reversed([x for x in posts.find()])))

if __name__ == '__main__':
    app.run(use_debugger=False, use_reloader=False, passthrough_errors=True)
