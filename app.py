from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt

app = Flask(__name__)

#------------------------------------DATABASE MANAGEMENT---------------------------------------------------------------------

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///sampledb.sqlite3"

db = SQLAlchemy(app)

app.app_context().push()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    users_id = db.Column(db.String(), unique = True, nullable = False)
    password = db.Column(db.String(256), unique = True, nullable = False)
    first_name = db.Column(db.String(), nullable = False)
    last_name = db.Column(db.String())
    phone_no = db.Column(db.String(10), nullable = False)
    security_question = db.Column(db.String(), nullable = False)
    security_answer = db.Column(db.String(),unique = True, nullable = False)

#-----------------------------------Routes-------------------------------------------------------------------------------------

@app.route('/', methods = ['GET', 'POST'])
def log_in():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        existing_user = db.session.query(Users).filter(Users.users_id == username).first()
        if existing_user:
            if sha256_crypt.verify(password, existing_user.password):
                return render_template("home.html", user = existing_user)
            else:
                return render_template("form.html", message = "Incorrect Password")
        else:
            return render_template("form.html", message = "No User Found")
    return render_template("form.html")

@app.route('/password', methods = ['GET', 'POST'])
def forgotten_password():
    if request.method == 'POST':
        username = request.form.get("username")
        existing_user = db.session.query(Users).filter(Users.users_id == username).first()
        if existing_user:
            return render_template("password.html", user = existing_user)
        else:
            return render_template("password.html", message = "Invalid User ID", user = None)
    return render_template("password.html", user = None)

@app.route('/question', methods = ['GET', 'POST'])
def question():
    if request.method == 'POST':
        ques = request.form.get("question")
        ans = request.form.get("answer")
        existing_user = db.session.query(Users).filter(Users.security_answer == ans).first()
        if(existing_user):
            return render_template("home.html", user = existing_user)
        else:
            return render_template("password.html", message = "Incorrect Security Answer", user = None)

@app.route('/create', methods = ['GET', 'POST'])
def create():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        password = request.form.get("password")
        password = sha256_crypt.encrypt(password)
        f_name = request.form.get("first_name")
        l_name = request.form.get("last_name")
        ph_no = request.form.get("phone_no")
        ques = request.form.get("security_question")
        ans = request.form.get("security_answer")
        new_user = Users(users_id = user_id, password = password, first_name = f_name, last_name = l_name, phone_no = ph_no, security_question = ques, security_answer = ans)
        try:
            db.session.add(new_user)
            db.session.commit()
            return render_template("form.html", message = "Registration Successful, New User Created")
        except:
            return render_template("form.html", message = "Resgistration Unsuccessful, Use Different User ID Try Again")
    return render_template("create.html")

if __name__ == "__main__":
    app.run(debug = True)