#!/usr/bin/env python3.4
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from project import app
from project.extensions import db
from commands.dbutils import DBUtils, DBUtilsCommand
from commands.static import StaticCommand, npm


manager = Manager(app)

devutils = DBUtils(app, db)
manager.add_command('dbutils', DBUtilsCommand)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

manager.add_command('static', StaticCommand)


@manager.command
def run():
    """ Run application """
    app.run(debug=True)


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
