"""
.. module:: vendor.forms.

   :synopsis: Defines forms used to manage vendor information
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms_alchemy import PhoneNumberField
from wtforms.validators import DataRequired, Length, Email, Regexp

regexp_message = "Must only contain alphanumeric characters or the following " \
                 "characters: ' ,-."


from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class VendorForm(FlaskForm):
    vendorName = StringField('Vendor Name', validators=[DataRequired()])
    vendorAddress = StringField('Vendor Address', validators=[DataRequired()])
    vendorPhone = StringField('Vendor Phone', validators=[DataRequired()])
    vendorFax = StringField('Vendor Fax', validators=[DataRequired()])
    vendorEmail = StringField('Vendor Email', validators=[DataRequired()])
    vendorTaxId = StringField('Vendor/Tax ID', validators=[DataRequired()])
    enable = BooleanField('Enable')
    mWbe = BooleanField('M/WBE')
    submit = SubmitField('Submit')




class NewVendorForm(FlaskForm):
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
    enabled = BooleanField(u'Enabled') # New field
    submit = SubmitField(u'Create Vendor')


class EditVendorForm(FlaskForm):
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
    enabled = BooleanField(u'Enabled') # New field
    submit = SubmitField(u'Edit Vendor')
