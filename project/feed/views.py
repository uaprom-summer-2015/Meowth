from flask import render_template, flash, jsonify
from flask_wtf.csrf import generate_csrf
from project.blueprints import feed_app
from project.models import Vacancy, Category, City
from project.feed.forms import ApplyForm
from project.bl.mail import send_mail_from_form
from project.bl.feed import VacancyBL


@feed_app.route('/')
def vacancies():
    return render_template('feed/vacancies.html')


@feed_app.route('/<name_in_url>/react/', methods=['GET', 'POST'])
def get_vacancy_react(name_in_url):
    vacancy = Vacancy.query.filter(Vacancy.name_in_url == name_in_url).one()
    vacancy.visits += 1
    vacancy.save()

    form = ApplyForm()
    if form.validate_on_submit():
        send_mail_from_form(form, vacancy)
        flash('Ответ отправлен')
    security_token = generate_csrf()
    return render_template(
        'feed/reactvacancy.html',
        vacancy=vacancy,
        form=form,
        security_token=security_token,
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


@feed_app.route('/<name_in_url>/', methods=['GET', 'POST'])
def get_vacancy(name_in_url):
    vacancy = Vacancy.query.filter(Vacancy.name_in_url == name_in_url).one()
    vacancy.visits += 1
    vacancy.save()

    form = ApplyForm()
    if form.validate_on_submit():
        send_mail_from_form(form, vacancy)
        flash('Ответ отправлен')

    return render_template('feed/vacancy.html',
                           vacancy=vacancy,
                           form=form)
