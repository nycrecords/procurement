from flask import Flask
from flask.ext.wtf import Form
from wtforms import StringField, SelectField, TextAreaField, DateField, \
    BooleanField, PasswordField, SubmitField, RadioField, DecimalField
from wtforms.validators import DataRequired, Length, Email
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
    ('SARA', 'SARA'),
    ('KOCH', 'KOCH'),
    ('Other', 'Other')
]


class NewRequestForm(Form):
    '''A form class for procurement new purchase requests'''
    request_name = StringField(u'Name*(required)', validators=[
        DataRequired('Please enter the requestor\'s name'), Length(1, 100)])
    division = SelectField(u'Division*', choices=divisions,
                           validators=[DataRequired('Please select the division')], default='')
    item = TextAreaField(u'Item*(required)', validators=[
        DataRequired('You must enter a FULL item description of your request'),
        Length(1, 100, 'The item description must be less than 100 characters')])
    quantity = StringField(u'Quantity*', validators=[
        DataRequired('Please enter the quantity')])
    unit_price = DecimalField(u'Price per item*', validators=[
        DataRequired('Please enter the price per item')])
    total_cost = DecimalField(u'Total price*', validators=[
        DataRequired('Please enter the total price')])
    funding_source = SelectField(u'Funding*', choices=funding,
                                 validators=[DataRequired('Please select the funding source')])
    funding_source_description = StringField(u'Funding Other')
    justification = TextAreaField(u'Justification*(required)', validators=[
        DataRequired('You must enter a justification for your request'),
        Length(1, 255, 'The justification must be less than 255 characters')])
    request_vendor_name = StringField(u'Vendor Name')
    request_vendor_address = StringField(u'Vendor Address')
    request_vendor_phone = PhoneNumberField(region='US', display_format='national')
    request_vendor_fax = PhoneNumberField(region='US', display_format='national')
    request_vendor_email = StringField(u'Email')
    request_vendor_taxid = StringField(u'Vendor Tax ID')
    request_MWBE = RadioField(u'MWBE', choices=[('True', 'Yes'), ('False', 'No')])
    submit = SubmitField(u'Submit Request')
