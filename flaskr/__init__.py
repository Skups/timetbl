import os
from flask import Flask, url_for

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    from . import database
    from . import auth
    from . import welcome
    from . import dashboard
    from . import timetable
    database.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(welcome.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(timetable.bp)

    return app