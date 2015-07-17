from flask_mail import Mail
from flask_wtf.csrf import CsrfProtect
from project.celery import make_celery
from project import app

celery = make_celery(app)
mail = Mail(app)
CsrfProtect(app)
