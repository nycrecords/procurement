from flask import Blueprint

procurement_request = Blueprint('procurement_request',
                                __name__,
                                url_prefix='/requests'
                                )

from . import views
