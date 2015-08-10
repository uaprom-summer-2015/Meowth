from flask import render_template
from project.blueprints import pages_app
from project.models import Page


# All pages are hardcoded for now

@pages_app.route("/")
def mainpage():
    page = Page.bl.get(Page.TYPE.MAINPAGE)
    return render_template('pages/mainpage.html', blocks=page.blocks)


@pages_app.route('/projects/')
def projects():
    page = Page.bl.get(Page.TYPE.PROJECTS)
    return render_template('pages/projects.html', blocks=page.blocks)


@pages_app.route('/about/')
def about():
    page = Page.bl.get(Page.TYPE.ABOUT)
    return render_template('pages/about.html', blocks=page.blocks)


@pages_app.route('/contacts/')
def contacts():
    page = Page.bl.get(Page.TYPE.CONTACTS)
    return render_template('pages/contacts.html', blocks=page.blocks)
