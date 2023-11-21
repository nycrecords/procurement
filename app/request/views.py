from flask import render_template, redirect, url_for, jsonify, request
from flask_login import login_required, current_user
from . import request_bp
from ..models import Vendor, Request, Comment
from .forms import RequestForm
from .. import db
import datetime
import uuid
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from werkzeug.urls import url_parse
from sqlalchemy.exc import OperationalError
from uuid import UUID
from flask import send_from_directory
from flask import request
from flask import current_app
from flask import render_template, redirect, url_for, flash
from .forms import EditRequestForm
from ..models import Request, Vendor
from app import db
from flask import send_from_directory
import os
from uuid import UUID
import re
from flask import abort
from flask_login import current_user, login_required


@request_bp.route('/update_status', methods=['POST'])
def update_status():
    # Your code to update the status
    ...


@request_bp.route('/')  # Define this as the root route
@request_bp.route('/requests')  # Define this as another route
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 50  # change this to the number of items you want per page
    requests = Request.query.order_by(Request.date_submitted.desc()).paginate(
        page=page, per_page=per_page, error_out=False)
    return render_template('request/requests.html', requests=requests)


@request_bp.route('/new_request', methods=['GET', 'POST'])
@login_required
def new_request():
    form = RequestForm()

    # Set the division and creator_id fields based on the current user
    form.division.data = current_user.division
    vendors = Vendor.query.filter(Vendor.enabled == True).all()
    vendor_choices = [(str(vendor.id), vendor.name) for vendor in vendors]
    # Add the None option at the beginning
    vendor_choices.insert(
        0, ('none', 'Select Vendor or Enter New Vendor Below'))
    form.request_vendor_dropdown.choices = vendor_choices

    if form.validate_on_submit():
        # Get vendor_id based on whether a new vendor was created or an existing one selected
        if form.request_vendor_dropdown.data == 'none':
            new_vendor = Vendor(
                name=form.request_vendor_name.data,
                address=form.request_vendor_address.data,
                phone=form.request_vendor_phone.data,
                fax=form.request_vendor_fax.data,
                email=form.request_vendor_email.data,
                tax_id=form.request_vendor_taxid.data,
                mwbe=form.request_vendor_mwbe.data,
                enabled=True,
            )
            db.session.add(new_vendor)
            db.session.flush()  # This is needed to get the new vendor's ID
            vendor_id = new_vendor.id
        else:
            vendor_id = form.request_vendor_dropdown.data

        # Set grant_name and project_name to None if not provided
        grant_name = form.grant_name.data if form.grant_name.data else None
        project_name = form.project_name.data if form.project_name.data else None

        # Create new Request
        new_request = Request(
            division=current_user.division,
            item=form.item.data,
            quantity=form.quantity.data,
            unit_price=form.unit_price.data,
            total_cost=form.total_cost.data,
            funding_source=form.funding_source.data,
            funding_source_description=None,
            grant_name=grant_name,
            project_name=project_name,
            justification=form.justification.data,
            status="New",
            creator_id=current_user.id,
            vendor_id=vendor_id,
        )

        if new_request.funding_source == "Grant":
            new_request.grant_name = form.grant_name.data
            new_request.project_name = form.project_name.data
        elif new_request.funding_source == "Other":
            new_request.funding_source_description = form.funding_source_description.data

        db.session.add(new_request)
        db.session.commit()  # Commit the changes to add the request to the database

        return jsonify(success=True, request_id=str(new_request.id))

    current_date = datetime.now().strftime('%m/%d/%Y')
    # or the attribute that stores the user's name
    current_username = current_user.first_name
    current_division = current_user.division
    return render_template('request/new_request.html', form=form, current_date=current_date, current_username=current_username, current_division=current_division)


