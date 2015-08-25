from urllib.parse import urljoin
from flask import request, url_for
from project.bl.utils import BaseBL
from werkzeug.security import check_password_hash, generate_password_hash
from project.lib.auth import generate_random_string
from sqlalchemy import func


class UserBL(BaseBL):

    def set_password(self, password):
        model = self.model
        model.password = generate_password_hash(password)

    def create(self, data):
        from project.lib.mail import send_mail
        model = self.model(**data)
        if 'password' in data:
            model.bl.set_password(data['password'])
        else:
            random_password = generate_random_string(8)
            model.bl.set_password(random_password)
            recipients = [data['email'], ]
            title = 'Вам была создана учетная запись на HR портале!'
            body = 'login: {}\npassword:{}'\
                .format(data['login'], random_password)
            send_mail(title=title,
                      recipients=recipients,
                      body=body)
        model.bl.save()
        return model

    def forgot_password(self, email):
        from project.models import Token
        from project.lib.mail import send_mail
        model = self.model
        u = model.query\
            .filter(func.lower(model.email) == func.lower(email))\
            .first()
        token = Token(token=generate_random_string(20), user=u)
        token.bl.save()
        recipients = [u.email, ]
        title = 'Cброс пароля на HR портале'
        url = urljoin(
            request.host_url,
            url_for('auth.confirm_reset', token=token.token)
        )
        body = 'Ваша ссылка для сброса пароля: {}'.format(url)
        send_mail(title=title,
                  body=body,
                  recipients=recipients)

    @staticmethod
    def reset_password(token):
        from project.models import Token
        from project.lib.mail import send_mail
        token = Token.query.filter(Token.token == token).first()
        if not token:
            return False
        u = token.user
        random_password = generate_random_string(8)
        u.bl.set_password(random_password)
        u.bl.save()
        recipients = [u.email, ]
        title = 'Сброс пароля на HR портале'
        body = 'Ваш пароль был успешно cброшен! \n Новый пароль: {}'\
            .format(random_password)
        send_mail(title=title,
                  body=body,
                  recipients=recipients)
        token.bl.delete()
        return True

    def create_superuser(self, login, password, email):
        model = self.model
        superuser = model.bl.create({
            'login': login,
            'password': password,
            'email': email ,
        })
        superuser.role = model.ROLE.superuser
        superuser.bl.save()
        return superuser

    def authenticate(self, login, password):
        model = self.model
        u = model.query.filter(model.login == login).first()
        if u and check_password_hash(u.password, password):
            return u


class TokenBL(BaseBL):
    pass
