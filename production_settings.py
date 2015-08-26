STATIC_DIST = './project/static/dist'

SQLALCHEMY_DATABASE_URI = \
    "postgres://postgres:postgres@127.0.0.1:5432/hrportal"
UPLOAD_FOLDER = "../hrportal/upload"

# Celery
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_BACKEND_URL = CELERY_BROKER_URL

# Email
MAIL_SERVER = "smtp.uaprom"
MAIL_PORT = "25"
MAIL_USE_SSL = False
MAIL_DEFAULT_SENDER = "hrportal@hrportal.uaprom"
