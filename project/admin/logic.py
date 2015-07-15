import weakref
from project.feed.ioc import registry
from project.feed.models import Vacancy, Category


def get_vacancies():
    vacancies = Vacancy.query.all()
    return vacancies


def get_vacancy(vacancy_id):
    vacancy = Vacancy.query.get(vacancy_id)
    return vacancy


def create_vacancy(data):
    vacancy = Vacancy(**data)
    vacancy.save()
    return vacancy


def update_vacancy(vacancy_id, data):

    vacancy = Vacancy.query.get(vacancy_id)
    for key, value in data.items():
        setattr(vacancy, key, value)
    vacancy.save()
    return vacancy


def get_categories():
    categories = Category.query.all()
    return categories


def get_category(category_id):
    category = Category.query.get(category_id)
    return category


def create_category(data):
    category = Category(**data)
    category.save()
    return category


def update_category(category_id, data):
    category = Category.query.get(category_id)
    for key, value in data.items():
        setattr(category, key, value)
    category.save()
    return category


class CategoryBL:
    _category = None

    def __init__(self, category):
        self._category = weakref.ref(category)

    @property
    def category(self):
        return self._category()

    def update(self, data):
        category = self.category

        for key, value in data.items():
            setattr(category, key, value)

        #category.save()

        return category

def init_resource_registry():
    registry.put('bl.category', lambda category: CategoryBL(category))

