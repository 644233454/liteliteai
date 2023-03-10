from datetime import datetime

from app import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    messages = db.relationship('Message', backref='user', lazy=True)

    __table_args__ = {'extend_existing': True}


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.String(30), nullable=True)
    role = db.Column(db.String(10))
    content = db.Column(db.String(50000))
    created_at = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    __table_args__ = {'extend_existing': True}


class ChatRoom(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    chat_title = db.Column(db.String(30), nullable=True, default="默认聊天室")
    chat_id = db.Column(db.String(30), nullable=True)
    setting = db.Column(db.String(10))
    status = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, nullable=True)

    __table_args__ = {'extend_existing': True}
