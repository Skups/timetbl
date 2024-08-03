import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.database import get_database

from psycopg.rows import dict_row

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_database()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
            
        if error is None:
            
            try:
                with db.cursor() as cur:
                    is_name_taken = cur.execute("SELECT * FROM teacher WHERE username = (%s)", (username,)).fetchall()
                    # print(is_name_taken)
                    if is_name_taken is None:
                        cur.execute("INSERT INTO teacher (username, password) VALUES (%s, %s)", (username, generate_password_hash(password)))
                        db.commit()
                    else:
                        error = f"User {username} is already registered."
                        flash(error)
                        return render_template("auth/register.html")
                        
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))
            
        flash(error)
    
    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        in_username = request.form["username"]
        in_password = request.form["password"]
        db = get_database()
        error = None

        with db.cursor(row_factory=dict_row) as cur:
            user = cur.execute(
                "SELECT * FROM teacher WHERE username = %s", (in_username,)
            ).fetchone()

        if user is None:
            error = "User does not exist."
        elif not check_password_hash(user["password"], in_password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            assert user is not None
            session["user_id"] = user["id"]
            return redirect(url_for("welcome.welcome"))
        
        flash(error)

    return render_template("/auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_database().execute(
            "SELECT * FROM teacher WHERE id = %s", (user_id,)
        ).fetchone()


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        
        return view(**kwargs)
    
    return wrapped_view

