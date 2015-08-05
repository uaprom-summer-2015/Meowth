from flask import session
from project.bl.utils import BaseBL


class MailTemplateBL(BaseBL):

    def update(self, data):
        self.update_user()
        super().update(data)

    def update_user(self):
        self.model.user_id = session['user_id']
