"""
.. module:: vendor.forms.

   :synopsis: Defines forms used to manage vendor information
"""
from flask_wtf import Form
from wtforms import StringField, SubmitField, BooleanField
from wtforms_alchemy import PhoneNumberField


class EditVendorForm(Form):
    """Form for editing vendor."""
    name = StringField(u'Vendor Name')
    address = StringField(u'Vendor Address')
    phone = PhoneNumberField(region='US', display_format='national')
    fax = PhoneNumberField(region='US', display_format='national')
    email = StringField(u'Email')
    taxid = StringField(u'Vendor Tax ID')
    mwbe = BooleanField(u'mwbe')
    save = SubmitField(u'Save Changes')
