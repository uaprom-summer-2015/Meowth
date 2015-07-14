from flask import Blueprint, render_template, request, redirect, url_for
from project.admin.forms import VacancyForm, CategoryForm
from project.admin import logic as bl

admin_app = Blueprint('admin', __name__)


@admin_app.route("/vacancies")
def vacancy_list():
    return render_template("admin/vacancies.html",
                           vacancies=bl.get_vacancies())


@admin_app.route("/vacancies/new", methods=['GET', 'POST'])
def vacancy_new():
    if request.method == 'GET':
        form = VacancyForm()

    elif request.method == 'POST':
        form = VacancyForm(request.form)
        if form.validate():
            bl.create_vacancy(form.data)
            return redirect(url_for("admin.vacancy_list"))

    return render_template(
        "admin/vacancy.html",
        vacancy_form=form
    )


@admin_app.route('/vacancies/<int:vacancy_id>',
                 methods=['GET', 'POST'])
def vacancy_detail(vacancy_id):
    if request.method == 'GET':
        vacancy = bl.get_vacancy(vacancy_id)
        form = VacancyForm(obj=vacancy)

    elif request.method == 'POST':
        form = VacancyForm(request.form)
        if form.validate():
            bl.update_vacancy(vacancy_id, form.data)
            return redirect(url_for("admin.vacancy_list"))

    return render_template(
        "admin/vacancy.html",
        vacancy_form=form,
    )


@admin_app.route("/categories")
def category_list():
    return render_template("admin/categories.html",
                           categories=bl.get_categories())


@admin_app.route("/categories/new", methods=['GET', 'POST'])
def category_new():
    if request.method == 'GET':
        form = CategoryForm()

    elif request.method == 'POST':
        form = CategoryForm(request.form)
        if form.validate():
            bl.create_category(form.data)
            return redirect(url_for("admin.vacancy_list"))

    return render_template(
        "admin/category.html",
        category_form=form
    )


@admin_app.route('/categories/<int:category_id>',
                 methods=['GET', 'POST'])
def category_detail(category_id):
    if request.method == 'GET':
        category = bl.get_category(category_id)
        form = CategoryForm(obj=category)

    elif request.method == 'POST':
        form = CategoryForm(request.form)
        if form.validate():
            bl.update_category(category_id, form.data)
            return redirect(url_for("admin.category_list"))

    return render_template(
        "admin/category.html",
        category_form=form,
    )
