from flask import Blueprint, render_template, request, redirect, flash, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        email_address = data.get("email_address")
        password = data.get("password")

        user = User.query.filter_by(email_address=email_address).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("You are now logged in", category="success")
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", "error")
        else:
            flash("Invalid email, try again or sign up.", "error")
        

    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You are now logged out.", "success")
    return redirect(url_for("views.home"))

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        data = request.form
        email_address = data.get("email_address")
        first_name = data.get("first_name")
        password1 = data.get("password1")
        password2 = data.get("password2")


        user = User.query.filter_by(email_address=email_address).first()
        if user:
            flash("User already exists, log in instead.", "error")
        elif len(email_address) < 4:
            flash("Email address must be longer than 4 characters.", category="error")
        elif len(first_name) < 1:
            flash("First name must be longer than 1 characters.", category="error")
        elif password1 != password2:
            flash("Passwords must match.", category="error")
        elif len(password1) < 8:
            flash("Password must be at least 8 characters long.", category="error")
        else:
            new_user = User(email_address=email_address, first_name=first_name, password=generate_password_hash(password1, "pbkdf2:sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created!", category="success")
            return redirect(url_for("views.home"))

    return render_template("sign_up.html", user=current_user)