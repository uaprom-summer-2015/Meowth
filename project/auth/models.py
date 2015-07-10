from sqlalchemy import Column, Integer, String, Boolean
from project.database import Base, db_session
from hashlib import sha256
from project import app


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(30), unique=True)
    password = Column(String(100))
    name = Column(String(30))
    surname = Column(String(30))
    email = Column(String(30), unique=True)
    role = Column(Boolean)  # False for staff, True for superuser

    def __init__(self, login, password, name=None, surname=None, email=None, role=False):
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
        return self.role

    @staticmethod
    def hash(password):
        encoded = (password + app.config['SALT']).encode('utf-8')
        return sha256(encoded).hexdigest()

    def set_password(self, password):
        self.password = self.hash(password)

    @staticmethod
    def authenticate(login, password):
        u = User.query.filter(User.login == login).one()
        if u.password == User.hash(password):
            return u
