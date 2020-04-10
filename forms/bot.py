from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class BotForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    access_token = StringField('Ключ доступа')
    confirmation_token = StringField('Код подтверждения')
    secret = StringField('Секретный ключ')
    group_id = StringField('ID Группы')
    submit = SubmitField('Сохранить')
