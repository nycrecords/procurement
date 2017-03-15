"""
.. module:: request.views.

   :synopsis: Provides routes for managing a specific request
"""
import datetime
import os
from flask import (
    render_template,
    request as flask_request,
    abort,
    redirect,
    url_for,
    send_from_directory,
    current_app,
    flash
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.email_notification import send_email
from app.request.forms import RequestForm, CommentForm, DeleteCommentForm, StatusForm
from app.models import Request, User, Vendor, Comment
from app.request import request as request
from app.constants import roles, status

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


@request.route('/', methods=['GET', 'POST'])
@login_required
def display_requests():
    """Return requests page that displays all requests."""
    if current_user.role == roles.ADMIN:
        requests = Request.query.order_by(Request.date_submitted.desc()).all()
    else:
        requests = Request.query.filter_by(division=current_user.division).order_by(Request.date_submitted.desc()).all()
    return render_template('request/requests.html', requests=requests)


@request.route('/new', methods=['GET', 'POST'])
@login_required
def new_request():
    """Return new request form for procurements."""
    form = RequestForm()

    vendors = Vendor.query.order_by(Vendor.name).all()

    if flask_request.method == 'POST':
        if form.validate_on_submit():
            date_submitted = datetime.datetime.now()

            current_status = status.NDA
            if current_user.role == roles.DIV:
                current_status = status.NCA
                if form.total_cost.data <= current_app.config['COST_LIMIT']:
                    current_status = status.PEN

            elif current_user.role == roles.COM:
                current_status = status.PEN

            elif current_user.role == roles.PROC:
                current_status = status.NCA

            new_request = Request(
                division=current_user.division,
                date_submitted=date_submitted,
                item=form.item.data,
                quantity=form.quantity.data,
                unit_price=form.unit_price.data,
                total_cost=form.total_cost.data,
                funding_source=form.funding_source.data,
                funding_source_description=None,
                grant_name=None,
                project_name=None,
                justification=form.justification.data,
                status=current_status,
                creator_id=current_user.id
            )

            if new_request.funding_source == "Grant":
                new_request.grant_name = form.grant_name.data
                new_request.project_name = form.project_name.data
            elif new_request == "Other":
                new_request.funding_source_description = form.funding_source_description.data

            request_vendor_name = str(form.request_vendor_name.data)
            request_vendor_phone = str(form.request_vendor_phone.data)
            request_vendor_fax = str(form.request_vendor_fax.data)
            request_vendor_mwbe = form.request_vendor_mwbe.data

            vendor_form = flask_request.form["vendor"]
            if vendor_form == "default":
                new_vendor = Vendor(name=request_vendor_name,
                                    address=form.request_vendor_address.data,
                                    phone=request_vendor_phone,
                                    fax=request_vendor_fax,
                                    email=form.request_vendor_email.data,
                                    tax_id=form.request_vendor_taxid.data,
                                    mwbe=request_vendor_mwbe)
                db.session.add(new_vendor)
                new_request.set_vendor_id(new_vendor.id)
            else:
                new_request.set_vendor_id(vendor_form)
            db.session.add(new_request)
            db.session.commit()

            # Email Notifications
            if current_status == status.NDA:
                # send notification to proc head
                receivers = [current_user.email]

                proc_query = db.session.query(User).filter(User.role == roles.PROC).\
                                                    filter(User.id != current_user.id).\
                                                    filter(User.division == current_user.division).all()
                for query in proc_query:
                    receivers.append(query.email)

                send_email(receivers, "Request {} has been Routed for Approval".format(new_request.id),
                           'request/new_request_notification',
                           user=current_user,
                           request=new_request)

            elif current_status == status.NCA:
                # send notification to admin
                print("NCA")
                receivers = [current_user.email]

                admin_query = db.session.query(User).filter(User.role == roles.ADMIN).\
                                                    filter(User.id != current_user.id).all()
                for query in admin_query:
                    receivers.append(query.email)

                send_email(receivers, "Request {} needs High Level Approval".format(new_request.id),
                           'request/new_request_notification',
                           user=current_user,
                           request=new_request)

            flash("Request was successfully created!")
            return redirect(url_for('request.display_request', request_id=new_request.id))
        else:
            print(form.errors)

    return render_template('request/new_request.html', form=form, user=current_user, vendors=vendors)


@request.route('/<request_id>', methods=['GET', 'POST'])
@login_required
def display_request(request_id):
    """Return page to view a specific request."""

    request = Request.query.filter_by(id=request_id).first()
    if current_user.role != roles.ADMIN and current_user.division != request.division:
        return redirect('requests')

    user = User.query.filter_by(id=request.creator_id).first()
    vendor = Vendor.query.filter_by(id=request.vendor_id).first()
    comments = Comment.query.filter_by(request_id=request_id).order_by(Comment.timestamp.desc()).all()

    comment_form = CommentForm()
    delete_form = DeleteCommentForm()
    status_form = StatusForm(status=request.status)

    # COST_LIMIT = 1000
    allowed_to_update = True
    choices = []

    # determine what options the current user has for updating status
    if current_user.role == roles.REG:
        allowed_to_update = False

    elif current_user.role == roles.ADMIN:
        choices = [(status.NDA, status.NDA),
                   (status.NCA, status.NCA),
                   (status.PEN, status.PEN),
                   (status.APR, status.APR),
                   (status.DEN, status.DEN),
                   (status.RES, status.RES),
                   (status.HOLD, status.HOLD)]

    elif current_user.role == roles.DIV:
        approved = status.NCA
        if request.total_cost <= current_app.config['COST_LIMIT']:
            approved = status.PEN

        choices = [(status.NDA, status.NDA),
                   (approved, "Approved"),
                   (status.DEN, status.DEN)]

        if request.status != status.NDA:
            allowed_to_update = False

    elif current_user.role == roles.COM:
        choices = [(status.NCA, status.NCA),
                   (status.PEN, "Approved"),
                   (status.HOLD, status.HOLD),
                   (status.DEN, status.DEN)]

        if request.status != status.NDA and request.status != status.NCA:
            allowed_to_update = False

    elif current_user.role == roles.PROC:
        choices = [(status.NDA, status.NDA),
                   (status.NCA, status.NCA),
                   (status.PEN, status.PEN),
                   (status.APR, status.APR),
                   (status.DEN, status.DEN),
                   (status.RES, status.RES),
                   (status.HOLD, status.HOLD)]

    status_form.status.choices = choices

    if request:
        return render_template(
                                'request/request.html',
                                current_user=current_user,
                                request=request,
                                user=user,
                                vendor=vendor,
                                comments=comments,
                                comment_form=comment_form,
                                status_form=status_form,
                                delete_form=delete_form,
                                allowed_to_update=allowed_to_update
                            )
    else:
        abort(404)


@request.route('/edit/<int:request_id>', methods=['GET', 'POST'])
@login_required
def edit_request(request_id):
    """Return page to edit a specific request."""
    if not current_user.role == roles.ADMIN:
        return redirect('requests')

    vendors = Vendor.query.order_by(Vendor.name).all()
    request, user, vendor = db.session.query(Request, User, Vendor).filter(Request.id == request_id). \
        filter(User.id == Request.creator_id). \
        filter(Request.vendor_id == Vendor.id).first()
    form = RequestForm()

    if flask_request.method == 'GET':
        form = RequestForm(item=request.item,
                           quantity=request.quantity,
                           unit_price=request.unit_price,
                           total_cost=request.total_cost,
                           funding_source=request.funding_source,
                           grant_name=request.grant_name,
                           project_name=request.project_name,
                           funding_source_description=request.funding_source_description,
                           justification=request.justification,
                           status=request.status)

        return render_template('request/edit_request.html',
                               form=form,
                               vendors=vendors,
                               selected_vendor_id=vendor.id,
                               user=user,
                               request=request)

    elif flask_request.method == 'POST':
        request.item = form.item.data
        request.quantity = form.quantity.data
        request.unit_price = form.unit_price.data
        request.total_cost = form.total_cost.data
        request.funding_source = form.funding_source.data
        request.justification = form.justification.data
        request.status = form.status.data

        if request.funding_source == "Grant":
            request.grant_name = form.grant_name.data
            request.project_name = form.project_name.data
            request.funding_source_description = None
        elif request.funding_source == "Other":
            request.grant_name = None
            request.project_name = None
            request.funding_source_description = form.funding_source_description.data
        else:
            request.grant_name = None
            request.project_name = None
            request.funding_source_description = None

        request_vendor_name = str(form.request_vendor_name.data)
        request_vendor_phone = str(form.request_vendor_phone.data)
        request_vendor_fax = str(form.request_vendor_fax.data)
        request_vendor_mwbe = form.request_vendor_mwbe.data

        vendor_form = flask_request.form["vendor"]
        if vendor_form == "default":
            new_vendor = Vendor(name=request_vendor_name,
                                address=form.request_vendor_address.data,
                                phone=request_vendor_phone,
                                fax=request_vendor_fax,
                                email=form.request_vendor_email.data,
                                tax_id=form.request_vendor_taxid.data,
                                mwbe=request_vendor_mwbe)
            db.session.add(new_vendor)
            new_request.set_vendor_id(new_vendor.id)
        else:
            request.set_vendor_id(vendor_form)
        db.session.commit()
        flash("Request was successfully updated!")

        return redirect(url_for('request.display_request', request_id=request_id))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@request.route('/add', methods=['GET', 'POST'])
def add_comment():
    comment_form = CommentForm()
    filename = None

    # Check if file was uploaded
    if comment_form.file.data is not None:
        filename = secure_filename(comment_form.file.data.filename)
        file_data = comment_form.file.data
        if file_data.filename != '' and file_data and allowed_file(file_data.filename):
            filename = secure_filename(datetime.datetime.now().strftime("%Y%m%d-%H%M") + file_data.filename)
            file_data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

    # Add comment to database
    new_comment = Comment(
        request_id=comment_form.request_id.data,
        user_id=current_user.id,
        timestamp=datetime.datetime.now(),
        content=comment_form.content.data,
        filepath=filename
    )
    db.session.add(new_comment)
    db.session.commit()

    # Email notification for edit
    receivers = []

    request, requestor = db.session.query(Request, User).filter(Request.id == comment_form.request_id.data). \
        filter(User.id == Request.creator_id).first()
    receivers.append(requestor.email)

    div_query = db.session.query(User).filter(User.role == roles.DIV). \
        filter(User.email != requestor.email). \
        filter(User.division == requestor.division).all()
    for query in div_query:
        receivers.append(query.email)

    proc_query = db.session.query(User).filter(User.role == roles.PROC). \
        filter(User.email != requestor.email). \
        filter(User.division == requestor.division).all()
    for query in proc_query:
        receivers.append(query.email)

    send_email(receivers, "New Comment Added to Request {}".format(comment_form.request_id.data),
               'request/comment_added',
               user=current_user,
               comment_form=comment_form)

    return redirect(url_for('request.display_request', request_id=comment_form.request_id.data))


@request.route('/delete', methods=['GET', 'POST'])
def delete_comment():
    delete_form = DeleteCommentForm()
    Comment.query.filter(Comment.id == delete_form.comment_id.data).delete()
    db.session.commit()
    return redirect(url_for('request.display_request', request_id=delete_form.request_id.data))


@request.route('/download/<int:comment_id>', methods=['GET'])
def download(comment_id):
    comment = Comment.query.filter(Comment.id == comment_id).first()
    print(comment.filepath)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], comment.filepath,
                               as_attachment=True, attachment_filename=comment.filepath[13:])


