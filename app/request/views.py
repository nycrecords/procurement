"""
.. module:: request.views.

   :synopsis: Provides routes for managing a specific request
"""
import datetime
import os
from decimal import Decimal

from flask import (
    render_template,
    request as flask_request,
    abort,
    redirect,
    url_for,
    send_from_directory,
    current_app,
    flash,
    jsonify
)
from flask_login import login_required, current_user
from sqlalchemy import desc
from sqlalchemy.sql.expression import true
from urllib.parse import urljoin
from werkzeug.utils import secure_filename

from app import db
from app.constants import roles, status, mimetypes
from app.email_notification import send_email
from app.errors import flash_errors
from app.models import Request, User, Vendor, Comment, StatusEvents
from app.request import request as requests
from app.request.forms import RequestForm, CommentForm, DeleteCommentForm, StatusForm
from app.request.utils import determine_fiscal_id, email_setup


@requests.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Return requests page that displays all requests."""
    duplicate_session = flask_request.args.get('duplicate_session')
    if current_user.role in (roles.ADMIN, roles.PROC, roles.COM):
        requests = Request.query.order_by(Request.date_submitted.desc()).all()

    elif current_user.role == roles.DIV:
        requests = Request.query.filter_by(division=current_user.division).order_by(Request.date_submitted.desc()).all()

    else:
        requests = Request.query.filter_by(creator_id=current_user.id).order_by(Request.date_submitted.desc()).all()
    return render_template('request/requests.html', requests=requests, duplicate_session=duplicate_session)


@requests.route('/new', methods=['GET', 'POST'])
@login_required
def new_request():
    """Return new request form for procurements."""
    form = RequestForm()

    vendors = Vendor.query.order_by(Vendor.name).all()

    if flask_request.method == 'POST' and form.validate_on_submit():
        date_submitted = datetime.datetime.now()

        request_id = determine_fiscal_id(date_submitted)

        # Strip dollar sign and replace comma from input mask and convert value into Decimal
        unit_price = Decimal(form.unit_price.data.strip('$').replace(',', ''))
        total_cost = Decimal(form.total_cost.data.strip('$').replace(',', ''))

        # determine what possible routes a request can take based on the request and the current user role
        current_status = status.NDA
        if current_user.role == roles.DIV:
            current_status = status.NCA
            if total_cost <= Decimal(current_app.config['COST_LIMIT']):
                current_status = status.APR

        elif current_user.role == roles.COM:
            current_status = status.APR

        elif current_user.role == roles.PROC:
            current_status = status.NCA

        new_request = Request(
            request_id=request_id,
            division=current_user.division,
            date_submitted=date_submitted,
            item=form.item.data,
            quantity=form.quantity.data,
            unit_price=unit_price,
            total_cost=total_cost,
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
        elif new_request.funding_source == "Other":
            new_request.funding_source_description = form.funding_source_description.data

        vendor_form = flask_request.form["request_vendor_dropdown"]
        if vendor_form == "default":
            vendor_name = str(form.request_vendor_name.data)
            existing_vendors = Vendor.query.filter(Vendor.name.ilike(vendor_name)).one_or_none()

            if existing_vendors:
                flash(
                    'Vendor already exists. Please select the existing vendor from dropdown or enter a new vendor name.',
                    category='danger')
                return render_template('request/new_request.html', form=form, user=current_user, vendors=vendors)

            else:
                new_vendor = Vendor(name=form.request_vendor_name.data,
                                    address=form.request_vendor_address.data,
                                    phone=form.request_vendor_phone.data,
                                    fax=form.request_vendor_fax.data,
                                    email=form.request_vendor_email.data,
                                    tax_id=form.request_vendor_taxid.data,
                                    mwbe=form.request_vendor_mwbe.data)
                db.session.add(new_vendor)
                db.session.commit()
                new_request.set_vendor_id(new_vendor.id)
        else:
            new_request.set_vendor_id(int(vendor_form))
        db.session.add(new_request)
        db.session.commit()

        # Email Notifications
        receivers, header = email_setup(current_user, new_request)

        send_email(receivers, header,
                   'request/new_request_notification',
                   user=current_user,
                   request=new_request,
                   url=urljoin(flask_request.host_url,
                               url_for('request.display_request', request_id=new_request.id, _external=True, _scheme='https')))

        flash("Request was successfully created!", category="success")
        return redirect(url_for('request.display_request', request_id=new_request.id))

    else:
        print(form.errors)

    return render_template('request/new_request.html', form=form, user=current_user, vendors=vendors)


@requests.route('/<request_id>', methods=['GET', 'POST'])
@login_required
def display_request(request_id):
    """Return page to view a specific request."""

    request = Request.query.filter_by(id=request_id).first()
    if current_user.role not in [roles.ADMIN, roles.PROC, roles.COM] and current_user.division != request.division:
        return redirect(url_for('request.index'))

    user = User.query.filter_by(id=request.creator_id).first()
    vendor = Vendor.query.filter_by(id=request.vendor_id).first()
    comments = Comment.query.filter_by(request_id=request_id).order_by(Comment.timestamp.desc()).all()

    comment_form = CommentForm()
    delete_form = DeleteCommentForm()
    status_form = StatusForm(status=request.status)

    allowed_to_update = True
    choices = []

    # determine what options the current user has for updating status
    if current_user.role == roles.REG:
        allowed_to_update = False

    elif current_user.role == roles.ADMIN:
        choices = [(status.NDA, status.NDA),
                   (status.NCA, status.NCA),
                   (status.NPA, status.NPA),
                   (status.APR, status.APR),
                   (status.OIP, status.OIP),
                   (status.DEN, status.DEN),
                   (status.RES, status.RES),
                   (status.HOLD, status.HOLD)]

    elif current_user.role == roles.DIV:
        approved = status.NCA
        if request.total_cost <= Decimal(current_app.config['COST_LIMIT']):
            approved = status.NPA

        choices = [
            (approved, "Approved"),
            (status.HOLD, status.HOLD),
            (status.DEN, status.DEN)]

        if request.status != status.NDA:
            allowed_to_update = True

    elif current_user.role == roles.COM:
        choices = [
            (status.APR, "Approved"),
            (status.HOLD, status.HOLD),
            (status.DEN, status.DEN)]

        if request.status != status.NDA and request.status != status.NCA:
            allowed_to_update = True

    elif current_user.role == roles.PROC:
        choices = [(status.NDA, status.NDA),
                   (status.NCA, status.NCA),
                   (status.NPA, status.NPA),
                   (status.APR, status.APR),
                   (status.OIP, status.OIP),
                   (status.DEN, status.DEN),
                   (status.RES, status.RES),
                   (status.HOLD, status.HOLD)]

    status_form.status.choices = choices

    if request:
        return render_template('request/request.html',
                               current_user=current_user,
                               request=request,
                               user=user,
                               vendor=vendor,
                               comments=comments,
                               comment_form=comment_form,
                               status_form=status_form,
                               delete_form=delete_form,
                               allowed_to_update=allowed_to_update)
    else:
        abort(404)


@requests.route('/edit/<request_id>', methods=['GET', 'POST'])
@login_required
def edit_request(request_id):
    """Return page to edit a specific request."""
    if current_user.role not in [roles.ADMIN, roles.PROC]:
        return redirect('requests')

    form = RequestForm()

    vendors = Vendor.query.order_by(Vendor.name).all()

    request, user, vendor = db.session.query(Request, User, Vendor).filter(Request.id == request_id). \
        filter(User.id == Request.creator_id). \
        filter(Request.vendor_id == Vendor.id).first()

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
                           request_vendor_dropdown=str(request.vendor_id))

        return render_template('request/edit_request.html',
                               form=form,
                               vendors=vendors,
                               selected_vendor_id=vendor.id,
                               user=user,
                               request=request)

    elif flask_request.method == 'POST' and form.validate_on_submit():
        request.item = form.item.data
        request.quantity = form.quantity.data
        request.unit_price = Decimal(form.unit_price.data.strip('$'))
        request.total_cost = Decimal(form.total_cost.data.strip('$'))
        request.funding_source = form.funding_source.data
        request.justification = form.justification.data

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

        vendor_form = flask_request.form["request_vendor_dropdown"]
        if vendor_form == "default":
            new_vendor = Vendor(name=request_vendor_name,
                                address=form.request_vendor_address.data,
                                phone=request_vendor_phone,
                                fax=request_vendor_fax,
                                email=form.request_vendor_email.data,
                                tax_id=form.request_vendor_taxid.data,
                                mwbe=request_vendor_mwbe)
            db.session.add(new_vendor)
            db.session.commit()
            new_request.set_vendor_id(new_vendor.id)
        else:
            request.set_vendor_id(int(vendor_form))
        db.session.commit()
        flash("Request was successfully updated!", category="success")

        return redirect(url_for('request.display_request', request_id=request_id))

    else:
        print(form.errors)

    return render_template('request/edit_request.html',
                           form=form,
                           vendors=vendors,
                           selected_vendor_id=vendor.id,
                           user=user,
                           request=request)


def allowed_file(filename):
    """Determines if filename is one of the allowed file types"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in mimetypes.ALLOWED_EXTENSIONS


