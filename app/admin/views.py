from flask import Blueprint
from app.admin.logic import get_vacancies


admin_app = Blueprint('admin', __name__)

@admin_app.route("/list")
def vacancy_list():
    return str(get_vacancies())
