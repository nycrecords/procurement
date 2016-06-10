"""Forms related to a specific request."""
from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import StringField, SelectField, TextAreaField, RadioField, \
    DecimalField, IntegerField


funding = [
    ('', ''),
    ('Expense', 'Expense'),
    ('MAARF', 'MAARRF'),
    ('SARA', 'SARA'),
    ('KOCH', 'KOCH'),
    ('Other', 'Other')
]


class EditRequestForm(Form):
    """A form for editing an existing request"""
    item = TextAreaField(u'Item*(required)', validators=[
    DataRequired('You must enter a FULL item description of your request'),
    Length(1, 100, 'The item description must be less than 100 characters')])
quantity = IntegerField(u'Quantity*', validators=[
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
request_MWBE = RadioField(u'MWBE', choices=[('True', 'Yes'), ('False', 'No')], validators=[Optional()])
submit = SubmitField(u'Submit Request')
