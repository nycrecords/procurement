"""
.. module:: vendor.forms.

   :synopsis: Defines forms used to manage vendor information
"""
from flask_wtf import Form
from wtforms import StringField, SubmitField, BooleanField, HiddenField
from wtforms_alchemy import PhoneNumberField
from wtforms.validators import DataRequired, Length, Email, Regexp

regexp_message = "Must only contain alphanumeric characters or the following " \
                 "characters: ' ,-."


class NewVendorForm(Form):
    """Form for creating new vendor."""
    vendor_name = StringField(u'Vendor Name', validators=[
        DataRequired('Please enter the name'),
        Regexp("^[\w, '-.]+$", message=regexp_message),
        Length(5)])
    vendor_address = StringField(u'Vendor Address', validators=[
        DataRequired('Please enter the address'),
        Regexp("^[\w, '-.]+$", message=regexp_message),
        Length(5)])
    vendor_phone = PhoneNumberField(region='US', display_format='national',
                                    validators=[DataRequired('Please enter the phone number')])
    vendor_fax = PhoneNumberField(region='US', display_format='national',
                                  validators=[DataRequired('Please enter the fax number')])
    vendor_email = StringField(u'Email', validators=[DataRequired('Please enter the email'), Email()])
    vendor_tax_id = StringField(u'Vendor Tax ID', validators=[DataRequired('Please enter the tax id')])
    vendor_mwbe = BooleanField(u'mwbe')
    submit = SubmitField(u'Create Vendor')


class EditVendorForm(Form):
    """Form for editing vendor."""
    vendor_name = StringField(u'Vendor Name', validators=[
        DataRequired('Please enter the name'),
        Regexp("^[\w, '-.]+$", message=regexp_message),
        Length(5)])
    vendor_address = StringField(u'Vendor Address', validators=[
        DataRequired('Please enter the address'),
        Regexp("^[\w, '-.]+$", message=regexp_message),
        Length(5)])
    vendor_phone = PhoneNumberField(region='US', display_format='national',
                                    validators=[DataRequired('Please enter the phone number')])
    vendor_fax = PhoneNumberField(region='US', display_format='national',
                                  validators=[DataRequired('Please enter the fax number')])
    vendor_email = StringField(u'Email', validators=[DataRequired('Please enter the email'), Email()])
    vendor_tax_id = StringField(u'Vendor Tax ID', validators=[DataRequired('Please enter the tax id')])
    vendor_mwbe = BooleanField(u'mwbe')
    submit = SubmitField(u'Edit Vendor')
