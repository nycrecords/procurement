"""
.. module:: request.views.

   :synopsis: Provides routes for managing a specific request.
"""
from flask import render_template, request as flask_request, abort, Response
from flask_login import login_required, current_user
from .. import db
from ..models import Request, User, Vendor, Comment
from . import request as request_blueprint


@request_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def display_request():
    """View the page for all the requests."""
    requests = Request.query.all()
    return render_template('request/requests.html', requests=requests)


@request_blueprint.route('/<request_id>', methods=['GET', 'POST'])
def view_request(request_id):
    """View the page for a specific request."""
    request = Request.query.filter_by(id=request_id).first()
    user = User.query.filter_by(id=request.creator_id).first()
    vendor = Vendor.query.filter_by(id=request.vendor_id).first()
    if request:
        return render_template(
                                'request/request.html',
                                request=request,
                                user=user,
                                vendor=vendor
                            )
    else:
        abort(404)


@request_blueprint.route('/edit', methods=['POST'])
def edit_request():
    """Edit a request."""
    if not flask_request.json or 'name' not in flask_request.json:
        abort(404)

    edit_request = flask_request.get_json()

    if not edit_request:
        abort(404)

    request = edit_request['pk']

    request.update_field(edit_request['name'], edit_request['value'])

    return Response(status=200, format='application/json')


@request_blueprint.errorhandler(404)
def not_found(error):
    """Return a 404 error page."""
    return render_template('request/not_found.html'), 404


@request_blueprint.errorhandler(400)
def bad_request(error):
    """Return a 400 error page."""
    return render_template('request/bad_request.html', 400)
