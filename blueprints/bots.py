from uuid import uuid3, NAMESPACE_DNS
from flask import Blueprint, render_template, redirect, request, abort
from flask_login import login_required, current_user
from database import session
from models.bot import Bot
from models.user import User
from forms.bot import BotForm
from utils.decorators import bot_exists_required, bot_owner_required, check_bot_limit

blueprint = Blueprint('bots', __name__, url_prefix='/bots')


@blueprint.route('/')
@login_required
def index():
    connect = session.create_session()
    bots = connect.query(Bot).filter(Bot.user == current_user).all()
    user = connect.query(User).get(current_user.id)
    can_create = len(user.bots) < user.role.bots_limit
    return render_template('bots/index.html', title='Мои боты', bots=bots, can_create=can_create)


@blueprint.route('/<string:bot_hash>', methods=['GET'])
@login_required
@bot_exists_required
@bot_owner_required
def show(bot_hash):
    connect = session.create_session()
    bot = connect.query(Bot).filter(Bot.hash == bot_hash).first()
    return render_template('bots/show.html', title=f'Бот / {bot.name}', bot=bot)


@blueprint.route('/create',  methods=['GET', 'POST'])
@login_required
@check_bot_limit
def create():
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


@blueprint.route('/<string:bot_hash>/edit', methods=['GET', 'POST'])
@login_required
@bot_exists_required
@bot_owner_required
def edit(bot_hash):
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


@blueprint.route('/<string:bot_hash>/delete', methods=['POST'])
@login_required
@bot_exists_required
@bot_owner_required
def delete(bot_hash):
    connect = session.create_session()
    bot = connect.query(Bot).filter(Bot.hash == bot_hash).first()
    connect.delete(bot)
    connect.commit()
    return redirect('/bots')


@blueprint.route('/<string:bot_hash>/toggle', methods=['POST'])
@login_required
@bot_exists_required
@bot_owner_required
def toggle(bot_hash):
    status = request.form.get('status')
    if status not in ['enable', 'disable']:
        return abort(401)
    connect = session.create_session()
    bot = connect.query(Bot).filter(Bot.hash == bot_hash).first()
    if status == 'enable' and not bot.enabled:
        bot.enabled = True
        connect.commit()
        return redirect(f'/bots/{bot_hash}')
    elif status == 'disable' and bot.enabled:
        bot.enabled = False
        connect.commit()
        return redirect(f'/bots/{bot_hash}')
    return abort(401)
