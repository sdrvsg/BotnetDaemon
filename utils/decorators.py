from functools import wraps
from flask import abort
from flask_login import current_user
from database import session
from models.bot import Bot


def bot_exists_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        bot_hash = kwargs.get('bot_hash', 0)
        bot = session.create_session().query(Bot).filter(Bot.hash == bot_hash).first()
        if not bot:
            return abort(404)
        return f(*args, **kwargs)
    return decorated_function


def bot_owner_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        bot_hash = kwargs.get('bot_hash', 0)
        bot = session.create_session().query(Bot).filter(Bot.hash == bot_hash).first()
        if bot.user != current_user:
            return abort(404)
        return f(*args, **kwargs)
    return decorated_function
