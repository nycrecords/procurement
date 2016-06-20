from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    """The User class containing user and login information"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, index=True)
    division = db.Column(db.String(100))
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Permission:
    VIEW = 0x01
    CREATE = 0x02
    COMMENT = 0x04
    CHANGE_STATUS = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        """Insert permissions for each role: employee, director, and administrator."""
        roles = {
            'Regular User': (Permission.VIEW |
                             Permission.CREATE |
                             Permission.COMMENT | True),
            'Division Head': (Permission.VIEW |
                              Permission.CREATE |
                              Permission.COMMENT |
                              Permission.CHANGE_STATUS, False),
            'Procurement Head': (Permission.VIEW |
                                 Permission.CREATE |
                                 Permission.COMMENT |
                                 Permission.CHANGE_STATUS, False),
            'Commissioner': (Permission.VIEW |
                             Permission.CREATE |
                             Permission.COMMENT |
                             Permission.CHANGE_STATUS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


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
    grant_name = db.Column(db.String(100))
    project_name = db.Column(db.String(100))
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
            grant_name,
            project_name,
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
        self.grant_name = grant_name
        self.project_name = project_name
        self.funding_source_description = funding_source_description
        self.justification = justification

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
