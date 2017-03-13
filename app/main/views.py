"""
.. module:: Provides url endpoints for the main application

    :synopsis:
"""

from datetime import datetime
from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_required, current_user
from app import db
from app.models import Request, Vendor, User
from app.constants import status
from app.main import main
from app.main.forms import RequestForm, UserForm, EditUserForm
from app.constants import roles


@main.route('/')
def index():
    """Return homepage with a button redirecting to the procurement request form."""
    return render_template('main/index.html')


@main.route('/new_request', methods=['GET', 'POST'])
@login_required
def new_request():
    """Return new request form for procurements."""
    form = RequestForm()

    vendors = Vendor.query.order_by(Vendor.name).all()

    if request.method == 'POST':
        if form.validate_on_submit():
            date_submitted = datetime.now()
            new_request = Request(
                division=current_user.division,
                date_submitted=date_submitted,
                item=form.item.data,
                quantity=form.quantity.data,
                unit_price=form.unit_price.data,
                total_cost=form.total_cost.data,
                funding_source=form.funding_source.data,
                funding_source_description=form.funding_source_description.data,
                justification=form.justification.data,
                status=status.SUB,
                creator_id=current_user.id,
                grant_name=form.grant_name.data,
                project_name=form.project_name.data
            )
            request_vendor_name = str(form.request_vendor_name.data)
            request_vendor_phone = str(form.request_vendor_phone.data)
            request_vendor_fax = str(form.request_vendor_fax.data)
            request_vendor_mwbe = str(form.request_vendor_mwbe.data)

            new_vendor = None
            vendor_form = request.form["vendor"]

            if request_vendor_name != '':
                if request_vendor_mwbe == "None":
                    request_vendor_mwbe = None
                if vendor_form == "default":
                    new_vendor = Vendor(name=request_vendor_name,
                                       address=form.request_vendor_address.data,
                                       phone=request_vendor_phone,
                                       fax=request_vendor_fax,
                                       email=form.request_vendor_email.data,
                                       tax_id=form.request_vendor_taxid.data,
                                       mwbe=request_vendor_mwbe)
                    db.session.add(new_vendor)
                    db.session.commit()
            else:
                print(form.errors)

            if new_vendor is not None:
                new_request.set_vendor_id(new_vendor.id)
            else:
                new_request.set_vendor_id(vendor_form)

            db.session.add(new_request)
            db.session.commit()
            return redirect(url_for('request.display_request', request_id=new_request.id))
        else:
            print(form.errors)

    return render_template('main/new_request.html', form=form, user=current_user, vendors=vendors)


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


@main.route('/parse_vendor', methods=['GET'])
def jsonify_fields():
    if request.args['vendor'] == "default":
        return jsonify("")
    v = Vendor.query.filter_by(id=request.args['vendor']).first()
    return jsonify(v.name, v.address, v.phone, v.fax, v.email, v.tax_id, v.mwbe)


@main.route('/admin_panel', methods=['GET', 'POST'])
@login_required
def admin_panel():
    """Return the admin panel where admins can create users, edit user information, and update login privileges."""
    if not current_user.role == roles.ADMIN:
        return redirect('requests')

    users = User.query.all()
    form = UserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(email=form.email.data,
                            division=form.division.data,
                            password='Change4me',
                            first_name=form.first_name.data,
                            last_name=form.last_name.data)
            db.session.add(new_user)
            db.session.commit()
            flash('User account successfully created!')
            return redirect(url_for('main.admin_panel'))
        else:
            print(form.errors)
    return render_template('main/admin_panel.html', users=users, form=form)


@main.route('/admin_panel/users/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    """Return the page for an admin to update user information."""
    if not current_user.role == roles.ADMIN:
        return redirect('requests')

    form = EditUserForm()
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        if form.validate_on_submit():
            if user.email == form.user_email.data or len(User.query.filter_by(email=form.user_email.data).all()) == 0:
                user_first_name = form.user_first_name.data
                user_last_name = form.user_last_name.data
                user_email = form.user_email.data
                user.first_name = user_first_name
                user.last_name = user_last_name
                user.email = user_email
                db.session.commit()
                flash('User information successfully updated!')
                return render_template('main/edit_user.html', user=user, form=form)
            else:
                flash('User email already exists.')
        else:
            print(form.errors)
    return render_template('main/edit_user.html', user=user, form=form)


@main.route('/admin_panel/users/reset/<int:id>', methods=['GET', 'POST'])
@login_required
def reset_password(id):
    """Resets the password of the user and then redirects to the edit user page."""
    if not current_user.role == roles.ADMIN:
        return redirect('requests')

    user = User.query.get_or_404(id)
    user.password = 'Change4me'
    db.session.commit()
    flash('User password was successfully reset!')
    return redirect(url_for('main.edit_user', id=id))


@main.route('/admin_panel/users/disable/<int:id>', methods=['GET', 'POST'])
@login_required
def disable(id):
    """Disables the user's login privileges and redirects to admin panel page."""
    if not current_user.role == roles.ADMIN:
        return redirect('requests')

    user = User.query.get_or_404(id)
    user.login = False
    db.session.commit()
    flash('User login privileges have been disabled.')
    return redirect(url_for('main.admin_panel'))


@main.route('/admin_panel/users/enable/<int:id>', methods=['GET', 'POST'])
@login_required
def enable(id):
    """Enables the user's login privileges and redirects to admin panel page."""
    if not current_user.role == roles.ADMIN:
        return redirect('requests')

    user = User.query.get_or_404(id)
    user.login = True
    db.session.commit()
    flash('User login privileges have been enabled.')
    return redirect(url_for('main.admin_panel'))
