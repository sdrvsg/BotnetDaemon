from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, HiddenField
from wtforms.validators import DataRequired, NumberRange


class PaymentForm(FlaskForm):
    test = HiddenField('test', default=0)
    money_amount = IntegerField('Укажите сумму', validators=[DataRequired(), NumberRange(10)])
    submit = SubmitField('Пополнить')