@requests.route('/add/<request_id>', methods=['GET', 'POST'])
def add_comment(request_id):
    """Adds a comment to the current request"""
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        # Check if file was uploaded
        fixed_filename = None
        if comment_form.file.data is not None:
            file_data = comment_form.file.data

            if not allowed_file(file_data.filename):
                flash("Invalid File Type")
                return redirect(url_for('request.display_request', request_id=request_id))

            if file_data.filename != '' and file_data and allowed_file(file_data.filename):
                fixed_filename = secure_filename(datetime.datetime.now().strftime("%Y%m%d-%H%M") + file_data.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], fixed_filename)
                file_data.save(file_path)

        # Add comment to database
        new_comment = Comment(
            request_id=request_id,
            user_id=current_user.id,
            timestamp=datetime.datetime.now(),
            content=comment_form.content.data,
            filepath=fixed_filename,
            editable=True
        )
        db.session.add(new_comment)
        db.session.commit()

        # Email notification for comment
        receivers = [current_app.config['PROCUREMENT_DL']]

        request, requestor = db.session.query(Request, User).filter(Request.id == request_id). \
            filter(User.id == Request.creator_id).first()
        receivers.append(requestor.email)

        div_query = db.session.query(User).filter(User.role == roles.DIV,
                                                  User.email != requestor.email,
                                                  User.division == requestor.division,
                                                  User.is_active == true()).all()
        for query in div_query:
            receivers.append(query.email)

        send_email(receivers, "New Comment Added to Request {}".format(request_id),
                   'request/comment_added',
                   filename=fixed_filename,
                   user=current_user,
                   request_id=request_id,
                   comment_form=comment_form)

    else:
        flash_errors(comment_form)

    return redirect(url_for('request.display_request', request_id=request_id))


