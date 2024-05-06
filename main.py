from flask import Blueprint, render_template, request, redirect, url_for
from database import db
from models import User, Workout
from auth import session

main = Blueprint("main", __name__)

# --------------------------------- WORKOUTS ----------------------------

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



@main.route("/new_workout")
def new_workout():

    # Verifica se o usuário está logado ou não
    if not "current_user_email" in session:
        return redirect(url_for("auth.login"))

    return render_template("main/create_workout.html")



@main.route("/new_workout", methods=["POST"])
def new_workout_post():
    
    # Verifica se o usuário está logado ou não
    if not "current_user_email" in session:
        return redirect(url_for("auth.login"))

    # Pegando os dados informados pelo usuário no formulário (método post)
    inputed_pushups = request.form.get("pushups")
    inputed_comment = request.form.get("comment")

    # Tratando possível erro caso o usuário tente enviar palavras ao invés de 
    # números no formulário
    try:
        inputed_pushups = int(inputed_pushups)
        if inputed_pushups <= 0:
            raise ValueError
    except ValueError:
        return render_template("main/create_workout.html")

    # Pegando a instância do usuário
    current_user_email = session["current_user_email"]
    current_user = User.query.filter_by(email=current_user_email).first_or_404()

    # Criando e guardando no banco de dados o exercício realizado
    workout = Workout(pushups=inputed_pushups, comment=inputed_comment, author=current_user)
    db.session.add(workout)
    db.session.commit()

    return render_template("main/create_workout.html")



@main.route("/all_workouts/<int:workout_id>/edit", methods=["GET", "POST"])
def edit_workout(workout_id):

    workout = Workout.query.get_or_404(workout_id)

    # Verifica se o usuário está logado ou não
    if not "current_user_email" in session:
        return redirect(url_for("auth.login"))

    if request.method == "GET":
        return render_template("main/edit_workout.html", workout=workout)
    
    elif request.method == "POST":
        
        # Pegando o exercício que estou querendo editar
        inputed_pushups = request.form.get("pushups")
        inputed_comment = request.form.get("comment")

        # Tratando possibilidade de valores inválidos fornecidos pelo usuário
        try:
            inputed_pushups = int(inputed_pushups)
            if inputed_pushups <= 0:
                raise ValueError
        except ValueError:
            return render_template("main/edit_workout.html")
        
        # Fazendo a edição caso esteja tudo OK
        workout.pushups = inputed_pushups
        workout.comment = inputed_comment
        db.session.commit()

        return redirect(url_for("main.all_workouts"))
    


@main.route("/all_workouts/<int:workout_id>/delete", methods=["GET", "POST"])
def delete_workout(workout_id):

    # Verifica se o usuário está logado ou não
    if not "current_user_email" in session:
        return redirect(url_for("auth.login"))

    # Excluindo o workout da base de dados
    workout = Workout.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()

    # Retornando à página
    return redirect(url_for("main.all_workouts"))

# --------------------------------- PROFILE ----------------------------

@main.route("/profile")
def profile():

    # Verifica se o usuário está logado ou não
    if not "current_user_email" in session:
        return redirect(url_for("auth.login"))
    
    
    return "Profile Here"