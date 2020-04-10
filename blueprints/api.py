from flask import Blueprint, make_response, request
from database import session
from models.bot import Bot
from utils.decorators import bot_exists_required

blueprint = Blueprint('api', __name__, url_prefix='/api')


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
    if event_type == 'confirmation':
        return make_response((bot.confirmation_token, 200))
    if bot.secret and secret != bot.secret:
        return make_response((f'secret code failed', 403))
    return make_response(('bad request', 403))
