from app import app
from flask import Flask, render_template, request, flash
from forms import NewRequestForm

@app.route('/')
def main():
		return render_template('index.html')

@app.route("/new", methods=["GET", "POST"])
def new_request():
		form = NewRequestForm(request.form)

		if request.method == 'POST':
				if form.validate_on_submit():
						print form.request_name.data
						print form.request_division.data
						print form.request_item.data
						print form.request_quantity.data
						print form.request_price_per_item.data
						print form.request_total.data
						print form.request_funding_source.data
						print form.request_funding_other.data
						print form.request_justification.data
				else:
						print form.errors
		return render_template('new_request2.html', form=form)
