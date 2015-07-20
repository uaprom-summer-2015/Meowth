from project.bl.utils import BaseBL
from werkzeug.security import check_password_hash, generate_password_hash
from project.lib.auth import generate_random_password

class UserBL(BaseBL):

    def set_password(self, password):
        model = self.model
        model.password = generate_password_hash(password)

    def create(self, data):
        from .mail import send_mail
        model = self.model(**data)
        if 'password' in data:
            model.bl.set_password(data['password'])
        else:
            random_password = generate_random_password(8)
            model.bl.set_password(random_password)
            recipients = [data['email'], ]
            title = 'Вам была создана учетная запись на HR портале!'
            body = 'login: {}\npassword:{}'.format(data['login'], random_password)
            send_mail(title, body, recipients)
        model.save()
        return model

    def update(self, data):
        model = self.model
        for key, value in data.items():
            setattr(model, key, value)
        model.bl.set_password(data['password'])
        model.save()
        return model

    def create_superuser(self, login, password):
        model = self.model
        superuser = model.bl.create({
             'login': login,
             'password': password,
        })
        superuser.role = model.ROLE.superuser
        superuser.save()
        return superuser

    def authenticate(self, login, password):
        model = self.model
        u = model.query.filter(model.login == login).first()
        if u and check_password_hash(u.password, password):
            return u

