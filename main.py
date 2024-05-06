from flask import Blueprint, render_template, request, redirect, url_for
from database import db
from models import User, Workout
from auth import session

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/all_workouts")
def all_workouts():

    # Verifica se o usuário está logado ou não
    if not "current_user_email" in session:
        return redirect(url_for("auth.login"))
    
    # Pegando o usuário e seus exercícios salvos no banco de dados
    current_user_email = session["current_user_email"]
    current_user = User.query.filter_by(email=current_user_email).first_or_404()
    workouts = current_user.workouts

    # Passando as informações a serem carregadas no html como argumento do render_template
    return render_template("main/all_workouts.html", user=current_user, workouts=workouts)

@main.route("/profile")
def profile():

    # Verifica se o usuário está logado ou não
    if not "current_user_email" in session:
        return redirect(url_for("auth.login"))
    
    
    return "Profile Here"

@main.route("/new_workout")
def new_workout():

    # Verifica se o usuário está logado ou não
    if not "current_user_email" in session:
        return redirect(url_for("auth.login"))

    return render_template("main/create_workout.html")

@main.route("/new_workout", methods=["POST"])
def new_workout_post():
    
    # Pegando os dados informados pelo usuário no formulário (método post)
    inputed_pushups = request.form.get("pushups")
    inputed_comment = request.form.get("comment")

    # Tratando possível erro caso o usuário tente enviar palavras ao invés de 
    # números no formulário, não guardando no banco de dados
    if not isinstance(inputed_pushups, int) or inputed_pushups <= 0:
        return render_template("main/create_workout.html")

    # Pegando a instância do usuário
    current_user_email = session["current_user_email"]
    current_user = User.query.filter_by(email=current_user_email).first_or_404()

    # Criando e guardando no banco de dados o exercício realizado
    workout = Workout(pushups=inputed_pushups, comment=inputed_comment, author=current_user)
    db.session.add(workout)
    db.session.commit()

    return render_template("main/create_workout.html")

