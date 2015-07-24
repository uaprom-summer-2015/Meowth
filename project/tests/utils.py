from flask.ext.testing import TestCase
from project import create_app as app_factory
from project.extensions import db
from project.fixtures import load_fixtures


class ProjectTestCase(TestCase):
    """
    Base class for all tests in project
    """

    def create_app(self):
        app = app_factory()
        with app.app_context():
            db.create_all()
            load_fixtures(app.config['FIXTURES_DIR'])
        return app
