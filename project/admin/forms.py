from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Regexp
from project.models import Category, City


class VacancyForm(Form):
    title = StringField(
        'Позиция',
        validators=[
            DataRequired('Required Field'),
            Length(
                max=100,
                message='Must not exceed 100 symbols'
            ),
            Regexp(
                '^[\.\d\w\sА-Яа-яІіЇїҐґ\-\+]+$',
                message='Should contain only cyrillic \
                         and latin letters,- ,+, . and \
                         spaces'
            )
        ]
    )
    name_in_url = StringField(
        "URL-имя",
        validators=[
            DataRequired('Required Field'),
            Length(
                max=50,
                message='Must not exceed 50 symbols'
            ),
            Regexp(
                '^[\d\w\-]+$',
                message='Should contain only \
                         latin characters and dashes'
            )
        ]
    )
    short_description = StringField(
        "Краткое описание",
        validators=[
            DataRequired('Required Field'),
            Length(
                max=300,
                message='Must not exceed 300 symbols'
            )
        ]
    )
    text = TextAreaField(
        'Текст вакансии',
        validators=[DataRequired('Required Field')]
    )
    category = QuerySelectField(
        'Категория',
        query_factory=lambda: Category.query.all(),
        validators=[DataRequired('Required field')]
    )
    city = QuerySelectField(
        'Город',
        query_factory=lambda: City.query.all(),
        validators=[DataRequired('Required field')]
    )
    hide = BooleanField(label='Не показывать вакансию')


class CategoryForm(Form):
    name = StringField("Название категории", validators=[DataRequired()])


class CityForm(Form):
    name = StringField('Название города', validators=[DataRequired()])


class PageChunkForm(Form):
    name = StringField('Название элемента', validators=[DataRequired()])
    text = TextAreaField('Текст элемента', validators=[DataRequired()])


class MailTemplateForm(Form):
    subject = StringField(
        'Тема письма',
        validators=[
            DataRequired(),
            Length(max=79,
                   message='Длина не дожна быть больше 79 символов'
                   ),
        ],
    )
    html = TextAreaField('Текст письма', validators=[DataRequired()])
