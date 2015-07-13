from sqlalchemy import Column, Integer, String
from project.database import Base, db_session
from werkzeug.security import generate_password_hash
from enum import IntEnum
from sqlalchemy.types import SmallInteger, TypeDecorator


class TypeEnum(TypeDecorator):

    impl = SmallInteger

    def __init__(self, enum, *args, **kwargs):
        self._enum = enum
        TypeDecorator.__init__(self, *args, **kwargs)

    def process_bind_param(self, enum, dialect):
        return enum.value

    def process_result_value(self, value, dialect):
        return self._enum(value)


class User(Base):
    __tablename__ = 'users'

    ROLE = IntEnum('Role', {
        'staff': 0,
        'superuser': 1,
    })

    id = Column(Integer, primary_key=True)
    login = Column(String(30), unique=True)
    password = Column(String(100))
    name = Column(String(30))
    surname = Column(String(30))
    email = Column(String(30))
    role = Column(TypeEnum(ROLE), default=ROLE.staff)

    def __init__(self, login, password, email, name=None,
                 surname=None):
        self.email = email
        self.login = login
        self.name = name
        self.surname = surname
        self.set_password(password)

    def __repr__(self):
        return '<User {}>'.format(self.get_full_name())

    def get_full_name(self):
        return '{} {}'.format(self.name, self.surname)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def is_superuser(self):
        return self.role == self.ROLE.superuser

    def set_password(self, password):
        self.password = generate_password_hash(password)
