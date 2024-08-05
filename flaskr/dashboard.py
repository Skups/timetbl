from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.database import get_database
from psycopg.rows import dict_row

from flaskr.auth import login_required

bp = Blueprint("dashboard", __name__)


@bp.route("/dashboard", methods=("GET", "POST"))
@login_required
def dashboard():
    user_id = session.get("user_id")
    db = get_database()
    with db.cursor(row_factory=dict_row) as cur:
        timetables = cur.execute("SELECT * FROM timetable WHERE teacher_id = (%s)", (user_id,)).fetchall()
        # for 
        # classes = cur.execute("SELECT * FROM class WHERE id = (%s)", (class_i,))
    print(timetables)


    return render_template("dashboard/dashboard.html", timetables=timetables)

@bp.route("/dashboard/new", methods=("GET", "POST"))
@login_required
def new_timetable():
    if request.method == "POST":
        for value in request.form:
            print(value)

    return render_template("dashboard/new_timetable.html")