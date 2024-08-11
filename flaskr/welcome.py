from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.database import get_database

bp = Blueprint("welcome", __name__, url_prefix="/")

@bp.route("/", methods=("GET", "POST"))
def welcome():
    if request.method == "POST":
        code = request.form["code"]
        return redirect(url_for("timetable.timetable", code=code))


    return render_template("index.html")