@requests.route('/delete', methods=['GET', 'POST'])
def delete_comment():
    """Deletes the selected comment"""
    delete_form = DeleteCommentForm()
    comment = Comment.query.filter(Comment.id == delete_form.comment_id.data).first()
    # delete attached files if any
    if comment.filepath is not None:
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], comment.filepath))
    Comment.query.filter(Comment.id == delete_form.comment_id.data).delete()
    db.session.commit()
    return redirect(url_for('request.display_request', request_id=delete_form.request_id.data))


@requests.route('/download/<int:comment_id>', methods=['GET'])
def download(comment_id):
    """Allows users to download files from comments"""
    comment = Comment.query.filter(Comment.id == comment_id).first()
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], comment.filepath,
                               as_attachment=True, download_name=comment.filepath[13:])


@requests.route('/status/<request_id>', methods=['GET', 'POST'])
def update_status(request_id):
    if flask_request.method == 'POST':
        """Updates the status of the current request"""
        status_form = StatusForm()
        request = Request.query.filter_by(id=request_id).first()
        old_status = request.status
        new_status = status_form.status.data
        if old_status != new_status:
            request.status = status_form.status.data

            new_status = StatusEvents(
                request_id=request_id,
                previous_value=old_status,
                new_value=request.status,
                user_id=current_user.id,
                timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            db.session.add(new_status)
            db.session.commit()
            flash("Status was successfully updated!", category="success")

        else:
            flash('No changes updated', category='danger')

        requester = User.query.filter_by(id=request.creator_id).first()

        # Email Notifications
        if old_status != request.status:
            receivers, header = email_setup(requester, request)

            send_email(receivers, header,
                       'request/status_update',
                       user=current_user,
                       request=request,
                       old_status=old_status,
                       url=urljoin(flask_request.host_url,
                                   url_for('request.display_request',
                                           request_id=request.id,
                                           _external=True,
                                           _scheme='https')))

        return redirect(url_for('request.display_request', request_id=request_id))

    elif flask_request.method == 'GET':
        events = StatusEvents.query.filter(StatusEvents.request_id == request_id).order_by(
            desc(StatusEvents.timestamp)).all()

        return jsonify(
            history_rows=render_template('request/history_row.html', events=events)
        ), 200


@requests.errorhandler(404)
def not_found(error):
    """Return a 404 error page."""
    return render_template('request/not_found.html'), 404


@requests.errorhandler(400)
def bad_request(error):
    """Return a 400 error page."""
    return render_template('request/bad_request.html'), 400
