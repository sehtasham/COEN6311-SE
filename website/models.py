from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_name = db.Column(db.String(10000))
    destination_name = db.Column(db.String(10000))
    departure_date = db.Column(db.DateTime(timezone=True), default=func.now())
    return_date = db.Column(db.DateTime(timezone=True), default=func.now())
    price = db.Column(db.Numeric(10,2))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200),  nullable=False)
    first_name = db.Column(db.String(200),  nullable=False)
    phonenumber = db.Column(db.String(200), nullable=True)
    city = db.Column(db.String(200), nullable=True)
    country = db.Column(db.String(200), nullable=True)
    postalcode = db.Column(db.String(200), nullable=True)

    admin = db.Column(db.Boolean, nullable=False, default=False)
    tiket = db.relationship('Ticket')


class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sourceLocation = db.Column(db.String(200), nullable=False)
    destinationLocation = db.Column(db.String(200), nullable=False)
    departureDate = db.Column(db.Date(), nullable=False)
    returnDate = db.Column(db.Date(), nullable=False)
    adults = db.Column(db.String(200), nullable=False)
    children = db.Column(db.String(200), nullable=False)
    notes = db.relationship('Note')

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'))

class Tickett(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_name = db.Column(db.String(10000))
    destination_name = db.Column(db.String(10000))
    departure_date = db.Column(db.String(10000))
    return_date = db.Column(db.String(200),  nullable=False)
    price = db.Column(db.String(200),  nullable=False)
    airline = db.Column(db.String(10000))
