import os
import production_settings

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    TESTING = False

    SECRET_KEY = 'im!mx2m(69)b^7n3j!yi)k!a7n(^09=^&*+pnan78hl^%_yp4u'

    CSRF = True
    CSRF_SECRET = 'im!mx2m(69)b^7n3j!yi)k!a7n(^09=^&*+pnan78hl^%_yp4u'

    JSONIFY_PRETTYPRINT_REGULAR = False

    UPLOAD_FOLDER = os.path.join(BASEDIR, 'media')

    IMG_MIMES = {
        'image/jpeg',
        'image/png',
        'image/gif',
    }
    DOC_MIMES = {
        'application/vnd.openxmlformats-officedocument'
        '.wordprocessingml.document',  # .docx
        'application/msword',  # .doc
        'application/pdf',  # .pdf
        'text/plain',  # .txt
        'application/vnd.openxmlformats-officedocument'
        '.presentationml.presentation',  # .pptx
        'application/vnd.ms-powerpoint',  # .ppt
        'application/rtf',  # .rtf
    }
    ALLOWED_MIMES = IMG_MIMES | DOC_MIMES

    MAX_CONTENT_LENGTH = 15 * 1024 * 1024

    FIXTURES_DIR = os.path.join(BASEDIR, 'fixtures')

    # Celery
    CELERY_IMPORTS = (
        "project.tasks.mail",
        "project.tasks.uploads",
    )
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
    SQLALCHEMY_DATABASE_URI = production_settings.SQLALCHEMY_DATABASE_URI

    UPLOAD_FOLDER = production_settings.UPLOAD_FOLDER

    # Celery
    CELERY_BROKER_URL = production_settings.CELERY_BROKER_URL
    CELERY_BACKEND_URL = production_settings.CELERY_BACKEND_URL

    # Email
    MAIL_SERVER = production_settings.MAIL_SERVER
    MAIL_PORT = production_settings.MAIL_PORT
    MAIL_USE_SSL = production_settings.MAIL_USE_SSL
    MAIL_USERNAME = getattr(production_settings, "MAIL_USERNAME", None)
    MAIL_PASSWORD = getattr(production_settings, "MAIL_PASSWORD", None)
    MAIL_DEFAULT_SENDER = production_settings.MAIL_DEFAULT_SENDER
    MAILS_TO_SEND = production_settings.MAILS_TO_SEND


class DevelopmentConfig(Config):
    # Flask
    DEBUG = True
    DEVELOPMENT = True

    SQLALCHEMY_ECHO = True

    # Database
    SQLALCHEMY_DATABASE_URI = 'postgresql://root:qwerty@localhost/hrportal'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
