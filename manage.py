#!/usr/bin/env python3.4
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from project import app
from project.extensions import db
from commands.dbutils import DBUtils, DBUtilsCommand
from commands.static import StaticCommand

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


if __name__ == "__main__":
    manager.run()
