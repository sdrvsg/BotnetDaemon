import sqlalchemy
from sqlalchemy import orm
from database.session import SqlAlchemyBase


class Ticket(SqlAlchemyBase):
    __tablename__ = 'tickets'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String(128), nullable=False)
    is_closed = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    priority = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    user = orm.relationship('User', back_populates='tickets', lazy='subquery')
    messages = orm.relationship('Message', back_populates='ticket', lazy='subquery')
