from functools import wraps
from flask import abort, request, make_response, jsonify
from flask_login import current_user
from database import session
from models.bot import Bot
from models.role import Role
from models.ticket import Ticket


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
            return make_response(('ok', 200))
        return f(*args, **kwargs)
    return decorated_function


def role_required(slug):
    def real_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            role = session.create_session().query(Role).filter(Role.slug == slug).first()
            if current_user.role.id != role.id:
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return real_decorator


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


def ticket_owner_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ticket_id = kwargs.get('ticket_id', 0)
        ticket = session.create_session().query(Ticket).filter(Ticket.id == ticket_id).first()
        if ticket.user != current_user:
            return abort(404)
        return f(*args, **kwargs)
    return decorated_function


def ticket_opened_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ticket_id = kwargs.get('ticket_id', 0)
        ticket = session.create_session().query(Ticket).filter(Ticket.id == ticket_id).first()
        if ticket.is_closed and request.method == 'POST':
            return abort(404)
        return f(*args, **kwargs)
    return decorated_function
