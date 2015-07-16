from project.bl.utils import BaseBL
# from project.database import db_session
from werkzeug.security import check_password_hash
# from project.models import User


class UserBL(BaseBL):
    def create_superuser(self, login, password):
        user_model = self._model
        superuser = user_model(login, password, email=None)
        superuser.role = user_model.ROLE.superuser
        u = user_model.query.filter(user_model.login == login).first()
        if not u:
            superuser.save()
            return True
        return False

    def authenticate(self, login, password):
        user_model = self._model
        u = user_model.query.filter(user_model.login == login).first()
        if u and check_password_hash(u.password, password):
            return u
