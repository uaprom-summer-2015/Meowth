import os
import logging
import logging.config

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    TESTING = False

    SECRET_KEY = 'im!mx2m(69)b^7n3j!yi)k!a7n(^09=^&*+pnan78hl^%_yp4u'

    CSRF = True
    CSRF_SECRET = 'im!mx2m(69)b^7n3j!yi)k!a7n(^09=^&*+pnan78hl^%_yp4u'

    UPLOAD_FOLDER = os.path.join(BASEDIR, 'media')
    IMG_EXTENSIONS = {
        'gif', 'jpeg', 'jpg', 'png',
    }
    ALLOWED_EXTENSIONS = {
        'txt', 'pdf', 'png', 'jpg',
        'jpeg', 'gif', 'doc', 'docx',
    }
    MAX_CONTENT_LENGTH = 15 * 1024 * 1024

    FIXTURES_DIR = os.path.join(BASEDIR, 'fixtures')

    # Celery
    CELERY_IMPORTS = ("project.tasks.mail", )
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_BACKEND_URL = CELERY_BROKER_URL

    # Email
    MAIL_SERVER = 'smtp.yandex.ru'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAILS_TO_SEND = ['hrportal@yandex.ru']
    MAIL_USERNAME = 'hrportal@yandex.ru'
    MAIL_PASSWORD = 'useaverystrongpasswordLuke'
    MAIL_DEFAULT_SENDER = 'hrportal@yandex.ru'

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
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', None)

    # Celery
    CELERY_BROKER_URL = os.environ.get('REDIS_URL', None)
    CELERY_BACKEND_URL = CELERY_BROKER_URL

    # Email
    MAIL_SERVER = os.environ.get("MAILGUN_SMTP_SERVER", None)
    MAIL_PORT = os.environ.get("MAILGUN_SMTP_PORT", None)
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get("MAILGUN_SMTP_LOGIN", None)
    MAIL_PASSWORD = os.environ.get("MAILGUN_SMTP_PASSWORD", None)
    MAIL_DEFAULT_SENDER = 'hrportal@hruaprom.herokuapp.com'


class DevelopmentConfig(Config):
    # Flask
    DEBUG = True
    DEVELOPMENT = True

    # Database
    SQLALCHEMY_DATABASE_URI = 'postgresql://root:qwerty@localhost/hrportal'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


logging.config.dictConfig(Config.LOG_CONFIG)
