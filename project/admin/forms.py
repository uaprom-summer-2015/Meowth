from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from project.admin.logic import get_categories


class VacancyForm(Form):
    title = StringField('Позиция', validators=[DataRequired()])
    name_in_url = StringField("URL-имя", validators=[DataRequired()])
    short_description = StringField("Краткое описание", [DataRequired()])
    text = TextAreaField('Текст вакансии', validators=[DataRequired()])
    category_id = QuerySelectField('Категория', query_factory=get_categories,
                                   validators=[DataRequired()])


class CategoryForm(Form):
    name = StringField("Название категории", validators=[DataRequired()])
