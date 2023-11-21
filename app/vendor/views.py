from flask import render_template, request, redirect, url_for, flash, current_app
from . import vendor
from .forms import VendorForm
from ..models import Vendor  # Import the Vendor model
from .. import db
from flask_login import login_required, current_user
from sqlalchemy.exc import OperationalError


@vendor.route('/edit_vendor/<vendor_id>', methods=['GET', 'POST'])
@login_required
def edit_vendor(vendor_id):
    vendor_instance = Vendor.query.get_or_404(vendor_id)
    # populate form with vendor instance
    form = VendorForm(obj=vendor_instance)

    if form.validate_on_submit():
        vendor_instance.name = form.vendorName.data
        vendor_instance.address = form.vendorAddress.data
        vendor_instance.phone = form.vendorPhone.data
        vendor_instance.fax = form.vendorFax.data
        vendor_instance.email = form.vendorEmail.data
        vendor_instance.tax_id = form.vendorTaxId.data
        vendor_instance.enabled = form.enable.data
        vendor_instance.mwbe = form.mWbe.data
        db.session.commit()
        flash('Vendor details updated successfully!', 'success')
        return redirect(url_for('vendor.vendors'))

    return render_template('vendor/edit_vendor.html', form=form, vendor=vendor_instance)


@vendor.route('/vendors')
@login_required
def vendors():
    page = request.args.get('page', 1, type=int)
    per_page = 50  # change this to the number of items you want per page
    try:
        vendors = Vendor.query.order_by(Vendor.id).paginate(
            page=page, per_page=per_page, error_out=False)
    except OperationalError:
        # Log the error for debugging
        current_app.logger.error(
            "Database connection error occurred.")  # <-- Change here
        # You can return a custom error message to the user
        return render_template('error.html', message="Unable to fetch vendors due to a database connection issue. Please try again later."), 500
    return render_template('vendor/vendors.html', vendors=vendors)


@vendor.route('/new_vendor', methods=['GET', 'POST'])
@login_required
def new_vendor():
    if request.method == 'POST':
        name = request.form.get('vendorName')
        address = request.form.get('vendorAddress')
        phone = request.form.get('vendorPhone')
        fax = request.form.get('vendorFax')
        email = request.form.get('vendorEmail')
        tax_id = request.form.get('vendorTaxId')
        mwbe = 'mWbe' in request.form

        # Check if name is None
        if name is None:
            flash('Error: Vendor Name is required.', 'danger')
            return redirect(url_for('vendor.new_vendor'))

        new_vendor = Vendor(name=name, address=address, phone=phone,
                            fax=fax, email=email, tax_id=tax_id, mwbe=mwbe)
        db.session.add(new_vendor)
        db.session.commit()

        flash('New vendor added successfully!', 'success')
        return redirect(url_for('vendor.vendors'))

    return render_template('vendor/new_vendor.html')


@vendor.route('/toggle_vendor/<vendor_id>', methods=['POST'])
@login_required
def toggle_vendor(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    vendor.enabled = not vendor.enabled
    db.session.commit()
    return redirect(url_for('vendor.vendors'))
