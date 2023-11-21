from .extensions import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer
from sqlalchemy.orm.attributes import set_attribute
from flask import current_app
from app.constants import division, roles
from app.extensions import db, login_manager
import re
import uuid
from sqlalchemy.dialects.postgresql import UUID


class User(UserMixin, db.Model):
    """The User class containing user and login information"""
    __tablename__ = 'user'
    __table_args__ = {'schema': 'main'}
    # Changed from db.Integer to UUID and added a default UUID generator
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, index=True)
    phone = db.Column(db.String(), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    division = db.Column(db.Enum(division.MRMD,
                                 division.ARC,
                                 division.GRA,
                                 division.LIB,
                                 division.EXEC,
                                 division.TECH,
                                 division.ADM, name="division"))
    password_hash = db.Column(db.String(128))
    login = db.Column(db.BOOLEAN, default=True)
    role = db.Column(db.String(100), default=roles.REG)

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

    # Generates token with default validity for 1 hour
    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    # Verifies the token and if valid, resets password
    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        # Checks if the new password is at least 8 characters with at least 1 UPPERCASE AND 1 NUMBER
        if not re.match(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{8,128}$', new_password):
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.first_name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Request(db.Model):
    __tablename__ = 'request'
    __table_args__ = {'schema': 'main'}

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('main.user.id'))
    division = db.Column(db.String(100))
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)
    date_closed = db.Column(db.DateTime)
    item = db.Column(db.String(500))
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Numeric)
    total_cost = db.Column(db.Numeric)
    funding_source = db.Column(db.String(100))
    grant_name = db.Column(db.String(100), nullable=True)
    project_name = db.Column(db.String(100), nullable=True)
    funding_source_description = db.Column(db.String(100), nullable=True)
    justification = db.Column(db.String(500))
    status = db.Column(db.String(100))
    vendor_id = db.Column(UUID(as_uuid=True), db.ForeignKey('main.vendor.id'))

    def __init__(self, division, item, quantity, unit_price, total_cost, funding_source, grant_name, project_name, funding_source_description, justification, status, creator_id, vendor_id=None):
        self.id = str(uuid.uuid4())  # Generate a new UUID for each request
        self.division = division
        # This will automatically set the current date and time
        self.date_submitted = datetime.utcnow()
        self.item = item
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_cost = total_cost
        self.funding_source = funding_source
        self.grant_name = grant_name
        self.project_name = project_name
        self.funding_source_description = funding_source_description
        self.justification = justification
        self.status = status
        self.creator_id = creator_id
        self.vendor_id = vendor_id  # Set vendor_id

    # Rest of the class code...

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
    __table_args__ = {'schema': 'main'}
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  #
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(), nullable=True)
    fax = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    tax_id = db.Column(db.String(100), nullable=True)
    mwbe = db.Column(db.Boolean, nullable=False, default=False)
    enabled = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(
            self,
            name,
            address,
            phone,
            fax,
            email,
            tax_id,
            mwbe,
            enabled=True,
    ):
        self.name = name
        self.address = address
        self.phone = phone
        self.fax = fax
        self.email = email
        self.tax_id = tax_id
        self.mwbe = mwbe
        self.enabled = enabled

    def __repr__(self):
        return '<Vendor {}>'.format(self.id)

    def update_field(self, key, value):
        """Update the specified field(s) from kwarg."""
        set_attribute(self, key, value)


class Comment(db.Model):
    """Comment and/or file that can be added to a specific request"""
    __tablename__ = 'comment'
    __table_args__ = {'schema': 'main'}

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    request_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey('main.request.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('main.user.id'))
    timestamp = db.Column(db.DateTime)
    content = db.Column(db.String())
    filepath = db.Column(db.String())
    editable = db.Column(db.Boolean, nullable=False, default=True)
    user = db.relationship("User", backref="user")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
