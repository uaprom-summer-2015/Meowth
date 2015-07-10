from flask import Flask
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)
app.config.from_object('config')

CsrfProtect(app)

from project.admin.views import admin_app
from project.auth.views import auth as AuthModule
from project.feed.views import feed
app.register_blueprint(admin_app, url_prefix='/admin')
app.register_blueprint(AuthModule, url_prefix='/auth')
app.register_blueprint(feed)
