"""
.. module:: vendor.views.

   :synopsis: Provides routes for managing a specific vendor.
"""

from flask import (
    render_template,
    request as flask_request,
    abort,
    Response,
    redirect,
    url_for
)
from .. import db
from ..models import Request, User, Vendor, Comment
from . import vendor as vendor_blueprint


@vendor_blueprint.route('/', methods=['GET'])
def display_vendors():
    """View all vendors."""
    vendors = Vendor.query.all()
    if vendors:
        return render_template('vendor/vendors.html', vendors=vendors)

    else:
        abort(404)


@vendor_blueprint.route('/<vendor_id>', methods=['GET'])
def view_vendor(vendor_id):
    vendor = Vendor.query.filter_by(id=vendor_id).first()
    if vendor:
        return render_template(
            'vendor/vendor.html',
            vendor=vendor
        )
    else:
        abort(404)


@vendor_blueprint.route('/edit', methods=['POST'])
def edit_edit():
    """Edit a vendor."""
    if not flask_request.form or 'name' not in flask_request.form:
        abort(404)

    edit_request = flask_request.form

    if not edit_request:
        abort(404)

    request = Request.query.filter_by(id=edit_request['pk']).first()

    request.update_field(
        edit_request['name'],
        edit_request['value'].strip('$')
    )
    return Response(status=200)
