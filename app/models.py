# /app/models.py

from . import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(db.String(10), nullable=False) 
    events = db.relationship('Event', backref='producer', lazy=True)
    attended_events = db.relationship('EventAttendees', back_populates='user')

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    events = db.relationship('Event', backref='category', lazy=True)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    producer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    attendees = db.relationship('EventAttendees', back_populates='event', cascade='all, delete-orphan')

class EventAttendees(db.Model):
    __tablename__ = 'event_attendees'
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    event = db.relationship('Event', back_populates='attendees')
    user = db.relationship('User', back_populates='attended_events')
