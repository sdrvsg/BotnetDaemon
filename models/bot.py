import sqlalchemy
from sqlalchemy import orm
from database.session import SqlAlchemyBase


class Bot(SqlAlchemyBase):
    __tablename__ = 'bots'

    id = sqlalchemy.Column(sqlalchemy.Integer, index=True, primary_key=True, autoincrement=True)
    hash = sqlalchemy.Column(sqlalchemy.Integer, index=True, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    access_token = sqlalchemy.Column(sqlalchemy.String)
    confirmation_token = sqlalchemy.Column(sqlalchemy.String)
    group_id = sqlalchemy.Column(sqlalchemy.Integer)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    user = orm.relationship('User', back_populates='bots')
