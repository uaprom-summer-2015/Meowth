from flask import url_for
from flask.ext.testing import TestCase
from project import create_app as app_factory
from project.extensions import db
from project.fixtures import load_fixtures
from project.lib.context_managers import disable_csrf


class ProjectTestCase(TestCase):
    """
    Base class for all tests in project
    """
    def log_in(self, login='cthulhu'):
        # assume that login is equal to password
        credentials = {"login": login, "password": login}
        with disable_csrf(self.app):
            self.client.post(url_for("auth.login"), data=credentials)

    # noinspection PyAttributeOutsideInit
    def create_app(self):
        self.app = app_factory()
        with self.app.app_context():
            db.create_all()
            load_fixtures(self.app.config['FIXTURES_DIR'])
        return self.app

    # noinspection PyPep8Naming
    def tearDown(self):
        """
        Drop it all!

        DO NOT FORGET TO CALL THIS METHOD WHEN OVERRIDING
        """
        with self.app.app_context():
            db.drop_all()
