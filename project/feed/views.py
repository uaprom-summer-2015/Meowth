from flask import render_template, jsonify, current_app, abort
from project.blueprints import feed_app
from project.lib.feed import get_visible_vacancies_list, get_vacancy4json
from project.models import Vacancy, Category, City
from project.feed.forms import apply_form_factory
from project.lib.mail import send_mail_from_form


@feed_app.route('/')
def vacancies():
    return render_template('feed/vacancies.html')


@feed_app.route('/<name_in_url>/')
def get_vacancy(name_in_url):
    vacancy = Vacancy.query.filter(Vacancy.name_in_url == name_in_url).one()
    if vacancy.condition_is_deleted or vacancy.condition_is_hidden:
        abort(404)
    vacancy.bl.visit()
    return render_template(
        'feed/vacancy.html',
        vacancy=vacancy,
    )

@feed_app.route('/<name_in_url>/json')
def get_vacancy_json(name_in_url):
    return jsonify(
        vacancy=get_vacancy4json(name_in_url)
    )


@feed_app.route('/list')
def json_vacancies():
    list_vacancies = get_visible_vacancies_list()
    list_categories = [c.bl.as_dict() for c in Category.query.all()]
    list_cities = [v.bl.as_dict() for v in City.query.all()]
    return jsonify(
        vacancies=list_vacancies,
        categories=list_categories,
        cities=list_cities,
    )


@feed_app.route('/<name_in_url>/form', methods=['POST'])
def apply_form(name_in_url):
    ApplyForm = apply_form_factory(config=current_app.config)
    form = ApplyForm()
    if form.validate_on_submit():
        vacancy = Vacancy.query.filter(
            Vacancy.name_in_url == name_in_url).one()
        send_mail_from_form(form, vacancy)
        return jsonify(success=True)
    else:
        return jsonify(success=False, **form.errors)
