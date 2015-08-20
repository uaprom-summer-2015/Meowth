from flask import current_app
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, upgrade as migrate_upgrade

from commands.utils import perform
from project.fixtures import load_fixtures
from project.gallery import load_images as load_dummy_images


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


@DBUtilsCommand.option(
    '-a', '--all',
    dest='drop_all',
    action='store_true',
    default=False,
    help='Drop ALL tables in database',
)
def drop(drop_all=False):
    """ Drop tables in project database
    """

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
    if drop_all:
        with perform(
            name='dbutils drop',
            before='Dropping all other tables in database',
            fail='Error occured while dropping other tables',
        ):
            current_app.extensions['meowth_dbutils'].db.reflect()
            current_app.extensions['meowth_dbutils'].db.drop_all()


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
@DBUtilsCommand.option(
    '--drop_all',
    dest='drop_all',
    action='store_true',
    default=False,
    help='Drop ALL tables in database',
)
@DBUtilsCommand.option(
    '--load-images',
    dest="load_gallery_images",
    action='store_true',
    default=False,
    help='Load dummy images to gallery',
)
@DBUtilsCommand.option(
    '--image-count',
    dest="image_count",
    default=100,
    help='Number of images to be loaded into gallery',
    type=int,
)
def init(
    populate_after_init=False,
    directory=None,
    drop_all=False,
    load_gallery_images=False,
    image_count=100,
):
    """ Create a new clean database
    """

    drop(drop_all=drop_all)
    with perform(
        name='dbutils init',
        before='initializing database to its latest version',
    ):
        migrate_upgrade()
    if populate_after_init:
        populate(directory)
    if load_gallery_images:
        load_images(image_count)


@DBUtilsCommand.option(
    '-d', '--directory',
    dest='directory',
    default=None,
    help='Directory to search fixtures in',
)
def populate(directory=None):
    """ Populate database with fixtures
    """

    if directory is None:
        directory = current_app.config['FIXTURES_DIR']
    with perform(
        name='dbutils populate',
        before='Loading fixtures from directory %s' % directory,
        fail='Error occured while loading fixtures',
    ):
        load_fixtures(directory)


@DBUtilsCommand.option(
    '-c', '--count',
    dest='count',
    default=100,
    help='Number of dummy images to be loaded',
    type=int,
)
def load_images(count=100):
    """ Load dummy images to populate gallery
    """

    with perform(
        name='dbutils load_images',
        before='Loading %d dummy images to gallery' % count,
        fail='Error occured while loading images to gallery',
    ):
        load_dummy_images(count)
