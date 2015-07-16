from flask import render_template, Blueprint, flash, request, jsonify
from project.feed.models import Vacancy, Category, City
from project.feed.forms import ApplyForm
from project.bl.mail import send_mail
from project.database import db_session



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
        attachment = request.files[form.attachment.name]

        send_mail(title='Ответ на вакансию',
                  body='Имя: {}\nEmail:{}'.format(form.name.data,
                                                  form.email.data),
                  attachment=attachment)
        flash('Ответ отправлен')

    return render_template('feed/vacancy.html',
                           vacancy=vacancy,
                           form=form)
