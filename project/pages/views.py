import logging
from flask import render_template
from project.blueprints import pages_app
from project.models import Page


# All pages are hardcoded for now

@pages_app.route("/")
def mainpage():
    page = Page.bl.get(4)
    return render_template('pages/mainpage.html', blocks=page.blocks)


@pages_app.route('/projects/')
def projects():
    page = Page.bl.get(1)
    return render_template('pages/projects.html', blocks=page.blocks)


@pages_app.route('/about/')
def about():
    page = Page.bl.get(2)
    return render_template('pages/about.html', blocks=page.blocks)


@pages_app.route('/contacts/')
def contacts():
    page = Page.bl.get(3)
    return render_template('pages/contacts.html', blocks=page.blocks)
