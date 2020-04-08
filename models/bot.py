import sqlalchemy
from sqlalchemy import orm
from database.session import SqlAlchemyBase


class Bot(SqlAlchemyBase):
    __tablename__ = 'bots'

    id = sqlalchemy.Column(sqlalchemy.Integer, index=True, primary_key=True, autoincrement=True)
    hash = sqlalchemy.Column(sqlalchemy.Integer, index=True, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    access_token = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    confirmation_token = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    secret = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    enabled = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=True)
    group_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    user = orm.relationship('User', back_populates='bots')
