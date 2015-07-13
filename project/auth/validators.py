from wtforms.validators import Regexp, ValidationError
from project.auth.models import User

# alphanumeric and special chars (-_.)
# Can not start with a digit, underscore or special character
LoginFormat = Regexp(regex='^[a-zA-Z][a-zA-Z0-9-_.]+$',
                     message='Логин должен состоять из латинских букв,' +
                             ' цифр, и символов (_.-), и начинаться с буквы')

# aplhanumeric characters and special chars (-_.)
# Can not start with a digit, underscore or special character
# Must contain at least one digit.
PasswordFormat = Regexp(regex='^(?=.*[0-9])[a-zA-Z][a-zA-Z0-9-_.]+$',
                        message='Пароль должен состоять из латинских букв,' +
                                ' цифр и символов (_.-), начинаться с буквы,' +
                                '  содержать хоть одну цифру')


class LoginExists(object):
    def __init__(self, message=None):
        if not message:
            message = 'Пользователь с таким логином уже существует'
        self.message = message

    def __call__(self, form, field):
        login = field.data
        u = User.query.filter(User.login == login).first()
        if u:
            raise ValidationError(self.message)
