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
				if form.validate() == False:
						flash('All fields are required.')
						return render_template('new_request2.html', form=form)
				else:
						return 'Form posted.'

		elif request.method == 'GET':
				return render_template('new_request2.html', form=form)