from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from flask_mail import Mail

mail = Mail()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .request import request as \
        request_blueprint
    app.register_blueprint(request_blueprint,
                           url_prefix='/requests')

    from .vendor import vendor as vendor_blueprint
    app.register_blueprint(vendor_blueprint, url_prefix='/vendor')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
