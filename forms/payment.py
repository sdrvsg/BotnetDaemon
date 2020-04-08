from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class PaymentForm(FlaskForm):
    money_amount = IntegerField('Укажите сумму', validators=[DataRequired(), NumberRange(10)])
    submit = SubmitField('Пополнить')
