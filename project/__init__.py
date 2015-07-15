from flask import Flask
from flask_wtf.csrf import CsrfProtect
from flask_mail import Mail

app = Flask(__name__, static_url_path='/static')
app.config.from_object('config')
mail = Mail(app)

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
