from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50))
    password = db.Column(db.String(32),  nullable=False)
    gender = db.Column(db.String(10))
    phonenumber = db.Column(db.BigInteger)
    birthday = db.Column(db.Date())
    address = db.Column(db.String(50))
    city = db.Column(db.String(50))
    country = db.Column(db.String(50))
    postalcode = db.Column(db.String(10))
    isadmin = db.Column(db.Boolean, nullable=True, default=False)
    notes = db.relationship('Note')

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    departureDate = db.Column(db.Date(), nullable=False)
    arrivalDate = db.Column(db.Date(), nullable=False)
    starttime = db.Column(db.Time())
    arrivaltime = db.Column(db.Time())
    airline = db.Column(db.String(50))
    firstqty = db.Column(db.Integer)
    availableqty = db.Column(db.Integer)
    notes = db.relationship('Note')