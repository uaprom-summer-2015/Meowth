from enum import IntEnum
import datetime
from project.bl.utils import Resource
from project.extensions import db
from project.lib.orm.types import TypeEnum, GUID
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.ext.associationproxy import association_proxy


class Vacancy(db.Model):
    __tablename__ = 'vacancies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    short_description = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', backref=db.backref('vacancies'))
    name_in_url = db.Column(db.String(50), nullable=False, unique=True)
    visits = db.Column(db.Integer, nullable=False, default=0)
    salary = db.Column(db.String(50))
    description = db.Column(db.String(200))  # for search spider
    keywords = db.Column(db.String(1000))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    city = db.relationship('City', backref=db.backref('vacancies'))
    hide = db.Column(db.Boolean, nullable=False, default=False)
    deleted = db.Column(db.Boolean, nullable=False, default=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now,
                           onupdate=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    who_updated = db.relationship('User')

    bl = Resource("bl.vacancy")

    def __repr__(self):
        return "[{}] {}".format(self.__class__.__name__, self.title)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    bl = Resource('bl.category')

    def __str__(self):
        return self.name

    def __repr__(self):
        return "[{}] {}".format(self.__class__.__name__, self.name)


class User(db.Model):
    __tablename__ = 'users'

    #  noinspection PyTypeChecker
    ROLE = IntEnum('Role', {
        'staff': 0,
        'superuser': 1,
    })

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(30))
    surname = db.Column(db.String(30))
    email = db.Column(db.String(30), nullable=False, unique=True)
    role = db.Column(TypeEnum(ROLE), nullable=False, default=ROLE.staff)

    bl = Resource('bl.user')

    def __repr__(self):
        return '<User {}>'.format(self.get_full_name())

    def get_full_name(self):
        return '{} {}'.format(self.name, self.surname)

    def is_superuser(self):
        return self.role == self.ROLE.superuser


class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    bl = Resource('bl.city')

    def __str__(self):
        return self.name

    def __repr__(self):
        return "[{}] {}".format(self.__class__.__name__, self.name)


class BlockPageAssociation(db.Model):
    __tablename__ = 'block_page_associations'
    page_id = db.Column(
        db.Integer,
        db.ForeignKey('pages.id'),
        primary_key=True
    )
    block_id = db.Column(
        db.Integer,
        db.ForeignKey('pageblocks.id'),
        primary_key=True
    )
    position = db.Column(db.Integer)
    block = db.relationship(
        'PageBlock',
    )


class PageChunk(db.Model):
    __tablename__ = 'pagechunks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    text = db.Column(db.Text)

    bl = Resource('bl.pagechunk')


class PageBlock(db.Model):
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

    id = db.Column(db.Integer, primary_key=True)
    block_type = db.Column(
        TypeEnum(TYPE),
        default=TYPE.img_left,
        nullable=False
    )

    # header
    title = db.Column(db.VARCHAR(128), nullable=True)

    text = db.Column(db.Text)

    # used for mainpage
    short_description = db.Column(db.VARCHAR(256), nullable=True)

    image = db.Column(db.Text, nullable=True)

    bl = Resource('bl.pageblock')

    def __str__(self):
        return '%s: %s' % (self.title, self.text or self.short_description)


class Page(db.Model):
    __tablename__ = 'pages'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(128))
    url = db.Column(db.Text)
    _blocks = db.relationship(
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


class Token(db.Model):
    __tablename__ = 'tokens'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(
        'User',
    )
    token = db.Column(db.String, nullable=False)
    bl = Resource('bl.token')


class MailTemplate(db.Model):
    __tablename__ = 'mailtemplates'

    #  noinspection PyTypeChecker
    MAIL = IntEnum('Mail', {
        'CV': 0,
        'REPLY': 1,
    })

    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(TypeEnum(MAIL), nullable=False)
    title = db.Column(db.String, nullable=False)
    subject = db.Column(db.String(79), nullable=False)
    html = db.Column(db.Text, nullable=False)
    help_msg = db.Column(db.Text)
    updated_at = db.Column(db.Date, onupdate=datetime.datetime.now,
                           default=datetime.datetime.now)
    bl = Resource('bl.mailtemplate')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    who_updated = db.relationship('User')

    def __repr__(self):
        return str(self.title)


class UploadedImage(db.Model):
    __tablename__ = 'uploaded_images'

    IMG_CATEGORY = IntEnum(
        '',
        {
            'other': 0,
            'gallery': 1,
        },
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(GUID, nullable=False)
    ext = db.Column(db.VARCHAR, nullable=False)
    img_category = db.Column(
        TypeEnum(IMG_CATEGORY),
        default=IMG_CATEGORY.other,
        nullable=False,
    )
    title = db.Column(db.VARCHAR(32))
    description = db.Column(db.VARCHAR(128))
    __table_args__ = (
        db.UniqueConstraint(
            'name',
            'ext',
            'img_category',
        ),
    )

    bl = Resource('bl.uploadedimage')


def init_db():
    db.drop_all()
    db.create_all()
