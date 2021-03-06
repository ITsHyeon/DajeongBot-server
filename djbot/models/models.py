# coding: utf-8

from djbot import db


class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(32), nullable=False)
    name = db.Column(db.String(32))
    birthday = db.Column(db.Date)
    account_type = db.Column(db.Integer, server_default=db.FetchedValue())
    bot_type = db.Column(db.Integer, server_default=db.FetchedValue())
    notify_time = db.Column(db.String(10), nullable=False, server_default=db.FetchedValue())
    ask_time = db.Column(db.String(10), nullable=False, server_default=db.FetchedValue())


class CustomAccount(Account):
    __tablename__ = 'custom_account'

    account_id = db.Column(db.ForeignKey('account.id'), primary_key=True)
    password = db.Column(db.String(50), nullable=False)


class ApiAccount(Account):
    __tablename__ = 'api_account'

    account_id = db.Column(db.ForeignKey('account.id'), primary_key=True)
    token = db.Column(db.String(100), nullable=False)


class Chat(db.Model):
    __tablename__ = 'chat'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.ForeignKey('account.id'), nullable=False, index=True)
    content = db.Column(db.String, nullable=False)
    node_type= db.Column(db.Integer, nullable=False)
    chat_type = db.Column(db.Integer, nullable=False)
    time = db.Column(db.String, nullable=False)
    isBot = db.Column(db.Integer, nullable=False)
    carousel_list = db.Column(db.String)
    slot_list = db.Column(db.String)

    # account = db.relationship('Account', primaryjoin='Chat.account_id == Account.id', backref='chats')


class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.ForeignKey('account.id'), nullable=False, index=True)
    schedule_when = db.Column(db.String, nullable=False)
    schedule_where = db.Column(db.String, nullable=False)
    schedule_what = db.Column(db.String, nullable=False)
    assign_time = db.Column(db.String, nullable=False)
    detail = db.Column(db.String)
    review = db.Column(db.String)
    notification_send = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    question_send = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    # account = db.relationship('Account', primaryjoin='Event.account_id == Account.id', backref='events')


class FcmToken(db.Model):
    __tablename__ = 'fcm_token'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.ForeignKey('account.id'), nullable=False, index=True)
    token = db.Column(db.String(300), nullable=False)

    # account = db.relationship('Account', primaryjoin='FcmToken.account_id == Account.id', backref='fcm_tokens')

