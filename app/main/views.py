"""
.. module:: main.views.

    :synopsis: Handles all core URL endpoints for the procurement application
"""
from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_required, current_user
from app import db
from app.models import Vendor, User
from app.main import main
from app.main.forms import UserForm, EditUserForm
from app.constants import roles


@main.route('/')
def index():
    """Return homepage with a button redirecting to the procurement request form."""
    return render_template('main/index.html')


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
