from flask import Blueprint, render_template
from project.models import Page, PageBlock
from project.pages.forms import PageBlockForm, PageForm

pages = Blueprint('pages', __name__)

@pages.route('/newpage', methods=['GET', 'POST'])
def newblock():
    form = PageForm()
    return render_template("admin/entry.html", entry_form=form)
