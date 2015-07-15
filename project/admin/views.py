from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask.views import MethodView
from project.admin.forms import VacancyForm, CategoryForm
from project.admin import logic as bl

admin_app = Blueprint('admin', __name__)


class EntryDetail(MethodView):
    # /entities/ GET → list of all entities
    # /entity/<id> GET → get entity
    # /entity/<id> POST → update entity
    # /entity/ GET → create new entity

    form = None
    # model = None
    template = None
    get_entry = None
    create_entry = None
    update_entry = None
    success_url = None

    def __init__(self, form, get_entry, create_entry, update_entry,
                 success_url, template="admin/entry.html"):
        self.form = form
        # self.model = model
        self.template = template
        self.get_entry = get_entry
        self.create_entry = create_entry
        self.update_entry = update_entry
        self.success_url = success_url

    def get(self, entry_id):
        if entry_id is None:
            # Add a new entry
            entry_form = self.form()
        else:
            # Update an old entry
            entry = self.get_entry(entry_id)

            if entry is None:
                abort(404)
            entry_form = self.form(obj=entry)
        return self.render_response(entry_form=entry_form)

    def post(self, entry_id):
        if entry_id is None:
            # Add a new entry
            form = self.form()
            if form.validate():
                self.create_entry(form.data)
                return redirect(url_for("admin."+self.success_url))
        else:
            # Update an old entry
            form = self.form(request.form)
            if form.validate():
                self.update_entry(entry_id, form.data)
                return redirect(url_for("admin."+self.success_url))

        return self.render_response(entry_form=form)

    def render_response(self, **kwargs):
        return render_template(self.template, **kwargs)


# VACANCIES
@admin_app.route("/vacancies")
def vacancy_list():
    return render_template("admin/vacancies.html",
                           vacancies=bl.get_vacancies())

vacancy_view = EntryDetail.as_view(
    name='vacancy_detail',
    form=VacancyForm,
    get_entry=bl.get_vacancy,
    update_entry=bl.update_vacancy,
    create_entry=bl.create_vacancy,
    template="admin/vacancy.html",
    success_url="vacancy_list"
)

admin_app.add_url_rule(
    "/vacancy/<int:entry_id>/",
    defaults={'entry_id': None},
    view_func=vacancy_view
)
admin_app.add_url_rule(
    "/vacancy/",
    defaults={'entry_id': None},
    view_func=vacancy_view
)

@admin_app.route("/categories")
def category_list():
    return render_template("admin/categories.html",
                           categories=bl.get_categories())


# CATEGORIES
category_view = EntryDetail.as_view(
    name='category_detail',
    form=CategoryForm,
    get_entry=bl.get_category,
    update_entry=bl.update_category,
    create_entry=bl.create_category,
    success_url="category_list"
)

admin_app.add_url_rule(
    "/category/<int:entry_id>/",
    view_func=category_view
)
admin_app.add_url_rule(
    "/category/",
    defaults={'entry_id': None},
    view_func=category_view
)
