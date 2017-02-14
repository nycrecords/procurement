"""
.. module:: request.views.

   :synopsis: Provides routes for managing a specific request.
"""
from flask import (
    render_template,
    request as flask_request,
    abort,
    Response,
    redirect,
    url_for
)
from sqlalchemy import update
from flask_login import login_required, current_user
from .. import db
from .forms import RequestForm
from ..models import Request, User, Vendor, Comment
from . import request as request_blueprint


@request_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def display_requests():
    """View the page for all the requests."""
    if current_user.is_admin:
        requests = Request.query.all()
    else:
        requests = Request.query.filter_by(division=current_user.division).all()
    return render_template('request/requests.html',
                           requests=requests
                           )


@request_blueprint.route('/<request_id>', methods=['GET', 'POST'])
def display_request(request_id):
    """View the page for a specific request."""
    request = Request.query.filter_by(id=request_id).first()
    user = User.query.filter_by(id=request.creator_id).first()
    vendor = Vendor.query.filter_by(id=request.vendor_id).first()
    if request:
        return render_template(
                                'request/request.html',
                                request=request,
                                user=user,
                                vendor=vendor
                            )
    else:
        abort(404)


@request_blueprint.route('/edit/<request_id>', methods=['GET', 'POST'])
def edit_request(request_id):
    """Edit a request."""

    if not current_user.is_admin:
        return redirect('requests')

    vendors = Vendor.query.order_by(Vendor.name).all()
    request, user, vendor = db.session.query(Request, User, Vendor).filter(Request.id == request_id).\
                                                    filter(User.id == Request.creator_id).\
                                                    filter(Request.vendor_id == Vendor.id).first()
    form = RequestForm()

    if flask_request.method == 'GET':
        form = RequestForm(item=request.item,
                           quantity=request.quantity,
                           unit_price=request.unit_price,
                           total_cost=request.total_cost,
                           funding_source=request.funding_source,
                           justification=request.justification)

        return render_template('request/edit_request.html',
                               form=form,
                               vendors=vendors,
                               selected_vendor_id=vendor.id,
                               user=user,
                               request=request)

    elif flask_request.method == 'POST':

        # UPDATE DATABASE TO MATCH THE NEW INFORMATION
        request.item = form.item.data
        request.quantity = form.quantity.data
        request.unit_price = form.unit_price.data
        request.total_cost = form.total_cost.data
        request.funding_source = form.funding_source.data
        request.justification = form.justification.data

        # Vendor Stuff
        request_vendor_name = str(form.request_vendor_name.data)
        request_vendor_phone = str(form.request_vendor_phone.data)
        request_vendor_fax = str(form.request_vendor_fax.data)
        request_vendor_mwbe = str(form.request_vendor_mwbe.data)

        newvendor = None
        vendor_form = flask_request.form["vendor"]

        if request_vendor_name != '':
            if request_vendor_mwbe == "None":
                request_vendor_mwbe = None
            if vendor_form == "default":
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
            request.set_vendor_id(newvendor.id)
        else:
            request.set_vendor_id(vendor_form)
        # db.session.add(request)
        db.session.commit()

        return redirect(url_for('request.display_request', request_id=request_id))



    # request.update_field(
    #     edit_request['name'],
    #     edit_request['value'].strip('$')
    # )
    # return Response(status=200)


@request_blueprint.errorhandler(404)
def not_found(error):
    """Return a 404 error page."""
    return render_template('request/not_found.html'), 404


@request_blueprint.errorhandler(400)
def bad_request(error):
    """Return a 400 error page."""
    return render_template('request/bad_request.html'), 400
