from sqlalchemy import Column, Integer, String
from project.database import Base, db_session
from werkzeug.security import generate_password_hash, check_password_hash
from enum import IntEnum
from sqlalchemy.types import SmallInteger, TypeDecorator


class TypeEnum(TypeDecorator):

    impl = SmallInteger

    def process_bind_param(self, value, dialect):
        return User.ROLE[value].value

    def process_result_value(self, value, dialect):
        return User.ROLE(value)


class User(Base):
    __tablename__ = 'users'

    ROLE = IntEnum('role', {'STAFF': 0,
                            'SUPERUSER': 1})

    id = Column(Integer, primary_key=True)
    login = Column(String(30), unique=True)
    password = Column(String(100))
    name = Column(String(30))
    surname = Column(String(30))
    email = Column(String(30))
    role = Column(TypeEnum())

    def __init__(self, login, password, email, name=None,
                 surname=None):
        self.name = name
        self.email = email
        self.login = login
        self.surname = surname
        self.role = self.ROLE.STAFF
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
        return self.role == self.ROLE.SUPERUSER

    def set_password(self, password):
        self.password = generate_password_hash(password)

    @staticmethod
    def create_superuser(login, password):
        superuser = User(login, password, email=None)
        superuser.role = User.ROLE.SUPERUSER
        u = User.query.filter(User.login == login).first()
        if not u:
            superuser.save()
            return True
        return False

    @staticmethod
    def authenticate(login, password):
        u = User.query.filter(User.login == login).first()
        if u and check_password_hash(u.password, password):
            return u
