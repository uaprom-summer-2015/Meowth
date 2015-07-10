from collections import namedtuple

# vacancy = namedtuple("vacancy", ["id", "title", "text", "category"])
from app.feed.models import Vacancy


def get_vacancies():
    # vacancies = \
    #     vacancy(1, "python dev", "some text", "python"), \
    #     vacancy(2, "python senior dev", "some another text", "python")
    vacancies = Vacancy.query.all()
    return vacancies


def get_vacancy(vacancy_id):
    vacancy = Vacancy.query.get(vacancy_id)
    return vacancy


def new_vacancy(data):
    return vacancy(**data)


def update_vacancy(data):
    return vacancy(**data)
