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

divisions = [
    ('', ''),
    ('MRMD', 'MRMD'),
    ('Archives', 'Archives'),
    ('Grants', 'Grants'),
    ('Library', 'Library'),
    ('Executive', 'Executive'),
    ('Tech', 'Tech'),
    ('Administration', 'Administration')
]

funding = [
    ('', ''),
    ('Expense', 'Expense'),
    ('MAARF', 'MAARRF'),
    ('Grant', 'Grant'),
    ('SARA', 'SARA'),
    ('KOCH', 'KOCH'),
    ('Other', 'Other')
]

statuses = [
    ('', ''),
    ('Submitted', 'Submitted'),
    ('Needs Division Approval', 'Needs Division Approval'),
    ('Needs Commissioner Approval', 'Needs Commissioner Approval'),
    ('Pending - Approved', 'Pending - Approved'),
    ('Denied', 'Denied'),
    ('Resolved', 'Resolved'),
    ('Hold', 'Hold')
]


class CommentForm(Form):
    """Form for creating a new comment."""
    content = TextAreaField(validators=[Length(0, 500), DataRequired()])
    request_id = HiddenField()
    file = FileField(u'Upload File...')
    submit = SubmitField(u'Add Comment')


class RequestForm(Form):
    """Form for creating a new request."""
    request_name = StringField(u'Name*(required)')
    division = SelectField(u'Division*', choices=divisions, default='')
    item = TextAreaField(u'Item*(required)')
    quantity = IntegerField(u'Quantity*', validators=[
        DataRequired('Please enter the quantity')])
    unit_price = DecimalField(u'Price per item*', validators=[
        DataRequired('Please enter the price per item')])
    total_cost = DecimalField(u'Total price*', validators=[
        DataRequired('Please enter the total price')])
    funding_source = SelectField(u'Funding*', choices=funding,
                                 validators=[DataRequired('Please select the funding source')])
    funding_source_description = StringField(u'Funding Other')
    grant_name = StringField(u'Grant Name')
    project_name = StringField(u'Project Name')
    justification = TextAreaField(u'Justification*(required)', validators=[
        DataRequired('You must enter a justification for your request'), Length(1, 500)])
    request_vendor_name = StringField(u'Vendor Name')
    request_vendor_address = StringField(u'Vendor Address')
    request_vendor_phone = PhoneNumberField(region='US', display_format='national')
    request_vendor_fax = PhoneNumberField(region='US', display_format='national')
    request_vendor_email = StringField(u'Email')
    request_vendor_taxid = StringField(u'Vendor Tax ID')
    request_vendor_mwbe = BooleanField(u'mwbe')
    status = SelectField(u'status', validators=[], choices=[(status.NDA, status.NDA),
                                                                          (status.NCA, status.NCA),
                                                                          (status.APR, status.APR),
                                                                          (status.DEN, status.DEN),
                                                                          (status.RES, status.RES),
                                                                          (status.HOLD, status.HOLD)],
                         default=status.NDA)
    # comment = TextAreaField(validators=[Length(0, 500)])
    submit = SubmitField(u'Submit Request')


class DeleteCommentForm(Form):
    """Form for deleting a comment."""
    request_id = HiddenField()
    comment_id = HiddenField()
    submit = SubmitField(u'delete')


class StatusForm(Form):
    status = SelectField(u'status', validators=[DataRequired()])
    submit = SubmitField(u'Update')
