from flask import Blueprint, render_template, request, redirect, url_for
from database import db
from models import User, Workout
from auth import session

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/all_workouts")
def all_workouts():
    if not "current_user_email" in session:
        return redirect(url_for("auth.login"))
    
    return render_template("main/all_workouts.html")

@main.route("/profile")
def profile():
    if not "current_user_email" in session:
        return redirect(url_for("auth.login"))
    
    
    return "Profile Here"

@main.route("/new_workout")
def new_workout():
    if not "current_user_email" in session:
        return redirect(url_for("auth.login"))

    return render_template("main/create_workout.html")

@main.route("/new_workout", methods=["POST"])
def new_workout_post():
    
    inputed_pushups = request.form.get("pushups")
    inputed_comment = request.form.get("comment")

    current_user_email = session["current_user_email"]
    current_user = User.query.filter_by(email=current_user_email).first()

    workout = Workout(pushups=inputed_pushups, comment=inputed_comment, author=current_user)
    db.session.add(workout)
    db.session.commit()

    return "Ok"

