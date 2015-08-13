from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, FileField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Regexp
from project.models import Category, City
from project.lib.media.validators import AllowedMime


class VacancyForm(Form):
    title = StringField(
        'Позиция',
        validators=[
            DataRequired('Required Field'),
            Length(
                max=100,
                message='Must not exceed 100 symbols'
            ),
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
    deleted = BooleanField(label='Удалить')


class CategoryForm(Form):
    name = StringField("Название категории", validators=[DataRequired()])


class CityForm(Form):
    name = StringField('Название города', validators=[DataRequired()])


class PageChunkForm(Form):
    title = StringField('Название элемента', validators=[DataRequired()])
    text = TextAreaField('Текст элемента', validators=[DataRequired()])


class MailTemplateForm(Form):
    title = StringField('Название письма (отображение в админке)',
                        validators=[DataRequired()])
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


def image_upload_form_factory(config, is_update=False):
    assert config is not None  # cause config=None can be passed

    class ImageUploadForm(Form):
        title = StringField(
            label='Название',
            validators=[
                Length(
                    max=32,
                    message='Must not exceed 32 symbols',
                )
            ],
        )
        description = TextAreaField(
            label='Описание (замещающий текст)',
            validators=[
                Length(
                    max=128,
                    message='Must not exceed 128 symbols',
                )
            ],
        )
        if not is_update:
            image = FileField(
                label='Картинка',
                validators=[
                    AllowedMime(config['IMG_MIMES']),
                    DataRequired(),
                ]
            )
        else:
            delete = BooleanField(
                label='Удалить',
                description='Эта картинка будет удалена навсегда'
                            ' (очень надолго!)',
            )
    return ImageUploadForm
