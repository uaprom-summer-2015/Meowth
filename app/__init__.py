from flask import Flask
from app.admin import admin_app

app = Flask(__name__)

app.register_blueprint(admin_app, url_prefix='/admin')
app.config.from_object('config')

from app.auth import views
