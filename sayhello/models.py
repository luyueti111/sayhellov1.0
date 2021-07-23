from datetime import datetime
from sayhello import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200))
    name = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)
    clickNum = db.Column(db.Integer, default=0)
    replyNum = db.Column(db.Integer, default=0)
    pages = db.relationship('Page', back_populates='message')


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    message = db.relationship('Message', back_populates='pages')
