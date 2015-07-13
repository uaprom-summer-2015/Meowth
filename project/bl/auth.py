from project.database import db_session
from werkzeug.security import check_password_hash

def create_superuser(cls, login, password):
    superuser = cls(login, password, email=None)
    superuser.role = cls.ROLE.superuser
    u = db_session.query(cls).filter(cls.login == login).first()
    if not u:
        superuser.save()
        return True
    return False


def authenticate(cls, login, password):
    u = db_session.query(cls).filter(cls.login == login).first()
    if u and check_password_hash(u.password, password):
        return u
