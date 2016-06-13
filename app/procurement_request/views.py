"""
.. module:: request.views.

   :synopsis: Provides routes for managing a specific request.
"""
from flask import render_template, request, abort
from .. import db
from ..models import Request, Vendor, Comment
from . import procurement_request as procurement_request_blueprint
from .forms import EditRequestForm


@procurement_request_blueprint.route('/<request_id>', methods=['GET', 'POST'])
def view_request(request_id):
    """View the page for a specific request."""
    procurement_request = Request.query.filter_by(id=request_id).first()
    if procurement_request:
        return render_template('request/request.html',
                               request=procurement_request)
    else:
        abort(404)


@procurement_request_blueprint.route('/edit/<request_id>',
                                     methods=['GET', 'POST'])
def edit_request(request_id):
    """Edit a request."""
    form = EditRequestForm()
    procurement_request = Request.query.filter_by(id=request_id).first()
    if procurement_request:
        if request.method == 'GET':
            vendor = Vendor.query.filter_by(id=request.vendor_id).first()
            form.item.data = procurement_request.item
            form.request_vendor_MWBE.data = vendor.mwbe
            return render_template('procurement_request/edit_request.html',
                                   request=procurement_request,
                                   form=form)
            # TODO: Implement GET handler
        elif request.method == 'POST':
            return str(procurement_request)
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