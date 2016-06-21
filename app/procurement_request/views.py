"""
.. module:: request.views.

   :synopsis: Provides routes for managing a specific request.
"""
from flask import render_template, request, abort, redirect, url_for
from .. import db
from ..models import Request, User, Vendor, Comment
from . import procurement_request as procurement_request_blueprint
from .forms import EditRequestForm
from flask_login import login_required, current_user

@procurement_request_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def display_request():
    """View the page for all the requests."""
    requests = Request.query.all()
    return render_template('procurement_request/requests.html', requests=requests)


@procurement_request_blueprint.route('/<request_id>', methods=['GET', 'POST'])
def view_request(request_id):
    """View the page for a specific request."""
    procurement_request = Request.query.filter_by(id=request_id).first()
    user = User.query.filter_by(id=procurement_request.creator_id).first()
    vendor = Vendor.query.filter_by(id=procurement_request.vendor_id).first()
    if procurement_request:
        return render_template(
                                'procurement_request/request.html',
                                request=procurement_request,
                                user=user,
                                vendor=vendor
                            )
    else:
        abort(404)


# TODO: Convert to API Endpoint
@procurement_request_blueprint.route('/edit/<request_id>',
                                     methods=['GET', 'POST'])
def edit_request(request_id):
    """Edit a request."""
    procurement_request = Request.query.filter_by(id=request_id).first()
    if procurement_request:
        if request.method == 'GET':
            form = EditRequestForm(obj=procurement_request)
            return render_template('procurement_request/edit_request.html',
                                   request=procurement_request,
                                   form=form)
            # TODO: Implement GET handler
        elif request.method == 'POST':
            # return str(procurement_request)
            return redirect(url_for('main.display_request'))
            # TODO: Implement POST handler
        else:
            abort(400)
    else:
        abort(404)


@procurement_request_blueprint.errorhandler(404)
def not_found(error):
    """Return a 404 error page."""
    return render_template('request/not_found.html', 404)


@procurement_request_blueprint.errorhandler(400)
def bad_request(error):
    """Return a 400 error page."""
    return render_template('request/bad_request.html', 400)
