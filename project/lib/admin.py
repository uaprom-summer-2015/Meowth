from sqlconstruct import Construct
from project.extensions import db
from project.models import Vacancy, City, Category, User


def get_actual_vacancies_list():
    vacancies_struct = Construct({
        'title': Vacancy.title,
        'city': City.name,
        'category': Category.name,
        'username': User.name,
        'hide': Vacancy.is_hidden,
        'salary': Vacancy.salary,
        'short_description': Vacancy.short_description,
        'updated_at': Vacancy.updated_at,
        'visits': Vacancy.visits,
        'id': Vacancy.id,
    })

    vacancies = (
        db.session.query(vacancies_struct)
        .outerjoin(
            Vacancy.city,
            Vacancy.category,
            Vacancy.who_updated
        )
        .filter(~Vacancy.condition_is_deleted)
        .all()
    )
    return vacancies
