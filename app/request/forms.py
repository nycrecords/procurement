"""
.. module:: request.forms.

   :synopsis: Defines forms used to manage procurement requests
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, BooleanField, HiddenField, SubmitField, DecimalField, \
    IntegerField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, Length, Email, Regexp, Optional
from wtforms_alchemy import PhoneNumberField
from app.constants import status
import re

funding = [
    ('', ''),
    ('Expense', 'Expense'),
    ('MAARF', 'MAARRF'),
    ('Grant', 'Grant'),
    ('SARA', 'SARA'),
    ('KOCH', 'KOCH'),
    ('Other', 'Other')
]

regexp_message = "Must only contain alphanumeric characters or the following " \
                 "characters: ' ,-."


class CommentForm(FlaskForm):
    """Form for creating a new comment."""
    content = TextAreaField(validators=[Length(0, 500), DataRequired('Please enter a comment')])
    file = FileField(u'Upload File...')
    submit = SubmitField(u'Add Comment')


class RequestForm(FlaskForm):
    """Form for creating a new request."""
    item = TextAreaField(u'Item*(required)', validators=[
        DataRequired('Please enter the item')])
    quantity = IntegerField(u'Quantity*', validators=[
        DataRequired('Please enter the quantity (only numbers are allowed)')])
    unit_price = DecimalField(u'Price per item*', validators=[
        DataRequired('Please enter the price per item (only numbers are allowed)')])
    total_cost = DecimalField(u'Total price*', validators=[
        DataRequired('Please enter the total price (only numbers are allowed)')])
    funding_source = SelectField(u'Funding*', choices=funding, validators=[
        DataRequired('Please select the funding source')])
    funding_source_description = StringField(u'Funding Other')
    grant_name = StringField(u'Grant Name')
    project_name = StringField(u'Project Name')
    justification = TextAreaField(u'Justification*(required)', validators=[
        DataRequired('You must enter a justification for your request'), Length(1, 500)])
    request_vendor_dropdown = SelectField(u'Vendor Information*')
    request_vendor_name = StringField(u'Vendor Name', validators=[Length(5),
                                                                  Regexp("^[\w, '-.]+$", message=regexp_message),
                                                                  DataRequired('Please enter the vendor name')])
    request_vendor_address = StringField(u'Vendor Address', validators=[Length(5),
                                                                        Regexp("^[\w, '-.]+$", message=regexp_message),
                                                                        DataRequired('Please enter the vendor address')])
    request_vendor_phone = PhoneNumberField(region='US', display_format='national', validators=[DataRequired('Please enter the vendor phone')])
    request_vendor_fax = PhoneNumberField(region='US', display_format='national')
    request_vendor_email = StringField(u'Email', validators=[Email(), DataRequired('Please enter the vendor email')])
    request_vendor_taxid = StringField(u'Vendor Tax ID')
    request_vendor_mwbe = BooleanField(u'mwbe')
    submit = SubmitField(u'Submit Request')

    def __init__(self, *args, **kwargs):
        """Fill the vendor dropdown with values from the database upon initialization"""
        super(RequestForm, self).__init__(*args, **kwargs)

        from app.models import Vendor
        vendors = Vendor.query.filter_by(enabled=True).order_by(Vendor.name).all()
        vendor_dropdown = [
            ('default', 'Select Vendor or Enter New Vendor Below')
        ]
        for vendor in vendors:
            vendor_dropdown.append((str(vendor.id), vendor.name))
        self.request_vendor_dropdown.choices = vendor_dropdown

    def validate(self, extra_validators=None):
        if not super(RequestForm, self).validate():
            return False

        # check if user selected other and filled out the field
        if self.funding_source.data == "Other" and not self.funding_source_description.data:
            self.funding_source.errors.append("You must specify if you entered Other")
            return False

        # check if user selected grant and filled out the fields
        if self.funding_source.data == "Grant" and (not self.grant_name.data or not self.project_name.data):
            self.funding_source.errors.append("You must include a grant and project name if you entered Grant")
            return False

        if self.request_vendor_dropdown.data == "default":
            # check if user filled out the vendor fields
            if not (self.request_vendor_name.data and self.request_vendor_address.data and
                    self.request_vendor_address.data and self.request_vendor_phone.data and
                    self.request_vendor_fax.data and self.request_vendor_email.data and
                    self.request_vendor_taxid.data):
                self.request_vendor_dropdown.errors.append("You must fill out all fields for Vendor Information")
                return False

        return True


class DeleteCommentForm(FlaskForm):
    """Form for deleting a comment."""
    request_id = HiddenField()
    comment_id = HiddenField()
    submit = SubmitField(u'Delete')


class StatusForm(FlaskForm):
    """Form for updating status of a request."""
    status = SelectField(u'Status', validators=[DataRequired()])
    submit = SubmitField(u'Update')
