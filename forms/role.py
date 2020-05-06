from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class RoleForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    styles = StringField('Дополнительные стили')
    cost = IntegerField('Стоимость', validators=[DataRequired()])
    bots_limit = IntegerField('Макс. кол-во ботов', validators=[DataRequired()])
    support_priority = IntegerField('Приоритет в поодержке (больше - важнее)', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
