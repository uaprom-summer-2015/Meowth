from flask_wtf import Form
from wtforms import StringField, FileField, TextAreaField
from wtforms_components import PhoneNumberField
from wtforms.validators import DataRequired, Email
from project.feed.validators import allowed_extension


class ApplyForm(Form):
    name = StringField(label='Имя',
                       validators=[DataRequired('Обязательное поле')])
    email = StringField(label='Email',
                        validators=[Email('Неверный e-mail адрес'),
                                    DataRequired('Обязательное поле')])
    phone = PhoneNumberField(label='Телефон',
                             country_code='UA',
                             validators=[DataRequired('Обязательное поле')])
    comment = TextAreaField(label='Коментарий')
    attachment = FileField(label='Резюме (макс. 15 Мб)',
                           validators=[allowed_extension()])
