from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import db, login_manager


class User(UserMixin, db.Model):
    """The User class containing user and login information"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, index=True)
    division = db.Column(db.String(100))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

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
    # Each request has a foreign key to many comments in the Comment table. Each request can have many comments.
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
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
            creator_id
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
        self.creator_id = creator_id

    def set_vendor_id(self, vendor_id):
        """Sets vendor_id in request table

            :param: vendor_id: Vendor ID
        """
        self.vendor_id = vendor_id

    def __repr__(self):
        return '<id {}>'.format(self.id)


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
        return '<id {}>'.format(self.id)


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    timestamp = db.Column(db.DateTime)
    content = db.Column(db.String())
    filepath = db.Column(db.String())
    # Each comment has a foreign key to a request.
    request = db.Column(db.Integer, db.ForeignKey('request.id'))
    # Each comment has a foreign key to a user.
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
