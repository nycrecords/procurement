from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.urls import url_parse
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from . import auth
from .forms import LoginForm
from ..models import User


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.index'))


@auth.route('/login')
def index():
    form = LoginForm()
    return render_template('auth/login.html', form=form)


@auth.route('/login_form', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('request.new_request'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            # Aquí puedes agregar la opción de "recordarme" si la quieres implementar
            login_user(user, remember=True)
            flash('Logged in successfully.')

            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('request.new_request')
            return redirect(next_page)
        else:
            flash('Invalid username or password.')
            print("Authentication failed.")  # debug message
    else:
        print(form.errors)  # print form errors for debugging
    return render_template('auth/login.html', form=form)
