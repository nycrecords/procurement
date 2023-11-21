import re
import os
from flask import Flask
from .extensions import db, login_manager
from .request import request_bp
from .vendor import vendor as vendor_blueprint
from .user import user as user_blueprint
from .auth import auth as auth_blueprint
from .config import Config
from .models import User
from sqlalchemy.exc import OperationalError


def is_valid_uuid(val):
    regex = re.compile(r'^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}\Z', re.I)
    match = regex.match(val)
    return bool(match)


@login_manager.user_loader
def load_user(user_id):
    try:
        if is_valid_uuid(user_id):
            return User.query.get(user_id)
        else:
            return None
    except OperationalError:
        print("Database connection error occurred.")
        return None


def create_app():
    app = Flask(__name__, template_folder='./templates',
                static_folder='./static')
    app.config.from_object(Config)

    app.secret_key = 'super secret key'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app/uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    app.register_blueprint(request_bp)
    app.register_blueprint(vendor_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(auth_blueprint)

    @app.route('/path')
    def path():
        return f"Upload Folder: {app.config['UPLOAD_FOLDER']}"

    return app