@request.route('/status/<int:request_id>', methods=['GET', 'POST'])
def update_status(request_id):
    status_form = StatusForm()
    request = Request.query.filter_by(id=request_id).first()
    old_status = request.status
    request.status = status_form.status.data
    db.session.commit()

    requester = db.session.query(User).filter(User.id == request.creator_id).first()

    # Email Notifications
    if old_status != request.status:
        if request.status == status.DEN:
            receivers = [requester.email]

            admin_query = db.session.query(User).filter(User.role == roles.ADMIN).\
                                                filter(User.id != requester.id).all()
            for query in admin_query:
                receivers.append(query.email)

            send_email(receivers, "Request {} has been Denied".format(request.id),
                       'request/status_update',
                       user=current_user,
                       request=request,
                       old_status=old_status)

        elif request.status == status.NDA:
            receivers = [requester.email]

            proc_query = db.session.query(User).filter(User.role == roles.PROC).\
                                                filter(User.id != requester.id).all()
            for query in proc_query:
                receivers.append(query.email)

            send_email(receivers, "Request {} has been Routed for Approval".format(request.id),
                       'request/status_update',
                       user=current_user,
                       request=request,
                       old_status=old_status)

        elif request.status == status.NCA:
            receivers = [requester.email]

            admin_query = db.session.query(User).filter(User.role == roles.ADMIN).\
                                                filter(User.id != requester.id).all()
            for query in admin_query:
                receivers.append(query.email)

            send_email(receivers, "Request {} needs High Level Approval".format(request.id),
                       'request/status_update',
                       user=current_user,
                       request=request,
                       old_status=old_status)

        elif request.status == status.PEN:
            receivers = [requester.email]

            admin_query = db.session.query(User).filter(User.role == roles.ADMIN).\
                                                filter(User.id != requester.id).all()
            for query in admin_query:
                receivers.append(query.email)

            send_email(receivers, "Request {} awaiting Procurement Head Approval".format(request.id),
                       'request/status_update',
                       user=current_user,
                       request=request,
                       old_status=old_status)

        elif request.status == status.HOLD:
            receivers = [requester.email]

            admin_query = db.session.query(User).filter(User.role == roles.ADMIN).\
                                                filter(User.id != requester.id).all()
            for query in admin_query:
                receivers.append(query.email)

            send_email(receivers, "Request {} has been put on Hold".format(request.id),
                       'request/status_update',
                       user=current_user,
                       request=request,
                       old_status=old_status)

    return redirect(url_for('request.display_request', request_id=request_id))


@request.errorhandler(404)
def not_found(error):
    """Return a 404 error page."""
    return render_template('request/not_found.html'), 404


@request.errorhandler(400)
def bad_request(error):
    """Return a 400 error page."""
    return render_template('request/bad_request.html'), 400
