from unittest.mock import Mock, patch
from werkzeug.security import check_password_hash
from project.bl import UserBL
from project.lib.admin import get_actual_vacancies_list
from project.lib.feed import get_visible_vacancies_list
from project.tests.utils import ProjectTestCase
from project.models import Category, User, Vacancy
import re
from uuid import uuid4


class TestBaseBL(ProjectTestCase):
    """ Tests `create` and `update` methods of BaseBL
        Using Category's BL for this as it is BaseBL
    """

    def test_create(self):
        """ Actually the purpose of this test is to check if BL won't fail
        """
        data = {
            'name': uuid4().hex,
        }
        result = Category.bl.create(data)
        self.assertEqual(result.name, data['name'])
        db_entry = Category.query.filter(Category.name == data['name']).one()
        self.assertEqual(result, db_entry)

    def test_update(self):
        """ Actually the purpose of this test is to check if BL won't fail
        """
        data = {
            'name': uuid4().hex,
        }
        result = Category.bl.create(data)
        data['name'] = uuid4().hex
        updated = result.bl.update(data)
        self.assertEqual(updated.name, data['name'])


class TestUserBlResetPassword(ProjectTestCase):

    def setUp(self):
        self.data = {
            'login': "nightmaremoon",
            'password': 'nightmaremoon',
            'email': 'nightmaremoon@canterlot.com',
            'name': 'Luna',
            'surname': 'Princess',
        }
        User.bl.create(self.data)
        with patch('project.tasks.mail.celery_send_mail.delay') as send_mail:
            User.bl.forgot_password(self.data['email'])
            self.mail_tok, *_ = send_mail.call_args[0]

    def test_is_mail_sent(self):
        self.assertIsNotNone(
            self.mail_tok,
            msg='Mail was not sent',
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

    def test_is_subject_correct(self):
        self.assertEqual(
            self.mail_tok.subject,
            "Cброс пароля на HR портале",
        )

    def test_is_recipient_correct(self):
        self.assertEqual(
            self.mail_tok.recipients,
            [self.data['email']],
        )

    def test_is_success(self):
        match = re.search(
            r'/auth/reset/(?P<token>\w{20})',
            self.mail_tok.body,
        )
        token = match.groupdict()['token'] if match else None
        with patch('project.tasks.mail.celery_send_mail.delay') as send_mail:
            is_success = User.bl.reset_password(token)
            mail_pwd, *_ = send_mail.call_args[0]
        self.assertTrue(is_success)
        usr = User.bl.authenticate(self.data['login'], self.data['password'])
        self.assertIsNone(
            usr,
            msg='user was authenticated w/ old password',
        )
        match = re.search(
            r'Новый пароль: (?P<new_password>\w{8})',
            mail_pwd.body,
        )
        new_password = match.groupdict()['new_password'] if match else None
        usr = User.bl.authenticate(self.data['login'], new_password)
        self.assertIsNotNone(
            usr,
            msg='user was not authenticated w/ new password',
        )


class TestUserBlCreateWithPassword(ProjectTestCase):

    def setUp(self):
        self.data = {
            'login': 'cadance',
            'password': 'cadance',
            'email': 'cadance@canterlot.com',
            'name': 'Cadance',
            'surname': 'Princess',
        }
        User.bl.create(self.data)

    def test_is_user_created(self):
        usr = User.bl.authenticate(self.data['login'], self.data['password'])
        self.assertIsNotNone(
            usr,
            msg="Cannot authenticate created user",
        )
        self.assertEqual(
            usr.name,
            self.data['name'],
            msg='Names do not match',
        )
        self.assertEqual(
            usr.surname,
            self.data['surname'],
            msg='Surnames do not match',
        )


class TestUserBlCreateWithoutPassword(ProjectTestCase):

    def setUp(self):
        self.data = {
            'login': 'celestia',
            'email': 'celestia@canterlot.com',
            'name': 'Celestia',
            'surname': 'Princess',
        }
        with patch('project.tasks.mail.celery_send_mail.delay') as send_mail:
            User.bl.create(self.data)
            self.mail, *_ = send_mail.call_args[0]

    def test_is_mail_sent(self):
        self.assertIsNotNone(
            self.mail,
            msg='Mail was not sent',
        )

    def test_is_mail_subject_correct(self):
        self.assertEqual(
            self.mail.subject,
            'Вам была создана учетная запись на HR портале!',
            msg='Incorrect mail subject',
        )

    def test_is_mail_recipients_correct(self):
        self.assertEqual(
            self.mail.recipients,
            [self.data['email']],
            msg='Incorrect recipients',
        )

    def test_is_user_created(self):
        match = re.search(
            r'login: (?P<_login>\w+)\npassword:(?P<_password>\w{8})',
            self.mail.body,
        )
        _login = match.groupdict()['_login'] if match else None
        _password = match.groupdict()['_password'] if match else None
        self.assertEqual(
            _login,
            self.data['login'],
            msg='Logins do not match!',
        )
        usr = User.bl.authenticate(_login, _password)
        self.assertIsNotNone(
            usr,
            msg="Cannot authenticate created user",
        )
        self.assertEqual(
            usr.name,
            self.data['name'],
            msg='Names do not match',
        )
        self.assertEqual(
            usr.surname,
            self.data['surname'],
            msg='Surnames do not match',
        )


class TestUserBL(ProjectTestCase):

    def test_set_password(self):
        """Check password setter correctness"""
        raw_pass = 'celestia'
        instance = Mock(password=None)
        bl = UserBL(instance)
        bl.set_password(raw_pass)
        self.assertIsNotNone(instance.password)
        self.assertTrue(check_password_hash(instance.password, raw_pass))

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


class TestVacancyBL(ProjectTestCase):

    def test_get_visible(self):
        visible_list = get_visible_vacancies_list()
        vacancy_list = Vacancy.query.all()

        for vacancy in vacancy_list:
            if vacancy.condition_is_deleted:
                self.assertTrue(
                    vacancy.title not in (v['title'] for v in visible_list),
                    msg='Vacancy returned by get_visible but it is deleted'
                )
            elif vacancy.condition_is_hidden:
                self.assertTrue(
                    vacancy.title not in (v['title'] for v in visible_list),
                    msg='Vacancy returned by get_visible but it is hide'
                )
            else:
                self.assertTrue(
                    vacancy.title in (v['title'] for v in visible_list),
                    msg='There is a visible vacancy which is not returned'
                        'with get_visible'
                )

    def test_get_actual(self):
        actual_list = get_actual_vacancies_list()
        vacancy_list = Vacancy.query.all()

        for vacancy in vacancy_list:
            if vacancy.condition_is_deleted:
                self.assertTrue(
                    vacancy.title not in (v['title'] for v in actual_list),
                    msg='Vacancy returned by get_actual but it is deleted'
                )
            else:
                self.assertTrue(
                    vacancy.title in (v['title'] for v in actual_list),
                    msg='There is a visible vacancy which is not returned'
                        'with get_actual'
                )
