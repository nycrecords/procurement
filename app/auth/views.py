"""
.. module:: auth.views.

    :synopsis: Provides url endpoints for authentication and user management
"""
from werkzeug.security import generate_password_hash
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.auth import auth
from app.models import User
from app.email_notification import send_email
from app.auth.utils import check_password_requirements
from app.auth.forms import (
    LoginForm,
    ChangePasswordForm,
    PasswordResetRequestForm,
    PasswordResetForm,
    SignupForm
)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Return the login page."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            if user.login is False:
                flash('Your account privileges have been disabled. Please contact an administrator.')
                return redirect(url_for('auth.login'))
            if user is not None and user.verify_password(form.password.data):
                login_user(user)
                return redirect('requests')
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """Logs out user and redirects to homepage."""
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Return page to change password."""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if check_password_requirements(current_user.email,
                                       form.old_password.data,
                                       form.password.data,
                                       form.password2.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            flash('Password must be at least 8 characters with at least 1 UPPERCASE and 1 NUMBER')
    return render_template("auth/change_password.html", form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    """Return page to reset password."""
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email([user.email], 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/request_reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if current_user.is_anonymous:
        signed_in = False
    else:
        signed_in = True
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            if signed_in:
                return redirect(url_for('main.profile'))
            return redirect(url_for('auth.login'))
        else:
            flash('Password must be at least 8 characters with at least 1 UPPERCASE and 1 NUMBER')
    return render_template('auth/reset_password.html', form=form, signed_in=signed_in)


@auth.route('/sign_up', methods=['GET', 'POST'])  # FIX TO ALLOW DIVISON TO BE SELECTED IN FORMS/VIEWS/HTML
def sign_up():
    """Return page to create a new account."""
    form = SignupForm()
    if form.validate_on_submit():
        newuser = User(email=form.email.data,
                       division=form.division.data,
                       password_hash=generate_password_hash(form.password.data),
                       first_name=form.first_name.data,
                       last_name=form.last_name.data)
        db.session.add(newuser)
        flash('User account successfully created!')
        return redirect(url_for('auth.login'))
    return render_template('auth/sign_up.html', form=form)
