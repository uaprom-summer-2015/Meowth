from wtforms.validators import Regexp

# alphanumeric and special chars (-_.)
# Can not start with a digit, underscore or special character
LoginFormat = Regexp(regex='^[a-zA-Z][a-zA-Z0-9-_.]+$',
                     message='Логин должен состоять из латинских букв, цифр, и символов (_.-), и начинаться с буквы')

# aplhanumeric characters and special chars (-_.)
# Can not start with a digit, underscore or special character and must contain at least one digit.
PasswordFormat = Regexp(regex='^(?=.*[0-9])[a-zA-Z][a-zA-Z0-9-_.]+$',
                        message='Пароль должен состоять из латинских букв, цифр и символов (_.-), начинаться с буквы')
