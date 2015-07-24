from unittest.mock import Mock
from werkzeug.security import check_password_hash
from project.bl import UserBL
from project.tests.utils import ProjectTestCase


class TestUserBL(ProjectTestCase):

    def test_set_password(self):
        """Check password setter correctness"""
        raw_pass = 'celestia'
        instance = Mock(password=None)
        bl = UserBL(instance)
        bl.set_password(raw_pass)
        self.assertIsNotNone(instance.password)
        self.assertTrue(check_password_hash(instance.password, raw_pass))
