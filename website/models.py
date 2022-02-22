from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200),  nullable=False)
    first_name = db.Column(db.String(200),  nullable=False)
    #admin = db.Column(db.Boolean, nullable=True, default=False)
    notes = db.relationship('Note')

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sourceLocation = db.Column(db.String(200), nullable=False)
    destinationLocation = db.Column(db.String(200), nullable=False)
    departureDate = db.Column(db.Date(), nullable=False)
    returnDate = db.Column(db.Date(), nullable=False)
    adults = db.Column(db.String(200), nullable=False)
    children = db.Column(db.String(200), nullable=False)
    notes = db.relationship('Note')