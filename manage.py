#!/usr/bin/env python3.4
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from project import app
from project.extensions import db
from project.models import User
from project.auth.forms import HelperForm
from project.lib.context_managers import disable_csrf
from commands.utils import perform
from commands.dbutils import DBUtils, DBUtilsCommand
from commands.static import StaticCommand
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


@manager.option(
    '-l', '--login',
    dest='login',
    action='store_true',
    default=None,
    help='Login'
)
@manager.option(
    '-e', '--email',
    dest='email',
    action='store_true',
    default=None,
    help='E-mail'
)
@manager.option(
    '-p', '--password',
    dest='password',
    action='store_true',
    default=None,
    help='Password'
)
def createsuperuser(login=None, email=None, password=None):
    """ Create user with admin rights"""
    login = login or ask_input('Введите логин')
    email = email or ask_input('Введите адрес электронной почты')
    passwd = password or ask_input('Введите пароль', hidden=True)
    confirmation = password or ask_input('Подтвердите пароль', hidden=True)

    while passwd != confirmation:
        print('Пароли не совпадают! Похоже, вы опечатались.')
        while True:
            choice = input('Повторить ввод? (y/n) ').lower()
            if choice in 'yes':
                passwd = ask_input('Введите пароль', hidden=True)
                confirmation = ask_input('Подтвердите пароль', hidden=True)
                break
            elif choice in 'no':
                return
            else:
                print('Пожалуйста, ответьте y (yes) или n (no)')

    with disable_csrf(app):
        form = HelperForm(
            name='dummy',
            surname='dummy',
            password=passwd,
            confirmation=passwd,
        )
        # dodge filling obj_data , just like browser form filling
        # (Existence validation comes false positive)
        form.login.data = login
        form.email.data = email
        if not form.validate():
            errors = [err for field in form.errors.values() for err in field]
            for error in errors:
                print(error)
            return
        else:
            with app.app_context(), perform(
                name='createsuperuser',
                before='Creating user',
                fail='Error occured while creating user',
                after='Superuser has been succesfully created!',
            ):
                User.bl.create_superuser(login, passwd, email)


if __name__ == "__main__":
    manager.run()
