from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField, SubmitField, \
     RadioField, DecimalField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, Optional
from wtforms_alchemy import PhoneNumberField


class EditVendorForm(Form):
    """Form for editing the vendor."""
    name = StringField(u'Vendor Name')
    address = StringField(u'Vendor Address')
    phone = PhoneNumberField(
                            region='US',
                            display_format='national'
                            )
    fax = PhoneNumberField(
                            region='US',
                            display_format='national'
                            )
    email = StringField(u'Email')
    taxid = StringField(u'Vendor Tax ID')
    mwbe = BooleanField(u'mwbe')
    save = SubmitField(u'Save Changes')
