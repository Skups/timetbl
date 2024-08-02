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

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    
    from . import database
    database.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import welcome
    app.register_blueprint(welcome.bp)

    @app.route("/")
    def default_redirect():
        return app.redirect(url_for("home"))
    
    return app