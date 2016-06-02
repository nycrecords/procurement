from flask import render_template, request
from .. import db
from ..models import Request
from . import main
from .forms import NewRequestForm


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/new', methods=['GET', 'POST'])
def new_request():
    form = NewRequestForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            newrequest = Request(form.name.data, form.division.data, form.item.data, form.quantity.data)
            db.session.add(newrequest)
            db.session.commit()
        else:
            print form.errors

    return render_template('new_request2.html', form=form)
