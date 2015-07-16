from flask import render_template, Blueprint, flash
from project.feed.models import Vacancy, Category
from project.feed.forms import ApplyForm
from project.bl.mail import mail_from_aplly_form

feed = Blueprint('feed', __name__)


@feed.route('/')
def vacancies():
    list_vacancies = Vacancy.query.all()
    list_category = Category.query.all()
    return render_template('feed/vacancies.html',
                           vacancies=list_vacancies,
                           categories=list_category)


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
