import logging
from flask import Blueprint, render_template
from project.models import Page

pages_app = Blueprint('pages', __name__)


@pages_app.route("/")
def mainpage():
    page = Page.bl.get(4)
    logging.info(page)
    logging.info(page.blocks)
    return render_template('pages/mainpage.html', blocks=page.blocks)


@pages_app.route('/projects/')
def projects():
    page = Page.bl.get(1)
    logging.info(page)
    logging.info(page.blocks)
    return render_template('pages/projects.html', blocks=page.blocks)


@pages_app.route('/about/')
def about():
    page = Page.bl.get(2)
    logging.info(page)
    logging.info(page.blocks)
    return render_template('pages/about.html', blocks=page.blocks)


@pages_app.route('/contacts/')
def contacts():
    page = Page.bl.get(3)
    logging.info(page)
    logging.info(page.blocks)
    return render_template('pages/contacts.html', blocks=page.blocks)
