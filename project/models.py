from enum import IntEnum

from sqlalchemy import Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, VARCHAR as Varchar
from project.bl.utils import Resource
from project.database import Base, db_session, engine
from project.lib.orm.types import TypeEnum
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.ext.associationproxy import association_proxy


class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    short_description = Column(String(300), nullable=False)
    text = Column(Text(), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category', backref=backref('vacancies'))
    name_in_url = Column(String(50), nullable=False, unique=True)
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
    name = Column(String(50), nullable=False, unique=True)

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
    email = Column(String(30), nullable=False, unique=True)
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
    name = Column(String(20), nullable=False, unique=True)
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


class BlockPageAssociation(Base):
    __tablename__ = 'block_page_association'
    page_id = Column(
        Integer,
        ForeignKey('pages.id'),
        primary_key=True
    )
    block_id = Column(
        Integer,
        ForeignKey('pageblocks.id'),
        primary_key=True
    )
    position = Column(Integer)
    block = relationship(
        'PageBlock',
    )

    def delete(self):
        """ Deletes the object immideately """
        db_session.delete(self)
        db_session.commit()

    def soft_delete(self):
        """ schedules object deletion """
        db_session.delete(self)


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
    block_type = Column(
        TypeEnum(TYPE),
        default=TYPE.img_left,
        nullable=False
    )
    title = Column(Varchar(128), nullable=True)  # if header needed
    text = Column(Text)  # block contents
    short_description = Column(Varchar(256), nullable=True)  # used for home
    image = Column(Text, nullable=True)

    bl = Resource('bl.pageblock')

    def __str__(self):
        return '%s: %s' % (self.title, self.text or self.short_description)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def delete(self):
        """ Deletes the object immideately """
        db_session.delete(self)
        db_session.commit()

    def soft_delete(self):
        """ schedules object deletion """
        db_session.delete(self)

    def save(self):
        # TODO: move save operation to bl
        db_session.add(self)
        db_session.commit()


class Page(Base):
    __tablename__ = 'pages'

    id = Column(Integer, primary_key=True)
    title = Column(Varchar(128))
    url = Column(Text)
    _blocks = relationship(
        "BlockPageAssociation",
        order_by='BlockPageAssociation.position',
        collection_class=ordering_list('position'),
        cascade='save-update, merge, delete, delete-orphan',
    )
    blocks = association_proxy(
        '_blocks',
        'block',
        creator=lambda _pb: BlockPageAssociation(block=_pb)
    )

    bl = Resource('bl.page')

    def __str__(self):
        return '%s (%s)' % (self.title, self.url)

    def save(self):
        # TODO: move save operation to bl
        db_session.add(self)
        db_session.commit()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def delete(self):
        """ Deletes the object immideately """
        db_session.delete(self)
        db_session.commit()

    def soft_delete(self):
        """ schedules object deletion """
        db_session.delete(self)


class Token(Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True)
    user = relationship('User', backref=backref('token'))
    user_id = Column(Integer, ForeignKey('users.id'))
    token = Column(String, nullable=False)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
