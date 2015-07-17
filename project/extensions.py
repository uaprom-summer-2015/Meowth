from celery import Celery
from flask_mail import Mail
from flask_wtf.csrf import CsrfProtect
from project import app

celery = Celery(app, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

mail = Mail(app)
CsrfProtect(app)
