"""
.. module:: Provides url endpoints for authentication and user management

    :synopsis:
"""


from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm, ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm
from .utils import check_password_requirements


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Login page for user login."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect('new')
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """Logout"""
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Password change page"""
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
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/request_reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            flash('Password must be at least 8 characters with at least 1 UPPERCASE and 1 NUMBER')
    return render_template('auth/reset_password.html', form=form)
