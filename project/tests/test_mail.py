from sqlalchemy.exc import StatementError
from project.models import MailTemplate
from project.tests.utils import ProjectTestCase


class TestMailTemplateBl(ProjectTestCase):

    def test_get(self):
        mail1 = MailTemplate.bl.get(MailTemplate.MAIL.CV)
        mail2 = MailTemplate.query.filter(
            MailTemplate.mail == MailTemplate.MAIL.CV
        ).one()
        self.assertEqual(mail1, mail2)

        with self.assertRaises(StatementError):
            MailTemplate.bl.get(100)
