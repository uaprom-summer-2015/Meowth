from wtforms.validators import Regexp, ValidationError
from project.models import User
from werkzeug.security import check_password_hash
from flask import session

# alphanumeric and special chars (-_.)
# Can not start with a digit, underscore or special character
LoginFormat = Regexp(
    regex='^[a-zA-Z][a-zA-Z0-9-_.]+$',
    message='Логин должен состоять из латинских букв, '
            'цифр, и символов (_.-), и начинаться с буквы',
)

# aplhanumeric characters and special chars (-_.)
# Can not start with a digit, underscore or special character
# Must contain at least one digit.
PasswordFormat = Regexp(regex='^(?=.*[0-9])[a-zA-Z][a-zA-Z0-9-_.]+$',
                        message='Пароль должен состоять из латинских букв,'
                                ' цифр и символов (_.-), начинаться с буквы,'
                                '  содержать хоть одну цифру')


class PasswordCorrect(object):
    def __init__(self, message=None):
        self.message = message or 'Неверный пароль'

    def __call__(self, _, field):
        user = User.query.get(session.get('user_id'))
        if not check_password_hash(user.password, field.data):
            raise ValidationError(self.message)
