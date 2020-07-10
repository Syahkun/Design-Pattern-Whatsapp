from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False, unique=True)
    # password = db.Column(db.String(255), nullable=False)
    # salt = db.Column(db.String(255), nullable=False)
    # status = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        'id': fields.Integer,
        'name':fields.String,
        'phone_number': fields.String,
        # 'status': fields.Boolean,
    }

    def __init__(self, name, phone_number,
    #  password, salt, status
     ):
        self.name = name
        self.phone_number = phone_number
        # self.password = password
        # self.salt = salt
        # self.status = status

    def __repr__(self):
        return '<User %r>' % self.id
