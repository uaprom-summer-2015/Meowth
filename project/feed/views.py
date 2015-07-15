from flask import render_template, Blueprint, jsonify, request
from project.feed.models import Vacancy, Category
from project.database import db_session

feed = Blueprint('feed', __name__)


@feed.route('/')
def vacancies():
    return render_template('feed/reactvacancies.html')

@feed.route('/list')
def json_vacancies():
    cat_id = request.args['category_id']
    if cat_id != '0':
        vacancies = Vacancy.query.filter(Vacancy.category_id == int(cat_id))
    else:
        vacancies = Vacancy.query.all()
    categories = Category.query.all()
    list_vacancies = list(map(lambda v: v.as_dict(), vacancies))
    list_categories = list(map(lambda c: c.as_dict(), categories))
    return jsonify(vacancies=list_vacancies, categories=list_categories)


@feed.route('/vacancy/<name_in_url>')
def get_vacancy(name_in_url):
    vacancy = Vacancy.query.filter(Vacancy.name_in_url == name_in_url).one()
    category = Category.query.filter(Category.id == vacancy.category_id).one()
    return render_template('feed/vacancy.html',
                           vacancy=vacancy,
                           category=category)
