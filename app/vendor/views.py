"""
.. module:: vendor.views.

   :synopsis: Provides routes for managing a specific vendor.
"""

from flask import render_template, request, abort, redirect, url_for
from .. import db
from ..models import Request, User, Vendor, Comment
from . import vendor as vendor_blueprint
from ..main.forms import RequestForm
from .forms import EditVendorForm


@vendor_blueprint.route('/<vendor_id>', methods=['GET', 'POST'])
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


@vendor_blueprint.route('/edit/<vendor_id>',
                        methods=['GET', 'POST'])
def edit_vendor(vendor_id):
    """Edit a vendor."""
    if request.method == 'GET':
        vendor = Vendor.query.filter_by(id=vendor_id).first()
        if vendor:
            form = EditVendorForm(obj=vendor)
        else:
            form = EditVendorForm()
        return render_template('vendor/edit_vendor.html',
                               vendor=vendor,
                               form=form)
        # TODO: Implement GET handler
    elif request.method == 'POST':
        return str(vendor)
        # TODO: Implement POST handler
    else:
        return redirect(url_for('vendor.new_vendor'))
        # abort(400)


@vendor_blueprint.route('/new_vendor/<request_id>')
def new_vendor(request_id):
    """

    :param request_id:
    :return:
    """
    form = EditVendorForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = str(form.name.data)
            phone = str(form.phone.data)
            fax = str(form.fax.data)
            mwbe = str(form.mwbe.data)

            newvendor = None

            if name != '':
                if mwbe == "None":
                    mwbe = None

            newvendor = Vendor(name=name,
                               address=form.address.data,
                               phone=phone,
                               fax=fax,
                               email=form.mail.data,
                               tax_id=form.taxid.data,
                               mwbe=mwbe)
            db.session.add(newvendor)
            db.session.commit()
        else:
            print(form.errors)
        if newvendor is not None:
            request_id.set_vendor_id(newvendor.id)
        db.session.add(newvendor)
        db.session.commit()
        return redirect(url_for('main.display_request'))
    return render_template('vendor/edit_vendor.html', form=form)
