from flask_wtf import Form
from wtforms import StringField, FileField, TextAreaField
from wtforms_components import PhoneNumberField
from wtforms.validators import DataRequired, Email
from project.lib.media.validators import AllowedMime


def apply_form_factory(config):
    assert config is not None

    class ApplyForm(Form):
        name = StringField(
            label='Имя',
            validators=[DataRequired('Введите пожалуйста ваши имя и фамилию')]
        )
        email = StringField(
            label='Email',
            validators=[
                Email('Неверный e-mail адрес'),
                DataRequired('Введите пожалуйста e-mail')
            ]
        )
        phone = PhoneNumberField(
            label='Телефон',
            country_code='UA',
            validators=[DataRequired('Введите пожалуйста телефон')]
        )
        comment = TextAreaField(label='Коментарий')
        attachment = FileField(
            label='Резюме (макс. 15 Мб)',
            validators=[AllowedMime(
                config['DOC_MIMES'],
                message='Недопустимое расширение файла')
            ]
        )
    return ApplyForm
