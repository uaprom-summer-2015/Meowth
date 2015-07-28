import os
import logging
import logging.config

_basedir = os.path.abspath(os.path.dirname(__file__))


class Hardcoded:
    MAIL_TO_SEND = 'hrportal@yandex.ru'


class Config:
    DEBUG = False
    TESTING = False

    SECRET_KEY = 'im!mx2m(69)b^7n3j!yi)k!a7n(^09=^&*+pnan78hl^%_yp4u'

    CSRF = True
    CSRF_SECRET = 'im!mx2m(69)b^7n3j!yi)k!a7n(^09=^&*+pnan78hl^%_yp4u'

    UPLOAD_FOLDER = os.path.join(_basedir, 'media')
    ALLOWED_EXTENSIONS = {
        'txt', 'pdf', 'png', 'jpg',
        'jpeg', 'gif', 'doc', 'docx',
    }
    MAX_CONTENT_LENGTH = 15 * 1024 * 1024

    FIXTURES_DIR = os.path.join(_basedir, 'fixtures')

    # Email
    MAIL_SERVER = 'smtp.yandex.ru'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'hrportal@yandex.ru'
    MAIL_PASSWORD = 'useaverystrongpasswordLuke'
    MAIL_DEFAULT_SENDER = 'hrportal@yandex.ru'

    # Celery
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_BACKEND_URL = CELERY_BROKER_URL
    CELERY_IMPORTS = ("project.tasks.mail", )

    # Logger configuration
    LOG_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'detailed',
                'stream': 'ext://sys.stdout',
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'formatter': 'detailed',
                'filename': '/tmp/junk.log',
                'mode': 'a',
                'maxBytes': 10485760,
                'backupCount': 5,
            },

        },
        'formatters': {
            'detailed': {
                'format': '%(asctime)s %(module)-17s line:%(lineno)-4d '
                          '%(levelname)-8s %(message)s',
            },
            'email': {
                'format': 'Timestamp: %(asctime)s\nModule: %(module)s\n'
                          'Line: %(lineno)d\nMessage: %(message)s',
            },
        },
        'loggers': {
            'extensive': {
                'level': 'DEBUG',
                'handlers': [
                    'file',
                ],
            },
        },
        'root': {
            'level': 'INFO',
            'handlers': [
                'console',
            ]
        }
    }


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', None)


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://root:qwerty@localhost/hrportal'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


logging.config.dictConfig(Config.LOG_CONFIG)
