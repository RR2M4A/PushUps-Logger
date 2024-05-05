from flask import Blueprint, render_template


main = Blueprint("main", __name__)


@main.route("/")
def home():
    return "Hello world"

@main.route("/profile")
def profile():
    return "Profile Here"

@main.route("/new_workout")
def new_workout():
    return render_template("main/create_workout.html")

@main.route("/new_workout", methods=["POST"])
def new_workout_post():
    return "OKAY"