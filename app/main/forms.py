"""
.. module:: main.forms.

    :synopsis: Defines forms used to create procurement requests
"""
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
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

divisions = [(None, None),
             (division.MRMD, division.MRMD),
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


class EditUserForm(FlaskForm):
    """Form for updating user information."""
    role = SelectField('role', validators=[DataRequired()], choices=roles)
    division = SelectField('division', validators=[DataRequired()], choices=divisions)
    phone = PhoneNumberField('Phone', region='US', display_format='national', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    update = SubmitField(u'Update Information')
