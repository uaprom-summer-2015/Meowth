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
    def __init__(self, data=None, message=None, reverse=False):
        if message:
            self.message = message
        self.old_data = data
        self.reverse = reverse

    def __call__(self, form, field):
        new_data = field.data
        if not hasattr(self, 'message'):
            if not self.reverse:
                self.message = 'Пользователь с таким {} уже существует'\
                    .format(field.name)
            else:
                self.message = 'Пользователь с таким {} не существует'\
                    .format(field.name)

        if not self.reverse:
            if self.old_data == new_data:
                return None
            u = User.query\
                .filter(getattr(User, field.name) == new_data)\
                .first()
            if u:
                raise ValidationError(self.message)
        else:
            u = User.query\
                .filter(getattr(User, field.name) == new_data)\
                .first()
            if not u:
                raise ValidationError(self.message)
