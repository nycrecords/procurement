"""
.. module:: vendor.views.

   :synopsis: Provides routes for managing a specific vendor.
"""

from flask import render_template, request, abort, redirect, url_for
from .. import db
from ..models import Request, User, Vendor, Comment
from . import vendor as vendor_blueprint


@vendor_blueprint.route('/<vendor_id>', methods=['GET'])
def view_vendor(vendor_id):
    vendor = Request.query.filter_by(id=vendor_id).first()
    user = User.query.filter_by(id=request.creator_id).first()
    vendor = Vendor.query.filter_by(id=vendor.vendor_id).first()
    if vendor:
        return render_template(
                                'vendor/request.html',
                                request=request,
                                user=user,
                                vendor=vendor
                            )
    else:
        abort(404)


@vendor_blueprint.route('/edit',
                        methods=['POST'])
def edit_vendor(vendor_id):
    """Edit a vendor."""
    if not request.json or 'name' not in request.json:
        abort(404)

    vendor_id = request.json.get('pk')
    vendor = Vendor.query.filter_by(id=vendor_id)

    vendor.update_field(request.json.get('key'), request.json.get('value'))

    return Response(status=200, format='application/json')
