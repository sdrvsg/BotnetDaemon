from uuid import uuid3, NAMESPACE_DNS
from flask import Blueprint, render_template, redirect, request, make_response, jsonify
from flask_login import login_required, current_user
import vk_api
from database import session
from models.bot import Bot
from forms.bot import BotForm
from utils.decorators import bot_exists_required, bot_owner_required

blueprint = Blueprint('main', __name__)


@blueprint.route('/')
def index():
    return render_template('index.html', title='Главная')


@blueprint.route('/bots')
@login_required
def bots_index():
    connect = session.create_session()
    params = {
        'bots': connect.query(Bot).filter(Bot.user == current_user).all()
    }
    return render_template('bots/index.html', title='Мои боты', **params)


@blueprint.route('/bots/<string:bot_hash>', methods=['GET'])
@login_required
@bot_exists_required
@bot_owner_required
def bots_show(bot_hash):
    connect = session.create_session()
    bot = connect.query(Bot).filter(Bot.hash == bot_hash).first()
    return render_template('bots/show.html', title=f'Бот / {bot.name}', bot=bot)


@blueprint.route('/bots/create',  methods=['GET', 'POST'])
@login_required
def bots_create():
    form = BotForm()
    if form.validate_on_submit():
        connect = session.create_session()
        bot = Bot()
        bot.name = form.name.data
        bot.access_token = form.access_token.data
        bot.confirmation_token = form.confirmation_token.data
        bot.secret = form.secret.data
        bot.group_id = form.group_id.data
        current_user.bots.append(bot)
        connect.merge(current_user)
        connect.commit()
        bot = connect.query(Bot).all()[-1]
        bot.hash = str(uuid3(NAMESPACE_DNS, f'bot::{bot.id}'))
        connect.commit()
        return redirect(f'/bots/{bot.hash}')
    return render_template('bots/create.html', title='Новый бот', form=form)


@blueprint.route('/bots/<string:bot_hash>/edit', methods=['GET', 'POST'])
@login_required
@bot_exists_required
@bot_owner_required
def bots_edit(bot_hash):
    form = BotForm()
    if request.method == 'GET':
        connect = session.create_session()
        bot = connect.query(Bot).filter(Bot.hash == bot_hash).first()
        form.name.data = bot.name
        form.access_token.data = bot.access_token
        form.confirmation_token.data = bot.confirmation_token
        form.secret.data = bot.secret
        form.group_id.data = bot.group_id
    if form.validate_on_submit():
        connect = session.create_session()
        bot = connect.query(Bot).filter(Bot.hash == bot_hash).first()
        bot.name = form.name.data
        bot.access_token = form.access_token.data
        bot.confirmation_token = form.confirmation_token.data
        bot.secret = form.secret.data
        bot.group_id = form.group_id.data
        connect.commit()
        return redirect(f'/bots/{bot.hash}')
    return render_template('bots/create.html', title='Редактирование бота', form=form)


@blueprint.route('/bots/<string:bot_hash>/delete', methods=['GET', 'POST'])
@login_required
@bot_exists_required
@bot_owner_required
def bots_delete(bot_hash):
    connect = session.create_session()
    bot = connect.query(Bot).filter(Bot.hash == bot_hash).first()
    connect.delete(bot)
    connect.commit()
    return redirect('/bots')


@blueprint.route('/callback/<string:bot_hash>', methods=['POST'])
@bot_exists_required
def callback(bot_hash):
    if type(request.json) is not dict:
        return make_response(('bad request', 403))
    event_type = request.json.get('type')
    group_id = request.json.get('group_id')
    secret = request.json.get('secret')
    connect = session.create_session()
    bot = connect.query(Bot).filter(Bot.hash == bot_hash).first()
    if bot.group_id != group_id:
        return make_response((f'group id invalid', 403))
    if secret and secret != bot.secret:
        return make_response((f'secret code failed', 403))
    if event_type == 'confirmation':
        return make_response((bot.confirmation_token, 200))
    return make_response(('bad request', 403))
