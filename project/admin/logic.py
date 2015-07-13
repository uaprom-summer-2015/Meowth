from collections import namedtuple


def get_vacancies():
    vacancy = namedtuple("vacancy", ["id", "title", "text", "category"])
    vacancies = vacancy(1, "python dev", "some text", "python"), \
                vacancy(2, "python senior dev", "other text", "python")  # NOQA
    return vacancies
