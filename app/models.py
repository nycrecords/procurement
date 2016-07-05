"""
.. module: models

    :synopsis: Defines the models and methods for database objects.
"""
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.orm.attributes import set_attribute
from . import db, login_manager
import re

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


class User(UserMixin, db.Model):
    """The User class containing user and login information"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, index=True)
    division = db.Column(db.String(divisions))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @property
    def name(self):
        return '%s %s' % (self.first_name, self.last_name)

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # generates token with default validity for 1 hour
    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    # verifies the token and if valid, resets password
    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        # checks if the new password is at least 8 characters with at least 1 UPPERCASE AND 1 NUMBER
        if not re.match(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{8,128}$', new_password):
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Request(db.Model):
    """The procurement request class"""
    __tablename__ = 'request'
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    division = db.Column(db.String(100))
    date_submitted = db.Column(db.DateTime)
    date_closed = db.Column(db.DateTime)
    item = db.Column(db.String(500))
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Numeric)
    total_cost = db.Column(db.Numeric)
    funding_source = db.Column(db.String(100))
    grant_name = db.Column(db.String(100))
    project_name = db.Column(db.String(100))
    funding_source_description = db.Column(db.String(100), nullable=True)
    justification = db.Column(db.String(500))
    # Each request has a foreign key to a vendor in the Vendor table. Each request can only have ONE vendor.
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))
    # Each request has a foreign key to a creator in the User table. Each request can only have ONE creator.
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(100))

    def __init__(
            self,
            division,
            date_submitted,
            item,
            quantity,
            unit_price,
            total_cost,
            funding_source,
            grant_name,
            project_name,
            funding_source_description,
            justification,
            creator_id
    ):
        self.division = division
        self.date_submitted = date_submitted
        # self.date_closed = date_closed
        self.item = item
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_cost = total_cost
        self.funding_source = funding_source
        self.grant_name = grant_name
        self.project_name = project_name
        self.funding_source_description = funding_source_description
        self.justification = justification
        self.creator_id = creator_id

    def set_vendor_id(self, vendor_id):
        """Sets vendor_id in request table

            :param: vendor_id: Vendor ID
        """
        self.vendor_id = vendor_id

    def update_field(self, key, value):
        """Update the specified field(s) from kwarg."""
        set_attribute(self, key, value)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Request {}>'.format(self.id)


class Vendor(db.Model):
    """The vendor class containing vendor information"""
    __tablename__ = 'vendor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(), nullable=True)
    fax = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    tax_id = db.Column(db.String(100), nullable=True)
    mwbe = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(
            self,
            name,
            address,
            phone,
            fax,
            email,
            tax_id,
            mwbe,
    ):
        self.name = name
        self.address = address
        self.phone = phone
        self.fax = fax,
        self.email = email
        self.tax_id = tax_id
        self.mwbe = mwbe

    def __repr__(self):
        return '<Vendor {}>'.format(self.id)

    def update_field(self, key, value):
        """Update the specified field(s) from kwarg."""
        set_attribute(self, key, value)


class Comment(db.Model):
    """Comment and/or file that can be added to a specific request"""
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime)
    content = db.Column(db.String())
    filepath = db.Column(db.String())
