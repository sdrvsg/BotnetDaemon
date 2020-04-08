from uuid import uuid3, NAMESPACE_DNS
from flask import Blueprint, render_template, redirect, request
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


@blueprint.route('/bots/<int:bot_id>', methods=['GET'])
@login_required
@bot_exists_required
@bot_owner_required
def bots_show(bot_id):
    connect = session.create_session()
    bot = connect.query(Bot).filter(Bot.id == bot_id).first()
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
        return redirect('/bots')
    return render_template('bots/create.html', title='Новый бот', form=form)


@blueprint.route('/bots/<int:bot_id>/edit', methods=['GET', 'POST'])
@login_required
@bot_exists_required
@bot_owner_required
def bots_edit(bot_id):
    form = BotForm()
    if request.method == 'GET':
        connect = session.create_session()
        bot = connect.query(Bot).filter(Bot.id == bot_id).first()
        form.name.data = bot.name
        form.access_token.data = bot.access_token
        form.confirmation_token.data = bot.confirmation_token
        form.secret.data = bot.secret
        form.group_id.data = bot.group_id
    if form.validate_on_submit():
        connect = session.create_session()
        bot = connect.query(Bot).filter(Bot.id == bot_id).first()
        bot.name = form.name.data
        bot.access_token = form.access_token.data
        bot.confirmation_token = form.confirmation_token.data
        bot.secret = form.secret.data
        bot.group_id = form.group_id.data
        connect.commit()
        return redirect(f'/bots/{bot.id}')
    return render_template('bots/create.html', title='Редактирование бота', form=form)


@blueprint.route('/bots/<int:bot_id>/delete', methods=['GET', 'POST'])
@login_required
@bot_exists_required
@bot_owner_required
def bots_delete(bot_id):
    connect = session.create_session()
    bot = connect.query(Bot).filter(Bot.id == bot_id).first()
    connect.delete(bot)
    connect.commit()
    return redirect('/bots')


@blueprint.route('/callback/<string:bot_hash>', methods=['GET'])
def callback(bot_hash):
    print(request.args)
