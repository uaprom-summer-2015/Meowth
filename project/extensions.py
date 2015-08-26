from flask.ext.celery import Celery
from flask.ext.sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_wtf.csrf import CsrfProtect

celery = Celery()
mail = Mail()
csrf = CsrfProtect()
db = SQLAlchemy()
