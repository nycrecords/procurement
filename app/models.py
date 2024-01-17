from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer
from sqlalchemy.orm.attributes import set_attribute
from flask import current_app
from app.constants import division, roles, auth_event_type
from app import db, login_manager
import re
import uuid
from sqlalchemy.dialects.postgresql import UUID, JSONB


class User(UserMixin, db.Model):
    """The User class containing user and login information"""
    __tablename__ = 'users'
    guid = db.Column(db.String(32), unique=True, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(32), nullable=True)
    middle_initial = db.Column(db.String(1), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    email_validated = db.Column(db.Boolean(), nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=False)
    last_sign_in_at = db.Column(db.DateTime, nullable=False)
    session_id = db.Column(db.String(254), nullable=True, default=None)
    phone = db.Column(db.String(), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    division = db.Column(db.Enum(division.MRMD,
                                 division.ARC,
                                 division.GRA,
                                 division.LIB,
                                 division.EXEC,
                                 division.TECH,
                                 division.ADM, name="division"))
    login = db.Column(db.BOOLEAN, default=True)
    roles = db.relationship('Role', secondary='user_roles')
    # role = db.Column(db.String(100), default=roles.REG)

    def __init__(self, **kwargs):
        db.Model.__init__(self,  **kwargs)

    @property
    def id(self):
        return str(self.guid)

    @property
    def role(self):
        return self.roles[0].name if self.roles else None

    @property
    def name(self):
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def is_admin(self):
        return any(role.name == 'admin' for role in self.roles)

    # def __repr__(self):
    #     return '<User %r>' % self.first_name


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRole(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.String(), db.ForeignKey('users.guid', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


class Request(db.Model):
    __tablename__ = 'requests'
    # __table_args__ = {'schema': 'main'}

    # id = db.Column(UUID(as_uuid=True), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.String(32),  db.ForeignKey('users.guid'), nullable=False)
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
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))
    user = db.relationship('User', foreign_keys=[creator_id])


    def __init__(self, division, item, quantity, unit_price, total_cost, funding_source, grant_name, project_name, funding_source_description, justification, status, creator_id, vendor_id=None):
        # self.id = str(uuid.uuid4())  # Generate a new UUID for each request
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
    @property
    def user_email(self):
        if self.user:
            return self.user.email
        else:
            return None

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

    # def __repr__(self):
    #     return '<Request {}>'.format(self.id)


class Vendor(db.Model):
    """The vendor class containing vendor information"""
    __tablename__ = 'vendors'
    # __table_args__ = {'schema': 'main'}
    # id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  #
    id = db.Column(db.Integer, primary_key=True)
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
    __tablename__ = 'comments'
    # __table_args__ = {'schema': 'main'}
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    request_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey('requests.id'))
    user_id = db.Column(db.String(32), db.ForeignKey('users.guid'))
    timestamp = db.Column(db.DateTime)
    content = db.Column(db.String())
    filepath = db.Column(db.String())
    editable = db.Column(db.Boolean, nullable=False, default=True)
    user = db.relationship("User", backref="users")


class AuthEvent(db.Model):
    """
    Define the Auth Events class with the following columns and relationships:

    id - an integer that is the primary key of an Events
    user_guid - a foreign key that links to the user_guid of the person who performed the event
    type - a string containing the type of event that occurred
    timestamp - a datetime that keeps track of what time an event was performed
    previous_value - a string containing the old value of the event
    new_value - a string containing the new value of the event
    """

    __tablename__ = 'auth_events'
    id = db.Column(db.Integer, primary_key=True)
    user_guid = db.Column(db.String(64), db.ForeignKey('users.guid'))
    type = db.Column(db.Enum(
        auth_event_type.USER_CREATED,
        auth_event_type.USER_LOGIN,
        auth_event_type.USER_FAILED_LOG_IN,
        auth_event_type.USER_LOGGED_OUT,
        auth_event_type.USER_ROLE_CHANGED,
        auth_event_type.AGENCY_USER_ACTIVATED,
        auth_event_type.AGENCY_USER_DEACTIVATED,
        name='auth_event_type'), nullable=False
    )
    previous_value = db.Column(JSONB)
    new_value = db.Column(JSONB)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    user = db.relationship("User", backref="auth_events")

    def __init__(self, user_guid, type_, previous_value=None, new_value=None, timestamp=None):
        self.user_guid = user_guid
        self.type = type_
        self.previous_value = previous_value
        self.new_value = new_value
        self.timestamp = timestamp or datetime.now(timezone('US/Eastern'))


class Events(db.Model):

    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    request_number = db.Column(db.String(32), db.ForeignKey('requests.id', ondelete='CASCADE'))
    type = db.Column(db.Enum(
        # Add event Types
        name='event_type'), nullable=False
    )
    user_id = db.Column(db.String(100), db.ForeignKey('users.guid'))
    timestamp = db.Column(db.DateTime)
    previous_value = db.Column(JSONB)
    new_value = db.Column(JSONB)
    user = db.relationship(
        "User",
        backref="events"
    )

    def __init__(self,
                 request_number,
                 type_,
                 user_id=None,
                 previous_value=None,
                 new_value=None,
                 timestamp=None,):
        self.request_number = request_number
        self.type = type_
        self.user_id = user_id
        self.previous_value = previous_value
        self.new_value = new_value
        self.timestamp = timestamp or datetime.now(timezone('US/Eastern'))
