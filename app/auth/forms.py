from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Email, InputRequired


class LoginForm(FlaskForm):
    username = StringField("Email Address", validators=[InputRequired(), Email()])
    submit = SubmitField("Log In")
