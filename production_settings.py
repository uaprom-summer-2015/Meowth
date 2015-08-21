import os

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")

STATIC_DIST = './project/static/dist'

# Celery
CELERY_BROKER_URL = os.environ.get('REDIS_URL')
CELERY_BACKEND_URL = CELERY_BROKER_URL

# Email
MAIL_SERVER = os.environ.get("MAIL_SMTP_SERVER")
MAIL_PORT = os.environ.get("MAIL_SMTP_PORT")
MAIL_USE_SSL = False
MAIL_USERNAME = os.environ.get("MAIL_SMTP_LOGIN")
MAIL_PASSWORD = os.environ.get("MAIL_SMTP_PASSWORD")
MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")

