"""
.. module:: request.utils.

    :synopsis: Defines the functions for request directory
"""
from app import db
from flask import current_app
from flask_login import current_user
from app.models import Request, User, Comment
from app.constants import roles, status
from sqlalchemy.sql.expression import true
import datetime


def determine_fiscal_id(date_submitted):
    """Returns the appropriate id based on the fiscal year"""
    if date_submitted.month < 7:
        id_first = "FY" + str(date_submitted.year) + "-"
    else:
        id_first = "FY" + str(date_submitted.year + 1) + "-"

    last_request = Request.query.filter(Request.id.like(id_first + "%")).order_by(Request.id.desc()).first()
    if last_request:
        id_last = str(int(last_request.id[-4:]) + 1)
        while len(id_last) < 4:
            id_last = '0' + id_last
        if len(id_last) > 4:
            id_last = id_last[-4:]
    else:
        id_last = "0001"

    request_id = id_first + id_last
    return request_id


def email_setup(requester, request):
    """Returns receivers and header based on the status of a request"""
    receivers = [current_app.config['PROCUREMENT_DL']]
    if requester.is_active:
        receivers.append(requester.email)

    header = ""

    if request.status == status.DEN:
        # record the denial time
        date_denied = datetime.datetime.now()
        new_comment = Comment(
            request_id=request.id,
            user_id=current_user.id,
            timestamp=date_denied,
            content="Request has been denied",
            editable=False
        )
        db.session.add(new_comment)
        db.session.commit()
        header = "Request {} has been Denied".format(request.id)

    elif request.status == status.NDA:
        div_query = User.query.filter(User.role == roles.DIV,
                                      User.id != requester.id,
                                      User.division == requester.division,
                                      User.is_active == true()).all()
        for query in div_query:
            receivers.append(query.email)

        header = "Request {} has been Routed for Approval".format(request.id)

    elif request.status == status.NCA:
        comm_query = User.query.filter(User.role == roles.COM,
                                       User.id != requester.id,
                                       User.is_active == true()).all()
        for query in comm_query:
            receivers.append(query.email)

        header = "Request {} needs High Level Approval".format(request.id)

    elif request.status == status.APR:
        header = "Request {} has been Approved".format(request.id)

    elif request.status == status.HOLD:
        header = "Request {} has been put on Hold".format(request.id)

    elif request.status == status.RES:
        # record the resolution time
        date_closed = datetime.datetime.now()
        request.date_closed = date_closed
        db.session.commit()
        header = "Request {} has been Resolved".format(request.id)

    elif request.status == status.NPA:
        header = "Request {} needs Procurement Head Approval".format(request.id)

    elif request.status == status.OIP:
        header = "Request {} has been updated to Order in Progress".format(request.id)

    return receivers, header
