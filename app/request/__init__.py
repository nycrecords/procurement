from flask import Blueprint

request = Blueprint('request', __name__, url_prefix='/requests')

from . import views
