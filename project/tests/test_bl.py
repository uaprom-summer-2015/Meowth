from unittest.mock import Mock
from werkzeug.security import check_password_hash
from project.bl import UserBL
from project.tests.utils import ProjectTestCase
from project.extensions import mail
from project.models import User


class TestUserBL(ProjectTestCase):

    def test_set_password(self):
        """Check password setter correctness"""
        raw_pass = 'celestia'
        instance = Mock(password=None)
        bl = UserBL(instance)
        bl.set_password(raw_pass)
        self.assertIsNotNone(instance.password)
        self.assertTrue(check_password_hash(instance.password, raw_pass))

    def test_reset_password(self):
        with mail.record_messages() as outbox:
            orig_password = 'nightmaremoon'
            email = 'nightmaremoon@canterlot.com'
            login = 'nightmaremoon'
            data = {
                'login': login,
                'password': orig_password,
                'email': email,
                'name': 'Luna',
                'surname': 'Princess',
            }
            User.bl.create(data)
            usr = User.bl.authenticate(login, orig_password)
            self.assertIsNotNone(usr)
            del usr
            User.bl.forgot_password(email)
            self.assertEqual(
                len(outbox),
                1,
            )
            self.assertEqual(
                outbox[0].subject,
                "Cброс пароля на HR портале",
                msg="Incorrect mail subject",
            )
            self.assertEqual(
                outbox[0].recipients,
                [email],
                msg="Incorrect recipients",
            )
            token = outbox[0].body[-20:]
            is_success = User.bl.reset_password(token)
            self.assertTrue(
                is_success,
                msg='Resetting password failed',
            )
            self.assertEqual(
                len(outbox),
                2,
            )
            self.assertEqual(
                outbox[1].recipients,
                [email],
                msg="Incorrect recipients",
            )
            usr = User.bl.authenticate(login, orig_password)
            self.assertIsNone(
                usr,
                msg="User authenticated w/ old password",
            )
            del usr
            new_password = outbox[1].body[-8:]
            usr = User.bl.authenticate(login, new_password)
            self.assertIsNotNone(
                usr,
                msg="User was not authenticated with new password"
            )
