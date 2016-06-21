"""
.. module:: request.forms.

   :synopsis: Defines forms used to manage Procurement requests.
"""
from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField, SubmitField, \
     RadioField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Length, Optional
from wtforms_alchemy import PhoneNumberField

funding = [
    ('', ''),
    ('Expense', 'Expense'),
    ('MAARF', 'MAARRF'),
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


class EditRequestForm(Form):
    """Form for editing a request."""

    status = SelectField(u'Status', choices=statuses)
    item = TextAreaField(u'Item', validators=[
        DataRequired('You must enter a FULL item description of your request'),
        Length(1, 100, 'The item description must be less than 100 characters')
        ])
    quantity = IntegerField(u'Quantity', validators=[
        DataRequired('Please enter the quantity')])
    unit_price = DecimalField(u'Price per item', validators=[
        DataRequired('Please enter the price per item')])
    total_cost = DecimalField(u'Total price', validators=[
        DataRequired('Please enter the total price')])
    funding_source = SelectField(u'Funding', choices=funding,
                                 validators=[DataRequired('Please select the funding source')])
    funding_source_description = StringField(u'Funding Other')
    justification = TextAreaField(u'Justification', validators=[
        DataRequired('You must enter a justification for your request'),
        Length(1, 255, 'The justification must be less than 255 characters')])
    save = SubmitField(u'Save Changes')

