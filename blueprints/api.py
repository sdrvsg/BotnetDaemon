from requests import get
from random import randint
import vk_api
from flask import Blueprint, make_response, request, jsonify
from database import session
from models.bot import Bot
from models.answer import Answer
from utils.decorators import bot_exists_required, bot_enabled_required
from utils.decorators import api_bot_exists_required, api_bot_owner_required, api_bot_enabled_required

blueprint = Blueprint('api', __name__, url_prefix='/api')


@blueprint.route('/callback/<string:bot_hash>', methods=['POST'])
@bot_exists_required
@bot_enabled_required
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
    if event_type == 'message_new':
        obj = request.json['object']['message']
        response = get('https://botnet-daemon.herokuapp.com/api/answers/get', params={
            'bot_hash': bot_hash,
            'question': obj['text']
        }).json()
        vk_session = vk_api.VkApi(token=bot.access_token)
        vk_session.auth(token_only=True)
        vk = vk_session.get_api()
        if 'error' in response.keys():
            vk.messages.send(
                user_id=obj['from_id'],
                random_id=randint(0, 2 ** 64),
                message='Произошла ошибка'
            )
        else:
            vk.messages.send(
                user_id=obj['from_id'],
                random_id=randint(0, 2 ** 64),
                message=response['answer']
            )
    return make_response(('bad request', 403))


@blueprint.route('/answers', methods=['GET'])
@api_bot_exists_required
@api_bot_owner_required
def answers_index():
    bot_hash = request.args.get('bot_hash')
    connect = session.create_session()
    bot = connect.query(Bot).filter(Bot.hash == bot_hash).first()
    return make_response((jsonify({
        'answers': [
            {
                'question': answer.question,
                'answer': answer.answer,
            } for answer in bot.answers]
    }), 200))


@blueprint.route('/answers/store', methods=['POST'])
@api_bot_exists_required
@api_bot_owner_required
def answers_store():
    bot_hash = request.form.get('bot_hash')
    q = request.form.get('question')
    a = request.form.get('answer')
    if not q or not a:
        return make_response((jsonify({'error': 'Неверные данные'}), 200))
    connect = session.create_session()
    bot = connect.query(Bot).filter(Bot.hash == bot_hash).first()
    answer = connect.query(Answer).filter(Answer.bot == bot, Answer.question == q).first()
    if not answer:
        answer = Answer()
        bot.answers.append(answer)
    answer.question = q
    answer.answer = a
    connect.merge(bot)
    connect.commit()
    return make_response((jsonify({'success': 'Сохранено'}), 200))


@blueprint.route('/answers/delete', methods=['DELETE'])
@api_bot_exists_required
@api_bot_owner_required
def answers_delete():
    bot_hash = request.form.get('bot_hash')
    q = request.form.get('question')
    if not q:
        return make_response((jsonify({'error': 'Неверные данные'}), 200))
    connect = session.create_session()
    bot = connect.query(Bot).filter(Bot.hash == bot_hash).first()
    answer = connect.query(Answer).filter(Answer.bot == bot, Answer.question == q).first()
    if not answer:
        return make_response((jsonify({'error': 'Неверные данные'}), 200))
    connect.delete(answer)
    connect.commit()
    return make_response((jsonify({'success': 'Удалено'}), 200))


@blueprint.route('/answers/get', methods=['GET'])
@api_bot_exists_required
@api_bot_enabled_required
def answers_get():
    bot_hash = request.args.get('bot_hash')
    q = request.args.get('question')
    if not q:
        return make_response((jsonify({'error': 'Неверные данные'}), 200))
    connect = session.create_session()
    bot = connect.query(Bot).filter(Bot.hash == bot_hash).first()
    for answer in bot.answers:
        for key_word in answer.question.split('|'):
            if q.lower().strip() == key_word.lower().strip():
                return make_response((jsonify({'answer': answer.answer}), 200))
    answer = connect.query(Answer).filter(Answer.bot == bot, Answer.question == '@default').first()
    if answer:
        return make_response((jsonify({'answer': answer.answer}), 200))
    return make_response((jsonify({'answer': 'Произошла ошибка на сервере'}), 200))
