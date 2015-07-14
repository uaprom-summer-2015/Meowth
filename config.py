import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
DEVELOPMENT = True
SECRET_KEY = 'im!mx2m(69)b^7n3j!yi)k!a7n(^09=^&*+pnan78hl^%_yp4u'
SQLALCHEMY_DATABASE_URI = 'postgresql://root:qwerty@localhost/hrportal'
SALT = 'useaverystrongsaltLuke'

UPLOAD_FOLDER = os.path.join(_basedir, 'media')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 15 * 1024 * 1024

CSRF = True
CSRF_SECRET = 'im!mx2m(69)b^7n3j!yi)k!a7n(^09=^&*+pnan78hl^%_yp4u'

# Email
MAIL_SERVER='smtp.yandex.ru'
MAIL_PORT=465
MAIL_USE_SSL=True
MAIL_USERNAME = 'hrportal@yandex.ru'
MAIL_PASSWORD = 'useaverystrongpasswordLuke'
MAIL_DEFAULT_SENDER = 'hrportal@yandex.ru'
MAIL_TO_SEND = MAIL_DEFAULT_SENDER
