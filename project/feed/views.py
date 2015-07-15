from flask import render_template, Blueprint, flash, request
from project.feed.models import Vacancy, Category
from project.feed.forms import ApplyForm
from project.bl.mail import send_mail

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
        attachment = request.files[form.attachment.name]

        send_mail(title='Ответ на вакансию',
                  body='Имя: {}\nEmail:{}'.format(form.name.data,
                                                  form.email.data),
                  attachment=attachment)
        flash('Ответ отправлен')

    return render_template('feed/vacancy.html',
                           vacancy=vacancy,
                           form=form)
