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
    #admin = db.Column(db.Boolean, nullable=True, default=False)
    tiket = db.relationship('Ticket')