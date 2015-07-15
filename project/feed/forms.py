from flask_wtf import Form
from wtforms import StringField, FileField
from wtforms.validators import DataRequired, Email
from project.feed.validators import allowed_extension, max_size


class ApplyForm(Form):
    name = StringField(label='Имя',
                       validators=[DataRequired('Обязательное поле')])
    email = StringField(label='Email',
                        validators=[Email('Неверный e-mail адрес'),
                                    DataRequired('Обязательное поле')])
    file = FileField(label='Резюме',
                     validators=[allowed_extension(), max_size()])
