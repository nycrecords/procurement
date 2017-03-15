from flask import Blueprint

vendor = Blueprint('vendor', __name__, url_prefix='/vendors')

from . import views
