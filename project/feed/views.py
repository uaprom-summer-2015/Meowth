from flask import render_template, Blueprint
from project.models import Vacancy, Category

feed = Blueprint('feed', __name__)


@feed.route('/')
def vacancies():
    list_vacancies = Vacancy.query.all()
    list_category = Category.query.all()
    return render_template('feed/vacancies.html',
                           vacancies=list_vacancies,
                           categories=list_category)


@feed.route('/vacancy/<name_in_url>')
def get_vacancy(name_in_url):
    vacancy = Vacancy.query.filter(Vacancy.name_in_url == name_in_url).one()
    category = Category.query.filter(Category.id == vacancy.category_id).one()
    return render_template('feed/vacancy.html',
                           vacancy=vacancy,
                           category=category)
