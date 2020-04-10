import sqlalchemy
from sqlalchemy import orm
from database.session import SqlAlchemyBase


class Role(SqlAlchemyBase):
    __tablename__ = 'roles'

    id = sqlalchemy.Column(sqlalchemy.Integer, index=True, primary_key=True, autoincrement=True)
    slug = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    bots_limit = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=1)
    users = orm.relationship('User', back_populates='role')
