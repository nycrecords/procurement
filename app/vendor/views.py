"""
.. module:: vendor.views.

   :synopsis: Provides routes for managing vendor information
"""
from flask import (
    render_template,
    request as flask_request,
    abort,
    Response
)
from app.models import Request, Vendor
from app.vendor import vendor as vendor


@vendor.route('/', methods=['GET'])
def display_vendors():
    """Return page that displays all vendors."""
    vendors = Vendor.query.all()
    if vendors:
        return render_template('vendor/vendors.html', vendors=vendors)
    else:
        abort(404)


@vendor.route('/<vendor_id>', methods=['GET'])
def view_vendor(vendor_id):
    """Return page to view a specific vendor."""
    vendor = Vendor.query.filter_by(id=vendor_id).first()
    if vendor:
        return render_template('vendor/vendor.html', vendor=vendor)
    else:
        abort(404)


@vendor.route('/edit', methods=['POST'])
def edit_edit():
    """Return page to edit vendor information."""
    edit_request = flask_request.form
    request = Request.query.filter_by(id=edit_request['pk']).first()
    request.update_field(
        edit_request['name'],
        edit_request['value'].strip('$')
    )
    return Response(status=200)
