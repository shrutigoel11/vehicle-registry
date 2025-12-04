from . import db
from flask_login import UserMixin
from datetime import datetime

class Franchise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    vehicles = db.relationship('Vehicle', backref='franchise', lazy=True)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # customer / owner
    franchise_id = db.Column(db.Integer, db.ForeignKey('franchise.id'), nullable=True)
    vehicles = db.relationship('Vehicle', backref='owner', lazy=True)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(50), unique=True, nullable=False)
    make = db.Column(db.String(50))
    model = db.Column(db.String(50))
    color = db.Column(db.String(50))
    issue_date = db.Column(db.Date, default=datetime.utcnow)
    registration_status = db.Column(db.String(20), default='Active')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    franchise_id = db.Column(db.Integer, db.ForeignKey('franchise.id'), nullable=False)
