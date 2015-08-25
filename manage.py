#!/usr/bin/env python3.4
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from project import app
from project.extensions import db
from project.models import User
from project.auth.forms import RegisterForm
from project.lib.context_managers import disable_csrf
from commands.utils import COLORS
from commands.dbutils import DBUtils, DBUtilsCommand
from commands.static import StaticCommand, npm
from getpass import getpass

manager = Manager(app)

devutils = DBUtils(app, db)
manager.add_command('dbutils', DBUtilsCommand)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

manager.add_command('static', StaticCommand)

def ask_input(message, *, hidden=False):
    input_func = getpass if hidden else input
    while True:
        try:
            ans = input_func('{}:\n'.format(message))
            print('\n')
            break
        except UnicodeDecodeError:
            print('Возникла ошибка, попробуйте еще раз')
    return ans


@manager.command
def run():
    """ Run application """
    app.run(debug=True)

@manager.command
def createsuperuser():
    """ Create user with admin rights"""
    print(
        '{RED}'
        'Внимание! Надежность пароля не проверяется. '
        'Пожалуйста, не злоупотребляйте этим\n'
        '{END}'
    )
    login = ask_input('Введите логин')
    email = ask_input('Введите адрес электронной почты')
    password = ask_input('Введите пароль', hidden=True)
    confirmation = ask_input('Подтвердите пароль', hidden=True)
    if password != confirmation:
        print('Пароли не совпадают!\n')
        return
    with disable_csrf(app):
        form = RegisterForm(
            login=login,
            email=email,
            name='dummy',
            surname='dummy',
        )
        if not form.validate():
            errors = [err for field in form.errors.values() for err in field]
            for error in errors:
                print(error)
        else:
            User.bl.create_superuser(login, password, email)
            print(
                '{GREEN}'
                'Суперпользователь успешно создан\n'
                '{END}'
            )


@manager.option(
    '--noinput',
    dest='noinput',
    action='store_true',
    default=False,
    help='Do not ask user anything',
)
def collectstatic(noinput=False):
    """ Collect and build all static """
    npm(noinput)

if __name__ == "__main__":
    manager.run()
