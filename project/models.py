from enum import IntEnum

from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash

from project.bl.utils import Resource
from project.database import Base, db_session
from project.lib.orm.types import TypeEnum


class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    short_description = Column(String(300))
    text = Column(Text())
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category', backref=backref('vacancies'))
    name_in_url = Column(String(50))
    visits = Column(Integer)
    salary = Column(String(50))
    description = Column(String(200))  # for search spider
    keywords = Column(String(1000))

    bl = Resource('bl.vacancy')

    def __init__(self, title, short_description, text, category,
                 name_in_url, description=None,
                 keywords=None, salary=None, visits=0):
        self.title = title
        self.short_description = short_description
        self.text = text
        self.category = category
        self.name_in_url = name_in_url
        self.visits = visits
        self.salary = salary
        self.description = description
        self.keywords = keywords

    def __repr__(self):
        return "[{}] {}".format(self.__class__.__name__, self.title)

    def save(self):
        db_session.add(self)
        db_session.commit()


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    bl = Resource('bl.category')

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "[{}] {}".format(self.__class__.__name__, self.name)

    def save(self):
        db_session.add(self)
        db_session.commit()


class User(Base):
    __tablename__ = 'users'

    #  noinspection PyTypeChecker
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

    @staticmethod
    def authenticate(login, password):
        from project.bl.auth import authenticate as bl_authenticate

        return bl_authenticate(login, password)

    @staticmethod
    def create_superuser(login, password):
        from project.bl.auth import create_superuser as bl_create_superuser

        return bl_create_superuser(login, password)
