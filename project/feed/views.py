from flask import render_template, jsonify
from project.blueprints import feed_app
from project.models import Vacancy, Category, City
from project.feed.forms import ApplyForm
from project.bl.mail import send_mail_from_form


@feed_app.route('/')
def vacancies():
    return render_template('feed/vacancies.html')


@feed_app.route('/<name_in_url>/')
def get_vacancy(name_in_url):
    vacancy = Vacancy.query.filter(Vacancy.name_in_url == name_in_url).one()
    vacancy.bl.visit()
    return render_template(
        'feed/reactvacancy.html',
        vacancy=vacancy,
    )


@feed_app.route('/list')
def json_vacancies():
    list_vacancies = [v.as_dict() for v in Vacancy.bl.get_visible()]
    list_categories = [c.as_dict() for c in Category.query.all()]
    list_cities = [v.as_dict() for v in City.query.all()]
    return jsonify(
        vacancies=list_vacancies,
        categories=list_categories,
        cities=list_cities,
    )


@feed_app.route('/<name_in_url>/form', methods=['POST'])
def apply_form(name_in_url):
    form = ApplyForm()
    if form.validate_on_submit():
        vacancy = Vacancy.query.filter(
            Vacancy.name_in_url == name_in_url).one()
        send_mail_from_form(form, vacancy)
        return jsonify(success=True)
    else:
        return jsonify(success=False, **form.errors)
