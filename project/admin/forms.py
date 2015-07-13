from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class VacancyForm(Form):
    title = StringField('Позиция', validators=[DataRequired()])
    text = TextAreaField('Текст вакансии', validators=[DataRequired()])
    category = StringField('Категория', validators=[DataRequired()])
