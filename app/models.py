from flask_login import UserMixin
from datetime import datetime
from . import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, index=True)
    division = db.Column(db.String(100))
    password_hash = db.Column(db.String(128))
    request_id = db.relationship('Request', backref='users', lazy='dynamic')
    note_id = db.relationship('Note', backref='users', lazy='dynamic')

    # def __repr__(self):
    #     return '<id {}>'.format(self.id)


class Request(db.Model):
    # The procurement request

    __tablename__ = 'request'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_submitted = db.Column(db.DateTime)
    date_closed = db.Column(db.DateTime)
    name = db.Column(db.String(100))
    item = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Numeric)
    total_cost = db.Column(db.Numeric)
    funding_source = db.Column(db.String(100))
    funding_source_description = db.Column(db.String(100))
    justification = db.Column(db.String(255))
    vendor_id = db.relationship('Vendor', backref='request', lazy='dynamic')
    note_id = db.relationship('Note', backref='request', lazy='dynamic')
    status = db.Column(db.String(100))

    def __init__(
            self,
            # id,
            name,
            date_submitted,
            # date_closed,
            item,
            quantity,
            unit_price,
            total_cost,
            funding_source,
            funding_source_description,
            justification,
            # vendor_id,
            # status
    ):
        # self.id = id
        self.name = name
        self.date_submitted = date_submitted
        # self.date_closed = date_closed
        self.item = item
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_cost = total_cost
        self.funding_source = funding_source
        self.funding_source_description = funding_source_description
        self.justification = justification
        # self.vendor_id = vendor_id
        # self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Vendor(db.Model):
    __tablename__ = 'vendor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    phone = db.Column(db.String())
    fax = db.Column(db.String())
    email = db.Column(db.String(100))
    tax_id = db.Column(db.String(100))
    mwbe = db.Column(db.Boolean, nullable=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'))

    def __init__(
            self,
            name,
            address,
            phone,
            fax,
            email,
            tax_id,
            mwbe,
            request_id,
    ):
        self.name = name
        self.address = address
        self.phone = phone
        self.fax = fax,
        self.email = email
        self.tax_id = tax_id
        self.mwbe = mwbe
        self.request_id = request_id

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Note(db.Model):
    __tablename__ = 'note'
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime)
    content = db.Column(db.String())
