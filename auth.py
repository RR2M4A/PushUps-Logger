from flask import Blueprint, render_template


auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("login_signup/login.html")

@auth.route("/signup")
def signup():
    return render_template("login_signup/signup.html")

@auth.route("/logout")
def logout():
    return "Logout page"