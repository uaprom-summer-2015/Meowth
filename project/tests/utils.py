from flask.ext.testing import TestCase
from project import app as flask_app


class ProjectTestCase(TestCase):
    """
    Base class for all tests in project
    """

    def create_app(self):
        app = flask_app
        app.config['TESTING'] = True
        return app
