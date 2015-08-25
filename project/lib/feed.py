from sqlconstruct import Construct
from project.extensions import db
from project.models import Vacancy, City


def get_visible_vacancies_list():
    vacancies_struct = Construct({
        'category_id': Vacancy.category_id,
        'city_id': Vacancy.city_id,
        'name_in_url': Vacancy.name_in_url,
        'title': Vacancy.title,
        'salary': Vacancy.salary,
        'short_description': Vacancy.short_description,
        'id': Vacancy.id,
    })

    vacancies = (
        db.session.query(vacancies_struct)
        .filter(
            ~Vacancy.condition_is_deleted,
            ~Vacancy.condition_is_hidden,
        ).all()
    )
    return vacancies


def get_vacancy4json(name_in_url):
    vacancy_struct = Construct({
        'title': Vacancy.title,
        'city': City.name,
        'salary': Vacancy.salary,
        'text': Vacancy.text
    })
    vacancy = (db.session.query(vacancy_struct)
               .outerjoin(Vacancy.city)
               .filter(Vacancy.name_in_url == name_in_url).one()
               )
    return vacancy
