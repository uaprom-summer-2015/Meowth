from project.bl.utils import BaseBL
from werkzeug.security import check_password_hash, generate_password_hash


class UserBL(BaseBL):

    def set_password(self, password):
        model = self.model
        model.password = generate_password_hash(password)
        return model

    def create_user(self, data):
        model = self.model(data)
        model.bl.set_password(data["password"])
        model.save()
        return model

    def create_superuser(self, login, password):
        model = self.model
        superuser = model.bl.create_user(login, password, email=None)
        superuser.role = model.ROLE.superuser
        superuser.save()
        return superuser

    def authenticate(self, login, password):
        model = self.model
        u = model.query.filter(model.login == login).first()
        if u and check_password_hash(u.password, password):
            return u
