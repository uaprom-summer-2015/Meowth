from flask import current_app
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, upgrade as migrate_upgrade

from commands.utils import perform
from project.fixtures import load_fixtures


class _DBUtilsConfig(object):

    def __init__(self, db):
        self.db = db

    @property
    def metadata(self):
        return self.db.metadata


class DBUtils(object):

    def __init__(self, app=None, db=None):
        if app is not None and db is not None:
            self.init_app(app, db)

    def init_app(self, app, db):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['meowth_dbutils'] = _DBUtilsConfig(db)
        Migrate(app, db)


DBUtilsCommand = Manager(usage='Perform basic dev database operations')


@DBUtilsCommand.command
def drop():
    engine = current_app.extensions['meowth_dbutils'].db.engine
    if current_app.extensions['meowth_dbutils'].metadata.bind is None:
        current_app.extensions['meowth_dbutils'].metadata.bind = engine
    with perform(
        name='dbutils drop',
        before='Dropping all project tables',
        fail='Error occured while droping project tables',
    ):
        current_app.extensions['meowth_dbutils'].metadata.drop_all()
    with perform(
        name='dbutils drop',
        before='Dropping alembic versioning table',
        fail='Error occured while dropping alembic table',
    ):
        engine.execute('drop table if exists alembic_version')


@DBUtilsCommand.option(
    '-p', '--populate',
    dest='populate_after_init',
    action='store_true',
    default=False,
    help='Populate fixtures after creating database',
)
@DBUtilsCommand.option(
    '-d', '--directory',
    dest='directory',
    default=None,
    help='Directory to search fixtures in',
)
def init(populate_after_init=False, directory=None):
    drop()
    with perform(
        name='dbutils init',
        before='initializing database to its latest version',
    ):
        migrate_upgrade()
    if populate_after_init:
        populate(directory)


@DBUtilsCommand.option(
    '-d', '--directory',
    dest='directory',
    default=None,
    help='Directory to search fixtures in',
)
def populate(directory=None):
    if directory is None:
        directory = current_app.config['FIXTURES_DIR']
    with perform(
        name='dbutils populate',
        before='Loading fixtures from directory %s' % directory,
        fail='Error occured while loading fixtures',
    ):
        load_fixtures(directory)
