#!/usr/bin/env python
from flask.ext.script import Manager
from project import app
from project.database import init_db as init
from project.fixtures import load_fixtures
import logging
from contextlib import contextmanager


@contextmanager
def wrap_logging(logger, before, fail, after):
    logger.info(before)
    try:
        yield
    except Exception as e:
        logger.error(fail)
        logger.error(e)
    else:
        logger.info(after)


manager = Manager(app)


@manager.command
def init_empty_db():
    """ Create empty database """
    with wrap_logging(
        logger=logging,
        before='Creating empty DB ...',
        fail='Cannot create empty DB',
        after='Done',
    ):
        init()


@manager.command
def init_db():
    """ Create database and populate it with fixtures """
    init_empty_db()
    with wrap_logging(
        logger=logging,
        before='Loading fixtures...',
        fail='Cannot populate fixtures',
        after='Done',
    ):
        load_fixtures('init-data.json')


@manager.command
def run():
    """ Run application """
    app.run(debug=True)


if __name__ == "__main__":
    manager.run()
