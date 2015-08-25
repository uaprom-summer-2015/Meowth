from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, Length
from .validators import LoginFormat, PasswordFormat, PasswordCorrect
from project.models import User
from project.lib.validators import Exists


class ResetForm(Form):
    email = StringField(
        'Email',
        validators=[
            Exists(model=User, reverse=True),
        ],
        filters=[
            lambda x: x.lower() if x else None,
        ],
    )


class LoginForm(Form):
    login = StringField(
        'Логин',
        validators=[DataRequired('Обязательное поле')]
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired('Обязательное поле')]
    )


class RegisterForm(Form):
    login = StringField(
        label='Логин',
        validators=[
            LoginFormat,
            Length(
                4,
                16,
                message='Логин должен быть от 6 до 16 символов в длину'
            ),
            Exists(model=User),
        ]
    )
    email = StringField(
        label='Email',
        validators=[
            Email('Неверный e-mail адрес'),
            DataRequired('Обязательное поле'),
            Exists(model=User),
        ],
        filters=[
            lambda x: x.lower() if x else None,
        ]
    )

    name = StringField(
        label='Имя',
        validators=[
            Length(
                2,
                16,
                message='Имя должно быть от 2 до 16 символов в длину'
            ),
        ]
    )
    surname = StringField(
        label='Фамилия',
        validators=[
            Length(
                2,
                25,
                message='Фамилия должна быть от 2 до 25 символов в длину'
            )
        ]
    )


class PasswordEditForm(Form):
    old_password = PasswordField(
        label='Старый пароль',
        validators=[
            PasswordCorrect(),
        ]
    )

    new_password = PasswordField(
        label='Новый пароль',
        validators=[
            EqualTo(
                'confirmation',
                message='Пароли не совпадают'
            ),
            PasswordFormat,
            Length(
                6,
                16,
                message='Пароль должен быть от 6 до 16 символов в длину'
            ),
        ]
    )
    confirmation = PasswordField(label='Подтвердите пароль')


class HelperForm(Form):
    login = StringField(
        label='Логин',
        validators=[
            LoginFormat,
            Length(
                4,
                16,
                message='Логин должен быть от 6 до 16 символов в длину'
            ),
            Exists(model=User),
        ]
    )
    email = StringField(
        label='Email',
        validators=[
            Email('Неверный e-mail адрес'),
            DataRequired('Обязательное поле'),
            Exists(model=User),
        ],
        filters=[
            lambda x: x.lower() if x else None,
        ]
    )
    password = PasswordField(
        label='Новый пароль',
        validators=[
            PasswordFormat,
            Length(
                6,
                16,
                message='Пароль должен быть от 6 до 16 символов в длину'
            ),
        ]
    )
