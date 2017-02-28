"""
.. module:: request.views.

   :synopsis: Provides routes for managing a specific request.
"""
from flask import (
    render_template,
    request as flask_request,
    abort,
    Response,
    redirect,
    url_for,
send_from_directory
)
import datetime
import smtplib
# from sqlalchemy import update
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from ..email_notification import send_email
from .. import db
from .forms import RequestForm, CommentForm, DeleteCommentForm
from ..models import Request, User, Vendor, Comment
from . import request as request_blueprint
from ..constants import roles, status
from flask import current_app

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


@request_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def display_requests():
    """View the page for all the requests."""
    if current_user.role == roles.ADMIN:
        requests = Request.query.order_by(Request.date_submitted.desc()).all()
    else:
        requests = Request.query.filter_by(division=current_user.division).order_by(Request.date_submitted.desc()).all()
    return render_template('request/requests.html',
                           requests=requests
                           )


@request_blueprint.route('/<request_id>', methods=['GET', 'POST'])
@login_required
def display_request(request_id):
    """View the page for a specific request."""

    current_request = Request.query.filter_by(id=request_id).first()
    if current_user.role != roles.ADMIN and current_user.division != current_request.division:
        return redirect('requests')

    request = Request.query.filter_by(id=request_id).first()
    user = User.query.filter_by(id=request.creator_id).first()
    vendor = Vendor.query.filter_by(id=request.vendor_id).first()
    comments = Comment.query.filter_by(request_id=request_id).order_by(Comment.timestamp.desc()).all()

    if not (current_user.role == roles.ADMIN or current_user.division == request.division):
        return redirect('requests')

    commentform = CommentForm()
    deleteform = DeleteCommentForm()

    if request:
        return render_template(
                                'request/request.html',
                                request=request,
                                user=user,
                                vendor=vendor,
                                comments=comments,
                                commentform=commentform,
                                deleteform=deleteform
                            )
    else:
        abort(404)


@request_blueprint.route('/edit/<int:request_id>', methods=['GET', 'POST'])
@login_required
def edit_request(request_id):
    """Edit a request."""

    if not current_user.role == roles.ADMIN:
        return redirect('requests')

    vendors = Vendor.query.order_by(Vendor.name).all()
    request, user, vendor = db.session.query(Request, User, Vendor).filter(Request.id == request_id).\
                                                    filter(User.id == Request.creator_id).\
                                                    filter(Request.vendor_id == Vendor.id).first()
    form = RequestForm()

    # if current_user.role == roles.ADMIN or current_user.role == roles.PROC:
    #     choices = [(status.SUB, status.SUB),
    #                (status.NDA, status.NDA),
    #                (status.NCA, status.NCA),
    #                (status.PEN, status.PEN),
    #                (status.DEN, status.DEN),
    #                (status.RES, status.RES),
    #                (status.HOLD, status.HOLD)]
    #
    # elif current_user.role == roles.DIV:
    #     choices = [(status.SUB, status.SUB),
    #                (status.NDA, status.NDA),
    #                (status.NCA, status.NCA),
    #                (status.PEN, status.PEN),
    #                (status.DEN, status.DEN),
    #                (status.RES, status.RES),
    #                (status.HOLD, status.HOLD)]
    #
    # elif current_user.role == roles.COM:
    #     pass
    #
    # elif current_user.role == roles.PROC:
    #     pass

    if flask_request.method == 'GET':
        form = RequestForm(item=request.item,
                           quantity=request.quantity,
                           unit_price=request.unit_price,
                           total_cost=request.total_cost,
                           funding_source=request.funding_source,
                           justification=request.justification,
                           status=request.status)

        # form.status.choices = choices

        return render_template('request/edit_request.html',
                               form=form,
                               vendors=vendors,
                               selected_vendor_id=vendor.id,
                               user=user,
                               request=request)

    elif flask_request.method == 'POST':

        # UPDATE DATABASE TO MATCH THE NEW INFORMATION
        request.item = form.item.data
        request.quantity = form.quantity.data
        request.unit_price = form.unit_price.data
        request.total_cost = form.total_cost.data
        request.funding_source = form.funding_source.data
        request.justification = form.justification.data
        request.status = form.status.data

        # Vendor Stuff
        request_vendor_name = str(form.request_vendor_name.data)
        request_vendor_phone = str(form.request_vendor_phone.data)
        request_vendor_fax = str(form.request_vendor_fax.data)
        request_vendor_mwbe = str(form.request_vendor_mwbe.data)

        newvendor = None
        vendor_form = flask_request.form["vendor"]

        if request_vendor_name != '':
            if request_vendor_mwbe == "None":
                request_vendor_mwbe = None
            if vendor_form == "default":
                newvendor = Vendor(name=request_vendor_name,
                                   address=form.request_vendor_address.data,
                                   phone=request_vendor_phone,
                                   fax=request_vendor_fax,
                                   email=form.request_vendor_email.data,
                                   tax_id=form.request_vendor_taxid.data,
                                   mwbe=request_vendor_mwbe)
                db.session.add(newvendor)
                db.session.commit()
        else:
            print(form.errors)
        if newvendor is not None:
            request.set_vendor_id(newvendor.id)
        else:
            request.set_vendor_id(vendor_form)
        # db.session.add(request)
        # db.session.commit()

        # # Add Notes
        # if form.comment is not None and form.comment.data.strip() is not "":
        #     newcomment = Comment(
        #         request_id=request.id,
        #         user_id=current_user.id,
        #         timestamp=datetime.datetime.now(),
        #         content=form.comment.data
        #     )
        #     db.session.add(newcomment)
        #
        # db.session.commit()
        #
        # # email notification for edit
        # sender = 'donotreply@records.nyc.gov'
        # receivers = [user.email]
        # # receivers = ['mlaikhram@gmail.com']
        # message = """\
        # From: Procurements <%s>
        # To: %s
        # Subject: Request %s Edited
        # A request you made has been edited.
        # %s
        # """ % (sender, ", ".join(receivers), request_id, form.comment.data.strip())
        #
        # print(message)
        #
        # try:
        #     smtpObj = smtplib.SMTP('localhost', 1025)
        #     smtpObj.sendmail(sender, receivers, message)
        #     print("Successfully sent email")
        # except:
        #     print("Error: unable to send email")

        return redirect(url_for('request.display_request', request_id=request_id))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@request_blueprint.route('/add', methods=['GET', 'POST'])
