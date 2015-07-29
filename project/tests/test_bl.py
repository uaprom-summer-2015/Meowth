from unittest.mock import Mock, patch
from werkzeug.security import check_password_hash
from project.bl import UserBL
from project.tests.utils import ProjectTestCase
from project.models import User, Vacancy
import re


celery_send_mail = Mock(return_value=None)


class TestUserBL(ProjectTestCase):

    def test_set_password(self):
        """Check password setter correctness"""
        raw_pass = 'celestia'
        instance = Mock(password=None)
        bl = UserBL(instance)
        bl.set_password(raw_pass)
        self.assertIsNotNone(instance.password)
        self.assertTrue(check_password_hash(instance.password, raw_pass))

    @patch('project.tasks.mail.celery_send_mail.delay')
    def test_reset_password(self, send_mail):
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
        self.assertEqual(send_mail.call_count, 1)
        mail, *_ = send_mail.call_args[0]
        del _
        self.assertIsNotNone(
            mail,
            msg='Mail was not sent',
        )
        self.assertEqual(
            mail.subject,
            "Cброс пароля на HR портале",
            msg="Incorrect mail subject",
        )
        self.assertEqual(
            mail.recipients,
            [email],
            msg="Incorrect recipients",
        )
        match = re.search(
            r'/auth/reset/(?P<token>\w{20})',
            mail.body,
        )
        del mail
        token = match.groupdict()['token'] if match else None
        is_success = User.bl.reset_password(token)
        self.assertTrue(
            is_success,
            msg='Resetting password failed',
        )
        self.assertEqual(send_mail.call_count, 2)
        mail, *_ = send_mail.call_args[0]
        del _
        self.assertIsNotNone(
            mail,
            msg='Mail was not sent',
        )
        self.assertEqual(
            mail.recipients,
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
            mail.body,
        )
        del mail
        new_password = match.groupdict()['new_password'] if match else None
        usr = User.bl.authenticate(login, new_password)
        self.assertIsNotNone(
            usr,
            msg="User was not authenticated with new password"
        )

    @patch('project.tasks.mail.celery_send_mail.delay')
    def test_reset_password_bad_token(self, send_mail):
        fake_token = '-1!~ -2'
        is_success = UserBL.reset_password(fake_token)
        self.assertFalse(
            is_success,
            msg='resetToken succeeded on bad token',
        )
        self.assertFalse(
            send_mail.called,
            msg='send_mail was called, while it shouldn\'t'
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

    @patch('project.tasks.mail.celery_send_mail.delay')
    def test_create_without_password(self, send_mail):
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
        self.assertEqual(send_mail.call_count, 1)
        mail, *_ = send_mail.call_args[0]
        del _
        self.assertIsNotNone(
            mail,
            msg='Mail was not sent',
        )
        self.assertEqual(
            mail.subject,
            'Вам была создана учетная запись на HR портале!',
            msg='Incorrect mail subject',
        )
        self.assertEqual(
            mail.recipients,
            [email],
            msg='Incorrect recipients',
        )
        match = re.search(
            r'login: (?P<_login>\w+)\npassword:(?P<_password>\w{8})',
            mail.body,
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

    def test_create_superuser(self):
        login = 'tirek'
        password = 'tirek'
        u = User.bl.create_superuser(login, password)
        self.assertIsNotNone(
            u,
            msg='created superuser is None',
        )
        self.assertEqual(
            u.role,
            User.ROLE.superuser,
            msg='created superuser is not actually a superuser',
        )
        del u
        u = User.bl.authenticate(login, password)
        self.assertIsNotNone(
            u,
            msg='Cannot authenticate created superuser',
        )
        self.assertEqual(
            u.role,
            User.ROLE.superuser,
            msg='authenticated superuser is not actually a superuser',
        )
        del u


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
