from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.database import get_database
from psycopg.rows import dict_row

from flaskr.dashboard import get_timetable

bp = Blueprint("timetable", __name__)

@bp.route("/timetable/<string:code>", methods=("GET", "POST"))
def timetable(code: str):
    if request.method == "POST":
        error = None
        name = request.form["name"]
        surname = request.form["surname"]
        chosen_classes = []
        for class_ in request.form:
            if class_ != "name" and class_ != "surname":
                chosen_classes.extend(class_.split(","))
        for i in range(4):
            chosen_classes[i] = int(chosen_classes[i])
        print(chosen_classes)

        if not name:
            error = "Meno je povinné"
        elif not surname:
            error = "Priezvisko je povinné"
        elif len(chosen_classes) != 4:
            error = "Vyberte 2 hodiny"

        if not error:
            db = get_database()
            with db.cursor(row_factory=dict_row) as cur:
                cur.execute("INSERT INTO student (username, password, name, surname) VALUES (%s, %s, %s, %s)", (name+surname, 0, name, surname))
                db.commit()
                student = cur.execute("SELECT * FROM student WHERE username=(%s)", (name+surname,)).fetchone()
                if student:
                    cur.execute("UPDATE class SET student_id=(%s) WHERE day=(%s) AND index=(%s)", (student["id"], chosen_classes[0], chosen_classes[1]))
                    cur.execute("UPDATE class SET student_id=(%s) WHERE day=(%s) AND index=(%s)", (student["id"], chosen_classes[2], chosen_classes[3]))
                    db.commit()
                else:
                    flash("Skúste znova")
                    return redirect(url_for("welcome.welcome"))
            flash("Hodiny úspešne zaregistrované")
            return redirect(url_for("welcome.welcome"))
        flash(error)

    db = get_database()
    with db.cursor(row_factory=dict_row) as cur:
        timetable = cur.execute("SELECT * FROM timetable WHERE id = %s", (code,)).fetchone()
        if not timetable:
            flash("Tento rozvrh neexistuje")
            return redirect(url_for("welcome.welcome"))

        timetable_out = get_timetable(timetable, cur)
    return render_template("timetable.html", code=code, timetable=timetable_out)