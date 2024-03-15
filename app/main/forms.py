"""
.. module:: main.forms.

    :synopsis: Defines forms used to create procurement requests
"""
from flask import Flask
from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField, SubmitField, BooleanField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Length, Email
from wtforms_alchemy import PhoneNumberField
from app.constants import division, roles

app = Flask(__name__)

funding = [
    ('', ''),
    ('Expense', 'Expense'),
    ('MAARF', 'MAARRF'),
    ('Grant', 'Grant'),
    ('KOCH', 'KOCH'),
    ('Other', 'Other')
]

divisions = [(division.MRMD, division.MRMD),
             (division.ARC, division.ARC),
             (division.GRA, division.GRA),
             (division.LIB, division.LIB),
             (division.EXEC, division.EXEC),
             (division.TECH, division.TECH),
             (division.ADM, division.ADM)]

roles = [(roles.REG, roles.REG),
         (roles.DIV, roles.DIV),
         (roles.COM, roles.COM),
         (roles.PROC, roles.PROC),
         (roles.ADMIN, roles.ADMIN)]


class RequestForm(Form):
    """Form for creating a new request."""
    request_name = StringField(u'Name*(required)')
    division = SelectField(u'Division*', choices=divisions, default='')
    item = TextAreaField(u'Item*(required)')
    quantity = IntegerField(u'Quantity*', validators=[DataRequired('Please enter the quantity')])
    unit_price = DecimalField(u'Price per item*', validators=[DataRequired('Please enter the price per item')])
    total_cost = DecimalField(u'Total price*', validators=[DataRequired('Please enter the total price')])
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


class UserForm(Form):
    """Form for creating a new user."""
    first_name = StringField('first_name', validators=[DataRequired(), Length(1, 300)])
    last_name = StringField('last_name', validators=[DataRequired(), Length(1, 200)])
    division = SelectField('division', validators=[DataRequired()], choices=divisions)
    email = StringField('Email', validators=[DataRequired(), Length(1, 200), Email()])
    phone = PhoneNumberField('Phone', region='US', display_format='national', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField(u'Create User')


class EditUserForm(Form):
    """Form for updating user information."""
    user_first_name = StringField(u'First Name*(required)', validators=[DataRequired(), Length(1, 100)])
    user_last_name = StringField(u'Last Name*(required)', validators=[DataRequired(), Length(1, 100)])
    user_role = SelectField('division', validators=[DataRequired()], choices=roles)
    user_email = StringField(u'Email*(required)', validators=[DataRequired(), Length(1, 100), Email()])
    user_phone = PhoneNumberField('Phone', region='US', display_format='national', validators=[DataRequired()])
    user_address = StringField('Address', validators=[DataRequired()])
    update = SubmitField(u'Update Information')
