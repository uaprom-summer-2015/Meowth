from flask import Flask
import logging
import os
from project.bl.auth import UserBL
from project.bl.feed import CategoryBL, VacancyBL, CityBL
from project.bl.pages import PageBL, PageBlockBL
from project.bl.utils import registry


def init_resource_registry():
    registry['bl.category'] = lambda category: CategoryBL(category)
    registry['bl.vacancy'] = lambda vacancy: VacancyBL(vacancy)
    registry['bl.city'] = lambda city: CityBL(city)
    registry['bl.user'] = lambda user: UserBL(user)
    registry['bl.pageblock'] = lambda pageblock: PageBlockBL(pageblock)
    registry['bl.page'] = lambda page: PageBL(page)

init_resource_registry()

app = Flask(__name__, static_url_path='/static')
app.config.from_object('config')

from project.extensions import mail, celery, CsrfProtect

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
