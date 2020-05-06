from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class MessageForm(FlaskForm):
    text = TextAreaField('Обращение', validators=[DataRequired(), Length(max=1024)])
    submit = SubmitField('Отправить')
