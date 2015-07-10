from flask import Blueprint, render_template
from project.admin.logic import get_vacancies


admin_app = Blueprint('admin', __name__)

@admin_app.route("/list")
def vacancy_list():
    return render_template("admin/vacancies.html", vacancies=get_vacancies())
