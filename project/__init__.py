from flask import Flask
from flask_wtf.csrf import CsrfProtect
import logging
import os

app = Flask(__name__)
app.config.from_object('config')

CsrfProtect(app)

from project.admin.views import admin_app
from project.auth.views import auth as auth_app
from project.feed.views import feed
app.register_blueprint(admin_app, url_prefix='/admin')
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(feed, url_prefix='/vacancies')

if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    logging.info(app.url_map)
