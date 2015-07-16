from enum import IntEnum

from sqlalchemy import Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String
from project.bl.utils import Resource
from project.database import Base, db_session, engine
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
    city_id = Column(Integer, ForeignKey('city.id'))
    city = relationship('City', backref=backref('vacancies'))
    hide = Column(Boolean)

    bl = Resource("bl.vacancy")

    def __repr__(self):
        return "[{}] {}".format(self.__class__.__name__, self.title)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    bl = Resource('bl.category')

    def __str__(self):
        return self.name

    def __repr__(self):
        return "[{}] {}".format(self.__class__.__name__, self.name)

    def save(self):
        db_session.rollback()
        db_session.add(self)
        db_session.commit()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


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

    bl = Resource('bl.user')

    def __repr__(self):
        return '<User {}>'.format(self.get_full_name())

    def get_full_name(self):
        return '{} {}'.format(self.name, self.surname)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def is_superuser(self):
        return self.role == self.ROLE.superuser


class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    bl = Resource('bl.city')

    def __str__(self):
        return self.name

    def __repr__(self):
        return "[{}] {}".format(self.__class__.__name__, self.name)

    def save(self):
        db_session.add(self)
        db_session.commit()

<<<<<<< HEAD:project/feed/models.py
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
=======

def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
>>>>>>> 0d97aadcf9a19d4593c82f84b8c9f578c4649f6a:project/models.py
