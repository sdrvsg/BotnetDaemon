import sqlalchemy
from sqlalchemy import orm
from database.session import SqlAlchemyBase


class Answer(SqlAlchemyBase):
    __tablename__ = 'answers'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    question = sqlalchemy.Column(sqlalchemy.String(128), nullable=False)
    answer = sqlalchemy.Column(sqlalchemy.String(128), nullable=False)
    bot_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('bots.id'), nullable=False)
    bot = orm.relationship('Bot', back_populates='answers', lazy='subquery')
