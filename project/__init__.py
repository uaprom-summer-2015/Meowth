from flask import Flask
from flask_wtf.csrf import CsrfProtect
from flask_mail import Mail
from project.celery import make_celery
import logging
import os
from project.bl.auth import UserBL
from project.bl.feed import CategoryBL, VacancyBL, CityBL
from project.bl.utils import registry


def init_resource_registry():
    registry['bl.category'] = lambda category: CategoryBL(category)
    registry['bl.vacancy'] = lambda vacancy: VacancyBL(vacancy)
    registry['bl.city'] = lambda city: CityBL(city)
    registry['bl.user'] = lambda user: UserBL(user)

init_resource_registry()

app = Flask(__name__, static_url_path='/static')
app.config.from_object('config')
mail = Mail(app)
celery = make_celery(app)

CsrfProtect(app)

from .database import db_session
db_session.rollback()

from project.admin.views import admin_app
from project.auth.views import auth as auth_app
from project.feed.views import feed
app.register_blueprint(admin_app, url_prefix='/admin')
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(feed, url_prefix='/vacancies')


@app.errorhandler(413)
def request_entity_too_large(error):
    return 'File Too Large', 413


if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    logging.info(app.url_map)
