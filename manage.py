from flask.ext.script import Manager
from project import app
from project.database import init_db as init
from project.fixtures import load_fixtures
import logging

manager = Manager(app)


@manager.command
def init_empty_db():
    """ Create empty database """
    logging.info('Creating empty database...')
    init()
    logging.info('Done')


@manager.command
def init_db():
    """ Create database and populate it with fixtures """
    init_empty_db()
    logging.info('Importing fixtures...')
    load_fixtures('init-data.json')
    logging.info('Done')


@manager.command
def run():
    """ Run application """
    logging.info('Starting app')
    app.run(debug=True)


if __name__ == "__main__":
    manager.run()
