from flask import request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from app.admin import admin
from app.admin.utils import assign_user_role, assign_user_division
from app.constants.division import USER_DIVISIONS, DIVISION_DROPDOWN
from app.constants.roles import USER_ROLES
from app.models import User


@admin.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    if not current_user.is_admin:
        flash("Insufficient privileges to view this page.")
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        user_guid = request.form.get('user')
        user = User.query.filter_by(guid=user_guid).one_or_none()
        role = request.form.get('role')
        division = request.form.get('division')

        if user.role != role and role != None:
            assign_user_role(user_guid, role)
        if user.division != division:
            assign_user_division(user_guid, division)

    users = User.query.all()

    return render_template('admin/index.html', user_list=users, roles=USER_ROLES, divisions=DIVISION_DROPDOWN)
