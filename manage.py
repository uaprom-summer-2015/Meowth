#!/usr/bin/env python3.4
from flask.ext.script import Manager
from project import app
from project.models import init_db as init
from project.fixtures import load_fixtures
import logging
from contextlib import contextmanager
from subprocess import call
import os

logger = logging.getLogger()


@contextmanager
def wrap_logging(before, fail, after):
    logger.info(before)
    try:
        yield
    except Exception as e:
        logger.error(fail)
        logger.error(e)
    else:
        logger.info(after)


def shexec(cmd, alt=None):
    try:
        call(cmd)
    except OSError as e:
        if e.errno == os.errno.ENOENT and alt:
            try:
                call(alt)
            except OSError as ex:
                raise ex
        else:
            raise e


manager = Manager(app)


@manager.command
def init_empty_db():
    """ Create empty database """
    with wrap_logging(
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
        before='Loading fixtures...',
        fail='Cannot populate fixtures',
        after='Done',
    ):
        load_fixtures(app.config['FIXTURES_DIR'])


@manager.command
def run():
    """ Run application """
    app.run(debug=True)


@manager.command
def do_npm():
    with wrap_logging(
        before='Installing node modules',
        fail='Cannot install node modules',
        after='Node modules installed successfully',
    ):
        shexec(["npm", "install"])


@manager.command
def do_bower():
    with wrap_logging(
        before='Installing bower components',
        fail='Cannot install bower components',
        after='Bower components installed successfully',
    ):
        shexec(
            cmd=["bower", "install"],
            alt=["./node_modules/bower/bin/bower", "install"],
        )


@manager.command
def do_gulp():
    with wrap_logging(
        before='Executing gulp scripts',
        fail='Error while executing gulp scripts',
        after='Gulp scripts executed successfully',
    ):
        shexec(
            cmd=["gulp", "build"],
            alt=["./node_modules/gulp/bin/gulp.js", "build"],
        )


@manager.command
def collectstatic():
    with wrap_logging(
        before='Collecting static...',
        fail='Error while collecting static',
        after='Done',
    ):
        do_npm()


if __name__ == "__main__":
    manager.run()
