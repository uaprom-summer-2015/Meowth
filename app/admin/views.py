from flask import render_template
from app import app
from app.admin.logic import get_vacancies


@app.route("/list")
def vacancy_list():
    return str(get_vacancies())
