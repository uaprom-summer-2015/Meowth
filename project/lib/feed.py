from sqlalchemy import false
from sqlconstruct import Construct
from project.extensions import db
from project.models import Vacancy


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
            Vacancy.deleted == false(),
            Vacancy.hide == false())
        .all()
    )
    return vacancies
