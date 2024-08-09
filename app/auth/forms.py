from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Email, InputRequired


# Development login
class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[InputRequired(), Email()])
    submit = SubmitField("Log In")
