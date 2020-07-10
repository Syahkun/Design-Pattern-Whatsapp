from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref

class Conversations(db.Model):
    __tablename__ = "conversations"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userA_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    userB_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    personal_message = db.relationship('PersonalMessages', backref='conversations', lazy=True, uselist=False)
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    
    response_fields = {
        'id':fields.Integer,
        'userA_id':fields.Integer,
        'userB_id':fields.Integer,
        'created_at':fields.DateTime
    }
    
    def __init__(self, userA_id, userB_id):
        self.userA_id = userA_id
        self.userB_id = userB_id
        
    def __repr__(self):
        return '<Conversation %r>' % self.id