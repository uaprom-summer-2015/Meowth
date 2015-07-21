from wtforms.validators import Regexp, ValidationError
from project.models import User

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


class Exists(object):
    def __init__(self, message=None, reverse=False):
        if message:
            self.message = message
        self.reverse = reverse

    def __call__(self, _, field):
        if field.object_data == field.data:
            return
        if not hasattr(self, 'message'):
            if not self.reverse:
                self.message = 'Пользователь с таким {} уже существует'\
                    .format(field.name)
            else:
                self.message = 'Пользователь с таким {} не существует'\
                    .format(field.name)

        u = True \
            if list(User.query.filter(getattr(User, field.name) == field.data)) \
            else False
        if self.reverse ^ u:
                raise ValidationError(self.message)
