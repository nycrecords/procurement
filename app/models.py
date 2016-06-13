from flask_login import UserMixin
from . import db
from datetime import datetime


class User(UserMixin, db.Model):
    """The User class containing user and login information"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, index=True)
    division = db.Column(db.String(100))
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.id)


class Request(db.Model):
    """The procurement request class"""
    __tablename__ = 'request'
    id = db.Column(db.Integer, primary_key=True)
    date_submitted = db.Column(db.DateTime)
    date_closed = db.Column(db.DateTime)
    name = db.Column(db.String(100))
    item = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Numeric)
    total_cost = db.Column(db.Numeric)
    funding_source = db.Column(db.String(100))
    funding_source_description = db.Column(db.String(100), nullable=True)
    justification = db.Column(db.String(255))
    # Each request has a foreign key to a vendor in the Vendor table. Each request can only have ONE vendor.
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))
    # Each request has a foreign key to a creator in the User table. Each request can only have ONE creator.
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(100))

    def __init__(
            self,
            name,
            date_submitted,
            item,
            quantity,
            unit_price,
            total_cost,
            funding_source,
            funding_source_description,
            justification,
    ):
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

    def set_vendor_id(self, vendor_id):
        """Sets vendor_id in request table

            :param: vendor_id: Vendor ID
        """
        self.vendor_id = vendor_id

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
    mwbe = db.Column(db.Boolean, nullable=True)

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


class Comment(db.Model):

    """Comment and/or file that can be added to a specific request"""
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime)
    content = db.Column(db.String())
    filepath = db.Column(db.String())

    def __init__(
        self,
        request_id,
        user_id,
        content,
        filepath=None
    ):
        """
        Create a comment.

        :param request_id: Request where comment was posted.
        :param user_id: User ID of poster.
        :param content: Content for the comment.
        :param filepath: Filepath of uploaded file (if any).

        :return: ID of created comment.
        """
        self.request_id = request_id
        self.user_id = user_id
        self.timestamp = datetime.now()
        self.content = content
        self.filepath = filepath

    def __repr__(self):
        """Return string representation of Comment. """
        return '<Comment {}>'.format(self.id)
