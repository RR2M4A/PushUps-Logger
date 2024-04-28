from flask import Blueprint, render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash
from models import Users
from database import db


auth = Blueprint("auth", __name__)


#---------------------- LOGIN ----------------------

@auth.route("/login")
def login():
    return render_template("login_signup/login.html")

@auth.route("/login", methods=["POST"])
def login_post():

    inputed_email = request.form.get("email")
    inputed_password = request.form.get("password")

    db_user = Users.query.filter_by(email=inputed_email).first()

    # Verificando se o usuário existe ou não no banco de dados
    if db_user:
        pass
        
    return render_template("login_signup/login.html")

#---------------------- SIGNUP ----------------------

@auth.route("/signup")
def signup():
    return render_template("login_signup/signup.html")

@auth.route("/signup", methods=["POST"])
def signup_post():

    inputed_name = request.form.get("name")
    inputed_email = request.form.get("email")
    inputed_password = request.form.get("password")

    db_user = Users.query.filter_by(email=inputed_email).first()

    # Verificando se o usuário já existe ou não no banco de dados
    if db_user:
        return render_template("login_signup/signup.html")
        
    # Criando o usuário e salvando no banco de dados caso ele não exista
    new_user = Users(email=inputed_email, password=generate_password_hash(inputed_password), name=inputed_name)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))

#---------------------- LOGOUT ----------------------

@auth.route("/logout")
def logout():
    return "Logout page"