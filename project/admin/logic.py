from project.feed.models import Vacancy, Category, City


def get_vacancies():
    vacancies = Vacancy.query.all()
    return vacancies


def get_vacancy(vacancy_id):
    vacancy = Vacancy.query.get(vacancy_id)
    return vacancy


def create_vacancy(form):
    vacancy = Vacancy('', '', '', None, '')
    form.populate_obj(vacancy)
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


def get_cities():
    cities = City.query.all()
    return cities


def get_city(city_id):
    return City.query.get(city_id)


def edit_city(data, city_id=None):
    if city_id is None:
        city = City(**data)
    else:
        city = City.query.get(city_id)
        for key, value in data.items():
            setattr(city, key, value)
    city.save()
    return city
