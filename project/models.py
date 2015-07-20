from enum import IntEnum

from sqlalchemy import Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String
from project.bl.utils import Resource
from project.database import Base, db_session, engine
from project.lib.orm.types import TypeEnum
from sqlalchemy.ext.orderinglist import ordering_list


class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    short_description = Column(String(300), nullable=False)
    text = Column(Text(), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category', backref=backref('vacancies'))
    name_in_url = Column(String(50), nullable=False)
    visits = Column(Integer, nullable=False, default=0)
    salary = Column(String(50))
    description = Column(String(200))  # for search spider
    keywords = Column(String(1000))
    city_id = Column(Integer, ForeignKey('city.id'))
    city = relationship('City', backref=backref('vacancies'))
    hide = Column(Boolean, nullable=False, default=False)

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
    name = Column(String(50), nullable=False)

    bl = Resource('bl.category')

    def __str__(self):
        return self.name

    def __repr__(self):
        return "[{}] {}".format(self.__class__.__name__, self.name)

    def save(self):
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
    login = Column(String(30), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    name = Column(String(30))
    surname = Column(String(30))
    email = Column(String(30), nullable=False)
    role = Column(TypeEnum(ROLE), nullable=False, default=ROLE.staff)

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
    name = Column(String(20), nullable=False)
    bl = Resource('bl.city')

    def __str__(self):
        return self.name

    def __repr__(self):
        return "[{}] {}".format(self.__class__.__name__, self.name)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class PageBlock(Base):
    __tablename__ = 'pageblocks'

    # noinspection PyTypeChecker
    TYPE = IntEnum(
        'Block_type',
        {
            'img_left': 0,
            'img_right': 1,
            'no_img': 2,
        },
    )

    id = Column(Integer, primary_key=True)
    block_type = Column(TypeEnum(TYPE), default=TYPE.img_left, nullable=False)
    title = Column(String(128), nullable=True)  # if header needed
    text = Column(String(1024))  # block contents
    short_description = Column(String(256), nullable=True)  # used for homepage
    # by http://stackoverflow.com/a/219664:
    image = Column(String(2083), nullable=True)
    position = Column(Integer, nullable=False)  # ordering blocks on pages
    page_id = Column(Integer, ForeignKey('pages.id'))  # belongs to page

    bl = Resource('bl.pageblock')

    def __str__(self):
        return '%s: %s' % (self.title, self.text or self.short_description)

    def save(self):
        # FIXME: temporary workaround to support current workflow:
        # TODO: replace w/ better logic later
        if not self.position:
            self.position = 0
        db_session.add(self)
        db_session.commit()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Page(Base):
    __tablename__ = 'pages'

    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    url = Column(String(2083))  # by http://stackoverflow.com/a/219664
    blocks = relationship(
        "PageBlock",
        backref="page",
        order_by='PageBlock.position',
        collection_class=ordering_list('position'),
    )

    bl = Resource('bl.page')

    def __str__(self):
        return '%s (%s)' % (self.title, self.url)

    def save(self):
        # TODO: move save operation to bl
        # Readd blocks to follow the order:
        # TODO: possible crutch:
        _ = [block for block in self.blocks]
        while (len(self.blocks)):
            self.blocks.pop()
        for block in _:
            self.blocks.append(block)
        del _
        db_session.add(self)
        db_session.commit()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
