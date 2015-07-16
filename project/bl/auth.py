from project.database import db_session
from werkzeug.security import check_password_hash
from project.models import User


def create_superuser(login, password):
    superuser = User(login, password, email=None)
    superuser.role = User.ROLE.superuser
    u = db_session.query(User).filter(User.login == login).first()
    if not u:
        superuser.save()
        return True
    return False


def authenticate(login, password):
    u = db_session.query(User).filter(User.login == login).first()
    if u and check_password_hash(u.password, password):
        return u
