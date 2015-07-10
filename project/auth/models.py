from sqlalchemy import Column, Integer, String, Enum
from project.database import Base, db_session
from hashlib import sha256
from project import app


roles_enum = ('superuser', 'staff')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(30), unique=True)
    password = Column(String(100))
    name = Column(String(30))
    surname = Column(String(30))
    email = Column(String(30))
    role = Column(Enum(*roles_enum, name='roles_enum'))

    def __init__(self, login, password, name=None, surname=None, email=None, role='staff'):
        self.name = name
        self.email = email
        self.login = login
        self.surname = surname
        self.role = role
        self.set_password(password)

    def __repr__(self):
        return '<User {}>'.format(self.get_full_name())

    def get_full_name(self):
        return '{} {}'.format(self.name, self.surname)

    def save(self):
        db = db_session()
        db.add(self)
        db.commit()
        db.close()

    def is_superuser(self):
        return True if self.role == 'superuser' else False

    def set_password(self, password):
        self.password = self.hash(password)

    @staticmethod
    def hash(password):
        encoded = (password + app.config['SALT']).encode('utf-8')
        return sha256(sha256(encoded).hexdigest().encode('utf-8')).hexdigest()  # two iterations

    @staticmethod
    def create_superuser(login, password):
        superuser = User(login, password, role='superuser')
        u = User.query.filter(User.login == login).first()
        if not u:
            superuser.save()
            return True
        return False

    @staticmethod
    def authenticate(login, password):
        u = User.query.filter(User.login == login).first()
        if u and u.password == User.hash(password):
            return u