def add_comment():
    commentform = CommentForm()

    filename = None

    # handle submitted file
    if commentform.file.data is not None:
        filename = secure_filename(commentform.file.data.filename)
        # commentform.file.data.save('uploads/' + filename)
        # commentform.file.data.save('uploads/' + filename)
        # file_data = flask_request.files[commentform.file.name].read()
        file_data = commentform.file.data
        if file_data.filename != '' and file_data and allowed_file(file_data.filename):
            filename = secure_filename(datetime.datetime.now().strftime("%Y%m%d-%H%M") + file_data.filename)
            file_data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

    # add to database
    newcomment = Comment(
        request_id=commentform.request_id.data,
        user_id=current_user.id,
        timestamp=datetime.datetime.now(),
        content=commentform.content.data,
        filepath=filename
    )
    db.session.add(newcomment)
    db.session.commit()

    # email notification for edit
    receivers = []

    request, requestor = db.session.query(Request, User).filter(Request.id == commentform.request_id.data).\
                                                    filter(User.id == Request.creator_id).first()
    receivers.append(requestor.email)

    div_query = db.session.query(User).filter(User.role == roles.DIV).\
                                       filter(User.email != requestor.email).\
                                       filter(User.division == requestor.division).all()
    for query in div_query:
        receivers.append(query.email)

    proc_query = db.session.query(User).filter(User.role == roles.PROC).\
                                        filter(User.email != requestor.email).\
                                        filter(User.division == requestor.division).all()
    for query in proc_query:
        receivers.append(query.email)

    # receivers = [requestor.email]
    # receivers = ['mlaikhram@gmail.com']
    # message = """\
    # From: Procurements <%s>
    # To: <%s>
    # Subject: New Comment Added to Request %s
    #
    # %s %s commented on your request:
    #
    # %s
    # """ % (sender,
    #        ">, <".join(receivers),
    #        commentform.request_id.data,
    #        current_user.first_name,
    #        current_user.last_name,
    #        commentform.content.data.strip())

    send_email(receivers, "New Comment Added to Request {}".format(commentform.request_id.data),
               'request/comment_added',
               user=current_user,
               commentform=commentform)

    # print(message)

    # try:
    #     smtpObj = smtplib.SMTP('localhost', current_app.config["MAIL_PORT"])
    #     smtpObj.sendmail(sender, receivers, message)
    #     print("Successfully sent email")
    # except:
    #     print("Error: unable to send email")

    return redirect(url_for('request.display_request', request_id=commentform.request_id.data))


@request_blueprint.route('/delete', methods=['GET', 'POST'])
def delete_comment():
    deleteform = DeleteCommentForm()
    Comment.query.filter(Comment.id == deleteform.comment_id.data).delete()
    db.session.commit()
    return redirect(url_for('request.display_request', request_id=deleteform.request_id.data))


@request_blueprint.route('/download/<int:comment_id>', methods=['GET'])
def download(comment_id):
    comment = Comment.query.filter(Comment.id == comment_id).first()
    print(comment.filepath)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], comment.filepath,
                               as_attachment=True, attachment_filename=comment.filepath[13:])


@request_blueprint.errorhandler(404)
def not_found(error):
    """Return a 404 error page."""
    return render_template('request/not_found.html'), 404


@request_blueprint.errorhandler(400)
def bad_request(error):
    """Return a 400 error page."""
    return render_template('request/bad_request.html'), 400
