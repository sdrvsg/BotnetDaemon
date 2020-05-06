import datetime
import sqlalchemy
from sqlalchemy import orm
from database.session import SqlAlchemyBase


class Message(SqlAlchemyBase):
    __tablename__ = 'messages'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String(128), nullable=False)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    user = orm.relationship('User', back_populates='messages', lazy='subquery')
    ticket_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tickets.id'), nullable=False)
    ticket = orm.relationship('Ticket', back_populates='messages', lazy='subquery')
