from project.feed.models import Vacancy, Category


def get_vacancies():
    vacancies = Vacancy.query.all()
    return vacancies


def get_vacancy(vacancy_id):
    vacancy = Vacancy.query.get(vacancy_id)
    return vacancy


def create_vacancy(data):
    data['category_id'] = data['category_id'].id
    vacancy = Vacancy(**data)
    vacancy.save()
    return vacancy


def update_vacancy(vacancy_id, data):
    vacancy = Vacancy.query.get(vacancy_id)

    vacancy.title = data["title"]
    vacancy.text = data["text"]
    vacancy.short_description = data["short_description"]
    vacancy.category_id = data["category_id"].id
    vacancy.name_in_url = data["name_in_url"]

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
    category.name = data["name"]
    category.save()
    return category
