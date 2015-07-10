from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
#
# Позиция
#     Кирилица и латиница верхнего и нижнего регистра
#     Точка
#
# Текст вакансии
#     кирилица и латиница верхнего и нижнего регистров (а-я, А-Я, a–z, A–Z)
#     Цифры от 0 до 9
#     Спецсимволы ! # $ % & ' * + - / = ? ^ _ . ,
#
# Контакты
#     кирилица и латиница верхнего и нижнего регистров (а-я, А-Я, a–z, A–Z)
#     Цифры от 0 до 9
#     Спецсимволы ! # $ % & ' * + - / = ? ^ _ . ,


class VacancyForm(Form):
    title = StringField('Позиция', validators=[DataRequired()])
    text = StringField('Текст вакансии', validators=[DataRequired()])
    category = StringField('Категория', validators=[DataRequired()])
