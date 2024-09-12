"""
.. module:: __init__.

    :synopsis: Sets up the procurement application
"""
from datetime import timedelta

from flask import Flask, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, LoginManager
from flask_session import Session
from flask_mail import Mail
from config import config

mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
sess = Session()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    db.init_app(app)
    sess.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .request import request as request
    app.register_blueprint(request, url_prefix='/requests')

    from .vendor import vendor as vendor
    app.register_blueprint(vendor, url_prefix='/vendors')

    from .auth import auth as auth
    app.register_blueprint(auth, url_prefix='/auth')

    @app.before_request
    def before_request():
        session.permanent = False
        app.permanent_session_lifetime = timedelta(minutes=35)
        session.modified = True
        g.user = current_user

    return app
