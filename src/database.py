from enum import unique
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random

db = SQLAlchemy()


class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    password=db.Column(db.Text() , nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.now())
    updated_at=db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self) -> str:
        return 'User >>> {self.username}'

class ThingItemMeasurement(db.Model):
    thing_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, primary_key=True)
    thing_name = db.Column(db.String(500), nullable=False)
    item_type = db.Column(db.String(500), nullable=False)
    item_name = db.Column(db.String(500), nullable=False)
    measurement_name = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"Thing Id: {self.thing_id}, Item Id: {self.item_id}, Thing: {self.thing_name}, Item Type: {self.item_type}, Item Name: {self.item_name}, Measurement: {self.measurement_name}"
    
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
            'thing_id': self.thing_id,
            'item_id': self.item_id,
            'device_name': self.device_name,
            'item_type': self.item_type,
            'item_name': self.item_name,
            'measurement_name': self.measurement_name
       }

class RoomStatus(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    status=db.Column(db.Boolean, nullable=False)
    amount=db.Column(db.Integer, nullable=False)
    timestamp=db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def serialize(self):
       """Return room status data in easily serializable format"""
       return {
            'id': self.id,
            'status': self.status,
            'amount': self.amount,
            'timestamp': self.timestamp,
       }