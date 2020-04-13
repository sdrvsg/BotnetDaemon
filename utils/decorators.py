from functools import wraps
from flask import abort, request, make_response, jsonify
from flask_login import current_user
from database import session
from models.bot import Bot
from models.role import Role


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


def bot_enabled_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        bot_hash = kwargs.get('bot_hash', 0)
        bot = session.create_session().query(Bot).filter(Bot.hash == bot_hash).first()
        if not bot.enabled:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


def role_required(f, slug):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        role = session.create_session().query(Role).filter(Role.slug == slug).first()
        if current_user.role != role:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


def check_bot_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        role = current_user.role
        if len(current_user.bots) >= role.bots_limit:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


def api_bot_exists_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        bot_hash = request.args.get('bot_hash', 0)
        if not bot_hash:
            bot_hash = request.form.get('bot_hash', 0)
        bot = session.create_session().query(Bot).filter(Bot.hash == bot_hash).first()
        if not bot:
            return make_response(jsonify({
                'error': 'Бота не существует'
            }))
        return f(*args, **kwargs)
    return decorated_function


def api_bot_owner_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        bot_hash = request.args.get('bot_hash', 0)
        if not bot_hash:
            bot_hash = request.form.get('bot_hash', 0)
        bot = session.create_session().query(Bot).filter(Bot.hash == bot_hash).first()
        if bot.user != current_user:
            return make_response(jsonify({
                'error': 'Вы не являетесь владельцем бота'
            }))
        return f(*args, **kwargs)
    return decorated_function


def api_bot_enabled_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        bot_hash = request.args.get('bot_hash', 0)
        if not bot_hash:
            bot_hash = request.form.get('bot_hash', 0)
        bot = session.create_session().query(Bot).filter(Bot.hash == bot_hash).first()
        if not bot.enabled:
            return make_response(jsonify({
                'error': 'Бот выключен'
            }))
        return f(*args, **kwargs)
    return decorated_function
