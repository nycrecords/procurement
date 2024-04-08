"""
.. module:: main.views.

    :synopsis: Handles all core URL endpoints for the procurement application
"""
from flask import render_template, request, redirect, url_for, jsonify, flash, session
from flask_login import login_required, current_user

from app import db, login_manager
from app.constants import roles
from app.db_utils import update_user_information
from app.main import main
from app.main.forms import EditUserForm
from app.models import Vendor, User


@login_manager.user_loader
def user_loader(guid: str) -> User:
    user = User.query.filter_by(guid=guid).one_or_none()
    if user is not None and user.session_id == session.sid:
        return user


@main.route('/')
def index():
    """Return homepage with a button redirecting to the procurement request history."""
    if current_user.is_authenticated:
        duplicate_session = request.args.get('duplicate_session')
        return redirect(url_for('request.index', duplicate_session=duplicate_session))
    return render_template('main/index.html')


@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Displays user information (redirects to profile page)."""
    return render_template('main/profile.html', current_user=current_user)


@main.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Allows a user to edit their own information"""
    user = User.query.get_or_404(current_user.id)
    form = EditUserForm(role=current_user.role, division=current_user.division)

    if request.method == 'POST':
        if form.validate_on_submit():
            fields = ['phone', 'address']
            if current_user.role == roles.ADMIN:
                fields.extend(['role', 'division'])
            update_user_information(form, fields, user)
    return render_template('main/edit_user.html', user=current_user, form=form)


@main.route('/divisions', methods=['GET'])
def divisions():
    divisions = {
        'MRMD': 'MRMD',
        'Archives': 'Archives',
        'Grants': 'Grants',
        'Library': 'Library',
        'Executive': 'Executive',
        'Tech': 'Tech',
        'Administration': 'Administration'
    }
    return jsonify(divisions)


@main.route('/parse_vendor', methods=['GET'])
def jsonify_fields():
    if request.args['vendor'] == "default":
        return jsonify("")
    v = Vendor.query.filter_by(id=int(request.args['vendor'])).first()
    if not v:
        return jsonify("Vendor not found"), 404
    return jsonify(v.name, v.address, v.phone, v.fax, v.email, v.tax_id, v.mwbe)


@main.route('/manage_users', methods=['GET', 'POST'])
@login_required
def manage_users():
    """Return the admin panel where admins can create users, edit user information, and update login privileges."""
    if not current_user.role == roles.ADMIN:
        return redirect(url_for('main.index'))

    users = User.query.filter(User.id != current_user.id).order_by(User.last_name).all()
    return render_template('main/manage_users.html', users=users)


@main.route('/manage_users/users/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    """Return the page for an admin to update user information."""
    if current_user.role != roles.ADMIN:
        return redirect(url_for('main.edit_profile'))

    user = User.query.get_or_404(id)
    form = EditUserForm(role=user.role, division=user.division)

    if request.method == 'POST':
        if form.validate_on_submit():
            fields = ['role', 'division', 'phone', 'address']
            update_user_information(form, fields, user)

    return render_template('main/edit_user.html', user=user, form=form)


@main.route('/manage_users/users/disable/<int:id>', methods=['GET', 'POST'])
@login_required
def disable(id):
    """Disables the user's login privileges and redirects to admin panel page."""
    if not current_user.role == roles.ADMIN:
        return redirect('requests')

    user = User.query.get_or_404(id)
    user.is_active = False
    db.session.commit()
    flash('User login privileges have been disabled.', category="success")
    return redirect(url_for('main.manage_users'))


@main.route('/manage_users/users/enable/<int:id>', methods=['GET', 'POST'])
@login_required
def enable(id):
    """Enables the user's login privileges and redirects to admin panel page."""
    if not current_user.role == roles.ADMIN:
        return redirect('requests')

    user = User.query.get_or_404(id)
    user.is_active = True
    db.session.commit()
    flash('User login privileges have been enabled.', category="success")
    return redirect(url_for('main.manage_users'))


@main.route('/active', methods=['POST'])
def active():
    """
    Extends a user's session.
    :return:
    """
    session.modified = True
    return 'OK'
