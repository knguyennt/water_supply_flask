from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, SubmitField, DateField, SelectField, RadioField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey' # csrf
db = SQLAlchemy(app) # start db_session at app runtime

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
    vault_size = IntegerField("Cỡ Van")
    vault_dma = StringField("DMA")
    vault_total_round = IntegerField("Tổng số vòng")
    vault_current_round = IntegerField("Vòng mở")
    vault_status = SelectField("Trạng thái", choices=["Đóng", "Mở"])
    vault_type = RadioField("Chức năng hiện tại", choices=[('Biên','Biên'),('Bước','Bước'), ('Tổng', 'Tổng')])
    vault_position = SelectField("Vị trí van", choices=["Dưới Nhựa", "Trên Lề"])
    vault_address = StringField("Địa chỉ")
    vault_cooperate_team = StringField("Đơn vị phối hợp")
    vault_conductor = StringField("Người thực hiện")
    vault_requirer = StringField("Người đề xuất")
    update_button = SubmitField("Update")


# Create Form class -> csrf
class NamerForm(FlaskForm):
    name = StringField("label for name", validators=[DataRequired()])
    submit = SubmitField("Submit label")

class AffectedAddressForm(FlaskForm):
    vault_id = StringField("Tra cứu danh bạ ảnh hưởng với mã van")
    submit = SubmitField("Submit")

# create model for database
class Users(db.Model):
    email = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(200))

    # Create a string
    def __repr__(self):
        return '<Name %r>' % self.name

class WardTable(db.Model):
    city_name = db.Column(db.String(50))
    ward_name = db.Column(db.String(50), primary_key=True)

class DistrictTable(db.Model):
    city_name = db.Column(db.String(50))
    district_name = db.Column(db.String(50), primary_key=True)

class VaultPosition(db.Model):
    vault_position = db.Column(db.String(20), primary_key=True)

class VaultDMA(db.Model):
    vault_dma = db.Column(db.String(20), primary_key=True)

class VaultType(db.Model):
    vault_type = db.Column(db.String(20), primary_key=True)

class CooperateTeam(db.Model):
    team_name = db.Column(db.String(50), primary_key=True)

class VaultStatus(db.Model):
    vault_status = db.Column(db.String(20), primary_key=True)

class Conductor(db.Model):
    conductor = db.Column(db.String(50),primary_key=True)

class Requirer(db.Model):
    requirer_name = db.Column(db.String(50), primary_key=True)

# class affected_address(db.Model):
#     vault_address = db.Column(db.String(50), primary_key=True)
#     vault_id = db.Column(db.String(20))

class VaultDetail(db.Model):
    vault_id = db.Column(db.String(20), primary_key=True)
    vault_dma = db.Column(db.String(20), db.ForeignKey(VaultDMA.vault_dma))
    vault_size = db.Column(db.Integer)
    vault_type = db.Column(db.String(20), db.ForeignKey("vault_type.vault_type")) # Chức năng van
    vault_position = db.Column(db.String(20), db.ForeignKey("vault_position.vault_position")) # Trên lề, dưới nhựa
    vault_total_round = db.Column(db.Integer) # Tổng số vòng van
    vault_current_round = db.Column(db.Integer) # Vòng van hiện tại
    vault_address = db.Column(db.String(50))
    vault_client = db.Column(db.String(20))
    vault_directorhy = db.Column(db.String(20))
    vault_cooperate_team = db.Column(db.String(20), db.ForeignKey("cooperate_team.team_name")) # Đơn vị phối hợp
    vault_conductor = db.Column(db.String(20), db.ForeignKey(Conductor.conductor)) # Người thực hiện
    vault_requirer = db.Column(db.String(20), db.ForeignKey(Requirer.requirer_name)) # người đề xuất
    vault_status = db.Column(db.String(20), db.ForeignKey(VaultStatus.vault_status))


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

