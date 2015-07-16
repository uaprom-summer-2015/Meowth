from flask import Flask
from flask_wtf.csrf import CsrfProtect
from project.bl.feed import VacancyBL, CategoryBL, CityBL
from project.bl.auth import UserBL
from project.bl.utils import registry
from flask_mail import Mail


def init_resource_registry():
    registry.put('bl.category', lambda category: CategoryBL(category))
    registry.put('bl.vacancy', lambda vacancy: VacancyBL(vacancy))
    registry.put('bl.city', lambda city: CityBL(city))
    registry.put('bl.user', lambda user: UserBL(user))

init_resource_registry()

app = Flask(__name__)
app.config.from_object('config')
mail = Mail(app)

CsrfProtect(app)

from project.admin.views import admin_app
from project.auth.views import auth as auth_app
from project.feed.views import feed
app.register_blueprint(admin_app, url_prefix='/admin')
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(feed, url_prefix='/vacancies')


@app.errorhandler(413)
def request_entity_too_large(error):
    return 'File Too Large', 413
