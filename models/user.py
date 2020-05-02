import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from database.session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(128), nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String(128), index=True, unique=True, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String(128), nullable=False)
    money = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    bots = orm.relationship('Bot', back_populates='user', lazy='subquery')
    role_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('roles.id'), nullable=False)
    role = orm.relationship('Role', back_populates='users', lazy='subquery')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
