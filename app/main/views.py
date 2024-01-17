from flask import render_template, session, redirect, url_for, request
from flask_login import login_required, current_user

from . import main
from .. import login_manager
from ..models import User, Request


@login_manager.user_loader
def user_loader(guid: str) -> User:
    user = User.query.filter_by(guid=guid).one_or_none()
    if user.session_id == session.sid:
        return user


@main.route('/')
# @login_required
def index():
    if current_user.is_authenticated:
        duplicate_session = request.args.get('duplicate_session')
        #TODO Test code
        page = request.args.get('page', 1, type=int)
        per_page = 50
        requests = Request.query.order_by(Request.date_submitted.desc()).paginate(
            page=page, per_page=per_page, error_out=False)
        return redirect(url_for('request.home', duplicate_session=duplicate_session))
        # return render_template(
        #     'request/requests.html',
        #     user=current_user.get_id(),
        #     duplicate_session=duplicate_session,
        #     requests=requests
        # )
    return redirect(url_for('auth.login'))


@main.route('/active', methods=['POST'])
def active():
    """
    Extends a user's session.
    :return:
    """
    session.modified = True
    return 'OK'
