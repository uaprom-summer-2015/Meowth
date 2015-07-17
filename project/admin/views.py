from collections import namedtuple
from flask import Blueprint, render_template, redirect, url_for, abort
from flask.views import MethodView
from project.admin.forms import VacancyForm, CategoryForm, CityForm
from project.auth.forms import UserForm
from project.models import Vacancy, Category, City, User

admin_app = Blueprint('admin', __name__)


def add_admin_url_rule(rule, view):
    admin_app.add_url_rule(
        rule+"/<int:entry_id>/",
        view_func=view
    )

    admin_app.add_url_rule(
        rule,
        defaults={'entry_id': None},
        view_func=view
    )


class EntryDetail(MethodView):
    """
        /entities/ GET → list of all entities
        /entity/<id> GET → get entity
        /entity/<id> POST → update entity
        /entity/ GET → create new entity
    """

    form = None
    model = None
    template = None
    success_url = None

    def __init__(self, form, model,
                 success_url, template="admin/entry.html"):
        self.form = form
        self.model = model
        self.template = template
        self.success_url = success_url

    def get(self, entry_id):
        if entry_id is None:
            # Add a new entry
            entry_form = self.form()
        else:
            # Update an old entry
            entry = self.model.bl.get(entry_id)

            if entry is None:
                abort(404)
            entry_form = self.form(obj=entry)

        return self.render_response(entry_form=entry_form)

    def post(self, entry_id):
        if entry_id is None:
            # Add a new entry
            form = self.form()
            if form.validate_on_submit():
                self.model.bl.create(form.data)
                return redirect(url_for("admin."+self.success_url))
        else:
            # Update an old entry
            form = self.form()
            if form.validate_on_submit():
                model = self.model.bl.get(entry_id)
                model.bl.update(form.data)
                return redirect(url_for("admin."+self.success_url))

        return self.render_response(entry_form=form)

    def render_response(self, **kwargs):
        return render_template(self.template, **kwargs)




# Vacancies
@admin_app.route("/vacancies/")
def vacancy_list():
    return render_template("admin/vacancies.html",
                           vacancies=Vacancy.query.all())

vacancy_view = EntryDetail.as_view(
    name='vacancy_detail',
    form=VacancyForm,
    model=Vacancy,
    template="admin/vacancy.html",
    success_url="vacancy_list",
)

add_admin_url_rule('/vacancy', vacancy_view)


# Categories
@admin_app.route("/categories/")
def category_list():
    return render_template(
        "admin/categories.html",
        categories=Category.query.all(),
    )

category_view = EntryDetail.as_view(
    name='category_detail',
    form=CategoryForm,
    model=Category,
    success_url="category_list",
)

add_admin_url_rule('/category/', category_view)


# Cities
@admin_app.route("/cities/")
def city_list():
    return render_template("admin/cities.html",
                           cities=City.query.all())

city_view = EntryDetail.as_view(
    name='city_detail',
    form=CityForm,
    model=City,
    success_url="city_list",
)

add_admin_url_rule("/city/", city_view)


# Users
@admin_app.route("/users/")
def user_list():
    return render_template("admin/users.html",
                           users=User.query.all())

user_view = EntryDetail.as_view(
    name='user_detail',
    form=UserForm,
    model=User,
    success_url="user_list",
)

add_admin_url_rule("/user/", user_view)


@admin_app.route("/")
def section():
    # TODO code smells
    section = namedtuple("Sect", ("title", "url"))
    sect_cont = list()

    sect_cont.append(section("Вакансии", url_for("admin.vacancy_list")))
    sect_cont.append(section("Пользователи", url_for("admin.user_list")))
    sect_cont.append(section("Категории", url_for("admin.category_list")))
    sect_cont.append(section("Города", url_for("admin.city_list")))
    return render_template(
        "admin/main.html",
        sections=sect_cont,
    )
