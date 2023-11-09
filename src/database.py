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

class DeviceItemMeasurement(db.Model):
    thing_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, primary_key=True)
    thing_name = db.Column(db.String(500), nullable=False)
    item_name = db.Column(db.String(500), nullable=False)
    measurement_name = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return 'Thing Id: {self.thing_id}, Item Id: {self.item_id}, Thing: {self.thing.name}, Item: {self.item.name}, Measurement: {self.measurement.name}'
    
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
            'thing_id': self.thing_id,
            'item_id': self.item_id,
            'device_name': self.device_name,
            'item_name': self.item_name,
            'measurement_name': self.measurement_name
       }