"""
.. module: models.

    :synopsis: Defines the models and methods for database objects
"""
from datetime import datetime, timezone

from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm.attributes import set_attribute

from app import db
from app.constants import division, roles, auth_event_type, status


class User(UserMixin, db.Model):
    """The User class containing user and login information"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(32), unique=True)
    first_name = db.Column(db.String(100))
    middle_initial = db.Column(db.String(1), nullable=True)
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, index=True)
    email_validated = db.Column(db.Boolean(), nullable=False, default=False)
    phone = db.Column(db.String(), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    division = db.Column(db.Enum(division.MRMD,
                                 division.ARC,
                                 division.GRA,
                                 division.LIB,
                                 division.EXEC,
                                 division.TECH,
                                 division.ADM, name="division"))
    last_sign_in_at = db.Column(db.DateTime, nullable=True)
    session_id = db.Column(db.String(254), nullable=True, default=None)
    is_active = db.Column(db.BOOLEAN, default=True)
    role = db.Column(db.String(100), default=roles.REG)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    def get_id(self):
        return str(self.guid)

    @property
    def name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def __repr__(self):
        return '<User %r>' % self.first_name


class Request(db.Model):
    """The procurement request class"""
    __tablename__ = 'requests'
    id = db.Column(db.String(11), primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
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
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))
    status = db.Column(db.String(100))

    def __init__(
            self,
            request_id,
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
            status,
            creator_id
    ):
        self.id = request_id
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
        self.status = status
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
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
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
            mwbe
    ):
        self.name = name
        self.address = address
        self.phone = phone
        self.fax = fax
        self.email = email
        self.tax_id = tax_id
        self.mwbe = mwbe
        self.enabled = True

    def __repr__(self):
        return '<Vendor {}>'.format(self.id)

    def update_field(self, key, value):
        """Update the specified field(s) from kwarg."""
        set_attribute(self, key, value)


class Comment(db.Model):
    """Comment and/or file that can be added to a specific request"""
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    request_id = db.Column(db.String(11), db.ForeignKey('requests.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
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


class StatusEvents(db.Model):
    """
    Define the Status Events class with the following columns and relationships:
    id - an integer that is the primary key of an Events
    previous_value = a string containing the previous value of the event
    new_value = a string containing the new value of the event
    request_id = a foreign key that links to the request_id of the request of the event
    user_id = a foreign key that links to the user_id of the person who updated the request
    timestamp - a datetime that keeps track of what time an event was performed
    """

    __tablename__ = 'status_events'
    id = db.Column(db.Integer, primary_key=True)
    previous_value = db.Column(db.Enum(status.NDA,
                                       status.NCA,
                                       status.NPA,
                                       status.APR,
                                       status.OIP,
                                       status.DEN,
                                       status.RES,
                                       status.HOLD, name="status"))
    new_value = db.Column(db.Enum(status.NDA,
                                  status.NCA,
                                  status.NPA,
                                  status.APR,
                                  status.OIP,
                                  status.DEN,
                                  status.RES,
                                  status.HOLD, name="status"))
    request_id = db.Column(db.String(11), db.ForeignKey('requests.id'))
    user_guid = db.Column(db.String(64), db.ForeignKey('users.guid'))
    timestamp = db.Column(db.DateTime, default=datetime)
    user = db.relationship("User", backref="status_events")

    def __init__(self,
                 previous_value=None,
                 new_value=None,
                 request_id=None,
                 user_guid=None,
                 timestamp=None):
        self.previous_value = previous_value
        self.new_value = new_value
        self.request_id = request_id
        self.user_guid = user_guid
        self.timestamp = timestamp or datetime.now(timezone('US/Eastern'))

    @property
    def status_history(self):
        return {
            'id': self.id,
            'user': self.user_guid,
            'previous_status': self.previous_value,
            'new_status': self.new_value,
            'timestamp': self.timestamp.strftime('%m/%d/%Y %I:%M:%S %p')
        }

    def __repr__(self):
        return '<Status History {}>'.format(self.id)
