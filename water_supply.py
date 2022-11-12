from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, SubmitField, DateField, SelectField, RadioField
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

class VaultForm(FlaskForm):
    vault_id = StringField("Mã Van")
    vault_position = StringField("Vị Trí")
    start_date = DateField("Ngày bắt đầu")
    end_date = DateField("Ngày kết thúc")
    submit = SubmitField("Tìm kiếm")


class VaultDetailModifyForm(FlaskForm):
    vault_id = StringField("Mã Van")
    vault_diameter = IntegerField("Đường kính")
    vault_model = StringField("Model")
    vault_serial = StringField("Số serial")
    vault_manafacture = StringField("Nhà sản xuất")
    vault_close_rotation = StringField("Chiều đóng van")
    vault_key_size = StringField("Cỡ chìa khóa")
    vault_total_rotation = IntegerField("Tổng số vòng van")
    vault_current_rotation = IntegerField("Số vòng")
    vault_state = SelectField("Trạng thái", choices=["Đóng", "Mở"])
    vault_function = RadioField("Chức năng hiện tại", choices=[('M','Male'),('F','Female')])
    vault_status = SelectField("Tình trạng")
    vault_position = SelectField("Vị trí van")
    close_button = SubmitField("Close")
    update_button = SubmitField("Update")


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

class VaultDetail(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    diameter = db.Column(db.Integer)
    model = db.Column(db.String(20))
    serial = db.Column(db.String(20))
    manafacture = db.Column(db.String(20))
    close_rotation = db.Column(db.String(20))
    key_size = db.Column(db.String(10))
    total_rotation = db.Column(db.Integer)
    current_rotation = db.Column(db.Integer)
    state = db.Column(db.String(20))
    function = db.Column(db.String(20))
    status = db.Column(db.String(20))
    position = db.Column(db.String(20))

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
    form = NamerForm()
    if form.validate_on_submit():
        flash("Form submitted successfully")
        name = form.name.data
        return render_template('test_template.html', form=form, name=name)
    return render_template('test_template.html', form=form)

@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        return redirect(url_for("vault_control"))
    return render_template("user_login.html")

@app.route("/welcome")
def welcome():
    return "Welcome to the first page"

@app.route("/vault_control")
def vault_control():
    form = VaultForm()
    if form.validate_on_submit():
        pass
    return render_template("vault_control.html", form=form)

@app.route("/vault_detail/<int:vault_id>")
def vault_detail(vault_id):
    vault_detail_form = VaultDetailModifyForm()
    return render_template("vault_detail.html", vault_id=vault_id, form=vault_detail_form)

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