from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.auth.views import current_user, login_required, admin_required
from app.models import Gig, Role, User
from app import db

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route("/gigs")
def gigs():
	gigs = Gig.query.all()
	return render_template("all_gigs.html", gigs=gigs)

@admin.route("/users")
def users():
	users = User.query.all()
	return render_template("all_users.html", users=users)

@admin.route("/delete-gig/<int:gig_id>", methods=["POST"])
def delete_gig(gig_id):
	gig = Gig.query.get(gig_id)
	if gig:
		flash("The gig \"" + gig.title +  "\" is deleted.", "success")
		db.session.delete(gig)
		db.session.commit()

	if "gig/info" in request.referrer:
		return redirect(url_for("admin.gigs"))
	else:
		return redirect(request.referrer)

@admin.route("/delete-user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
	user = User.query.get(user_id)
	if user:
		flash("The account \"" + user.username +  "\" is deleted.", "success")
		db.session.delete(user)
		db.session.commit()

		if "user/profile" in request.referrer:
			return redirect(url_for("admin.users"))
		else:
			return redirect(request.referrer)

@admin.route('/remove_apply/<int:gig_id>/<int:musician_id>', methods=["POST"])
def remove_gig_application(gig_id, musician_id):
	gig = Gig.query.get(gig_id)
	musician = User.query.get(musician_id)

	if gig and musician:
		musician.remove_application(gig)
		db.session.commit()

		flash("Application of the user \"" + musician.username + "\" is removed from the gig \"" + gig.title + "\"", "success")
		return redirect(request.referrer)

	flash("Something went wrong.", "danger")
	return redirect(request.referrer)

@admin.before_request
@login_required
@admin_required
def check_admin_in_each_view():
	# Print some kind of a log
    print("Admin " + current_user.username + " accessed " + request.url)
