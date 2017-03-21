"""
.. module:: vendor.views.

   :synopsis: Provides routes for managing vendor information
"""
from flask import (
    render_template,
    abort,
    request,
    redirect,
    url_for,
    flash
)
from flask_login import login_required
from app import db
from app.models import Vendor
from app.vendor.forms import NewVendorForm, EditVendorForm
from app.vendor import vendor as vendor
from app.errors import flash_errors


@vendor.route('/', methods=['GET'])
@login_required
def display_vendors():
    """Return page that displays all vendors."""
    vendors = Vendor.query.all()
    if vendors:
        return render_template('vendor/vendors.html', vendors=vendors)
    else:
        abort(404)


@vendor.route('/new', methods=['GET', 'POST'])
@login_required
def new_vendor():
    """Return page to create a new vendor."""
    form = NewVendorForm()
    if request.method == "POST" and form.validate_on_submit():
        vendor_name = str(form.vendor_name.data)
        vendor_address = form.vendor_address.data
        vendor_phone = str(form.vendor_phone.data)
        vendor_fax = str(form.vendor_fax.data)
        vendor_email = form.vendor_email.data
        vendor_tax_id = form.vendor_tax_id.data
        vendor_mwbe = form.vendor_mwbe.data
        new_vendor = Vendor(name=vendor_name,
                            address=vendor_address,
                            phone=vendor_phone,
                            fax=vendor_fax,
                            email=vendor_email,
                            tax_id=vendor_tax_id,
                            mwbe=vendor_mwbe
                            )
        db.session.add(new_vendor)
        db.session.commit()
        flash("Vendor was successfully added!")
        return redirect(url_for('vendor.display_vendors'))

    else:
        flash_errors(form)

    return render_template('vendor/new_vendor.html', form=form)


@vendor.route('/<vendor_id>', methods=['GET'])
@login_required
def view_vendor(vendor_id):
    """Return page to view a specific vendor."""
    vendor = Vendor.query.filter_by(id=vendor_id).first()
    return render_template('vendor/vendor.html', vendor=vendor)


@vendor.route('/edit/<int:vendor_id>', methods=['GET', 'POST'])
@login_required
def edit_vendor(vendor_id):
    """Return page to edit vendor information."""
    vendor = Vendor.query.filter_by(id=vendor_id).first()
    form = EditVendorForm()
    if request.method == "POST" and form.validate_on_submit():
        vendor.name = str(form.vendor_name.data)
        vendor.address = form.vendor_address.data
        vendor.phone = str(form.vendor_phone.data)
        vendor.fax = str(form.vendor_fax.data)
        vendor.email = form.vendor_email.data
        vendor.tax_id = form.vendor_tax_id.data
        vendor.mwbe = form.vendor_mwbe.data
        db.session.commit()
        flash("Vendor information was successfully updated!")
        return redirect(url_for('vendor.display_vendors'))

    else:
        flash_errors(form)

    return render_template('vendor/edit_vendor.html', vendor=vendor, form=form)
