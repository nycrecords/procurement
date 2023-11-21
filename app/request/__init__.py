from flask import Blueprint

request_bp = Blueprint('request', __name__)

from . import views   # This will import views.py where you will use request_bp
