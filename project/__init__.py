from flask import Flask
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)
app.config.from_object('config')

CsrfProtect(app)

from project.admin.views import admin_app as admin_module
from project.auth.views import auth as AuthModule
app.register_blueprint(admin_module, url_prefix='/admin')
app.register_blueprint(AuthModule, url_prefix='/auth')
