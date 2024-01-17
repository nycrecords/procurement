import os
from datetime import timedelta

from flask import Flask, session, g
from flask_login import current_user, LoginManager
from flask_mail import Mail
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from config import config

# Flask extensions
db = SQLAlchemy()
sess = Session()
mail = Mail()
login_manager = LoginManager()


def create_app(config_name):
    """
    Set up the Flask Application context

    :param config_name: Configuration for specific application context

    :return: Flask application
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    mail.init_app(app)

    # UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app/uploads')
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    sess.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth
    app.register_blueprint(auth, url_prefix="/auth")

    from .request import request
    app.register_blueprint(request)

    from .vendor import vendor
    app.register_blueprint(vendor)

    from .admin import admin
    app.register_blueprint(admin)

    @app.route('/path')
    def path():
        return f"Upload Folder: {app.config['UPLOAD_FOLDER']}"

    @app.before_request
    def before_request():
        session.permanent = False
        app.permanent_session_lifetime = timedelta(minutes=35)
        session.modified = True
        g.user = current_user

    return app

