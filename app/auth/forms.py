"""
.. module:: auth.forms

    :synopsis: Defines for the functionality of user accounts.
"""


from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Length
from ..models import User


class LoginForm(Form):
    """Form for user login"""
    email = StringField('Email', validators=[DataRequired('Please enter your email address'), Length(1, 100), Email()])
    password = PasswordField('Password', validators=[DataRequired('Please enter your password')])
    submit = SubmitField('Log In')


class ChangePasswordForm(Form):
    """Form for changing password"""
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[DataRequired()])
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(Form):
    """Initial request form for password reset"""
    email = StringField('Email', validators=[DataRequired(), Length(1, 100),
                                             Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(Form):
    """Password reset form after email confirmation"""
    email = StringField('Email', validators=[DataRequired(), Length(1, 100),
                                             Email()])
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')
