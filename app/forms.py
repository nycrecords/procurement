from flask import Flask
from flask.ext.wtf import Form
from wtforms import StringField, SelectField, TextAreaField, DateField, \
		BooleanField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, Email

app = Flask(__name__)

divisions = [
		('', ''),
		('MRMD', 'MRMD'),
		('Archives', 'Archives'),
		('Grants', 'Grants'),
		('Library', 'Library'),
		('Executive', 'Executive'),
		('MIS/Web', 'MIS/Web'),
		('Administration', 'Administration')
		]

funding = [
		('', ''),
		('Expense', 'Expense'),
		('MAARF', 'MAARRF'),
		('SARA', 'SARA'),
		('KOCH', 'KOCH'),
		('Other','Other')
		]

class NewRequestForm(Form):
		request_name = StringField(u'Name', validators=[
				DataRequired('Please enter the requestor\'s name')])
		request_division = SelectField(u'Division*', choices=divisions,
																	 validators=[DataRequired(
																			 'The request division is required')])
		request_item = TextAreaField(u'Item*(required)', validators=[
			DataRequired('You must enter a FULL item ''description of your request'),
			Length(1, 250,'Your request summary must be less than 250 characters')])
		request_quantity = StringField(u'Quantity*', validators=[
				DataRequired('Please enter the quantity')])
		request_funding_source = SelectField(u'Funding*', choices=funding,
																		validators=[DataRequired(
																				'The request funding source is required')])  
		submit = SubmitField(u'Submit Request')  

