from flask import render_template, Blueprint, flash, jsonify
from project.models import Vacancy, Category, City
from project.feed.forms import ApplyForm
from project.bl.mail import mail_from_aplly_form


feed = Blueprint('feed', __name__)


@feed.route('/')
def vacancies():
    return render_template('feed/reactvacancies.html')

@feed.route('/list')
def json_vacancies():
    vacancies = Vacancy.query.all()
    categories = Category.query.all()
    cities = City.query.all()
    list_vacancies = list(map(lambda v: v.as_dict(), vacancies))
    list_categories = list(map(lambda c: c.as_dict(), categories))
    list_cities = list(map(lambda v: v.as_dict(), cities))
    return jsonify(vacancies=list_vacancies, categories=list_categories, cities=list_cities)


@feed.route('/vacancy/<name_in_url>', methods=['GET', 'POST'])
def get_vacancy(name_in_url):
    vacancy = Vacancy.query.filter(Vacancy.name_in_url == name_in_url).one()
    vacancy.visits += 1
    vacancy.save()

    form = ApplyForm()
    if form.validate_on_submit():
        mail_from_aplly_form(form)
        flash('Ответ отправлен')

    return render_template('feed/vacancy.html',
                           vacancy=vacancy,
                           form=form)
