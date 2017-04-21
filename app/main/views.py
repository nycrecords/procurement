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
    """Return homepage with a button redirecting to the procurement request history."""
    return render_template('main/index.html')


@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Displays user information (redirects to profile page."""
    return render_template('main/profile.html',
                           current_user=current_user)


@main.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Allows a user to edit their own information"""
    form = EditUserForm(user_role=current_user.role)
    if request.method == 'POST':
        if form.validate_on_submit():
            if current_user.email == form.user_email.data or \
                            len(User.query.filter_by(email=form.user_email.data).all()) == 0:
                user_first_name = form.user_first_name.data
                user_last_name = form.user_last_name.data
                user_role = form.user_role.data
                user_email = form.user_email.data
                user_phone = str(form.user_phone.data)
                user_address = form.user_address.data
                current_user.first_name = user_first_name
                current_user.last_name = user_last_name
                current_user.role = user_role
                current_user.email = user_email
                current_user.phone = user_phone
                current_user.address = user_address
                db.session.commit()
                flash('User information successfully updated!')
                return redirect(url_for('main.profile'))
            else:
                flash('User email already exists.')
        else:
            print(form.errors)
    return render_template('main/edit_user.html', user=current_user, form=form)


@main.route('/profile/reset', methods=['GET', 'POST'])
@login_required
def profile_password_reset():
    token = current_user.generate_reset_token()
    return redirect(url_for('auth.password_reset', token=token))


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
    return jsonify(v.name, v.address, v.phone, v.fax, v.email, v.tax_id, v.mwbe)


@main.route('/manage_users', methods=['GET', 'POST'])
@login_required
def manage_users():
    """Return the admin panel where admins can create users, edit user information, and update login privileges."""
    if not current_user.role == roles.ADMIN:
        return redirect('requests')

    users = User.query.filter(User.id != current_user.id).order_by(User.last_name).all()
    form = UserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(email=form.email.data.lower(),
                            phone=str(form.phone.data),
                            address=form.address.data,
                            division=form.division.data,
                            password='Change4me',
                            first_name=form.first_name.data,
                            last_name=form.last_name.data)
            db.session.add(new_user)
            db.session.commit()
            flash('User account successfully created!')
            return redirect(url_for('main.manage_users'))
        else:
            print(form.errors)
    return render_template('main/manage_users.html', users=users, form=form)


@main.route('/manage_users/users/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    """Return the page for an admin to update user information."""
    if not current_user.role == roles.ADMIN:
        return redirect('requests')

    user = User.query.get_or_404(id)
    form = EditUserForm(user_role=user.role)
    if request.method == 'POST':
        if form.validate_on_submit():
            if user.email == form.user_email.data or len(User.query.filter_by(email=form.user_email.data).all()) == 0:
                user_first_name = form.user_first_name.data
                user_last_name = form.user_last_name.data
                user_role = form.user_role.data
                user_email = form.user_email.data
                user_phone = str(form.user_phone.data)
                user_address = form.user_address.data
                user.first_name = user_first_name
                user.last_name = user_last_name
                user.role = user_role
                user.email = user_email
                user.phone = user_phone
                user.address = user_address
                db.session.commit()
                flash('User information successfully updated!')
                return redirect(url_for('main.manage_users'))
                # return render_template('main/edit_user.html', user=user, current_user=current_user, form=form)
            else:
                flash('User email already exists.')
        else:
            print(form.errors)
    return render_template('main/edit_user.html', user=user, form=form)


@main.route('/manage_users/users/reset/<int:id>', methods=['GET', 'POST'])
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


@main.route('/manage_users/users/disable/<int:id>', methods=['GET', 'POST'])
@login_required
def disable(id):
    """Disables the user's login privileges and redirects to admin panel page."""
    if not current_user.role == roles.ADMIN:
        return redirect('requests')

    user = User.query.get_or_404(id)
    user.login = False
    db.session.commit()
    flash('User login privileges have been disabled.')
    return redirect(url_for('main.manage_users'))


@main.route('/manage_users/users/enable/<int:id>', methods=['GET', 'POST'])
@login_required
def enable(id):
    """Enables the user's login privileges and redirects to admin panel page."""
    if not current_user.role == roles.ADMIN:
        return redirect('requests')

    user = User.query.get_or_404(id)
    user.login = True
    db.session.commit()
    flash('User login privileges have been enabled.')
    return redirect(url_for('main.manage_users'))