from flask import Blueprint, render_template

pages_app = Blueprint('pages', __name__)


@pages_app.route('/')
def mainpage():
    return render_template('pages/mainpage.html')


@pages_app.route('/projects/')
def projects():
    return render_template('pages/projects.html')


@pages_app.route('/about/')
def about():
    return render_template('pages/about.html')


@pages_app.route('/contacts/')
def contacts():
    return render_template('pages/contacts.html')
