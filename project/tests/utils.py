from flask.ext.testing import TestCase
from project import create_app as app_factory
from project.extensions import db
from project.fixtures import load_fixtures


class ProjectTestCase(TestCase):
    """
    Base class for all tests in project
    """

    def create_app(self):
        self.app = app_factory()
        with self.app.app_context():
            db.create_all()
            load_fixtures(self.app.config['FIXTURES_DIR'])
        return self.app

    def tearDown(self):
        """
        Drop it all!

        DO NOT FORGET TO CALL THIS METHOD WHEN OVERRIDING
        """
        with self.app.app_context():
            db.drop_all()
