from . import db


class Request(db.Model):
    # The procurement request

    __tablename__ = 'request'
    id = db.Column(db.Integer, primary_key=True)
    date_submitted = db.Column(db.DateTime)
    name = db.Column(db.String(100))
    division = db.Column(db.String(100))
    item = db.Column(db.String(100))
    quantity = db.Column(db.Integer)

    def __init__(self, name, date_submitted, division, item, quantity):
        if date_submitted and str(type(date_submitted)) == "<type 'datetime.date'>":
            self.date_submitted = date_submitted
        self.name = name
        self.division = division
        self.item = item
        self.quantity = quantity

    def __repr__(self):
        return '<id {}>'.format(self.id)


