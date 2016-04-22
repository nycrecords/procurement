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
				validators=[DataRequired('Please select the division')], default='')
		request_item = TextAreaField(u'Item*(required)', validators=[
				DataRequired('You must enter a FULL item description of your request'),
				Length(1, 100,'The item description must be less than 100 characters')])
		request_quantity = StringField(u'Quantity*', validators=[
				DataRequired('Please enter the quantity')])
		request_price_per_item = StringField(u'Price per item*', validators=[
				DataRequired('Please enter the price per item')])
		request_total = StringField(u'Total price*', validators=[
				DataRequired('Please enter the total price')])
		request_funding_source = SelectField(u'Funding*', choices=funding,
				validators=[DataRequired('Please select the funding source')])
		request_funding_other = StringField(u'Funding Other')
		request_justification = TextAreaField(u'Justification*(required)', validators=[
				DataRequired('You must enter a justification for your request'),
				Length(1, 255,'The justification must be less than 255 characters')])  
		submit = SubmitField(u'Submit Request')  

