from flask import render_template, Blueprint, request, flash
from project.feed.models import Vacancy, Category
from project.feed.forms import ApplyForm
from project.bl.mail import send_mail
from project import app

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
    if request.method == 'POST':
        form = ApplyForm(request.form)
        if form.validate_on_submit():
            # TODO review
            file = request.files['file']
            file_name = file.filename
            file_type = file.content_type
            file_bytes = file.read(app.config['MAX_FILE_SIZE'] + 1)
            if len(file_bytes) == app.config['MAX_FILE_SIZE']:
                form.file.errors.append('Слишком большой файл')
            else:
                send_mail('Ответ на вакансию',
                          '{}\n{}'.format(form.name.data,
                                          form.email.data),
                          file_name, file_type, file_bytes)
                flash('Ответ отправлен')
    else:
        form = ApplyForm()
    vacancy = Vacancy.query.filter(Vacancy.name_in_url == name_in_url).one()
    vacancy.visits += 1
    vacancy.save()
    return render_template('feed/vacancy.html',
                           vacancy=vacancy,
                           form=form)
