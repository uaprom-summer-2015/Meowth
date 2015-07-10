from flask import Blueprint, render_template, request, redirect, url_for
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
        return render_template(
            "admin/vacancy.html",
            vacancy=get_vacancy(vacancy_id)
        )

    elif request.method == 'POST':
        new_vacancy(request.form)
    elif request.method == 'PUT':
        update_vacancy(request.form)
    return redirect(url_for("vacancy_detail", vacancy_id=vacancy_id))
