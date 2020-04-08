from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class BotForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    access_token = StringField('Ключ доступа', validators=[DataRequired()])
    confirmation_token = StringField('Код подтверждения', validators=[DataRequired()])
    secret = StringField('Секретный ключ')
    group_id = IntegerField('ID Группы', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
