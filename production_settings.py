import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, "project")

STATIC_DIST = './project/static/dist'

SQLALCHEMY_DATABASE_URI = \
    "postgres://postgres:postgres@127.0.0.1:5432/hrportal"

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "upload",
)

# Celery
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/1'
CELERY_BACKEND_URL = CELERY_BROKER_URL

# Email
MAIL_SERVER = "smtp.uaprom"
MAIL_PORT = "25"
MAIL_USE_SSL = False
MAIL_DEFAULT_SENDER = "hrportal@hrportal.uaprom"
