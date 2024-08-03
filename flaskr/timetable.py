from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.database import get_database

bp = Blueprint("timetable", __name__)

@bp.route("/timetable/<int:code>", methods=("GET", "POST"))
def timetable(code):
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]

        if not name:
            error = "Name is required"
        elif not surname:
            error = "Surname is required"


    days = 5

    # TODO
    # classes will be an array of tuples (start_time, is_registered)
    classes = ["13:15","13:50","14:25","15:00", "15:35", "16:15", "16:50", "17:25"]

    return render_template("timetable.html", code=code, days=days, classes=classes)