@request_bp.route('/get_vendor/<string:vendor_id>')
def get_vendor(vendor_id):
    # Convert the string vendor_id to a UUID
    vendor_id = UUID(vendor_id)

    vendor = Vendor.query.get(vendor_id)
    if vendor is not None:
        return jsonify({
            'name': vendor.name,
            'address': vendor.address,
            'phone': vendor.phone,
            'fax': vendor.fax,
            'email': vendor.email,
            'tax_id': vendor.tax_id,
            'mwbe': vendor.mwbe,
            'enabled': vendor.enabled,
        })
    else:
        return jsonify(error="Vendor not found"), 404


@request_bp.app_template_filter()
def truncate_by_words(s, num_words):
    words = s.split()
    if len(words) > num_words:
        words = words[:num_words]
        words.append('...')
    return ' '.join(words)


UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app/uploads')


@request_bp.route('/request/<request_id>')
@login_required
def view_request(request_id):
    request_id_uuid = uuid.UUID(request_id)  # convert request_id to a UUID
    request = Request.query.get_or_404(request_id_uuid)
    vendor = Vendor.query.get_or_404(request.vendor_id)  # get vendor
    comments = Comment.query.filter_by(request_id=request_id_uuid).order_by(
        Comment.timestamp.desc()).all()  # get all comments ordered by timestamp
    return render_template('request/request.html', request=request, vendor=vendor, comments=comments)


@request_bp.route('/submit_comment', methods=['POST'])
@login_required
def submit_comment():
    if current_user.is_authenticated:
        request_id = uuid.UUID(request.form.get('request_id'))
        comment_content = request.form.get('comment')
        file = request.files.get('file')
        file_path = None

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

        new_comment = Comment(
            id=str(uuid.uuid4()),  # Generate a new UUID for the comment
            request_id=request_id,
            user_id=current_user.id,
            timestamp=datetime.now(),
            content=comment_content,
            filepath=file_path  # filepath will be None if no file was attached
        )

        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for('request.view_request', request_id=request_id))
    else:
        # handle unauthenticated user here, for example:
        return "User not authenticated", 403


def is_valid_uuid(uuid_string):
    pattern = re.compile(
        r'^[a-f\d]{8}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{12}$')
    return bool(pattern.match(uuid_string))


@request_bp.route('/download/<string:comment_id>', methods=['GET'])
def download(comment_id):
    """Allows users to download files from comments"""
    if not is_valid_uuid(comment_id):
        abort(400, "Invalid UUID format")
    comment = Comment.query.get_or_404(UUID(comment_id))
    directory = current_app.config['UPLOAD_FOLDER']
    filename = os.path.basename(comment.filepath)
    return send_from_directory(directory, filename, as_attachment=True)


@request_bp.route('/edit_request/<request_id>', methods=['GET', 'POST'])
def edit_request(request_id):
    try:
        req = Request.query.get_or_404(request_id)
        vendor = Vendor.query.get_or_404(req.vendor_id)

        form = EditRequestForm(obj=req)
        form.request_vendor_dropdown.choices = [
            (v.id, v.name) for v in Vendor.query.all()]
        form.division.data = current_user.division
        current_date = datetime.now().strftime('%m/%d/%Y')
        current_username = current_user.first_name
        current_division = current_user.division

        if request.method == 'GET':
            form.request_vendor_dropdown.data = req.vendor_id

        if form.validate_on_submit():
            req.vendor_id = form.request_vendor_dropdown.data
            form.populate_obj(req)

            # Update the database fields based on the funding source
            if req.funding_source == "Grant":
                req.funding_source_description = None  # Set the description to None
            elif req.funding_source == "Other":
                req.grant_name = None  # Clear the grant name
                req.project_name = None  # Assuming you meant project name as grant description

            db.session.commit()
            flash('Request information updated successfully', 'success')
            return redirect(url_for('request.home'))

        return render_template('request/edit_request.html', req=req, vendor=vendor, form=form, current_date=current_date, current_username=current_username, current_division=current_division)

    except OperationalError as e:
        db.session.rollback()  # Rollback the session to a clean state
        print(f"Error: {e}")  # You can also use proper logging here
        flash("There was a problem connecting to the database. Please try again.", "danger")
        # Redirect back to the home as an example
        return redirect(url_for('request.home'))
