"""
.. module:: Provides url endpoints for the main application

    :synopsis:
"""

from datetime import datetime
from flask import render_template, request, redirect, url_for, jsonify
from .. import db
from ..models import Request, Vendor, User
from . import main
from .forms import RequestForm
from flask_login import login_required, current_user


@main.route('/')
def index():
    """Homepage with button that links to the procurement request form."""
    return render_template('main/index.html')


@main.route('/new', methods=['GET', 'POST'])
@login_required
def new_request():
    """Create a new procurement request."""
    form = RequestForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            date_submitted = datetime.now()
            if current_user.is_authenticated:
                newrequest = Request(
                                     division=current_user.division,
                                     date_submitted=date_submitted,
                                     item=form.item.data,
                                     quantity=form.quantity.data,
                                     unit_price=form.unit_price.data,
                                     total_cost=form.total_cost.data,
                                     funding_source=form.funding_source.data,
                                     funding_source_description=form.funding_source_description.data,
                                     justification=form.justification.data,
                                     creator_id=current_user.id
                                     )
            else:
                newrequest = Request(form.request_name.data,
                                     date_submitted,
                                     form.item.data,
                                 form.quantity.data, form.unit_price.data,
                                 form.total_cost.data, form.funding_source.data,
                                 form.funding_source_description.data, form.justification.data,
                                 creator_id=current_user.id)
            request_vendor_name = str(form.request_vendor_name.data)
            request_vendor_phone = str(form.request_vendor_phone.data)
            request_vendor_fax = str(form.request_vendor_fax.data)
            request_vendor_mwbe = str(form.request_vendor_mwbe.data)

            newvendor = None

            if request_vendor_name != '':
                if request_vendor_mwbe == "None":
                    request_vendor_mwbe = None

                newvendor = Vendor(name=request_vendor_name,
                                   address=form.request_vendor_address.data,
                                   phone=request_vendor_phone,
                                   fax=request_vendor_fax,
                                   email=form.request_vendor_email.data,
                                   tax_id=form.request_vendor_taxid.data,
                                   mwbe=request_vendor_mwbe)
                db.session.add(newvendor)
                db.session.commit()
            else:
                print(form.errors)
            if newvendor is not None:
                newrequest.set_vendor_id(newvendor.id)
            db.session.add(newrequest)
            db.session.commit()
            return redirect(url_for('request.display_request'))
        else:
            print(form.errors)

    return render_template('main/new_request.html', form=form, user=current_user)


@main.route('/divisions', methods=['GET'])
def divisions():
    divisions = {
                    'MRMD': 'MRMD',
                    'Archives': 'Archives',
                    'Grants': 'Grants',
                    'Library': 'Library',
                    'Executive': 'Executive',
                    'MIS/Web': 'MIS/Web',
                    'Administration': 'Administration'
                }

    return jsonify(divisions)
