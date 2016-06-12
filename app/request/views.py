"""
.. module:: request.views.

   :synopsis: Provides routes for managing a specific request.
"""
from flask import render_template, request, abort
from .. import db
from ..models import Request, Vendor, Comment
from . import request
from .forms import EditRequestForm


@request.route('/<request_id>', methods=['GET, POST'])
def view_request(request_id):
    """View the page for a specific request."""
    request = Request.query.filter_by(id=request_id).first()
    if request:
        return render_template('request/request.html', request)
    else:
        abort(404)


@request.route('/edit/<request_id>', methods=['GET, POST'])
def edit_request(request_id):
    """Edit a request."""
    request = Request.query.filter_by(id=request_id).first()
    if request:
        if request.method == 'GET':
            pass
            # TODO: Implement GET handler
        if request.method == 'POST':
            pass
            # TODO: Implement POST handler
        else:
            abort(400)
    else:
        abort(404)


@request.errorhandler(404)
def not_found(error):
    """Return a 404 error page."""
    return render_template('request/not_found.html', 404)


@request.errorhandler(400)
def bad_request(error):
    """Return a 400 error page."""
    return render_template('request/bad_request.html', 400)
