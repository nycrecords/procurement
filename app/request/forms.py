from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DecimalField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional

class RequestForm(FlaskForm):
    """Form for creating a new request."""
    item = TextAreaField('Item*(required)', validators=[DataRequired('Please enter the item'), Length(1, 500)])
    quantity = IntegerField('Quantity*', validators=[DataRequired('Please enter the quantity (only numbers are allowed)')])
    unit_price = DecimalField('Unit Price*', validators=[DataRequired('Please enter the price per unit (only numbers are allowed)')])
    total_cost = DecimalField('Total price*', validators=[DataRequired('Please enter the total price (only numbers are allowed)')])
    funding_source = SelectField('Funding*', choices=[('Expense', 'Expense'), ('MAARRF', 'MAARRF'), ('Grant', 'Grant'), ('SARA', 'SARA'), ('KOCH', 'KOCH'), ('Other', 'Other')], validators=[DataRequired('Please select the funding source')])
    funding_source_description = StringField('Funding Other')
    justification = TextAreaField('Justification*(required)', validators=[DataRequired('You must enter a justification for your request'), Length(1, 500)])

    # Updated field
    division = StringField('Division')
    grant_name = StringField('Grant Name')
    project_name = StringField('Project Name')


    # Vendor fields
    request_vendor_dropdown = SelectField('Vendor', validators=[Optional()], choices=[('default', 'Select Vendor or Enter new Vendor below'), ('1', 'Vendor 1'), ('2', 'Vendor 2')])
    request_vendor_name = StringField('Vendor Name', validators=[Length(5), Optional()])
    request_vendor_address = StringField('Vendor Address', validators=[Length(5), Optional()])
    request_vendor_phone = StringField('Vendor Phone')
    request_vendor_fax = StringField('Vendor Fax')
    request_vendor_email = StringField('Email', validators=[Email(), Optional()])
    request_vendor_taxid = StringField('Vendor Tax ID')
    request_vendor_mwbe = BooleanField('mwbe')
    request_vendor_enable = BooleanField('Vendor Enable')

    submit = SubmitField('Submit Request')

    def __init__(self, *args, **kwargs):
        """Fill the vendor dropdown with values from the database upon initialization"""
        super(RequestForm, self).__init__(*args, **kwargs)

        from ..models import Vendor
        vendors = Vendor.query.filter_by(enabled=True).order_by(Vendor.name).all()
        vendor_dropdown = [
            (0, 'Select Vendor or Enter New Vendor Below')
        ]
        for vendor in vendors:
            vendor_dropdown.append((vendor.id, vendor.name))
        self.request_vendor_dropdown.choices = vendor_dropdown

    def validate(self, extra_validators=None):
        if not FlaskForm.validate(self):
            print(self.errors)  # Print form errors
            return False

        # Check if user selected other and filled out the field
        if self.funding_source.data == "Other" and not self.funding_source_description.data:
            self.funding_source.errors.append("You must specify if you entered Other")
            return False

        return True

class EditRequestForm(FlaskForm):
    """Form for editing an existing request."""
    # assuming same fields as RequestForm
    item = TextAreaField('Item*(required)', validators=[DataRequired('Please enter the item'), Length(1, 500)])
    quantity = IntegerField('Quantity*', validators=[DataRequired('Please enter the quantity (only numbers are allowed)')])
    unit_price = DecimalField('Unit Price*', validators=[DataRequired('Please enter the price per unit (only numbers are allowed)')])
    total_cost = DecimalField('Total price*', validators=[DataRequired('Please enter the total price (only numbers are allowed)')])
    funding_source = SelectField('Funding*', choices=[('Expense', 'Expense'), ('MAARRF', 'MAARRF'), ('Grant', 'Grant'), ('SARA', 'SARA'), ('KOCH', 'KOCH'), ('Other', 'Other')], validators=[DataRequired('Please select the funding source')])
    funding_source_description = StringField('Funding Other')
    justification = TextAreaField('Justification*(required)', validators=[DataRequired('You must enter a justification for your request'), Length(1, 500)])

    # Updated field
    division = StringField('Division')
    grant_name = StringField('Grant Name')
    project_name = StringField('Project Name')

    # Vendor fields
    request_vendor_dropdown = SelectField('Vendor', validators=[Optional()], choices=[('default', 'Select Vendor or Enter new Vendor below'), ('1', 'Vendor 1'), ('2', 'Vendor 2')])
    request_vendor_name = StringField('Vendor Name', validators=[Length(5), Optional()])
    request_vendor_address = StringField('Vendor Address', validators=[Length(5), Optional()])
    request_vendor_phone = StringField('Vendor Phone')
    request_vendor_fax = StringField('Vendor Fax')
    request_vendor_email = StringField('Email', validators=[Email(), Optional()])
    request_vendor_taxid = StringField('Vendor Tax ID')
    request_vendor_mwbe = BooleanField('mwbe')
    request_vendor_enable = BooleanField('Vendor Enable')

    submit = SubmitField('Submit Request')

    # Similar to RequestForm, fill the vendor dropdown with values from the database upon initialization
    def __init__(self, *args, **kwargs):
        """Fill the vendor dropdown with values from the database upon initialization"""
        super(EditRequestForm, self).__init__(*args, **kwargs)

        from ..models import Vendor
        vendors = Vendor.query.filter_by(enabled=True).order_by(Vendor.name).all()
        vendor_dropdown = [
            (0, 'Select Vendor or Enter New Vendor Below')
        ]
        for vendor in vendors:
            vendor_dropdown.append((vendor.id, vendor.name))
        self.request_vendor_dropdown.choices = vendor_dropdown
