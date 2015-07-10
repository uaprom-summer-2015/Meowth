from flask import Blueprint, render_template, request, redirect, url_for
from project.admin.forms import VacancyForm
from project.admin.logic import get_vacancies, get_vacancy, new_vacancy, \
    update_vacancy

admin_app = Blueprint('admin', __name__)


@admin_app.route("/vacancies")
def vacancy_list():
    return render_template("admin/vacancies.html", vacancies=get_vacancies())


@admin_app.route('/vacancies/<int:vacancy_id>',
                 methods=['GET', 'POST', 'PUT'])
def vacancy_detail(vacancy_id):
    if request.method == 'GET':
        vacancy = get_vacancy(vacancy_id)
        form = VacancyForm(obj=vacancy)
        return render_template(
            "admin/vacancy.html",
            vacancy_form=form
        )

    elif request.method == 'POST':
        form = VacancyForm(request.form)
        if form.validate():
            new_vacancy(form.data)
    elif request.method == 'PUT':
        update_vacancy(request.form)
    return redirect(url_for("admin.vacancy_detail", vacancy_id=vacancy_id))
