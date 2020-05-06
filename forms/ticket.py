from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class TicketForm(FlaskForm):
    title = StringField('Тема', validators=[DataRequired(), Length(max=128)])
    text = TextAreaField('Обращение', validators=[DataRequired(), Length(max=1024)])
    submit = SubmitField('Отправить')
