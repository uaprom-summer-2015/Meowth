from flask import render_template, Blueprint
from project.feed.models import Vacancy

feed = Blueprint('feed', __name__)


@feed.route('/vacancies')
def vacancies():
    list_vacancies = Vacancy.query.all()
    return render_template('feed/vacancies.html', vacancies=list_vacancies)
