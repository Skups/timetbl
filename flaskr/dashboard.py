from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import re

from base64 import urlsafe_b64encode
from random import randbytes

from flaskr.database import get_database
from psycopg.rows import dict_row

from flaskr.auth import login_required

bp = Blueprint("dashboard", __name__)

def get_timetable(timetable, cur):
    classes_grid = [[] for _ in range(5)]
    timetable_id = timetable["id"]
    classes = cur.execute("SELECT * FROM class WHERE timetable_id = (%s)", (timetable_id,)).fetchall()
    max_classes = 0
    for class_ in classes:
        if class_["index"] > max_classes:
            max_classes = class_["index"]
    for i in range(5):
        for _ in range(max_classes+1):
            classes_grid[i].append(0)
    for class_ in classes:
        row = class_["day"]
        i = class_["index"]
        class_["time"] = class_["time"].strftime("%H:%M")
        if not class_["student_id"]:
            class_["student_id"] = "-"
        else:
            student = cur.execute("SELECT * FROM student WHERE id = %s", (class_["student_id"],)).fetchone()
            if student:
                class_["student_id"] = student["name"] + ' ' + student["surname"]
        classes_grid[row][i] = class_

    return (timetable["name"], timetable["id"], max_classes, classes_grid)

@bp.route("/dashboard", methods=("GET", "POST"))
@login_required
def dashboard():
    user_id = session.get("user_id")
    db = get_database()
    timetables_out = []
    with db.cursor(row_factory=dict_row) as cur:
        timetables = cur.execute("SELECT * FROM timetable WHERE teacher_id = (%s)", (user_id,)).fetchall()
        for timetable in timetables:
            timetable_ = get_timetable(timetable, cur)

            timetables_out.append(timetable_)
    return render_template("dashboard/dashboard.html", timetables=timetables_out)

@bp.route("/dashboard/new", methods=("GET", "POST"))
@login_required
def new_timetable():
    if request.method == "POST":
        user_id = session.get("user_id")
        error = None
        timetable = []
        for name, value in request.form.items():
            split = re.match(r"(\d+)(timeInput)(\d+)", name)
            if split:
                day = split.group(1)
                class_i = split.group(3)

                timetable.append((value, 10, class_i, day))
            elif name == "timetableName":
                timetable_name = value

        db = get_database()
        with db.cursor(row_factory=dict_row) as cur:
            if cur.execute("SELECT * FROM timetable WHERE name = %s AND teacher_id = %s", (timetable_name, user_id)).fetchone():
                error = "name already exists"
            else:
                cur.execute("INSERT INTO timetable (id, name, teacher_id) VALUES (%s, %s, %s)", (urlsafe_b64encode(randbytes(8)), timetable_name, user_id))
                timetable_obj = cur.execute("SELECT * FROM timetable WHERE name = %s", (timetable_name,)).fetchone()
                if timetable_obj:
                    timetable_id = timetable_obj["id"]
                cur.executemany("INSERT INTO class (time, duration, index, day, timetable_id) VALUES (%s, %s, %s, %s, %s)",
                                [(time, duration, index, day, timetable_id) for (time, duration, index, day) in timetable])
                db.commit()
                return redirect(url_for("dashboard.dashboard"))

        flash(error)
    return render_template("dashboard/new_timetable.html")

@bp.route("/dashboard/delete/<string:id>", methods=["GET"])
@login_required
def delete_timetable(id):
    db = get_database()
    with db.cursor(row_factory=dict_row) as cur:
        id_from_db = cur.execute("SELECT * FROM timetable WHERE id = %s", (id,))
        if not id_from_db:
            flash("Taky rozvrh neexistuje")
        else:
            cur.execute("DELETE FROM class WHERE timetable_id = %s", (id,))
            cur.execute("DELETE FROM timetable WHERE id = %s", (id,))
            db.commit()
    return redirect(url_for("dashboard.dashboard"))