"""
.. module:: request.forms.

    :synopsis: Defines forms used to create Procurement requests.
"""

from flask import Flask
from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField, SubmitField, \
     BooleanField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Length
from wtforms_alchemy import PhoneNumberField
app = Flask(__name__)

divisions = [
    ('', ''),
    ('MRMD', 'MRMD'),
    ('Archives', 'Archives'),
    ('Grants', 'Grants'),
    ('Library', 'Library'),
    ('Executive', 'Executive'),
    ('MIS/Web', 'MIS/Web'),
    ('Administration', 'Administration')
]

funding = [
    ('', ''),
    ('Expense', 'Expense'),
    ('MAARF', 'MAARRF'),
    ('Grant', 'Grant'),
    ('KOCH', 'KOCH'),
    ('Other', 'Other')
]


class RequestForm(Form):
    """Form for creating a new request"""
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
    submit = SubmitField(u'Submit Request')
