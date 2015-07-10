from project.database import db_session
from project.feed.models import Vacancy


def get_vacancies():
    vacancies = Vacancy.query.all()
    return vacancies


def get_vacancy(vacancy_id):
    vacancy = Vacancy.query.get(vacancy_id)
    return vacancy


def new_vacancy(data):

    vacancy = Vacancy(**data)
    db_session.add(vacancy)
    db_session.commit()
    return vacancy


def update_vacancy(data):

    vacancy = Vacancy.query.get(data['id'])
    vacancy.update(**data)
    db_session.add(vacancy)
    db_session.commit()
    return vacancy
