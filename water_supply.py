from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
from flask_login import UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey' # csrf
db = SQLAlchemy(app) # start db_session at app runtime

# app.app_context().push()

class UserForm(FlaskForm):
    email = EmailField("User email")
    name = StringField("User name")
    employee_id = StringField("User id")
    submit = SubmitField("Submit")

# Create Form class -> csrf
class NamerForm(FlaskForm):
    name = StringField("label for name", validators=[DataRequired()])
    submit = SubmitField("Submit label")

# create model for database
class Users(db.Model):
    email = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(200))

    # Create a string
    def __repr__(self):
        return '<Name %r>' % self.name

@app.route("/add_user", methods=["POST", "GET"])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data, name=form.name.data).first()
        if user is None:
            new_user = Users(name=form.name.data, email=form.email.data)
            db.session.add(new_user)
            db.session.commit()
    return render_template('add_user.html', form=form)
    
@app.route('/name', methods=["POST", "GET"])
def name():
    # name = None
    form = NamerForm()
    if form.validate_on_submit():
        flash("Form submitted successfully")
        name = form.name.data
        return render_template('test_template.html', form=form, name=name)
    return render_template('test_template.html', form=form)

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

@app.route('/test')
def test_template():
    return render_template('test_template.html')

@app.errorhandler
def page_not_found(e):
    return render_template("404.html"), 404



if __name__=="__main__":
    app.run(debug=True)