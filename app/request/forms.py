"""
.. module:: request.forms.

   :synopsis: Defines forms used to manage Procurement requests.
"""
from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField, SubmitField, \
     RadioField, DecimalField, IntegerField
from flask_wtf.file import FileField
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


class CommentForm(Form):
    body = StringField(u'Enter your comment', validators=[DataRequired()])
    file = FileField(u'Upload File...')
    submit = SubmitField(u'Add Comment')
