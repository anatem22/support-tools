"""Application Models"""
import config, os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utc import UtcDateTime, utcnow
from datetime import datetime

db = SQLAlchemy()

class Users(db.Model):
    """Users Model"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True)
    login = db.Column(db.String(50), nullable=False)
    roles = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    def __init__(self, username, email, login, roles, active):
        self.username = username
        self.email = email
        self.login = login
        self.roles = roles
        self.active = active

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def get_user(self, user_email):
        """Get a user by id"""
        Users.query.filter_by(email=user_email).first()

class Dosc(db.Model):
    """Documents Model"""
    __tablename__ = 'del_documents'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuidDocs = db.Column(db.String(50), nullable=False)
    createDate = db.Column(db.DateTime, nullable=False)
    masterid = db.Column(db.String(50), nullable=False)
    docType = db.Column(db.String(100), nullable=False)
    initiator = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.String(100), nullable=False)
    deleteDate = db.Column('deleteDate', UtcDateTime(), default=utcnow())
    executor=db.Column(db.Integer, nullable=False)

    def __init__(self, uuidDocs, createDate, masterid, docType, initiator, reason, executor):
        self.uuidDocs = uuidDocs
        self.createDate = createDate
        self.masterid = masterid
        self.docType = docType
        self.initiator = initiator
        self.reason = reason
        self.executor = executor
