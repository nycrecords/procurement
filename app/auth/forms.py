"""
.. module:: auth.forms.

    :synopsis: Defines for the functionality of user accounts
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app.models import User
from app.constants import division


class LoginForm(FlaskForm):
    """Form for user login."""
    email = StringField('Email', validators=[DataRequired('Please enter your email address'), Length(1, 100), Email()])
    password = PasswordField('Password', validators=[DataRequired('Please enter your password')])
    submit = SubmitField('Log In')


class ChangePasswordForm(FlaskForm):
    """Form for changing password."""
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), Length(8), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[DataRequired(), Length(8)])
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(FlaskForm):
    """Initial request form for password reset."""
    email = StringField('Email', validators=[DataRequired(), Length(1, 100), Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    """Password reset form after email confirmation."""
    email = StringField('Email', validators=[DataRequired(), Length(1, 100), Email()])
    password = PasswordField('New Password',
                             validators=[DataRequired(), Length(8), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired(), Length(8)])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')


class SignupForm(FlaskForm):
    """Form for creating a new user account."""
    first_name = StringField('first_name', validators=[DataRequired(), Length(1, 100)])
    last_name = StringField('last_name', validators=[DataRequired(), Length(1, 100)])
    division = SelectField('division', validators=[DataRequired()], choices=[(division.MRMD, division.MRMD),
                                                                             (division.ARC, division.ARC),
                                                                             (division.GRA, division.GRA),
                                                                             (division.LIB, division.LIB),
                                                                             (division.EXEC, division.EXEC),
                                                                             (division.TECH, division.TECH),
                                                                             (division.ADM, division.ADM)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 100), Email()])
    password = PasswordField('password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError('Email address already in use.')