@app.route("/vault_control", methods=["GET", "POST"])
def vault_control():
    form = VaultForm()
    field_map = {
        'vault_id': 'vault_id',
        'vault_position': 'vault_address'
    }
    if form.is_submitted():
        filter_dict = dict()
        for field_name, data in form.data.items():
            if data and field_name != "submit" and field_name != "csrf_token" and field_name != "end_date" and field_name != "start_date":
                filter_dict[field_map[field_name]] = data
        vault_filter = VaultDetail.query.filter_by(**filter_dict).all()
        if form.start_date.data:
            if form.end_date.data:
                vault_filter = VaultDetail.query.filter_by(**filter_dict).filter(VaultDetail.vault_operation_date >= form.start_date.data).filter(VaultDetail.vault_operation_date <= form.start_date.data)
            else:
                vault_filter = VaultDetail.query.filter_by(**filter_dict).filter_by(vault_operation_date = form.start_date.data)
    else:
        vault_filter = VaultDetail.query.all()
    return render_template("vault_control.html", form=form, vault_filter=vault_filter)


@app.route("/vault_detail/<string:vault_id>", methods=["GET", "POST"])
def vault_detail(vault_id):

    vault_detail_form = VaultDetailModifyForm()
    vault_detail = VaultDetail.query.filter_by(vault_id=vault_id).first()
    if vault_detail_form.validate_on_submit():
        vault_detail.vault_id = vault_detail_form.vault_id.data
        vault_detail.vault_dma = vault_detail_form.vault_dma.data
        vault_detail.vault_size = vault_detail_form.vault_size.data
        vault_detail.vault_type = vault_detail_form.vault_type.data
        vault_detail.vault_position = vault_detail_form.vault_position.data
        vault_detail.vault_total_round = vault_detail_form.vault_total_round.data
        vault_detail.vault_current_round = vault_detail_form.vault_current_round.data
        vault_detail.vault_address = vault_detail_form.vault_address.data
        vault_detail.vault_cooperate_team = vault_detail_form.vault_cooperate_team.data
        vault_detail.vault_conductor = vault_detail_form.vault_conductor.data
        vault_detail.vault_requirer = vault_detail_form.vault_requirer.data
        vault_detail.vault_status = vault_detail_form.vault_status.data
        db.session.commit()

    # add default value here
    vault_detail_form.vault_id.default = vault_detail.vault_id
    vault_detail_form.vault_dma.default = vault_detail.vault_dma
    vault_detail_form.vault_size.default = vault_detail.vault_size
    vault_detail_form.vault_type.default = vault_detail.vault_type
    vault_detail_form.vault_position.default = vault_detail.vault_position
    vault_detail_form.vault_total_round.default = vault_detail.vault_total_round
    vault_detail_form.vault_current_round.default = vault_detail.vault_current_round
    vault_detail_form.vault_address.default = vault_detail.vault_address
    vault_detail_form.vault_cooperate_team.default = vault_detail.vault_cooperate_team
    vault_detail_form.vault_conductor.default = vault_detail.vault_conductor
    vault_detail_form.vault_requirer.default = vault_detail.vault_requirer
    vault_detail_form.vault_status.default = vault_detail.vault_status
    vault_detail_form.process()
    # end adding default value
    return render_template("vault_detail.html", vault_id=vault_id, form=vault_detail_form, vault_detail=vault_detail)

@app.route("/vault_report", methods=["GET", "POST"])
def vault_report():
    form = AffectedAddressForm()
    affected_address_filter = None

    affected_filter = VaultDetail.query.filter(VaultDetail.vault_status == "Đóng").with_entities(VaultDetail.vault_id, VaultDetail.vault_address)
    affected_address = [(id, address) for id, address in affected_filter]
    
    if form.is_submitted():
        search_affected_address_filter = VaultDetail.query.filter(VaultDetail.vault_id==form.vault_id.data.strip()).with_entities(VaultDetail.vault_address)
        affected_address_filter = [address[0] for address in search_affected_address_filter]

    return render_template("vault_report.html", affected_address=affected_address, form=form, affected_address_filter=affected_address_filter)

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