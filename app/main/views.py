from datetime import datetime
from flask import render_template, request
from .. import db
from ..models import Request, Vendor
from . import main
from .forms import NewRequestForm


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/new', methods=['GET', 'POST'])
def new_request():
    form = NewRequestForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            date_submitted = datetime.now()

            newrequest = Request(form.request_name.data, date_submitted, form.item.data,
                                 form.quantity.data, form.unit_price.data,
                                 form.total_cost.data, form.funding_source.data,
                                 form.funding_source_description.data, form.justification.data
                                 )
            db.session.add(newrequest)
            db.session.commit()

            request_vendor_phone = str(form.request_vendor_phone.data)
            request_vendor_fax = str(form.request_vendor_fax.data)
            request_vendor_mwbe = str(form.request_MWBE.data)
            request_vendor_name = str(form.request_vendor_name.data)

            if request_vendor_name != '':
                if request_vendor_mwbe == "None":
                    request_vendor_mwbe = None

                newvendor = Vendor(request_vendor_name, form.request_vendor_address.data,
                                   request_vendor_phone, request_vendor_fax,
                                   form.request_vendor_email.data, form.request_vendor_taxid.data,
                                   request_vendor_mwbe, request_id=newrequest.id)
                db.session.add(newvendor)
                db.session.commit()

        else:
            print form.errors

    return render_template('new_request.html', form=form)


@main.route('/requests', methods=['GET'])
def display_request():
    """Display Procurement requests stored in db"""
    requests = Request.query.all()
    return render_template('display_request.html', requests=requests)