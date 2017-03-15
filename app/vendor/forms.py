"""
.. module:: vendor.forms.

   :synopsis: Defines forms used to manage vendor information
"""
from flask_wtf import Form
from wtforms import StringField, SubmitField, BooleanField
from wtforms_alchemy import PhoneNumberField


class NewVendorForm(Form):
    """Form for creating new vendor."""
    vendor_name = StringField(u'Vendor Name')
    vendor_address = StringField(u'Vendor Address')
    vendor_phone = PhoneNumberField(region='US', display_format='national')
    vendor_fax = PhoneNumberField(region='US', display_format='national')
    vendor_email = StringField(u'Email')
    vendor_tax_id = StringField(u'Vendor Tax ID')
    vendor_mwbe = BooleanField(u'mwbe')
    submit = SubmitField(u'Create Vendor')


class EditVendorForm(Form):
    """Form for editing vendor."""
    vendor_name = StringField(u'Vendor Name')
    vendor_address = StringField(u'Vendor Address')
    vendor_phone = PhoneNumberField(region='US', display_format='national')
    vendor_fax = PhoneNumberField(region='US', display_format='national')
    vendor_email = StringField(u'Email')
    vendor_tax_id = StringField(u'Vendor Tax ID')
    vendor_mwbe = BooleanField(u'mwbe')
    submit = SubmitField(u'Edit Vendor')
