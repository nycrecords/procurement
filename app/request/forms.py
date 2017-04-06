"""
.. module:: request.forms.

   :synopsis: Defines forms used to manage procurement requests
"""
from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField, BooleanField, HiddenField, SubmitField, DecimalField, \
    IntegerField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, Length
from wtforms_alchemy import PhoneNumberField
from app.constants import status


# divisions = [
#     ('', ''),
#     ('MRMD', 'MRMD'),
#     ('Archives', 'Archives'),
#     ('Grants', 'Grants'),
#     ('Library', 'Library'),
#     ('Executive', 'Executive'),
#     ('Tech', 'Tech'),
#     ('Administration', 'Administration')
# ]

funding = [
    ('', ''),
    ('Expense', 'Expense'),
    ('MAARF', 'MAARRF'),
    ('Grant', 'Grant'),
    ('SARA', 'SARA'),
    ('KOCH', 'KOCH'),
    ('Other', 'Other')
]

# statuses = [
#     ('', ''),
#     ('Submitted', 'Submitted'),
#     ('Needs Division Approval', 'Needs Division Approval'),
#     ('Needs Commissioner Approval', 'Needs Commissioner Approval'),
#     ('Pending - Approved', 'Pending - Approved'),
#     ('Denied', 'Denied'),
#     ('Resolved', 'Resolved'),
#     ('Hold', 'Hold')
# ]

# request_statuses = [
#     (status.NDA, status.NDA),
#     (status.NCA, status.NCA),
#     (status.APR, status.APR),
#     (status.DEN, status.DEN),
#     (status.RES, status.RES),
#     (status.HOLD, status.HOLD)
# ]


class CommentForm(Form):
    """Form for creating a new comment."""
    content = TextAreaField(validators=[Length(0, 500), DataRequired('Please enter a comment')])
    file = FileField(u'Upload File...')
    submit = SubmitField(u'Add Comment')


class RequestForm(Form):
    """Form for creating a new request."""
    item = TextAreaField(u'Item*(required)', validators=[
        DataRequired('Please enter the item')])
    quantity = IntegerField(u'Quantity*', validators=[
        DataRequired('Please enter the quantity')])
    unit_price = DecimalField(u'Price per item*', validators=[
        DataRequired('Please enter the price per item')])
    total_cost = DecimalField(u'Total price*', validators=[
        DataRequired('Please enter the total price')])
    funding_source = SelectField(u'Funding*', choices=funding, validators=[
        DataRequired('Please select the funding source')])
    funding_source_description = StringField(u'Funding Other')
    grant_name = StringField(u'Grant Name')
    project_name = StringField(u'Project Name')
    justification = TextAreaField(u'Justification*(required)', validators=[
        DataRequired('You must enter a justification for your request'), Length(1, 500)])
    request_vendor_dropdown = SelectField(u'Vendor Information*')
    request_vendor_name = StringField(u'Vendor Name')
    request_vendor_address = StringField(u'Vendor Address')
    request_vendor_phone = PhoneNumberField(region='US', display_format='national')
    request_vendor_fax = PhoneNumberField(region='US', display_format='national')
    request_vendor_email = StringField(u'Email')
    request_vendor_taxid = StringField(u'Vendor Tax ID')
    request_vendor_mwbe = BooleanField(u'mwbe')
    submit = SubmitField(u'Submit Request')

    def __init__(self, *args, **kwargs):
        """Fill the vendor dropdown with values from the database upon initialization"""
        super(RequestForm, self).__init__(*args, **kwargs)

        from app.models import Vendor
        vendors = Vendor.query.order_by(Vendor.name).all()
        vendor_dropdown = [
            ('default', 'Select Vendor or Enter New Vendor Below')
        ]
        for vendor in vendors:
            vendor_dropdown.append((str(vendor.id), vendor.name))
        self.request_vendor_dropdown.choices = vendor_dropdown

    def validate(self):
        if not Form.validate(self):
            return False

        # check if user selected other and filled out the field
        if self.funding_source.data == "Other" and not self.funding_source_description.data:
            self.funding_source.errors.append("You must specify if you entered Other")
            return False

        # check if user selected grant and filled out the fields
        if self.funding_source.data == "Grant" and (not self.grant_name.data or not self.project_name.data):
            self.funding_source.errors.append("You must include a grant and project name if you entered Grant")
            return False

        # check if user filled out the vendor fields
        if self.request_vendor_dropdown.data == "default" and not \
                (self.request_vendor_name.data and self.request_vendor_address.data and
                self.request_vendor_address.data and self.request_vendor_phone.data and
                self.request_vendor_fax.data and self.request_vendor_email.data and
                self.request_vendor_taxid.data):
            self.request_vendor_name.errors.append("You must fill out all fields for Vendor Information")
            return False

        return True


class DeleteCommentForm(Form):
    """Form for deleting a comment."""
    request_id = HiddenField()
    comment_id = HiddenField()
    submit = SubmitField(u'Delete')


class StatusForm(Form):
    """Form for updating status of a request."""
    status = SelectField(u'Status', validators=[DataRequired()])
    submit = SubmitField(u'Update')
