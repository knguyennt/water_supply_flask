from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app) # start db_session at app runtime

class User(db.Model, UserMixin):
    employee_id = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)

@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        return redirect(url_for("welcome"))
    return render_template("user_login.html")

@app.route("/welcome")
def welcome():
    return "Welcome to the first page"

@app.route("/signin", methods=[])
def signin():
    pass

@app.error_handler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__=="__main__":
    app.run(debug=True)