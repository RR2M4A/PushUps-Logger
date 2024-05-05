from flask import Blueprint, render_template, url_for, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
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

    db_user = User.query.filter_by(email=inputed_email).first()

    # Verificando se o usuário não existe no banco de dados ou se a senha está incorreta
    if not db_user or not check_password_hash(db_user.password, inputed_password):
        return render_template("login_signup/login.html")
        
    # Com usuário e senha válidos, será enviado à página home
    session["current_user_email"] = inputed_email
    return redirect(url_for("main.all_workouts"))
        
#---------------------- SIGNUP ----------------------

@auth.route("/signup")
def signup():
    return render_template("login_signup/signup.html")



@auth.route("/signup", methods=["POST"])
def signup_post():

    inputed_name = request.form.get("name")
    inputed_email = request.form.get("email")
    inputed_password = request.form.get("password")

    db_user = User.query.filter_by(email=inputed_email).first()

    # Verificando se o usuário já existe no banco de dados
    if db_user:
        return render_template("login_signup/signup.html")
        
    # Criação do usuário
    new_user = User(email=inputed_email, password=generate_password_hash(inputed_password), name=inputed_name)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))

#---------------------- LOGOUT ----------------------

@auth.route("/logout")
def logout():
    if not "current_user_email" in session:
        return redirect(url_for("auth.login"))
    
    session.pop("current_user_email")
    return redirect(url_for("auth.login"))