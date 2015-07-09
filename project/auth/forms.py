from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, Length
from project.auth.validators import LoginFormat, PasswordFormat


class LoginForm(Form):
    login = StringField('Логин', validators=[DataRequired('Обязательное поле')])
    password = PasswordField('Пароль', validators=[DataRequired('Обязательное поле')])

class RegisterForm(Form):
    login = StringField(label='Логин',
                        validators=[LoginFormat,
                                    Length(4, 16,
                                           message='Логин должен быть от 6 до 16 символов в длину')])
    password = PasswordField(label='Пароль',
                             validators=[PasswordFormat,
                                         EqualTo('confirmation',
                                                 message='Пароли не совпадают'),
                                         Length(6, 16,
                                                message='Пароль должен быть от 6 до 16 символов в длину')])
    confirmation = PasswordField(label='Подтвердите пароль')
    email = StringField(label='Email',
                        validators=[Email('Неверный e-mail адрес'),
                                    DataRequired('Обязательное поле')])
    name = StringField(label='Имя',
                       validators=[Length(2, 16,
                                          message='Имя должно быть от 2 до 16 символов в длину')])
    surname = StringField(label='Фамилия',
                          validators=[Length(2, 25,
                                             message='Фамилия должна быть от 2 до 20 символов в длину')])


