from flask import render_template, flash, jsonify
from project.blueprints import feed_app
from project.models import Vacancy, Category, City
from project.feed.forms import ApplyForm
from project.bl.mail import send_mail_from_form


@feed_app.route('/')
def vacancies():
    return render_template('feed/vacancies.html')


@feed_app.route('/<name_in_url>/react/', methods=['GET', 'POST'])
def get_vacancy_react(name_in_url):
    vacancy = Vacancy.query.filter(Vacancy.name_in_url == name_in_url).one()
    vacancy.visits += 1
    vacancy.save()

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


@feed_app.route('/<name_in_url>/', methods=['GET', 'POST', 'PUT'])
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


@feed_app.route('/<name_in_url>/react/form', methods=['POST'])
def apply_form(name_in_url):
    form = ApplyForm()
    if form.validate_on_submit():
        send_mail_from_form(form, Vacancy.query.filter(
            Vacancy.name_in_url == name_in_url).one())
        return jsonify(success=True)
    else:
        return jsonify(success=False, **form.errors)
