"""
.. module:: auth.views.

    :synopsis: Provides url endpoints for authentication and user management
"""
from datetime import datetime

from flask import render_template, redirect, url_for, flash, request, make_response, current_app, session
from flask_login import current_user, login_required, login_user, logout_user

from . import auth
from .forms import LoginForm
from .utils import prepare_onelogin_request, init_saml_auth, saml_sso, saml_slo, saml_acs, saml_sls, \
    log_duplicate_session, create_auth_event
from ..constants import auth_event_type
from ..db_utils import update_object
from ..models import User


@auth.route('/login')
def login():
    if current_app.config['USE_SAML']:
        return redirect(url_for('main.index'))
    return redirect(url_for('auth.local_login'))


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    timeout = request.args.get('timeout')
    duplicate_session = request.args.get('duplicate_session')
    saml_errors = request.args.get('error_message')
    user_guid = session.get('_user_id')
    error_message = None

    if duplicate_session:
        return redirect(url_for("main.index"))

    if saml_errors:
        error_message = saml_errors
    elif current_user.is_authenticated and timeout:
        error_message = 'timeout'

    if current_user.is_authenticated:
        update_object({'session_id': None}, User, user_guid, by_guid=True)

    logout_user()
    create_auth_event(user_guid, auth_event_type.USER_LOGGED_OUT, {'success': True, 'errors': error_message})

    if timeout:
        flash("Your session timed out. Please login again", category="info")
    else:
        flash("You have been successfully logged out.", category="info")
    return redirect(url_for("auth.login"))


@auth.route('/saml', methods=['GET', 'POST'])
def saml():
    onelogin_request = prepare_onelogin_request(request)
    onelogin_saml_auth = init_saml_auth(onelogin_request)

    if 'sso' in request.args or len(request.args) == 0:
        return saml_sso(onelogin_saml_auth)
    elif 'sso2' in request.args:
        return_to = '%sattrs/' % request.host_url
        return redirect(onelogin_saml_auth.login(return_to))
    elif 'slo' in request.args:
        return redirect(saml_slo(onelogin_saml_auth))
    elif 'acs' in request.args:
        return saml_acs(onelogin_saml_auth, onelogin_request)
    elif 'sls' in request.args:
        return saml_sls(onelogin_saml_auth)
    else:
        flash(
            "Oops! Something went wrong. Please try to perform your action again later.",
            category="warning"
        )
        return redirect(url_for("main.index"))


@auth.route('/metadata/')
def metadata():
    req = prepare_onelogin_request(request)
    auth = init_saml_auth(req)
    settings = auth.get_settings()
    metadata = settings.get_sp_metadata()
    errors = settings.validate_metadata(metadata)

    if len(errors) == 0:
        resp = make_response(metadata, 200)
        resp.headers['Content-Type'] = 'text/xml'
    else:
        resp = make_response(', '.join(errors), 500)
    return resp


@auth.route('/local_login', methods=['GET', 'POST'])
def local_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data, is_active=True).one_or_none()
        if user is None:
            flash('Invalid Email Address.', category='danger')
        else:
            if user.division:
                login_user(user)
                duplicate_session = user.session_id is not None
                return_url = None

                if duplicate_session:
                    log_duplicate_session(user.guid)
                    return_url = url_for('main.index', duplicate_session=True)

                update_object({
                    'session_id': session.sid,
                    'last_sign_in_at': datetime.utcnow()
                },
                    User,
                    user.id
                )
                create_auth_event(user.guid, auth_event_type.USER_LOGIN, {'success': True})
                return redirect(return_url) if return_url else redirect(url_for('main.index'))
            else:
                create_auth_event(user.guid,
                                  auth_event_type.USER_FAILED_LOG_IN,
                                  {
                                      'User Data': user.email,
                                      'message': 'Awaiting division assignment.',
                                      'success': False
                                  })
            return render_template('contact_us.html')
    return render_template('auth/login.html', form=form)
