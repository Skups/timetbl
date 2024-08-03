from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.database import get_database

bp = Blueprint("welcome", __name__, url_prefix="/")

@bp.route("/", methods=("GET", "POST"))
def welcome():
    if request.method == "POST":
        code = request.form["code"]

        db = get_database()
        error = None

        if not code:
            error = "Code is required"
        

        # TODO
        # 'code' has to correspond to an existing one from the database

        if error is None:
            # print(url_for("timetable.timetable")+f'/{code}')
            return redirect(url_for("timetable.timetable",code=code))
        
        flash(error)

    return render_template("index.html")