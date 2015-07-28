from unittest.mock import Mock, patch
from werkzeug.security import check_password_hash
from project.bl import UserBL
from project.tests.utils import ProjectTestCase
from project.extensions import mail
from project.models import User, Vacancy
from project.tasks.mail import celery_send_mail
import re


class TestUserBL(ProjectTestCase):

    def test_set_password(self):
        """Check password setter correctness"""
        raw_pass = 'celestia'
        instance = Mock(password=None)
        bl = UserBL(instance)
        bl.set_password(raw_pass)
        self.assertIsNotNone(instance.password)
        self.assertTrue(check_password_hash(instance.password, raw_pass))

    @patch(
        target='project.tasks.mail.celery_send_mail.delay',
        new=celery_send_mail,
    )
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
            match = re.search(
                r'/auth/reset/(?P<token>\w{20})',
                outbox[0].body,
            )
            token = match.groupdict()['token'] if match else None
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
            match = re.search(
                r'Новый пароль: (?P<new_password>\w{8})',
                outbox[1].body,
            )
            new_password = match.groupdict()['new_password'] if match else None
            usr = User.bl.authenticate(login, new_password)
            self.assertIsNotNone(
                usr,
                msg="User was not authenticated with new password"
            )

    def test_create_with_password(self):
        password = 'cadence'
        email = 'cadence@canterlot.com'
        login = 'cadence'
        name = 'Cadence'
        surname = 'Princess'
        data = {
            'login': login,
            'password': password,
            'email': email,
            'name': name,
            'surname': surname,
        }
        User.bl.create(data)
        usr = User.bl.authenticate(login, password)
        self.assertIsNotNone(
            usr,
            msg="Cannot authenticate created user",
        )
        self.assertEqual(
            usr.name,
            name,
            msg='Names do not match',
        )
        self.assertEqual(
            usr.surname,
            surname,
            msg='Surnames do not match',
        )

    @patch(
        target='project.tasks.mail.celery_send_mail.delay',
        new=celery_send_mail,
    )
    def test_create_without_password(self):
        with mail.record_messages() as outbox:
            email = 'celestia@canterlot.com'
            login = 'celestia'
            name = 'Celestia'
            surname = 'Princess'
            data = {
                'login': login,
                'email': email,
                'name': name,
                'surname': surname,
            }
            User.bl.create(data)
            self.assertEqual(
                len(outbox),
                1,
            )
            self.assertEqual(
                outbox[0].subject,
                'Вам была создана учетная запись на HR портале!',
                msg='Incorrect mail subject',
            )
            self.assertEqual(
                outbox[0].recipients,
                [email],
                msg='Incorrect recipients',
            )
            match = re.search(
                r'login: (?P<_login>\w+)\npassword:(?P<_password>\w{8})',
                outbox[0].body,
            )
            _login = match.groupdict()['_login'] if match else None
            _password = match.groupdict()['_password'] if match else None
            self.assertEqual(
                _login,
                login,
                msg='Logins do not match!',
            )
            usr = User.bl.authenticate(login, _password)
            self.assertIsNotNone(
                usr,
                msg="Cannot authenticate created user",
            )
            self.assertEqual(
                usr.name,
                name,
                msg='Names do not match',
            )
            self.assertEqual(
                usr.surname,
                surname,
                msg='Surnames do not match',
            )


class TestVacancyBL(ProjectTestCase):

    def test_get_visible(self):
        visible_list = Vacancy.bl.get_visible()
        vacancy_list = Vacancy.query.all()

        for vacancy in visible_list:
            self.assertTrue(
                vacancy in vacancy_list,
                msg='Vacancy returned by get_visible is not in all vacancies',
            )
            self.assertFalse(
                vacancy.hide,
                msg='Vacancy returned by get_visible is hidden',
            )
        for vacancy in vacancy_list:
            if vacancy not in visible_list:
                self.assertTrue(
                    vacancy.hide,
                    msg='There is a visible vacancy which is not returned'
                        'with get_visible',
                )
